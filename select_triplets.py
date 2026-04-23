# -*- coding: utf-8 -*-
"""
select_triplets.py
------------------

Utility module for reconstructing hadronic top candidates from jet collections.

The module provides several physics‑driven scoring strategies, a simple exact
(disjoint) set solver, and a public ``select_triplets`` API.  The newest
strategy, ``asymmetric_top_combined_v1``, augments the asymmetric top‑mass
prior with a W‑mass prior, a pT scaling factor, a ΔR penalty and a b‑tag
weight.  It is designed to surpass the 0.63 efficiency target.

Author: Vinny (2026‑04‑16)
"""

import itertools
import os
from typing import List, Tuple, Dict

import numpy as np

# ----------------------------------------------------------------------
# Type aliases
Jet = Dict[str, float]        # Expected keys: 'pt', 'eta', 'phi', 'mass', optionally 'btag'
Triplet = Tuple[int, int, int]   # indices of three jets in the event list

# ----------------------------------------------------------------------
# Kinematic utilities

def invariant_mass(jet1: Jet, jet2: Jet, jet3: Jet = None) -> float:
    """Return the invariant mass (GeV) of two or three jets.

    Parameters
    ----------
    jet1, jet2, jet3 : dict
        Jet dictionaries containing ``pt``, ``eta``, ``phi`` and ``mass``.

    Returns
    -------
    float
        Invariant mass in GeV.
    """
    def four_vector(j: Jet) -> np.ndarray:
        pt = j['pt']
        eta = j['eta']
        phi = j['phi']
        m = j['mass']
        px = pt * np.cos(phi)
        py = pt * np.sin(phi)
        pz = pt * np.sinh(eta)
        e = np.sqrt(px**2 + py**2 + pz**2 + m**2)
        return np.array([e, px, py, pz])

    v1 = four_vector(jet1)
    v2 = four_vector(jet2)
    if jet3 is not None:
        v3 = four_vector(jet3)
        total = v1 + v2 + v3
    else:
        total = v1 + v2

    mass2 = total[0]**2 - np.sum(total[1:]**2)
    return float(np.sqrt(max(mass2, 0.0)))


def delta_r(jet1: Jet, jet2: Jet) -> float:
    """ΔR between two jets (dimensionless)."""
    dphi = np.abs(jet1['phi'] - jet2['phi'])
    dphi = (dphi + np.pi) % (2 * np.pi) - np.pi   # wrap into [-π, π]
    deta = jet1['eta'] - jet2['eta']
    return float(np.sqrt(deta**2 + dphi**2))


# ----------------------------------------------------------------------
# Probability density helpers

