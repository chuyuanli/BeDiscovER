## Dataset source

- DISRPT25 shared task on discourse relation recognition
  - Paper: https://aclanthology.org/2025.disrpt-1.1/
  - Website: https://sites.google.com/view/disrpt2025/
  - GitHub: https://github.com/disrpt/sharedtask2025/tree/master
  - Licensing: each dataset retains its original license, so please check the license for each corpus as needed. Our post-processing code is licensed under the **Apache License 2.0**.


## Data pre-processing

- Raw files obtained from https://github.com/disrpt/sharedtask2025/tree/master/data
- We read `.rels` and `.collu` files.
- Size:
  - 38 datasets in the original collection; we provide 34 here
  - 16 languages
  - 6 frameworks
- **Four corpora are not publicly available**: `eng.rst.rstdt`, `eng.pdtb.pdtb`, `tur.pdtb.tdb`, and `zho.pdtb.cdtb`.
  - We therefore cannot distribute the processed versions of these datasets directly.
  - To support post-processing, we provide the script `read_raw.py`.
  - To reconstruct the raw data, users must first obtain the original corpora themselves, for example from LDC, and then run `utils/process_underscores.py` in the DISRPT25 repository.
