Coco Evaluation
===============

Evaluation codes for caption generation or machine translation. 

Original code: [COCO Caption](https://github.com/tylin/coco-caption)

Also includes code from [Visual Question Answering](https://github.com/VT-vision-lab/VQA).

Update!: Now supports TER (using [tercom](https://github.com/jhclark/tercom)) and sentence-level BLEU[from Nematus](https://github.com/rsennrich/nematus/tree/master/nematus/metrics)!.

## Requirements ##
- java 1.8.0
- python 2.7

## Installation ##

```
export PYTHONPATH="/path/to/coco-caption:$PYTHONPATH"
```

## References ##

- [Microsoft COCO Captions: Data Collection and Evaluation Server](http://arxiv.org/abs/1504.00325)
- PTBTokenizer: We use the [Stanford Tokenizer](http://nlp.stanford.edu/software/tokenizer.shtml) which is included in [Stanford CoreNLP 3.4.1](http://nlp.stanford.edu/software/corenlp.shtml).
- BLEU: [BLEU: a Method for Automatic Evaluation of Machine Translation](http://www.aclweb.org/anthology/P02-1040.pdf)
- Meteor: [Project page](http://www.cs.cmu.edu/~alavie/METEOR/) with related publications. We use the latest version (1.5) of the [Code](https://github.com/mjdenkowski/meteor). Changes have been made to the source code to properly aggreate the statistics for the entire corpus.
- Rouge-L: [ROUGE: A Package for Automatic Evaluation of Summaries](http://anthology.aclweb.org/W/W04/W04-1013.pdf)
- CIDEr: [CIDEr: Consensus-based Image Description Evaluation](http://arxiv.org/pdf/1411.5726.pdf)
- TER: [Translation Edit Rate with Targeted Human Annotation](https://www.cs.umd.edu/~snover/pub/amta06/ter_amta.pdf)

## Developers ##
- Xinlei Chen (CMU)
- Hao Fang (University of Washington)
- Tsung-Yi Lin (Cornell)
- Ramakrishna Vedantam (Virgina Tech)
- Álvaro Peris (Universitat Politècnica de València)

## Acknowledgement ##
- David Chiang (University of Norte Dame)
- Michael Denkowski (CMU)
- Alexander Rush (Harvard University)