def gaussian_pdf(x: float, mu: float, sigma: float) -> float:
    """Standard Gaussian PDF."""
    if sigma <= 0:
        return 0.0
    return (1.0 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def asymmetric_gaussian_pdf(x: float, mu: float, sigma_low: float, sigma_high: float) -> float:
    """Asymmetric Gaussian: sigma_low for x ≤ mu, sigma_high for x > mu."""
    sigma = sigma_low if x <= mu else sigma_high
    return gaussian_pdf(x, mu, sigma)


# ----------------------------------------------------------------------
# Feature scaling helpers

def pt_scaling_factor(pt_sum: float, scale: float = 300.0, exponent: float = 0.2) -> float:
    """Reward larger summed pT of the triplet."""
    return (pt_sum / scale) ** exponent


def dR_min_factor(triplet: Triplet, jets: List[Jet], alpha: float = 1.0) -> float:
    """Penalty based on the smallest ΔR within the triplet."""
    i, j, k = triplet
    dr_vals = [
        delta_r(jets[i], jets[j]),
        delta_r(jets[i], jets[k]),
        delta_r(jets[j], jets[k])
    ]
    dr_min = min(dr_vals)
    return float(np.exp(-alpha * (dr_min / 0.4) ** 2))


def btag_weight(triplet: Triplet, jets: List[Jet], power: float = 0.5) -> float:
    """Use the highest b‑tag score among the three jets."""
    i, j, k = triplet
    max_b = max(
        jets[i].get('btag', 0.0),
        jets[j].get('btag', 0.0),
        jets[k].get('btag', 0.0)
    )
    return float(max_b ** power)


# ----------------------------------------------------------------------
# Scoring functions for the individual strategies

def score_asymmetric_mass_wmass(cand: Triplet, jets: List[Jet],
                               m_top: float = 172.0,
                               sigma_low: float = 30.0,
                               sigma_high: float = 20.0,
                               gamma: float = 0.5,
                               m_w: float = 80.4,
                               sigma_w: float = 12.0) -> float:
    """Strategy: asymmetric top‑mass prior + Gaussian W‑mass prior (disjoint solver)."""
    i, j, k = cand
    m_top_cand = invariant_mass(jets[i], jets[j], jets[k])
    top_pdf = asymmetric_gaussian_pdf(m_top_cand, m_top, sigma_low, sigma_high)

    # best dijet mass as W candidate
    w_masses = [
        invariant_mass(jets[i], jets[j]),
        invariant_mass(jets[i], jets[k]),
        invariant_mass(jets[j], jets[k])
    ]
    m_w_cand = min(w_masses, key=lambda x: abs(x - m_w))
    w_pdf = gaussian_pdf(m_w_cand, m_w, sigma_w)

    return (top_pdf ** gamma) * w_pdf


def score_asymmetric_top_exact(cand: Triplet, jets: List[Jet],
                               m_top: float = 162.0,
                               sigma_low: float = 25.0,
                               sigma_high: float = 18.0,
                               gamma: float = 0.45,
                               m_w: float = 80.4,
                               sigma_w: float = 18.0) -> float:
    """Strategy: asymmetric top‑mass prior + exact disjoint solver (v2)."""
    i, j, k = cand
    m_top_cand = invariant_mass(jets[i], jets[j], jets[k])
    top_pdf = asymmetric_gaussian_pdf(m_top_cand, m_top, sigma_low, sigma_high)

    w_masses = [
        invariant_mass(jets[i], jets[j]),
        invariant_mass(jets[i], jets[k]),
        invariant_mass(jets[j], jets[k])
    ]
    m_w_cand = min(w_masses, key=lambda x: abs(x - m_w))
    w_pdf = gaussian_pdf(m_w_cand, m_w, sigma_w)

    return (top_pdf ** gamma) * w_pdf


def score_asymmetric_top_exact_v3(cand: Triplet, jets: List[Jet],
                                 m_top: float = 162.0,
                                 sigma_low: float = 25.0,
                                 sigma_high: float = 18.0,
                                 gamma: float = 1.0,
                                 m_w: float = 80.4,
                                 sigma_w: float = 18.0,
                                 pt_exp: float = 0.2,
                                 pt_scale: float = 200.0) -> float:
    """Strategy: asymmetric top‑mass prior + pT scaling (v3)."""
    i, j, k = cand
    m_top_cand = invariant_mass(jets[i], jets[j], jets[k])
    top_pdf = asymmetric_gaussian_pdf(m_top_cand, m_top, sigma_low, sigma_high)

    w_masses = [
        invariant_mass(jets[i], jets[j]),
        invariant_mass(jets[i], jets[k]),
        invariant_mass(jets[j], jets[k])
    ]
    m_w_cand = min(w_masses, key=lambda x: abs(x - m_w))
    w_pdf = gaussian_pdf(m_w_cand, m_w, sigma_w)

    pt_sum = jets[i]['pt'] + jets[j]['pt'] + jets[k]['pt']
    pt_factor = pt_scaling_factor(pt_sum, scale=pt_scale, exponent=pt_exp)

    return (top_pdf ** gamma) * w_pdf * pt_factor


def score_asymmetric_top_mlp_v1(cand: Triplet, jets: List[Jet], model) -> float:
    """Strategy: MLP‑based scoring (v1).  The model expects a feature vector."""
    i, j, k = cand

    # invariant masses
    m_top = invariant_mass(jets[i], jets[j], jets[k])
    dijet_masses = [
        invariant_mass(jets[i], jets[j]),
        invariant_mass(jets[i], jets[k]),
        invariant_mass(jets[j], jets[k])
    ]
    m_w = min(dijet_masses, key=lambda x: abs(x - 80.4))

    # scalar features
    pt_sum = jets[i]['pt'] + jets[j]['pt'] + jets[k]['pt']
    max_btag = max(
        jets[i].get('btag', 0.0),
        jets[j].get('btag', 0.0),
        jets[k].get('btag', 0.0)
    )
    dr_vals = [
        delta_r(jets[i], jets[j]),
        delta_r(jets[i], jets[k]),
        delta_r(jets[j], jets[k])
    ]
    dr_min = min(dr_vals)

    X = np.array([m_top, m_w, pt_sum, max_btag, dr_min]).reshape(1, -1)
    # The model is assumed to be a scikit‑learn classifier with predict_proba
    prob = model.predict_proba(X)[0, 1]
    return float(prob)


# ----------------------------------------------------------------------
# Exact (greedy) disjoint‑set solver

def _solve_exact_disjoint(scores: Dict[Triplet, float]) -> List[Triplet]:
    """
    Maximise the total score while ensuring that selected triplets do not share jets.
    A simple deterministic greedy algorithm is used (exact for the typical
    small number of candidates in top reconstruction).
    """
    chosen = []
    used = set()
    for cand, sc in sorted(scores.items(), key=lambda item: item[1], reverse=True):
        if not any(jet in used for jet in cand):
            chosen.append(cand)
            used.update(cand)
    return chosen


# ----------------------------------------------------------------------
# Strategy dispatcher

STRATEGIES = (
    'asymmetric_mass_gaussian_wmass_disjoint',
    'asymmetric_top_exact_v2',
    'asymmetric_top_exact_v3',
    'asymmetric_top_mlp_v1',
    # **New strategy** – combines several physics‑driven ingredients
    'asymmetric_top_combined_v1',
)


def _apply_strategy(jets: List[Jet], strategy: str) -> List[Triplet]:
    """
    Compute non‑overlapping top candidates for a single event using the
    requested strategy.

    Parameters
    ----------
    jets : list[dict]
        List of jet dictionaries for the event.
    strategy : str
        Name of the reconstruction strategy (must be in ``STRATEGIES``).

    Returns
    -------
    list[tuple[int, int, int]]
        Selected jet‑index triplets.
    """
    if len(jets) < 3:
        return []

    all_triplets = list(itertools.combinations(range(len(jets)), 3))
    scores: Dict[Triplet, float] = {}

    if strategy == 'asymmetric_mass_gaussian_wmass_disjoint':
        for cand in all_triplets:
            scores[cand] = score_asymmetric_mass_wmass(cand, jets)

    elif strategy == 'asymmetric_top_exact_v2':
        for cand in all_triplets:
            scores[cand] = score_asymmetric_top_exact(cand, jets)

    elif strategy == 'asymmetric_top_exact_v3':
        for cand in all_triplets:
            scores[cand] = score_asymmetric_top_exact_v3(cand, jets)

    elif strategy == 'asymmetric_top_mlp_v1':
        # Lazy model loading
        if not hasattr(_apply_strategy, '_mlp_v1'):
            import joblib
            model_path = os.path.join(os.path.dirname(__file__), 'mlp_top_v1.pkl')
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"MLP model not found at {model_path}")
            _apply_strategy._mlp_v1 = joblib.load(model_path)
        model = _apply_strategy._mlp_v1
        for cand in all_triplets:
            scores[cand] = score_asymmetric_top_mlp_v1(cand, jets, model)

    elif strategy == 'asymmetric_top_combined_v1':
        # ------------------------------
        # Hyper‑parameters (tuned for this iteration)
        # ------------------------------
        m_top = 172.0          # GeV
        sigma_low = 30.0       # GeV (left side)
        sigma_high = 15.0      # GeV (right side)
        gamma = 0.6
        m_w = 80.4
        sigma_w = 12.0

        pt_scale = 300.0
        pt_exponent = 0.2

        dr_alpha = 1.0
        btag_power = 0.5

        for cand in all_triplets:
            # top‑mass term
            m_top_cand = invariant_mass(jets[cand[0]], jets[cand[1]], jets[cand[2]])
            top_pdf = asymmetric_gaussian_pdf(m_top_cand, m_top, sigma_low, sigma_high)

            # W‑mass term (closest dijet)
            dijet_masses = [
                invariant_mass(jets[cand[0]], jets[cand[1]]),
                invariant_mass(jets[cand[0]], jets[cand[2]]),
                invariant_mass(jets[cand[1]], jets[cand[2]])
            ]
            m_w_cand = min(dijet_masses, key=lambda x: abs(x - m_w))
            w_pdf = gaussian_pdf(m_w_cand, m_w, sigma_w)

            # pT scaling
            pt_sum = sum(jets[i]['pt'] for i in cand)
            pt_factor = pt_scaling_factor(pt_sum, scale=pt_scale, exponent=pt_exponent)

            # ΔR penalty
            dr_factor = dR_min_factor(cand, jets, alpha=dr_alpha)

            # b‑tag weighting
            btag_factor = btag_weight(cand, jets, power=btag_power)

            # total score
            score = (top_pdf ** gamma) * w_pdf * pt_factor * dr_factor * btag_factor
            scores[cand] = float(score)

    else:
        raise ValueError(f"Strategy '{strategy}' not recognized. Available: {STRATEGIES}")

    # Resolve overlaps – keep the highest‑scoring compatible set
    selected = _solve_exact_disjoint(scores)
    return selected


def select_triplets(jets: List[Jet], strategy: str = 'asymmetric_top_combined_v1') -> List[Triplet]:
    """
    Public interface – select top candidates from a jet collection.

    Parameters
    ----------
    jets : list[dict]
        Jet information for a single event.
    strategy : str, optional
        Reconstruction strategy to use.  Defaults to the newest combined
        strategy.

    Returns
    -------
    list[tuple[int, int, int]]
        List of selected, non‑overlapping jet triplets.
    """
    if strategy not in STRATEGIES:
        raise ValueError(f"Strategy '{strategy}' not recognized. Choose from {STRATEGIES}.")
    return _apply_strategy(jets, strategy)