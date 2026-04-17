import json
import argparse


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

# 20% fraction in test set, in total ~8.7k instances (compared to 43k instances in full test)
DISRPT_FRAC_MAP = {
    "ces.rst.crdt": 1.0,
    "deu.pdtb.pcc": 1.0,
    "deu.rst.pcc": 1.0,
    "eng.dep.covdtb": 0.1,
    "eng.dep.scidtb": 0.1,
    "eng.erst.gentle": 0.1,
    "eng.erst.gum": 0.07,
    "eng.pdtb.gentle": 0.3,
    "eng.pdtb.gum": 0.15,
    "eng.pdtb.pdtb": 0.05,
    "eng.pdtb.tedm": 0.7,
    "eng.rst.oll": 1.0,
    "eng.rst.rstdt": 0.1,
    "eng.rst.sts": 0.8,
    "eng.rst.umuc": 0.5,
    "eng.sdrt.msdc": 0.04,
    "eng.sdrt.stac": 0.2,
    "eus.rst.ert": 0.5,
    "fas.rst.prstc": 0.4,
    "fra.sdrt.annodis": 0.4,
    "ita.pdtb.luna": 0.6,
    "nld.rst.nldt": 0.6,
    "pcm.pdtb.disconaija": 0.2,
    "pol.iso.pdc": 0.3,
    "por.pdtb.crpc": 0.2,
    "por.pdtb.tedm": 0.7,
    "por.rst.cstn": 1.0,
    "rus.rst.rrt": 0.1,
    "spa.rst.rststb": 0.5,
    "spa.rst.sctb": 1.0,
    "tha.pdtb.tdtb": 0.2,
    "tur.pdtb.tdb": 0.5,
    "tur.pdtb.tedm": 0.7,
    "zho.dep.scidtb": 1.0,
    "zho.pdtb.cdtb": 0.3,
    "zho.pdtb.ted": 0.2,
    "zho.rst.gcdt": 0.2,
    "zho.rst.sctb": 1.0
}


DIRECTION_MAP = {"1>2": "From Unit1 to Unit2.", "1<2": "From Unit2 to Unit1.", "_": "Unknown."}


def load_raw_data(task, dataset_dir, dataset_name, subset, num=0):
    if task == 'so':
        f_name = dataset_dir + f'/{task}/{dataset_name}/{subset}_id.jsonl'
        with open(f_name, 'r') as f:
            data = [json.loads(line) for _i, line in enumerate(f) if num <= 0 or _i < num]
            for obj in data:
                if "shuf_idx" in obj:
                    obj["gold"] = ' '.join(obj["shuf_idx"]) # use "shuf_idx" as "gold" key for eval
    elif task in ['tr', 'dm', 'ddp']:
        f_name = dataset_dir + f'/{task}/{dataset_name}/{subset}_id.json'
        with open(f_name, 'r') as f:
            data = json.load(f)[:num] if num > 0 else json.load(f)
    elif task == 'dr':
        f_name = dataset_dir + f'/{task}/disrpt25/{dataset_name}/{subset}_id.json'
        with open(f_name, 'r') as f:
            data = json.load(f)[:num] if num > 0 else json.load(f)
            for obj in data:
                if "label" in obj:
                    obj["gold"] = obj.pop("label") # remove "label" key, use "gold" key instead
    else:
        raise NotImplementedError

    return data


def load_data(args):
            
    if args.task == 'dr' and args.dataset_names[0] == 'disrpt25':
        args.dataset_names = DISRPT_TEST_NAMES
        if args.dataset_fracs[0] == 1.0:
            args.dataset_fracs = [args.dataset_fracs[0] for _ in args.dataset_names]
            print('Set all disrpt25 dataset fracs to 1.0.')
        elif args.dataset_fracs[0] == 0.2: # means in total take 20% of all disrpt25 data
            args.dataset_fracs = list(DISRPT_FRAC_MAP.values())
            assert list(DISRPT_FRAC_MAP.keys()) == args.dataset_names
            print("Set disrpt25 dataset fracs to 20%.")
    
    test_all = []
    for dataset_name, dataset_frac in zip(args.dataset_names, args.dataset_fracs):
        test_data = load_raw_data(args.task, args.data_root, dataset_name, args.split)
        test_data = test_data[:int(dataset_frac * len(test_data))]
        test_all += test_data

    return test_all


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, default='so', choices=['so', 'tr', 'dr', 'dm', 'ddp'],
                        help="""so: sentence ordering; tr: temporal reasoning; 
                        dr: discourse relation recognition (DISRPT25 version);
                        dm: discourse marker sense recognition (otherwise, just);
                        ddp: dialogue discourse parsing (stac, molweni, msdc)""")
    parser.add_argument("--data_root", type=str, default="data")
    parser.add_argument("--dataset_names", type=str, nargs='+', default=[''])
    parser.add_argument("--dataset_fracs", type=float, nargs='+', default=[1.0])
    parser.add_argument("--split", type=str, default='test')
    args = parser.parse_args()

    load_data(args)

    # Usage examples: 
    # python load_data.py --task dm --dataset_names just --dataset_fracs 1.0 --split test
    # python load_data.py --task dm --dataset_names otherwise --dataset_fracs 1.0 --split test
    # python load_data.py --task tr --dataset_names tbd-ee tdd-man --dataset_fracs 1.0 1.0 --split test
    # python load_data.py --task tr --dataset_names tot-arithmetic --dataset_fracs 1.0 --split test
    # python load_data.py --task dr --dataset_names disrpt25 --dataset_fracs 0.2 --split test
    # python load_data.py --task so --dataset_names aan-abstract arxiv-abstracts nips-abs nsf roc sind-captions wiki-movies --dataset_fracs 0.3 0.05 1.0 0.08 0.09 0.16 0.25 --split test
    # python load_data.py --task ddp --dataset_names stac molweni msdc --dataset_fracs 1.0 1.0 1.0 --split test
    
