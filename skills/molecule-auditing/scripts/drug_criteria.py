"""drug_criteria.py — RDKit implementations of established drug-discovery
property rules and scores.

See ../references/drug-discovery-criteria.md for thresholds, citations, and
context-of-use guidance.

Public functions take a SMILES string and return one of:
  - (n_violations: int, violations: list[str]) for hard filters
  - float for composite scores
  - bool for single-rule risk flags
  - dict[str, str] for structural-alert hits
  - str ("BBB" | "HIA" | "outside") for BOILED-Egg

If the SMILES cannot be parsed, hard filters return (None, []), scores return
None, flags return None, alerts return {}.
"""

from __future__ import annotations

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, Lipinski, QED, Crippen
    from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False


def _mol(smiles):
    if not RDKIT_AVAILABLE:
        raise ImportError(
            "RDKit is required for drug_criteria. Install via `pip install rdkit`."
        )
    return Chem.MolFromSmiles(smiles) if smiles else None


def descriptors(smiles):
    """Compute the set of physicochemical descriptors used across the rules
    in this module. Returns a dict, or None for an invalid SMILES.

    LogP is the Wildman–Crippen value (RDKit `MolLogP`), commonly written as
    WLogP. MR is the Wildman–Crippen molar refractivity.
    """
    mol = _mol(smiles)
    if mol is None:
        return None
    return _descriptors_from_mol(mol)


def _descriptors_from_mol(mol):
    return {
        "MW":          Descriptors.MolWt(mol),
        "LogP":        Descriptors.MolLogP(mol),
        "HBD":         Descriptors.NumHDonors(mol),
        "HBA":         Descriptors.NumHAcceptors(mol),
        "TPSA":        Descriptors.TPSA(mol),
        "RotB":        Descriptors.NumRotatableBonds(mol),
        "Rings":       Descriptors.RingCount(mol),
        "ArRings":     Lipinski.NumAromaticRings(mol),
        "Fsp3":        Descriptors.FractionCSP3(mol),
        "HAC":         mol.GetNumHeavyAtoms(),
        "Heteroatoms": Descriptors.NumHeteroatoms(mol),
        "Carbons":     sum(1 for a in mol.GetAtoms() if a.GetSymbol() == "C"),
        "MR":          Crippen.MolMR(mol),
    }


# ---------------------------------------------------------------------------
# Rule-of-X hard filters
# ---------------------------------------------------------------------------

def lipinski_violations(smiles):
    """Lipinski's Rule of Five — Lipinski et al., Adv Drug Deliv Rev 1997.
    MW≤500, LogP≤5, HBD≤5, HBA≤10. ≥2 violations → poor oral bioavailability."""
    mol = _mol(smiles)
    if mol is None:
        return None, []
    d = _descriptors_from_mol(mol)
    v = []
    if d["MW"]   > 500: v.append(f"MW={d['MW']:.0f}")
    if d["LogP"] > 5:   v.append(f"LogP={d['LogP']:.1f}")
    if d["HBD"]  > 5:   v.append(f"HBD={d['HBD']}")
    if d["HBA"]  > 10:  v.append(f"HBA={d['HBA']}")
    return len(v), v


def ro3_violations(smiles):
    """Rule of 3 for fragment-based screening — Congreve et al., Drug Discov Today 2003.
    MW≤300, LogP≤3, HBD≤3, HBA≤3, RotB≤3, TPSA≤60."""
    mol = _mol(smiles)
    if mol is None:
        return None, []
    d = _descriptors_from_mol(mol)
    v = []
    if d["MW"]   > 300: v.append(f"MW={d['MW']:.0f}")
    if d["LogP"] > 3:   v.append(f"LogP={d['LogP']:.1f}")
    if d["HBD"]  > 3:   v.append(f"HBD={d['HBD']}")
    if d["HBA"]  > 3:   v.append(f"HBA={d['HBA']}")
    if d["RotB"] > 3:   v.append(f"RotB={d['RotB']}")
    if d["TPSA"] > 60:  v.append(f"TPSA={d['TPSA']:.0f}")
    return len(v), v


