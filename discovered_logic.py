import numpy as np
def get_scores(w, data):
    m123, pt, eta, score_xgb, r_ab, dr_ab = data['m123'], data['pt'], data['eta'], data['score_xgb'], data['r_ab'], data['dr_ab']
    def scoring_logic(candidates, w):\n    import numpy as np\n    X = np.array([c['features'] for c in candidates])\n    w = np.array(w)\n    raw_score = X @ w\n    final_scores = 1/(1+np.exp(-raw_score))\n    for i, cand in enumerate(candidates):\n        cand['score'] = float(final_scores[i])\n    return final_scores
    return final_scores

def select(candidates, top_k=10):\n    # Assumes `score` field is present in each candidate dict\n    sorted_cands = sorted(candidates, key=lambda c: c.get('score', -float('inf')), reverse=True)\n    selected = sorted_cands[:top_k]\n    # Return shallow copy of each selected candidate as a dict\n    return [dict(c) for c in selected]