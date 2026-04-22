## Dataset source

Licensing note: redistributed data files in this repository for the `so` task
should be treated under **CC BY 4.0**. Individual source datasets remain
subject to their original upstream notices.

Raw data obtained from:
- [arXiv](https://drive.google.com/drive/folders/0B-mnK8kniGAiNVB6WTQ4bmdyamc)
- [Wiki Movie Plots](https://www.kaggle.com/jrobischon/wikipedia-movie-plots)
- [SIND](http://visionandlanguage.net/VIST/dataset.html)
- [NSF](https://archive.ics.uci.edu/ml/datasets/NSF+Research+Award+Abstracts+1990-2003)
- [ROCStories](https://www.cs.rochester.edu/nlp/rocstories/)
- [NeurIPS](https://www.kaggle.com/benhamner/nips-papers)
- [AAN](https://github.com/EagleW/ACL_titles_abstracts_dataset)



## Dataset sizes

### test split (full)

|      | aan-abstract | arxiv-abstracts | nips-abs | nsf | roc | sind-captions | wiki-movies |
|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|
| nb examples | 2,687 | 179,691 | 377 | 20,366 | 9,816 | 5,055 | 3,345 |
| avg length | 5.17 | 5.65 | 6.40 | 10.26 | 5.00 | 4.90 | 13.51 |

### test split (20% fraction, used in our setting)

| | aan-abstract 0.3 | arxiv-abstracts 0.05 | nips-abs 1.0 | nsf 0.08 | roc 0.09 | sind-captions 0.16 | wiki-movies 0.25 |
|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|
| nb examples | 806 | 898 | 377 | 814 | 883 | 808 | 836 |
| avg sentences | 5.25 | 5.61 | 6.40 | 10.26 | 5.00 | 4.88 | 13.67 |
