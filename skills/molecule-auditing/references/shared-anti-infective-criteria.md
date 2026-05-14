# Shared Anti-Infective Criteria

> Cross-bucket concepts that every anti-infective audit pulls in. Per-bucket files (`gram-negative-criteria.md`, `antimycobacterial-criteria.md`, etc.) link back here for shared rules and only specialise where pathogen biology demands it. Generic drug-discovery rules (Lipinski/Veber tables, PAINS RDKit catalog usage, Ersilia ADMET column patterns) live in [`drug-discovery-criteria.md`](./drug-discovery-criteria.md); this file is about how those generic rules apply differently to anti-infectives.

## Quick rules (Claude reads these first)

- **Anti-infectives often violate Ro5** legitimately (macrolides, glycopeptides, polymyxins, polyenes, ivermectin). Do not auto-disqualify based on Lipinski alone — check the bucket-specific property windows first.
- **AMES-positive ≠ disqualifying for anti-infectives**: nitroimidazole and nitrofuran clinical drugs (metronidazole, nifurtimox, benznidazole, fexinidazole, delamanid, pretomanid, nitrofurantoin) are mechanism-of-action AMES positives. Flag but contextualise.
- **hERG is still relevant** for most anti-infective candidates — fluoroquinolones and macrolides have documented cardiac risk. Apply a hERG probability threshold of 0.5 regardless of bucket.
- **Resistance-class proxy**: a hit that strongly resembles a known clinical antibiotic (Tanimoto ≥ 0.5 to bucket reference) is more likely to share class-level resistance — relevant when `--mode novel` is requested.
- **Lead-likeness, not drug-likeness, at hit triage**: keep MW ≤ 350, ClogP ≤ 3 as a *soft* preference for lead-stage hits to leave room for optimisation. Mature clinical molecules will obviously exceed these.
- **Different pathogen groups require different physchem profiles** — gram-negatives demand small + polar + amine-bearing, mycobacteria reward lipophilic, antimalarials accept higher LogP. Apply the bucket's window, not a generic one.
- **Long-treatment indications (TB, leishmaniasis) need cleaner safety profiles** than short-course therapy. Weight hepatotox / cardiotox signals more heavily.

## Anti-infective vs general drug-discovery differences

General small-molecule drug discovery optimises a compound that the host's cells will absorb, retain, and metabolise predictably. Anti-infective drug discovery has to do that *and* deliver the compound into a pathogen whose biology often opposes host pharmacokinetics. The consequences:

- **A second permeability barrier** beyond the host's gut and BBB — the pathogen's own envelope (gram-negative outer membrane, mycobacterial mycolic acid layer, fungal cell wall, kinetoplastid endosomal trafficking). What's good for host PK can be bad for pathogen entry.
- **Selectivity over a closely-related target.** Antifungals and antiparasitics target eukaryotic pathogens that share much of host biology (ergosterol vs cholesterol, tubulin variants). Therapeutic windows are tighter than for antibacterials.
- **Resistance is a moving target.** Clinical use selects for resistant strains within months to years; this shapes both target choice and structural strategy (novel scaffolds preferred when resistance is class-wide).
- **Tropical / NTD-specific constraints**: oral dosing, heat stability, paediatric formulations, low cost-of-goods, single-dose or short-course preferred. The TDR / MMV / DNDi target candidate profile (TCP) frameworks codify these.

## Lipinski / Veber / PAINS / Brenk in anti-infective context

The generic rules apply — but the violations carry different weight.

