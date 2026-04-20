## Dataset source

- Otherwise: 
  - https://aclanthology.org/2025.codi-1.7/, MIT license
  - 294 human-annotated passages that contains "otherwise" at the begining of Arg2. The template looks like: `ARG1. Otherwise, ARG2.`. https://aclanthology.org/2025.codi-1.7/, 
- Just: 
  - https://aclanthology.org/2025.findings-acl.1117/, CC-By 4.0
  - Just contains two subsets: `Just-manual` and `Just-subtitle`. The latter is curated from http://www.opensubtitles.org/. 
  - Data files are split according to the sub-set: the "manually-constructed" dataset is in `manual.tsv`, and the "subtitles" datasets are in `subtitles<i>.tsv`, where `i` represents the number of prior context dialogue turns included. 


## Data pre-processing

- Both datasets have no train or validation set
- Sizes: 
    - `otherwise`: 294 instances. No context, "Otherwise" in between [Arg1] and [Arg2]
    - `just`: 239 instances (90 manual + 149 subtitle). manual part has no context, just appears in one single sentence; subtitle part has context2 and context5, which refer to 2 and 5 sentences before the target sentence.

- Distribution:
    - `otherwise`: CONSQ. ARG. ENUM. EXCPT. = .19 .45 .13 .26 $\rightarrow$ Majority vote = 45%
    - `just`: 
        - manual section has a uniform distribution $\rightarrow$ Majority vote = 16.7%
        - subtitle section: Exclusive 60 Unelaboratory 12 Unexplanatory 22 Emphatic 21 Temporal 33 Adjective 1 $\rightarrow$ Majority vote = 40.3%
