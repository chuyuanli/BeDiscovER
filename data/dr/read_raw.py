import io
import os
import re
import glob
import json
import conllu
from pathlib import Path


DISRPT_TEST_NAMES = [
    "ces.rst.crdt", 
    "deu.pdtb.pcc", "deu.rst.pcc", 
    "eng.dep.covdtb", "eng.dep.scidtb", 
    "eng.erst.gentle", "eng.erst.gum", 
    "eng.pdtb.gentle", "eng.pdtb.gum", "eng.pdtb.pdtb", "eng.pdtb.tedm", 
    "eng.rst.oll", "eng.rst.rstdt", "eng.rst.sts", "eng.rst.umuc",
    "eng.sdrt.msdc", "eng.sdrt.stac", 
    "eus.rst.ert", 
    "fas.rst.prstc", 
    "fra.sdrt.annodis", 
    "ita.pdtb.luna", 
    "nld.rst.nldt", 
    "pcm.pdtb.disconaija", 
    "pol.iso.pdc", 
    "por.pdtb.crpc", "por.pdtb.tedm", "por.rst.cstn", 
    "rus.rst.rrt", 
    "spa.rst.rststb", "spa.rst.sctb", 
    "tha.pdtb.tdtb", 
    "tur.pdtb.tdb", "tur.pdtb.tedm", 
    "zho.dep.scidtb", "zho.pdtb.cdtb", "zho.pdtb.ted", "zho.rst.gcdt", "zho.rst.sctb"
    ]

LABELS = [
    "contrast",
    "condition",
    "mode",
    "organization",
    "frame",
    "temporal",
    "concession",
    "reformulation",
    "comment",
    "query",
    "attribution",
    "alternation",
    "purpose",
    "explanation",
    "elaboration",
    "causal",
    "conjunction"
]

DIRECTION_MAP = {"1>2": "From Unit1 to Unit2.", "1<2": "From Unit2 to Unit1.", "_": "Unknown."}

NO_TRAIN = ['eng.dep.covdtb', 'eng.erst.gentle', 'eng.pdtb.gentle', 'eng.pdtb.tedm', 
            'fra.sdrt.summre', 'por.pdtb.tedm', 'tur.pdtb.tedm']


def read_conll_sentences_split(filepath):
    if not Path(filepath).exists():
        raise FileNotFoundError(f"Conll file {filepath} does not exist.")

    with open(filepath, encoding="utf-8") as f:
        text = f.read()
        conllu_sentences = conllu.parse(text)
    return conllu_sentences


def get_conllu_sentences_by_docs(split_prefix):
    """
    Organizes conllu sentences into a dictionary indexed by doc_id.
    Each entry in the dictionary contains the sentences for that doc_id.
    """
    # Read the .conllu/tok files and convert them to a dataset
    filepath = split_prefix + ".conllu"
    conllu_sentences = read_conll_sentences_split(filepath)
    organized_sentences = {}
    doc_id = None  # Initialize doc_id to None
    for sentence in conllu_sentences:
        sent_id = 0
        if 'newdoc id' in sentence.metadata:
            doc_id = sentence.metadata['newdoc id']
            assert doc_id not in organized_sentences, f"Duplicate doc_id found: {doc_id}"
            organized_sentences[doc_id] = []
        # sent_id = sentence.metadata['sent_id']
        # assert doc_id is not None, f"Doc_id should be set before adding sentences. At sent_id {sent_id} without doc_id"
        organized_sentences[doc_id].append(sentence)
    return organized_sentences


# using conllu: some tok files don't have seg information
def get_segs_and_toks_for_docs_from_conllu(split_prefix):
    data = get_conllu_sentences_by_docs(split_prefix)

    sents_for_docs = dict()  # {'file_name': [[tok1, tok2, ...], ...]}
    toks_for_docs = dict()

    for fn in data:
        sents_for_docs[fn] = []
        toks_for_docs[fn] = []
        for sentence in data[fn]:
            sent = []
            for token in sentence:
                if '-' not in str(token['id']) and '.' not in str(token['id']):
                    sent.append(token['form'])
                    toks_for_docs[fn].append(token['form'])
            sents_for_docs[fn].append(sent)

    # Index for fast access
    lr2idx = {} # {'file_name': {(l, r): idx}}, l and r stand for sentence start and end index
    idx2lr = {} # {'file_name': {idx: (l, r)}}

    for fn in sents_for_docs:
        sentence_ls = sents_for_docs[fn]
        cnt = 1
        for idx, sent in enumerate(sentence_ls):
            l = cnt
            cnt += len(sent)
            r = cnt - 1
            if fn not in idx2lr:
                idx2lr[fn], lr2idx[fn] = {}, {}
            idx2lr[fn][idx] = (l, r)
            lr2idx[fn][(l, r)] = idx

    return lr2idx, idx2lr, toks_for_docs