def ghose_violations(smiles):
    """Ghose filter — Ghose, Viswanadhan & Wendoloski, J Comb Chem 1999.
    160≤MW≤480, -0.4≤LogP≤5.6, 40≤MR≤130, 20≤heavy atoms≤70."""
    mol = _mol(smiles)
    if mol is None:
        return None, []
    d = _descriptors_from_mol(mol)
    v = []
    if not (160  <= d["MW"]   <= 480):  v.append(f"MW={d['MW']:.0f}")
    if not (-0.4 <= d["LogP"] <= 5.6):  v.append(f"LogP={d['LogP']:.1f}")
    if not (40   <= d["MR"]   <= 130):  v.append(f"MR={d['MR']:.0f}")
    if not (20   <= d["HAC"]  <= 70):   v.append(f"HAC={d['HAC']}")
    return len(v), v


def veber_violations(smiles):
    """Veber's rules — Veber et al., J Med Chem 2002. TPSA≤140, RotB≤10."""
    mol = _mol(smiles)
    if mol is None:
        return None, []
    d = _descriptors_from_mol(mol)
    v = []
    if d["TPSA"] > 140: v.append(f"TPSA={d['TPSA']:.0f}")
    if d["RotB"] > 10:  v.append(f"RotB={d['RotB']}")
    return len(v), v


def egan_violations(smiles):
    """Egan rule for passive absorption — Egan, Merz & Baldwin, J Med Chem 2000.
    TPSA≤131.6, LogP≤5.88."""
    mol = _mol(smiles)
    if mol is None:
        return None, []
    d = _descriptors_from_mol(mol)
    v = []
    if d["TPSA"] > 131.6: v.append(f"TPSA={d['TPSA']:.0f}")
    if d["LogP"] > 5.88:  v.append(f"LogP={d['LogP']:.1f}")
    return len(v), v


def muegge_violations(smiles):
    """Muegge filter — Muegge, Heald & Brittelli, J Med Chem 2001.
    200≤MW≤600, -2≤LogP≤5, TPSA≤150, rings≤7, carbons≥4, heteroatoms≥1,
    RotB≤15, HBA≤10, HBD≤5."""
    mol = _mol(smiles)
    if mol is None:
        return None, []
    d = _descriptors_from_mol(mol)
    v = []
    if not (200 <= d["MW"]   <= 600): v.append(f"MW={d['MW']:.0f}")
    if not (-2  <= d["LogP"] <= 5):   v.append(f"LogP={d['LogP']:.1f}")
    if d["TPSA"]        > 150: v.append(f"TPSA={d['TPSA']:.0f}")
    if d["Rings"]       > 7:   v.append(f"Rings={d['Rings']}")
    if d["Carbons"]     < 4:   v.append(f"Carbons={d['Carbons']}")
    if d["Heteroatoms"] < 1:   v.append(f"Het={d['Heteroatoms']}")
    if d["RotB"]        > 15:  v.append(f"RotB={d['RotB']}")
    if d["HBA"]         > 10:  v.append(f"HBA={d['HBA']}")
    if d["HBD"]         > 5:   v.append(f"HBD={d['HBD']}")
    return len(v), v


def cns_violations(smiles):
    """CNS small-molecule envelope — Pajouhesh & Lenz, NeuroRx 2005;
    Hitchcock & Pennington, J Med Chem 2006.
    MW≤450, 1≤LogP≤5, TPSA≤90, HBD≤3."""
    mol = _mol(smiles)
    if mol is None:
        return None, []
    d = _descriptors_from_mol(mol)
    v = []
    if d["MW"]   > 450:           v.append(f"MW={d['MW']:.0f}")
    if not (1 <= d["LogP"] <= 5): v.append(f"LogP={d['LogP']:.1f}")
    if d["TPSA"] > 90:            v.append(f"TPSA={d['TPSA']:.0f}")
    if d["HBD"]  > 3:             v.append(f"HBD={d['HBD']}")
    return len(v), v


