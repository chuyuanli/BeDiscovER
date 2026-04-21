## Dataset source

Licensing note: redistributed data files in this repository should be treated under the repository-level data notice in [LICENSE](../../LICENSE), namely **CC BY-NC-SA 4.0**. Original dataset-specific source notices still apply where required. Our post-processing code `read_raw.py` is licensed under the **Apache License 2.0**.

- DISRPT25 shared task on discourse relation recognition
  - Website: https://sites.google.com/view/disrpt2025/
  - GitHub: https://github.com/disrpt/sharedtask2025/tree/master
  - Cite DISRPT dataset: https://aclanthology.org/2024.lrec-main.447/ 
  - Cite DISRPT25 shared task: https://aclanthology.org/2025.disrpt-1.1/


## Data pre-processing

- Raw files obtained from https://github.com/disrpt/sharedtask2025/tree/master/data
- Size:
  - 38 datasets in the original collection; we provide 34 here
  - 16 languages
  - 6 frameworks
- **Four corpora are not publicly available**: `eng.rst.rstdt`, `eng.pdtb.pdtb`, `tur.pdtb.tdb`, and `zho.pdtb.cdtb`.
  - We therefore cannot distribute the processed versions of these datasets directly.
  - To reconstruct the raw data, users must first obtain the original corpora themselves, for example from LDC, and then run `utils/process_underscores.py` in the [DISRPT25 repository](https://github.com/disrpt/sharedtask2025/tree/master).
  - To obtain post-processed data, we provide the script `read_raw.py`, which reads `.rels` and `.conllu` files in the DISRPT format and generates `.json` files in the BeDiscovER format.
