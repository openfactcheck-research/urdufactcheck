<p align="center">
  <img alt="OpenFactCheck Logo" src="assets/splash.png" height="120" />
  <p align="center">An Agentic Fact-Checking Framework for Urdu
with Evidence Boosting and Benchmarking
    <br>
  </p>
</p>

---

<p align="center">
    <a href="#overview">Overview</a> •
    <a href="#installation">Installation</a> •
    <a href="#usage">Usage</a>
</p>

## Overview

UrduFactCheck is an open-source fact-checking pipeline for Urdu language. It is designed to be integrated in [OpenFactCheck](https://github.com/mbzuai-nlp/OpenFactCheck).

## Installation

First step is to clone the repository:

```bash
git clone github.com/mbzuai-nlp/UrduFactCheck.git
cd UrduFactCheck
```

Then, install the required packages, OpenFactCheck will also be installed as a submodule:

```bash
pip install -r requirements.txt
```

## Usage

To use UrduFactCheck, you first need to set up the `config.json` file for OpenFactCheck. You can use [this](src/urdufactcheck/config.json) as a template. 

UrduFactCheck provide three type of retrievers:

1. `urdufactcheck_retriever`: This retriever retrieves the evidence directly in Urdu language.
2. `urdufactcheck_translator_retriever`: This retriever first translates the query to English and then retrieves the evidence in English and finally translates the evidence back to Urdu.
3. `urdufactcheck_thresholded_translator_retriever`: This retriever first retrieves the evidence in Urdu language. If the evidence count is less than the threshold, it boosts the evidence as `urdufactcheck_translator_retriever`.

These retrievers can be specified in the `pipeline` section of the `config.json` file. For example:

```json
{
    "pipeline": [
        "urdufactcheck_claimprocessor",
        "urdufactcheck_thresholded_translator_retriever",
        "urdufactcheck_verifier"
    ],
}
```

To run the pipeline, you can create a python script as follows:

```python
from openfactcheck import OpenFactCheck, OpenFactCheckConfig

config = OpenFactCheckConfig(
    filename_or_path="config.json"
)

response = OpenFactCheck(config).ResponseEvaluator.evaluate(
    response="قائداعظم محمد علی جناح پاکستان کے بانی اور پہلے گورنر جنرل تھے۔",
)
```

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
    ISBN = "979-8-89176-335-7",
}
```