def bro5_violations(smiles):
    """Beyond-Ro5 oral envelope — Doak, Over, Giordanetto & Kihlberg,
    Chem Biol 2014. MW≤1000, -2≤LogP≤10, HBD≤6, HBA≤15, RotB≤20, TPSA≤250."""
    mol = _mol(smiles)
    if mol is None:
        return None, []
    d = _descriptors_from_mol(mol)
    v = []
    if d["MW"]   > 1000:            v.append(f"MW={d['MW']:.0f}")
    if not (-2 <= d["LogP"] <= 10): v.append(f"LogP={d['LogP']:.1f}")
    if d["HBD"]  > 6:               v.append(f"HBD={d['HBD']}")
    if d["HBA"]  > 15:              v.append(f"HBA={d['HBA']}")
    if d["RotB"] > 20:              v.append(f"RotB={d['RotB']}")
    if d["TPSA"] > 250:             v.append(f"TPSA={d['TPSA']:.0f}")
    return len(v), v


# ---------------------------------------------------------------------------
# Single-rule risk flags
# ---------------------------------------------------------------------------

def pfizer_3_75_flag(smiles):
    """Pfizer 3/75 in vivo toxicity rule — Hughes et al., Bioorg Med Chem Lett 2008.
    Returns True if LogP > 3 AND TPSA < 75 (~2.5× higher in vivo tox risk)."""
    mol = _mol(smiles)
    if mol is None:
        return None
    d = _descriptors_from_mol(mol)
    return d["LogP"] > 3 and d["TPSA"] < 75


def gsk_4_400_flag(smiles):
    """GSK 4/400 promiscuity / ADMET rule — Gleeson, J Med Chem 2008.
    Returns True if MW > 400 AND LogP > 4 (higher promiscuity and ADMET risk)."""
    mol = _mol(smiles)
    if mol is None:
        return None
    d = _descriptors_from_mol(mol)
    return d["MW"] > 400 and d["LogP"] > 4


# ---------------------------------------------------------------------------
# Composite drug-likeness scores
# ---------------------------------------------------------------------------

def qed_score(smiles):
    """QED — Bickerton et al., Nat Chem 2012. Returns float in [0, 1];
    ≥0.5 is a common drug-like cut-off."""
    mol = _mol(smiles)
    return float(QED.qed(mol)) if mol is not None else None


def fsp3(smiles):
    """Fraction of sp³ carbons — Lovering, Bikker & Humblet, J Med Chem 2009.
    ≥0.42 correlates with clinical success."""
    mol = _mol(smiles)
    return float(Descriptors.FractionCSP3(mol)) if mol is not None else None


def n_aromatic_rings(smiles):
    """Aromatic ring count — Ritchie & Macdonald, Drug Discov Today 2009.
    >3 hurts developability (solubility, hERG, CYP)."""
    mol = _mol(smiles)
    return int(Lipinski.NumAromaticRings(mol)) if mol is not None else None


def cns_mpo(smiles):
    """CNS MPO — Wager, Hou, Verhoest & Villalobos, ACS Chem Neurosci 2010.

    Multi-parameter desirability function over 6 properties:
    ClogP, ClogD7.4, MW, TPSA, HBD, most-basic pKa. Each property is mapped to
    a 0–1 desirability via trapezoidal/triangular functions; the sum (max 6)
    is the score. Original cut-off: ≥4 favourable.

    ClogD7.4 and pKa cannot be computed from SMILES with stock RDKit, so this
    implementation returns a 4-property approximation (LogP, MW, TPSA, HBD;
    max 4.0). Treat ≥2.7 as a rough equivalent to the 6-property ≥4 cut-off.
    """
    mol = _mol(smiles)
    if mol is None:
        return None
    d = _descriptors_from_mol(mol)

    def step_then_ramp(x, x_one, x_zero):
        if x <= x_one:  return 1.0
        if x >= x_zero: return 0.0
        return 1.0 - (x - x_one) / (x_zero - x_one)

    def trap(x, x1, x2, x3, x4):
        if x <= x1 or x >= x4: return 0.0
        if x2 <= x <= x3:      return 1.0
        if x < x2:             return (x - x1) / (x2 - x1)
        return (x4 - x) / (x4 - x3)

    s_logp = step_then_ramp(d["LogP"], 3.0, 5.0)
    s_mw   = step_then_ramp(d["MW"], 360.0, 500.0)
    s_tpsa = trap(d["TPSA"], 20.0, 40.0, 90.0, 120.0)
    s_hbd  = step_then_ramp(d["HBD"], 0.0, 3.5)
    return s_logp + s_mw + s_tpsa + s_hbd