def get_context(s1ors2, doc_id, s_toks, lr2idx, idx2lr, toks_for_docs, context_sent, context_tok):
    lr2idx = lr2idx[doc_id]
    idx2lr = idx2lr[doc_id]
    toks_for_docs = toks_for_docs[doc_id]

    # eng.pdtb.tedm talk_1927_en line 52 614-623,624-715
    if "," in s_toks:
        ranges = s_toks.split(",")
        s_start, s_end = None, None

        for r in ranges:
            s, e = map(int, r.split('-'))

            if s_start is None or s < s_start:
                s_start = s
            if s_end is None or e > s_end:
                s_end = e

    elif "-" in s_toks:
        s_start, s_end = s_toks.split("-")
    else:
        s_start = s_end = s_toks

    if (int(s_start), int(s_end)) in lr2idx:
        s = ' '.join(toks_for_docs[(int(s_start)-1):int(s_end)])
        idx = lr2idx[(int(s_start), int(s_end))]
    else:
        # example: eng.rst.rstdt_dev wsj_0629 (942, 1042)
        sentence_range = []

        for (start, end), sentence_number in lr2idx.items():
            if not (int(s_end) < start or int(s_start) > end):
                sentence_range.append(sentence_number)

        s = ' '.join(' '.join(toks_for_docs[s_start-1:s_end]) for s_r in sentence_range for s_start, s_end in [idx2lr[s_r]])
        idx = sentence_range[0] if s1ors2 == 1 else sentence_range[-1]
        
    context_idx = idx
    context = []
    while abs(idx - context_idx) < context_sent or sum(len(sublist) for sublist in context) < context_tok:
        context_idx = context_idx - 1 if s1ors2 == 1 else context_idx + 1
        if context_idx not in idx2lr:
            break
        lr = idx2lr[context_idx]
        context.insert(0, toks_for_docs[lr[0]-1:lr[1]]) if s1ors2 == 1 else context.append(toks_for_docs[lr[0]-1:lr[1]])
    return s, " ".join(word for sublist in context for word in sublist)


def read_rels_split(split_prefix, lang, framework, corpus, context_sent, context_tok):
    # Ref: https://github.com/disrpt/sharedtask2025/blob/091404690ed4912ca55873616ddcaa7f26849308/utils/disrpt_eval_2024.py#L246
    data = io.open(split_prefix + ".rels", encoding="utf-8").read().strip().replace("\r", "")
    lines = data.split("\n")
    header = lines[0]
    split_lines = [line.split("\t") for line in lines[1:]]
    DIRECTION_ID = -4
    TYPE_ID = -3
    LABEL_ID = -1
    UNIT_1_TOKS = 1
    UNIT_2_TOKS = 2
    U1_ID = 5
    U2_ID = 6
    S1_TOKS = 7
    S2_TOKS = 8
    S1_SENT_ID = 9
    S2_SENT_ID = 10
    DIRECTION_ID = -4

    labels = [line[LABEL_ID] for line in split_lines]
    doc_ids = [line[0] for line in split_lines]
    # tackle pcm.pdtb.disconaija
    if "pcm.pdtb.disconaija" in split_prefix:
        doc_ids = [line[0].removesuffix(".txt") for line in split_lines]
    u1s = [line[U1_ID] for line in split_lines]
    u1_toks = [line[UNIT_1_TOKS].split("-") for line in split_lines]
    u2s = [line[U2_ID] for line in split_lines]
    u2_toks = [line[UNIT_2_TOKS].split("-") for line in split_lines]
    u1_sents = [line[S1_SENT_ID] for line in split_lines]
    u2_sents = [line[S2_SENT_ID] for line in split_lines]
    directions = [line[DIRECTION_ID] for line in split_lines]
    types = [line[TYPE_ID] for line in split_lines]
    s1_toks = [line[S1_TOKS] for line in split_lines]
    s2_toks = [line[S2_TOKS] for line in split_lines]

    print(f"Loading {split_prefix} with LFC features: {lang} {framework} {corpus} ")

    lr2idx, idx2lr, toks_for_docs = get_segs_and_toks_for_docs_from_conllu(split_prefix)
    contexts = []
    if context_sent > 0 or context_tok > 0:
        for i in range(0, len(split_lines)):
            doc_id = doc_ids[i]
            s1_tok = s1_toks[i]
            s2_tok = s2_toks[i]
            s1, s1_context = get_context(1, doc_id, s1_tok, lr2idx, idx2lr, toks_for_docs, context_sent, context_tok)
            s2, s2_context = get_context(2, doc_id, s2_tok, lr2idx, idx2lr, toks_for_docs, context_sent, context_tok)

            if s1_tok == s2_tok:
                context = [s1_context, s1, s2_context]
            else:
                context = [s1_context, s1+''+s2, s2_context]
            contexts.append(context)

    # contains features for whole dataset
    data_dict = {
        "id": list(range(len(labels))),
        "lang": [lang] * len(labels),
        "framework": [framework] * len(labels),
        "corpus": [corpus] * len(labels),
        "label": labels,
        "type": types,
        "doc_id": doc_ids,
        "u1": u1s,
        "u1_toks": u1_toks,
        "u2": u2s,
        "u2_toks": u2_toks,
        "u1_sent": u1_sents,
        "u2_sent": u2_sents,
        "text": [f"{u1} {u2}" for u1, u2 in zip(u1s, u2s)],
        "direction": directions,
    }
    if len(contexts) > 0:
        data_dict["context"] = contexts

    return data_dict


