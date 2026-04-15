# Antibiotic Drug Discovery Criteria

Reference guide for antibiotic-specific molecule auditing. Use when `--context` involves antibiotics, antimicrobials, or bacterial pathogens, and/or when `--mode similar` or `--mode novel` is specified.

---

## Antibiotic Classes Overview

The major antibacterial classes differ in their targets, property profiles, and structural diversity. This matters for how you interpret screening results.

| Class | Mechanism | Typical MW (Da) | LogP range | Key structural features |
|---|---|---|---|---|
| β-lactams | Cell wall (PBP inhibition) | 300–500 | −1 to 2 | β-lactam ring; low logP |
| Fluoroquinolones | DNA gyrase / Topo IV | 300–450 | −1 to 2 | Quinolone core, F substituent |
| Aminoglycosides | Ribosome (30S) | 400–800 | −6 to −2 | Multiple amino sugars; very hydrophilic |
| Macrolides | Ribosome (50S) | 700–900 | 2 to 4 | Large lactone ring; complex stereochemistry |
| Tetracyclines | Ribosome (30S) | 400–550 | −1 to 1 | Naphthacene/polycyclic core |
| Glycopeptides | Cell wall (lipid II) | 1100–1800 | −3 to 2 | Peptide scaffold, glycosylated |
| Sulfonamides | Folate synthesis (DHPS) | 200–350 | 0 to 2 | Sulfonamide group, amine |
| Diaminopyrimidines | Folate synthesis (DHFR) | 250–350 | 0 to 2 | Pyrimidine-2,4-diamine |
| Oxazolidinones | Ribosome (50S, initiation) | 300–450 | 0 to 3 | Oxazolidinone ring |
| Nitroimidazoles | DNA (anaerobes/protozoa) | 150–300 | −0.5 to 0.5 | Imidazole with nitro group |
| Nitrofurans | DNA (reductive activation) | 200–300 | −0.5 to 1 | Furan with nitro group |
| Rifamycins | RNA polymerase | 700–900 | 2 to 5 | Ansamycin macrocycle |
| Polymyxins | Membrane disruption | 1000–1200 | 0 to 4 | Cyclic lipopeptide |
| Chloramphenicol | Ribosome (50S) | 300–350 | 1 to 2 | Dichloroacetamide, nitrobenzene |

---

## Property Considerations for Antibiotics

Unlike CNS or oral oncology drugs, antibiotics often violate Lipinski's Rule of Five — macrolides, aminoglycosides, glycopeptides, and rifamycins are all large, hydrophilic, and/or have high HBD count. Apply Lipinski only when the context calls for oral bioavailability (e.g. community-acquired infections where oral dosing matters). For IV-administered or topical antibiotics, Lipinski violations are less relevant.

**Key ADMET properties for antibiotics:**
- **Membrane permeability**: gram-negative pathogens have an outer membrane barrier. Compounds must either be small/hydrophilic enough to enter via porins, or lipophilic enough for diffusion. Caco-2/PAMPA permeability is a useful proxy.
- **Efflux pump susceptibility**: many antibiotics are substrates for efflux pumps (PgP, MexAB, AcrAB). P-gp substrate predictions are relevant.
- **hERG safety**: still relevant even for antibacterials — fluoroquinolones and macrolides have known cardiac risk.
- **AMES / mutagenicity**: nitroimidazoles and nitrofurans activate reductively; AMES flags are more common and need contextual interpretation (known antibiotic classes like metronidazole test AMES-positive but are still used clinically).
- **Metabolic stability**: relevant for oral drugs; less so for IV-only compounds.

---

## Similar vs Novel Mode

This is a strategic choice about what kind of compounds you're looking for.

### `--mode similar` (lead optimisation within known chemical space)

Use this when:
- You want to find analogs or derivatives of known antibiotics
- You're trying to improve potency, spectrum, or ADMET of an existing class
- You want to understand if hits from a screen resemble anything clinically validated

Tanimoto similarity ≥ 0.5 to any reference compound: close analog, likely similar mechanism.
Tanimoto similarity 0.3–0.5: scaffold-related, possibly same class.

**Trade-offs**: Compounds similar to known antibiotics have lower novelty risk (known mechanism, potentially understood resistance patterns) but may face class-level resistance (e.g., a new β-lactam may still be hydrolysed by β-lactamases).

### `--mode novel` (first-in-class discovery)

Use this when:
- You want to find compounds structurally unlike anything in clinical use
- You're targeting pathogens where existing antibiotic classes have failed (MDR/XDR bacteria)
- You are specifically looking for new chemical entities for neglected tropical diseases, where novel scaffolds are especially valuable because: (a) they avoid pre-existing resistance, (b) existing drugs may not reach or retain activity in the disease context

Tanimoto similarity < 0.3 to ALL reference compounds → structurally novel.

**Trade-offs**: Novel scaffolds have higher attrition risk (unknown mechanism, harder to optimise, fewer SAR analogies) but can overcome resistance and may access new target space. For the Ersilia mission (neglected tropical diseases, global health equity), novelty is often the scientifically braver and more impactful choice.

**In the audit report**: Novel Promising candidates should be called out explicitly. A structurally novel molecule with strong antibacterial activity is a genuinely exciting finding even if it has more ADMET uncertainty than a known-class analog.

---

## Tanimoto Threshold Guidance

The `assets/antibiotic_reference.csv` file contains 1–3 representative SMILES per major class. The similarity threshold used is **0.3 (Morgan fingerprints, radius=2, 2048 bits)**.

- **≥ 0.5**: likely same or closely related scaffold (analog)
- **0.3–0.5**: broadly class-related or shares key pharmacophore elements
- **< 0.3**: structurally distinct → `novelty_flag = True`

This threshold is conservative (generous about novelty). Adjust interpretation accordingly: a compound at 0.28 similarity may still share a partial scaffold. For the report, use the Tanimoto value as a continuous signal, not a binary classifier.

---

## AMES Mutagenicity in Antibiotic Context

Several established antibiotic classes (nitroimidazoles, nitrofurans) are AMES-positive due to their mechanism of action (reductive activation). An AMES flag should not automatically disqualify a compound in an antibiotic screen — consider whether the compound's scaffold is related to these known classes. Note the flag in the report but contextualise it.

---

## Reference SMILES Source

The representative SMILES in `assets/antibiotic_reference.csv` are drawn from PubChem canonical SMILES for the named compounds. Complex natural products (vancomycin, macrolides, aminoglycosides) may have simplified stereo representation; they serve for scaffold-level similarity comparison, not exact structure verification. The list covers the major chemical classes but is not exhaustive — Ersilia or the user may extend it with additional compounds relevant to their specific campaign.