def boiled_egg(smiles):
    """BOILED-Egg — Daina & Zoete, ChemMedChem 2016. Predicts HIA (white) and
    BBB (yolk) from TPSA and WLogP.

    Returns "BBB" (yolk: both BBB+ and HIA+), "HIA" (white: HIA+, not BBB),
    or "outside".

    Uses a bounding-box approximation of the original ellipses (TPSA≤79 &
    0.4≤WLogP≤6 for BBB; TPSA≤142 & -1.5≤WLogP≤5.9 for HIA). Consult the
    paper for exact elliptical regions.
    """
    mol = _mol(smiles)
    if mol is None:
        return None
    d = _descriptors_from_mol(mol)
    tpsa, wlogp = d["TPSA"], d["LogP"]
    if 0 <= tpsa <= 79 and 0.4 <= wlogp <= 6.0:
        return "BBB"
    if 0 <= tpsa <= 142 and -1.5 <= wlogp <= 5.9:
        return "HIA"
    return "outside"


# ---------------------------------------------------------------------------
# Efficiency metrics (require activity input)
# ---------------------------------------------------------------------------

def ligand_efficiency(smiles, pIC50):
    """LE = 1.4 × pIC50 / heavy-atom count — Hopkins, Groom & Alex,
    Drug Discov Today 2004. Target ≥0.3 kcal/mol/atom."""
    mol = _mol(smiles)
    if mol is None or pIC50 is None:
        return None
    return 1.4 * pIC50 / mol.GetNumHeavyAtoms()


def lip_e(smiles, pIC50):
    """LipE / LLE = pIC50 − LogP — Leeson & Springthorpe, Nat Rev Drug Discov 2007.
    Target ≥5."""
    mol = _mol(smiles)
    if mol is None or pIC50 is None:
        return None
    return pIC50 - Descriptors.MolLogP(mol)


def bei(smiles, pIC50):
    """Binding Efficiency Index = pIC50 / MW (kDa) — Abad-Zapatero & Metz,
    Drug Discov Today 2005. Target ≥20."""
    mol = _mol(smiles)
    if mol is None or pIC50 is None:
        return None
    return pIC50 / (Descriptors.MolWt(mol) / 1000.0)


def sei(smiles, pIC50):
    """Surface Efficiency Index = pIC50 / (TPSA/100) — Abad-Zapatero & Metz,
    Drug Discov Today 2005. Target ≥15."""
    mol = _mol(smiles)
    if mol is None or pIC50 is None:
        return None
    tpsa = Descriptors.TPSA(mol)
    if tpsa <= 0:
        return None
    return pIC50 / (tpsa / 100.0)


def pfi(smiles):
    """Property Forecast Index — Young et al., Drug Discov Today 2011.
    PFI = LogD7.4 + #aromatic rings; ≤7 favours developability.

    LogD7.4 is approximated by LogP (Wildman–Crippen) since pKa is not
    available from SMILES alone.
    """
    mol = _mol(smiles)
    if mol is None:
        return None
    return Descriptors.MolLogP(mol) + Lipinski.NumAromaticRings(mol)


# ---------------------------------------------------------------------------
# Structural alerts via RDKit FilterCatalog
# ---------------------------------------------------------------------------

_CATALOG_MAP = None


