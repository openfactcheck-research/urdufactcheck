<div align="center">

<img alt="UrduFactCheck" src="assets/splash.png" height="40" />

# UrduFactCheck

<strong>An Agentic Fact-Checking Framework for Urdu with Evidence Boosting and Benchmarking</strong>

<sub>Sarfraz Ahmad · Hasan Iqbal · Momina Ahsan · Numaan Naeem · Muhammad Ahsan Riaz Khan · Arham Riaz</sub>

<sub>Muhammad Arslan Manzoor · Yuxia Wang · Preslav Nakov</sub>

<sub>MBZUAI, Abu Dhabi, UAE</sub>

<br>

[![Paper](https://img.shields.io/badge/Findings%20of%20EMNLP-2025-c0392b?style=flat-square&logo=acm&logoColor=white)](https://aclanthology.org/2025.findings-emnlp.1240/)
[![arXiv](https://img.shields.io/badge/arXiv-2505.15063-b31b1b?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2505.15063)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![OpenFactCheck](https://img.shields.io/badge/Built%20for-OpenFactCheck-0f766e?style=flat-square)](https://github.com/mbzuai-nlp/OpenFactCheck)
[![License](https://img.shields.io/badge/License-GPL%20v3-lightgrey?style=flat-square)](LICENSE)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Repository Structure](#repository-structure)
- [Citation](#citation)

---

## Overview

UrduFactCheck is an open-source, modular fact-checking pipeline for Urdu. It is designed to integrate with [OpenFactCheck](https://github.com/mbzuai-nlp/OpenFactCheck) and supports evidence retrieval under low-resource conditions through monolingual and translation-augmented strategies.

The project introduces and evaluates:

- UrduFactBench for claim verification in Urdu.
- UrduFactQA for factual consistency evaluation of Urdu QA outputs.
- A configurable fact-checking framework with evidence boosting.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/mbzuai-nlp/UrduFactCheck.git
cd UrduFactCheck
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Configure OpenFactCheck using [src/urdufactcheck/config.json](src/urdufactcheck/config.json) as a template.

UrduFactCheck provides three retrievers:

1. `urdufactcheck_retriever`: Retrieves evidence directly in Urdu.
2. `urdufactcheck_translator_retriever`: Translates the query to English, retrieves English evidence, then translates evidence back to Urdu.
3. `urdufactcheck_thresholded_translator_retriever`: Tries Urdu retrieval first, then boosts with translation-based retrieval if evidence is below threshold.

Example pipeline configuration:

```json
{
  "pipeline": [
    "urdufactcheck_claimprocessor",
    "urdufactcheck_thresholded_translator_retriever",
    "urdufactcheck_verifier"
  ]
}
```

Example usage:

```python
from openfactcheck import OpenFactCheck, OpenFactCheckConfig

config = OpenFactCheckConfig(filename_or_path="config.json")

response = OpenFactCheck(config).ResponseEvaluator.evaluate(
    response="قائداعظم محمد علی جناح پاکستان کے بانی اور پہلے گورنر جنرل تھے۔"
)
```

---

## Repository Structure

```
UrduFactCheck/
├── datasets/
│   ├── raw/              # Raw benchmark data (claims, QA)
│   └── processed/        # Processed claims and QA data
└── src/
    ├── download/         # Dataset download and preparation scripts
    ├── translate/        # Translation pipelines and examples
    └── urdufactcheck/    # Core framework, config, evaluation scripts, and outputs
```

---

## Citation

If you use UrduFactCheck in your research, please cite:

```bibtex
@inproceedings{ahmad-etal-2025-urdufactcheck,
    title = "{U}rdu{F}act{C}heck: An Agentic Fact-Checking Framework for {U}rdu with Evidence Boosting and Benchmarking",
    author = "Ahmad, Sarfraz  and
      Iqbal, Hasan  and
      Ahsan, Momina  and
      Naeem, Numaan  and
      Khan, Muhammad Ahsan Riaz  and
      Riaz, Arham  and
      Manzoor, Muhammad Arslan  and
      Wang, Yuxia  and
      Nakov, Preslav",
    editor = "Christodoulopoulos, Christos  and
      Chakraborty, Tanmoy  and
      Rose, Carolyn  and
      Peng, Violet",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2025",
    month = nov,
    year = "2025",
    address = "Suzhou, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.findings-emnlp.1240/",
    doi = "10.18653/v1/2025.findings-emnlp.1240",
    pages = "22788--22802",
    ISBN = "979-8-89176-335-7"
}
```
