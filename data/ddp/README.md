## Dataset source

- STAC: https://aclanthology.org/L16-1432/
- Molweni: https://aclanthology.org/2020.coling-main.238/
- MSDC: https://aclanthology.org/2024.lrec-main.444/


## Data processing

- STAC data files come from [seq2seq-ddp](https://github.com/chuyuanli/Seq2Seq-DDP/tree/main/data) `natural` format. This is an incremental parsing format. Each new entry contains one new speech turn and previous established structures. 
- Same for molweni.
- Converted MSDC original data to incremental style from https://github.com/linagora-labs/MinecraftStucturedDialogueCorpus/tree/main.

- Sizes (test split)
    - STAC: 1045 instances
    - Molweni: 3930 instances
    - MSDC: 4914 instances