def _get_catalog_map():
    global _CATALOG_MAP
    if _CATALOG_MAP is None and RDKIT_AVAILABLE:
        catalogs = FilterCatalogParams.FilterCatalogs
        _CATALOG_MAP = {
            "PAINS":   catalogs.PAINS,
            "PAINS_A": catalogs.PAINS_A,
            "PAINS_B": catalogs.PAINS_B,
            "PAINS_C": catalogs.PAINS_C,
            "BRENK":   catalogs.BRENK,
            "NIH":     catalogs.NIH,
            "ZINC":    catalogs.ZINC,
        }
    return _CATALOG_MAP


def structural_alerts(smiles, catalogs=("PAINS",)):
    """Run RDKit FilterCatalog against the molecule.

    catalogs: subset of ("PAINS", "PAINS_A", "PAINS_B", "PAINS_C",
                        "BRENK", "NIH", "ZINC").
    Returns a dict mapping catalog name → first-match description for each
    catalog that fired. Empty dict means no alerts (or invalid SMILES).

    References:
      PAINS — Baell & Holloway, J Med Chem 2010 (A/B/C subsets by frequency).
      BRENK — Brenk et al., ChemMedChem 2008.
      NIH   — NIH MLSMR experimental-annoyance filters.
      ZINC  — Irwin & Shoichet ZINC drug-like sanity filters.

    RDKit's FilterCatalog enum does not currently include CHEMBL or
    vendor-specific subsets (Lilly, Glaxo, BMS, Dundee, Inpharmatica). Apply
    those via custom SMARTS sets if needed.
    """
    mol = _mol(smiles)
    if mol is None:
        return {}
    cmap = _get_catalog_map()
    fired = {}
    for name in catalogs:
        cat_enum = cmap.get(name)
        if cat_enum is None:
            continue
        params = FilterCatalogParams()
        params.AddCatalog(cat_enum)
        entry = FilterCatalog(params).GetFirstMatch(mol)
        if entry:
            fired[name] = entry.GetDescription()
    return fired


# ---------------------------------------------------------------------------
# One-shot evaluation
# ---------------------------------------------------------------------------

def evaluate(smiles, pIC50=None, alert_catalogs=("PAINS", "BRENK")):
    """Run every rule, score, and alert set; return a single report dict.

    Activity-dependent metrics (LE, LipE, BEI, SEI) are computed only when
    pIC50 is supplied.
    """
    out = {
        "smiles":      smiles,
        "descriptors": None,
        "filters":     {},
        "flags":       {},
        "scores":      {},
        "alerts":      {},
    }
    mol = _mol(smiles)
    if mol is None:
        return out
    out["descriptors"] = _descriptors_from_mol(mol)
    for name, fn in [
        ("lipinski", lipinski_violations),
        ("ro3",      ro3_violations),
        ("ghose",    ghose_violations),
        ("veber",    veber_violations),
        ("egan",     egan_violations),
        ("muegge",   muegge_violations),
        ("cns",      cns_violations),
        ("bro5",     bro5_violations),
    ]:
        n, v = fn(smiles)
        out["filters"][name] = {"n_violations": n, "violations": v}
    out["flags"]["pfizer_3_75"] = pfizer_3_75_flag(smiles)
    out["flags"]["gsk_4_400"]   = gsk_4_400_flag(smiles)
    out["scores"]["qed"]            = qed_score(smiles)
    out["scores"]["fsp3"]           = fsp3(smiles)
    out["scores"]["aromatic_rings"] = n_aromatic_rings(smiles)
    out["scores"]["cns_mpo_4prop"]  = cns_mpo(smiles)
    out["scores"]["boiled_egg"]     = boiled_egg(smiles)
    out["scores"]["pfi"]            = pfi(smiles)
    if pIC50 is not None:
        out["scores"]["LE"]   = ligand_efficiency(smiles, pIC50)
        out["scores"]["LipE"] = lip_e(smiles, pIC50)
        out["scores"]["BEI"]  = bei(smiles, pIC50)
        out["scores"]["SEI"]  = sei(smiles, pIC50)
    out["alerts"] = structural_alerts(smiles, alert_catalogs)
    return out