**Ro5 ([Lipinski 1997](https://doi.org/10.1016/S0169-409X(96)00423-1))** was derived from orally absorbed Phase II compounds; many clinically successful anti-infectives violate it (see next section). Treat ≥2 Lipinski violations as a flag worth explaining, not an automatic disqualification.

**Veber ([Veber 2002](https://doi.org/10.1021/jm020017n))** TPSA ≤ 140 Å² and rotatable bonds ≤ 10 are reasonable for oral anti-infectives but routinely violated by macrolides (rotatable bonds), lipopeptides, and complex natural products.

**PAINS ([Baell & Holloway 2010](https://doi.org/10.1021/jm901137j))** filters were derived from biochemical screens against soluble protein targets, *not* phenotypic antibacterial screens. Some PAINS-flagged motifs (nitro groups, hydrazones, catechols) appear in legitimate anti-infective MoAs. Flag but contextualise; do not auto-deprioritise.

**Brenk ([Brenk 2008](https://doi.org/10.1002/cmdc.200700139))** alerts overlap with PAINS but are broader. Same caveat: nitroaromatic flag in a phenotypic antiparasitic hit is mechanistically expected.

## Anti-infectives that legitimately violate Ro5

| Class | Example | Why it violates |
|---|---|---|
| Macrolides | Azithromycin | MW 749, RotBonds ~7, HBD 5 — large lactone ring |
| Glycopeptides | Vancomycin, teicoplanin | MW > 1400, many HBD — peptide + sugar scaffolds |
| Polymyxins | Colistin | MW > 1100, ~16 HBD, ~24 RotBonds — cyclic lipopeptide |
| Lipopeptides | Daptomycin | MW > 1600, many HBD — large depsipeptide |
| Polyenes | Amphotericin B | MW ~924, ~12 HBD — macrolactone with many OH |
| Avermectins | Ivermectin | MW ~875, ~8 RotBonds — macrocyclic lactone |
| Echinocandins | Caspofungin | MW > 1000, many HBD — semi-synthetic peptide |
| Rifamycins | Rifampicin | MW 823 — ansamycin macrocycle |

These compounds work because they bind targets that other small molecules cannot reach (cell wall, ribosomal surfaces, membrane assemblies). Their violation pattern is a *feature*, not a bug — recognising the pattern is more useful than enforcing Ro5.

## Reductive activation AMES caveat

Several anti-infective MoAs rely on reductive activation of a nitro group inside the pathogen. The resulting reactive species damages pathogen DNA selectively because pathogen nitroreductases differ from host. Standard Ames mutagenicity assays test the parent compound in *Salmonella* nitroreductase-expressing strains and routinely score these positive — but they have decades of clinical use:

- **Nitroimidazoles**: metronidazole, tinidazole, benznidazole, delamanid, pretomanid, fexinidazole
- **Nitrofurans**: nitrofurantoin, nifurtimox, furazolidone
- **Nitrothiazoles**: nitazoxanide

For audit reports, flag the AMES signal but state explicitly when a hit's nitro group is part of a recognised clinical scaffold. Distinguish "AMES from MoA" (acceptable risk, well-characterised) from "AMES from incidental nitro group" (genuine concern in a novel scaffold).

## hERG and cardiotoxicity context

hERG-mediated QT prolongation is real for anti-infectives, not a niche concern:
- **Fluoroquinolones** (moxifloxacin > levofloxacin > ciprofloxacin) — used as the positive control in cardiac safety pharmacology
- **Macrolides** (erythromycin, clarithromycin)
- **Azoles** (especially via CYP3A4 inhibition of co-administered drugs)
- **Bedaquiline** has a QT signal that gated its TB approval

Apply the standard 0.5 probability threshold for hERG-flag columns. Long-treatment indications (TB ≥ 6 months, visceral leishmaniasis weeks) tolerate less hERG risk than short-course therapy.

## Lead-likeness vs drug-likeness

For early-stage hits, lead-like criteria ([Teague 1999](https://doi.org/10.1002/(SICI)1521-3773(19991216)38:24%3C3743::AID-ANIE3743%3E3.0.CO;2-U); [Hann & Keserü 2012](https://doi.org/10.1038/nrd3701)) — MW ≤ 350, ClogP ≤ 3 — leave room for the inevitable MW/logP creep during optimisation. Drug-like (full Ro5) is the destination, not the starting point.

Anti-infective lead-likeness is a *soft* preference, not a gate: phenotypic hits with MW 400–500 are common and successful. Use this only to rank candidates of comparable activity, not to filter.

## TDR / MMV / DNDi Target Candidate Profile framework

The major neglected-disease product-development partnerships publish Target Candidate Profiles (TCPs) and Target Product Profiles (TPPs) that codify the property windows acceptable for a clinical candidate in their indication. Audits in those areas should cross-reference the matching TCP:

- **MMV (malaria)**: TCP-1 (clears asexual blood-stage), TCP-2 (prevents relapse), TCP-3 (chemoprotection), TCP-4 (transmission blocking), TCP-5 (P. vivax radical cure). See [Burrows 2017](https://doi.org/10.1186/s12936-017-1733-z) and [MMV's TCP page](https://www.mmv.org/research-development/information-scientists).
- **DNDi**: indication-specific TPPs for HAT, Chagas, leishmaniasis, mycetoma, paediatric HIV. See [DNDi target product profiles](https://dndi.org/research-development/target-product-profile/).
- **TB**: [Working Group for New TB Drugs](https://www.newtbdrugs.org/) maintains the public TB drug pipeline tracker.

[Katsuno 2015](https://doi.org/10.1038/nrd4683) is the canonical cross-disease summary of hit / lead / preclinical-candidate criteria for infectious diseases of the developing world. Read this if uncertain what stage criteria to apply.

## Common Ersilia ADMET column interpretation

The full table of Ersilia output column patterns and their recommended `scoring_role` / `want_high` assignments lives in [`drug-discovery-criteria.md`](./drug-discovery-criteria.md). The anti-infective-specific overrides:

- **AMES column** in a bucket with reductive-activation chemistry (antikinetoplastid, antimycobacterial) — keep as `safety_flag` but lower the report-narrative weight when the molecule has a nitro group on a recognised scaffold.
- **hERG column** in long-treatment buckets (antimycobacterial, antikinetoplastid VL, antimalarial radical cure) — keep as `safety_flag` and call out flagged compounds explicitly in the report.
- **P-gp efflux column** — relevant everywhere, but mandatory caveat for gram-negative (AcrAB-TolC is a major resistance mechanism).
- **Bioavailability / HIA columns** — pin to oral indications only; IV-only anti-infectives (echinocandins, polymyxins, amphotericin B) do not need oral PK.

## References

| # | Author, Year | Title | Source | Link |
|---|---|---|---|---|
| 1 | Lipinski et al., 1997 | Experimental and computational approaches to estimate solubility and permeability in drug discovery and development settings | Adv Drug Deliv Rev | https://doi.org/10.1016/S0169-409X(96)00423-1 |
| 2 | Veber et al., 2002 | Molecular properties that influence the oral bioavailability of drug candidates | J Med Chem | https://doi.org/10.1021/jm020017n |
| 3 | Baell & Holloway, 2010 | New substructure filters for removal of pan assay interference compounds (PAINS) from screening libraries | J Med Chem | https://doi.org/10.1021/jm901137j |
| 4 | Brenk et al., 2008 | Lessons learnt from assembling screening libraries for drug discovery for neglected diseases | ChemMedChem | https://doi.org/10.1002/cmdc.200700139 |
| 5 | Katsuno et al., 2015 | Hit and lead criteria in drug discovery for infectious diseases of the developing world | Nat Rev Drug Discov | https://doi.org/10.1038/nrd4683 |
| 6 | Brown & Wright, 2016 | Antibacterial drug discovery in the resistance era | Nature | https://doi.org/10.1038/nature17042 |
| 7 | O'Shea & Moser, 2008 | Physicochemical properties of antibacterial compounds: implications for drug discovery | J Med Chem | https://doi.org/10.1021/jm800219f |
| 8 | Teague et al., 1999 | The design of leadlike combinatorial libraries | Angew Chem Int Ed | https://doi.org/10.1002/(SICI)1521-3773(19991216)38:24%3C3743::AID-ANIE3743%3E3.0.CO;2-U |
| 9 | Hann & Keserü, 2012 | Finding the sweet spot: the role of nature and nurture in medicinal chemistry | Nat Rev Drug Discov | https://doi.org/10.1038/nrd3701 |
| 10 | Burrows et al., 2017 | New developments in anti-malarial target candidate and product profiles | Malar J | https://doi.org/10.1186/s12936-017-1733-z |

_Last reviewed: 2026-05_
