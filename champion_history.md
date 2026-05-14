
--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- New Champion: 0.6345 (cumulative_v30006) ---
Motivation: None
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor

--- Champion: 0.6345 (cumulative_v30006) ---
Logic:
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor
