---
description: Generate a metadata.yml file for an Ersilia Model Hub (eos-template) repository from a paper PDF or URL
argument-hint: <pdf-path-or-url> [--model-id <eosXXXX>] [--source-code <url>] [--contributor <github-username>]
allowed-tools: [Read, WebFetch, Write, AskUserQuestion]
---

# Draft metadata.yml for Ersilia Model Hub

You are generating a `metadata.yml` file for an Ersilia Model Hub model repository (eos-template format), based on a scientific publication provided as a local PDF path or a URL.

## Important Constraints

- Do all reasoning yourself. Do NOT call any external scripts, APIs, or LLMs to assist with metadata extraction or suggestion. This includes — but is not limited to — `.github/scripts/suggest_metadata_with_llm.py` or any script that invokes OpenAI, Anthropic, or any other AI service.
- Do NOT use `Bash` to run any Python script that contacts an external API.
- The only tools you may use are: `Read` (to read local PDFs), `WebFetch` (to read publication pages), `Write` (to write the output file), and `AskUserQuestion` (to clarify ambiguous fields with the user).

## Parse Arguments

- `<pdf-path-or-url>` (required): Local path to a PDF file, or a URL to a publication (HTML or PDF)
- `--model-id <eosXXXX>` (optional): Ersilia model identifier. If not provided, leave as `null` and note that it must be filled in later.
- `--source-code <url>` (optional): URL to the model source code repository (e.g. GitHub). If not provided, try to extract it from the paper.
- `--contributor <github-username>` (optional): GitHub username of the contributor. Leave blank if not provided.

## Step 1: Read the Publication

**If a local PDF path is provided**: Use the Read tool to read the PDF file.

**If a URL is provided**: Use WebFetch to retrieve the page content with this prompt:
> "Extract the full text of this scientific publication including: title, authors, abstract, methods, model description, input/output format, training data, performance metrics, license, and any links to code repositories."

From the publication, extract:
- **Title** of the paper and a concise model title (max 100 chars, should describe what the model predicts/does)
- **Abstract and methods** — understand what the model does
- **Input type**: What goes in? (molecules/SMILES, protein sequences, text, etc.)
- **Output type**: What comes out? (scalar values, probabilities, embeddings, generated molecules, etc.)
- **Output dimension**: How many values per input? (1 for a single score, N for fingerprints/embeddings)
- **ML task**: Is this featurization, property prediction, activity prediction, generation, similarity search, projection?
- **Biological context**: What disease, organism, or property does it target?
- **Publication URL** (the URL of the paper itself)
- **Source code URL** (GitHub or similar — look in the paper body, supplementary, or abstract)
- **License** (check the paper, GitHub repo mention, or supplementary)
- **Publication year**
- **Publication type**: peer reviewed journal, preprint (arXiv, bioRxiv, ChemRxiv), or other
- **Performance metrics** (for context, to inform the Interpretation field)
- **Slug suggestion**: a short, lowercase, hyphenated identifier for the model (5–60 chars)

## Step 2: Map to Ersilia Metadata Vocabulary

Use ONLY values from the controlled vocabulary lists below. Do not invent new values.

### Task (pick exactly one)
- `Representation` — model produces molecular/protein representations (embeddings, fingerprints, descriptors)
- `Annotation` — model predicts a property or label for a molecule (ADMET, bioactivity, toxicity, etc.)
- `Sampling` — model generates new molecules or modifies existing ones

### Subtask (pick exactly one)
- `Featurization` — converts input to a feature vector (fingerprints, descriptors, embeddings)
- `Projection` — dimensionality reduction (PCA, UMAP, t-SNE)
- `Property calculation or prediction` — predicts a physicochemical or ADMET property
- `Activity prediction` — predicts biological activity (IC50, MIC, binding affinity, etc.)
- `Similarity search` — computes similarity scores between molecules
- `Generation` — generates new molecular structures

### Input (pick one or more from list)
`Compound`, `Protein`, `Text`

### Output (pick one or more from list)
`Compound`, `Score`, `Value`, `Text`

- Use `Score` for probabilities, binary outputs, classification scores (0–1 range)
- Use `Value` for continuous regression values (logS, logP, IC50 in µM, embeddings coordinates, etc.)
- Use `Compound` for generated or transformed SMILES output
- Use `Text` for textual output

### Output Consistency
- `Fixed` — same input always gives the same output (deterministic models)
- `Variable` — output may differ between runs (generative/stochastic models)

### Tag (select 1–5 from this list)
AIDS, Alzheimer, Cancer, Cardiotoxicity, Cytotoxicity, COVID19, Dengue, Malaria, Neglected tropical disease, Schistosomiasis, Tuberculosis, A.baumannii, E.coli, E.faecium, HBV, HIV, HDAC1, Human, K.pneumoniae, Mouse, M.tuberculosis, P.aeruginosa, P.falciparum, N.gonorrhoeae, Rat, Sars-CoV-2, S.aureus, ESKAPE, BACE, CYP450, GPCR, hERG, Fraction bound, IC50, Half-life, LogD, LogP, LogS, MIC90, Molecular weight, Papp, pKa, ADME, Antimicrobial activity, Antiviral activity, Bioactivity profile, Lipophilicity, Metabolism, Microsomal stability, Natural product, Price, Quantum properties, Permeability, Side effects, Solubility, Synthetic accessibility, Target identification, Therapeutic indication, Toxicity, ChEMBL, DrugBank, MoleculeNet, Tox21, ToxCast, TDCommons, ZINC, Chemical graph model, Chemical language model, Chemical notation, Chemical synthesis, Compound generation, Descriptor, Drug-likeness, Embedding, Fingerprint, Similarity, Biomedical text, Mycetoma, Antifungal activity, Frequent hitter

