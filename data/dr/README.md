## Dataset source

- DISRPT25 shared task on discourse relation recognition: https://aclanthology.org/2025.disrpt-1.1/
- Website: https://sites.google.com/view/disrpt2025/
- Github: https://github.com/disrpt/sharedtask2025/tree/master


## Data pre-processing

- Raw files obtained from https://github.com/disrpt/sharedtask2025/tree/master/data
- Read `.rels` and `.collu` files 
- Size:
    - 38 datasests $\rightarrow$ here we provide 34
    - 16 languages
    - 6 frameworks
- **Note that 4 corpora are not publically available** (`eng.rst.rstdt`, `eng.pdtb.pdtb`, `tur.pdtb.tdb`, `zho.pdtb.cdtb`). 
  - For these datasets, we cannot distribute the processed data directly. Instead, we provide the script `read_raw.py` to help with post-processing. 
  - Users will need to obtain the original data themselves (for example, from LDC) and then run `utils/process_underscores.py` in the disrpt25 repository to reconstruct the raw data.