def get_meta_features_for_dataset(dataset_name):
    lang, framework, source_dataset = dataset_name.split(".")
    source_dataset = source_dataset.split("_")[0]  # Remove any suffix like -v1
    return lang, framework, source_dataset


def load_disrpt_dataset_to_json(dataset_name, split, sentences_for_context, tokens_for_context):
    """
    Adapted from DeDisco codebase: https://github.com/gucorpling/disrpt25-task
    Load a dataset from the specified directory and split.
    Args:
        dataset_name (str): Name of the dataset (e.g., 'eng.pdtb.gum').
        split (str): Split to load ('train', 'dev', 'test').
        sentences_for_context (int): Number of sentences to include as context.
        tokens_for_context (int): Number of tokens to include as context.
    Returns:
        List[Dict]: List of records with features.
    """

    dataset = {}
    dataset_prefix = f"{DATA_DIR}/{dataset_name}/"
    lang, framework, corpus = get_meta_features_for_dataset(dataset_name)

    def load_split_if_it_exists(split_name):
        rels_file = f"{dataset_prefix}{dataset_name}_{split_name}.rels"
        if Path(rels_file).exists() is True:
            conllu_file = f"{dataset_prefix}{dataset_name}_{split_name}.conllu"
            rels = read_rels_split(f"{DATA_DIR}/{dataset_name}/{dataset_name}_{split_name}", 
                                   lang, framework, corpus, 
                                   sentences_for_context, tokens_for_context)
                        
            dataset[split_name] = rels
        else:
            raise ValueError(f"No {split_name} split found for {dataset_name}.")
    
    load_split_if_it_exists(split_name=split)
    
    records = [dict(zip(dataset[split].keys(), values)) for values in zip(*dataset[split].values())]    
    return records


if __name__ == "__main__":

    DATA_DIR = "data/dr/raw"
    subset = 'test'

    dataset_list = sorted([child.name for child in Path(DATA_DIR).iterdir() if child.is_dir() and child.name in DISRPT_TEST_NAMES])
    
    for dataset_name in dataset_list:
        if subset == 'train' and dataset_name in NO_TRAIN:
            print(f"Skipping {dataset_name} for no train set.")
            continue
        records = load_disrpt_dataset_to_json(dataset_name, split=subset,
                                              sentences_for_context=1, tokens_for_context=30)        
        
        output_dir = f"data/dr/disrpt25/{dataset_name}"
        if os.path.exists(output_dir) is False:
            os.makedirs(output_dir, exist_ok=True)
        with open(f"{output_dir}/{subset}_id.json", mode='w', encoding="utf-8") as outf:
            json.dump(records, outf, ensure_ascii=False, indent=4)