### Biomedical Area (select one or more from list)
Any, ADMET, Antimicrobial resistance, Malaria, Tuberculosis, COVID-19, Gonorrhea, Cancer, Mycetoma, AIDS, Schistosomiasis, Hepatitis, Alzheimer, Chagas, Cryptosporidiosis, Leprosy

### Target Organism (select one or more from list)
Any, Homo sapiens, Mus musculus, Rattus norvegicus, Plasmodium falciparum, Plasmodium vivax, Mycobacterium tuberculosis, Fast-acid bacteria, Fungi, Gram-negative bacteria, Gram-positive bacteria, Schistosoma mansoni, Madurella mycetomatis, Burkholderia cenocepacia, Acinetobacter baumannii, Neisseria gonorrhoeae, Staphylococcus aureus, Pseudomonas aeruginosa, Enterobacteriaceae spp, Enterococcus faecium, Escherichia coli, Helicobacter pylori, Campylobacter spp, Salmonella spp, Streptococcus pneumoniae, Haemophilus influenzae, Shigella spp, SARS-CoV-2, SARS-CoV-1, MERS, Hepatitis B virus, Hepatitis C virus, HIV, Ebola virus, Klebsiella pneumoniae

### Publication Type
- `Peer reviewed` — published in a peer-reviewed journal
- `Preprint` — arXiv, bioRxiv, ChemRxiv, or similar
- `Other` — anything else (blog post, thesis, technical report)

### License (pick from list)
MIT, GPL-3.0-only, GPL-3.0-or-later, LGPL-3.0-only, LGPL-3.0-or-later, AGPL-3.0-only, AGPL-3.0-or-later, Apache-2.0, BSD-2-Clause, BSD-3-Clause, MPL-2.0, CC-BY-3.0, CC-BY-4.0, CC0-1.0, Proprietary, None

### Source Type
- `External` — model from a third-party author (most common for incorporated models)
- `Replicated` — model reimplemented by Ersilia
- `Internal` — model developed by Ersilia

## Step 3: Compose the metadata.yml

Fill in all pre-deployment fields. Leave post-deployment fields (DockerHub, S3, Docker Architecture, Model Size, Environment Size, Image Size, Computational Performance, Last Packaging Date, Incorporation Date, Release, Docker Pack Method) out of the file entirely — they are filled in automatically by CI/CD after packaging.

Use this exact format (note YAML style with list items using `- ` and multiline strings with `\n  ` continuation):

```yaml
Identifier: <eosXXXX or null>
Slug: <lowercase-hyphenated-slug>
Status: In progress
Title: <concise title, max 100 chars>
Description: <At least 200 characters. Single paragraph. Describe what the model
  does, the method, the training data, and the key result. Wrap long lines with
  two-space continuation.>
Deployment:
  - Local
Source: Local
Source Type: External
Task: <one of: Representation | Annotation | Sampling>
Subtask: <one of the six subtask values>
Input:
  - <Compound | Protein | Text>
Input Dimension: 1
Output:
  - <Score | Value | Compound | Text>
Output Dimension: <integer>
Output Consistency: <Fixed | Variable>
Interpretation: <10–300 chars. One sentence on how to read the output.>
Tag:
  - <tag1>
  - <tag2>
Biomedical Area:
  - <area>
Target Organism:
  - <organism>
Publication Type: <Peer reviewed | Preprint | Other>
Publication Year: <YYYY>
Publication: <URL or empty>
Source Code: <URL or empty>
License: <license identifier>
Contributor: <github-username or empty>
```

## Step 4: Validate

Before writing the file, verify:
- `Identifier`: matches `eos[1-9][a-z0-9]{3}` or is null
- `Slug`: lowercase, 5–60 chars, no spaces
- `Title`: 10–300 chars
- `Description`: ≥200 chars
- `Task`, `Subtask`, `Input`, `Output`, `Output Consistency`, `Tag`, `Biomedical Area`, `Target Organism`, `Publication Type`, `License`, `Source Type`: all values are from the controlled vocabulary
- `Input Dimension`, `Output Dimension`: positive integers
- `Interpretation`: 10–300 chars
- `Publication`, `Source Code`: valid URLs or empty

If `--model-id` was not provided, set `Identifier` to `null` and add a note that it must be assigned before submission.

## Step 5: Write and Report

Write the file to `./metadata.yml` in the current working directory (or to the output directory if the user specified one).

Then display:
- The full contents of the generated `metadata.yml`
- A validation summary (which fields were confidently extracted vs. which need human review)
- Any fields that could not be determined from the paper and require manual completion, listed explicitly

If a field cannot be determined from the paper, use a reasonable default and flag it as needing review rather than stopping.
