import os, json, time, math, subprocess, urllib.request, re, random
from pathlib import Path

MAX_HOURS = 72
WORK_DIR = "/global/u1/v/vinny/projects/topreco-agent"
PIPELINE_DIR = "/global/u1/v/vinny/projects/topreconstruction"
CODE_PATH = f"{PIPELINE_DIR}/top_reco/src/triplet_ml/select_triplets.py"
LAB_PATH = f"{WORK_DIR}/labbook.md"
CHAMP_PATH = f"{WORK_DIR}/champion_state.json"
API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = "https://api.cborg.lbl.gov/v1/chat/completions"
MODEL = "lbl/gpt-oss-120b"

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("hybrid_discovery_v1.log", "a") as f: f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")

def call_model(msgs):
    data = json.dumps({"model": MODEL, "messages": msgs}).encode("utf-8")
    req = urllib.request.Request(BASE_URL, data=data, headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp: return json.loads(resp.read().decode())["choices"][0]["message"]["content"]
    except Exception as e:
        log(f"API Error: {e}")
        return None

def sanitize_logic(raw_logic):
    clean = raw_logic.replace('\\n', '\n').replace('\u2011', '-').replace('\u2013', '-').replace('\u202F', ' ')
    lines = []
    for l in clean.split('\n'):
        l = l.strip()
        if not l or l.startswith('#') or 'print(' in l: continue
        if '=' not in l and '(' not in l and not l.startswith('return'): continue
        lines.append("            " + l)
    return "\n".join(lines)

def run_eval(iter_idx, slug, logic):
    subprocess.run(f"cd {PIPELINE_DIR} && git checkout top_reco/src/triplet_ml/select_triplets.py", shell=True)
    subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/reset_and_feature_patch.py", shell=True)
    with open(CODE_PATH, "r") as f: content = f.read()
    content = re.sub(r'STRATEGIES = .*', f'STRATEGIES = ("greedy_disjoint", "top1", "topk", "threshold", "best_pair_avg_disjoint", "{slug}")', content)
    
    impl = f"    if strategy == \"{slug}\":\n"
    impl += "        scored_cands = []\n"
    impl += "        for t in candidates:\n"
    impl += "            from math import *\n"
    impl += "            score=t.score; triplet_mass=t.triplet_mass; triplet_pt=t.triplet_pt; triplet_eta=t.triplet_eta\n"
    impl += "            ratio_ab=t.ratio_ab; ratio_ac=t.ratio_ac; ratio_bc=t.ratio_bc\n"
    impl += "            dr_ab=t.dr_ab; dr_ac=t.dr_ac; dr_bc=t.dr_bc\n"
    impl += f"{logic}\n"
    impl += "            new_cand = TripletCandidate(i=t.i, j=t.j, k=t.k, score=combined_score, is_truth=t.is_truth, triplet_pt=t.triplet_pt, triplet_eta=t.triplet_eta, triplet_phi=t.triplet_phi, triplet_mass=t.triplet_mass, mij_ab=t.mij_ab, mij_ac=t.mij_ac, mij_bc=t.mij_bc, dr_ab=t.dr_ab, dr_ac=t.dr_ac, dr_bc=t.dr_bc, ratio_ab=t.ratio_ab, ratio_ac=t.ratio_ac, ratio_bc=t.ratio_bc)\n"
    impl += "            scored_cands.append(new_cand)\n"
    impl += "        scored_cands.sort(key=lambda x: (-x.score, x.i, x.j, x.k))\n"
    impl += "        return _solve_exact_disjoint(scored_cands, max_top=max_top_per_event)\n"

    content = content.replace('    if strategy == "greedy_disjoint":', impl + '\n    if strategy == "greedy_disjoint":')
    with open(CODE_PATH, "w") as f: f.write(content)
    
    if subprocess.run(f"agent_kit/.venv/bin/python3 -m py_compile {CODE_PATH}", shell=True).returncode == 0:
        eval_cmd = f"PYTHONPATH={PIPELINE_DIR}/top_reco/src /global/homes/v/vinny/.conda/envs/topml/bin/python -m triplet_ml select_triplets --inference {PIPELINE_DIR}/artifacts/run_prof/infer_eval/inference_test_xgb.parquet --strategy {slug} --output-dir artifacts/iter{iter_idx}_eval --min-score 0.0 --max-top-per-event 4 --no-progress"
        subprocess.run(eval_cmd, shell=True)
        res = subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/real_eval.py artifacts/iter{iter_idx}_eval/selected_triplets.parquet 0 2000", shell=True, capture_output=True, text=True)
        if res.stdout and "Efficiency: " in res.stdout:
            return float(res.stdout.split("Efficiency: ")[1].split("\n")[0].strip())
    return 0.0

def main():
    start_time, iter_idx = time.time(), 90000
    log("=== Top Reconstruction Marathon Harness v15.1 (BRANCHING) ===")
    
    while (time.time() - start_time) < (MAX_HOURS * 3600):
        with open(CHAMP_PATH, "r") as f: champ = json.load(f)

        mode, is_mut = ("MUTATION", True) if random.random() < 0.25 else ("REFINEMENT", False)
        
        if is_mut:
            mut_type = random.choice(["physics", "nn", "feature_eng"])
            if mut_type == "physics":
                prompt = f"Propose RADICAL physics logic. Baseline: {champ['efficiency']}. Return JSON {{'slug': 'mut_v...', 'logic': 'combined_score = ...'}}"
            elif mut_type == "nn":
                prompt = f"Propose an MLP/Neural-Network style scoring logic (multi-layer activations). Baseline: {champ['efficiency']}. Return JSON."
            else:
                prompt = f"Propose complex BDT-like feature engineering/scoring. Baseline: {champ['efficiency']}. Return JSON."
        else:
            prompt = f"Tweak best logic: {champ['logic']}. Define 'combined_score'. Return JSON."
        
        resp = call_model([{"role": "user", "content": prompt}])
        if not resp: iter_idx += 1; continue
        
        try:
            discovery = json.loads(re.search(r"\{.*\}", resp, re.DOTALL).group())
            strat_logic = sanitize_logic(discovery["logic"])
            if "combined_score" not in strat_logic: continue
        except: continue

        eff = run_eval(iter_idx, f"h_{iter_idx}", strat_logic)
        log(f"Iteration {iter_idx} Result: {eff:.4f}")

        if eff > champ["efficiency"]:
            log(f"*** NEW CHAMPION! {eff:.4f} ***")
            champ.update({"efficiency": eff, "slug": discovery["slug"], "logic": strat_logic})
            with open(CHAMP_PATH, "w") as f: json.dump(champ, f, indent=2)
        elif eff > 0.95 * champ["efficiency"] and is_mut:
            log(f"!!! PROMISING BRANCH ({eff:.4f}) !!!")
            curr_b_eff, curr_b_logic = eff, strat_logic
            for b_i in range(3):
                b_prompt = f"Refine this promising logic: {curr_b_logic}. Current: {curr_b_eff}. Return JSON."
                b_resp = call_model([{"role": "user", "content": b_prompt}])
                if not b_resp: continue
                try:
                    b_disc = json.loads(re.search(r"\{.*\}", b_resp, re.DOTALL).group())
                    b_logic = sanitize_logic(b_disc["logic"])
                    b_eff = run_eval(f"{iter_idx}_b{b_i}", f"hb_{iter_idx}_{b_i}", b_logic)
                    log(f"  Branch {b_i} Result: {b_eff:.4f}")
                    if b_eff > curr_b_eff:
                        curr_b_eff, curr_b_logic = b_eff, b_logic
                        if b_eff > champ["efficiency"]:
                            log("  *** BRANCH BEAT CHAMPION! ***")
                            champ.update({"efficiency": b_eff, "slug": b_disc["slug"], "logic": b_logic})
                            with open(CHAMP_PATH, "w") as f: json.dump(champ, f, indent=2)
                except: continue

        iter_idx += 1; time.sleep(1)

if __name__ == "__main__": main()
