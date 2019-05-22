#! /usr/bin/env python3
import json
from tqdm import tqdm
import random

SHARED_DIR: str = "/projects/instr/19sp/cse481n/GatesNLP/"
TRAIN = SHARED_DIR + 'train.txt'
DEV = SHARED_DIR + 'dev.txt'
TEST = SHARED_DIR + 'test.txt'

def main():
    count_pairs(TRAIN)
    count_pairs(DEV)
    count_pairs(TEST)


def count_pairs(filename):
    print(filename)
    f = open(filename, 'r')
    text = dict()
    outCitations = dict()
    total = 0
    for line in f:
        total += 1
        paper = json.loads(line)
        id = paper['id']
        text[id] = paper['title'] + ' ' + paper['paperAbstract']
        outCitations[id] = paper['outCitations']

    # counts numbers for train/dev/test split
    true_citation_count = 0
    one_hop_count = 0
    for paper1, text1 in text.items():
        for paper2 in outCitations[paper1]:
            if paper2 in text.keys():
                true_citation_count += 1
    for paper1, text1 in text.items():
        seen = set()
        for paper2 in outCitations[paper1]:
            if paper2 in text.keys():
                for paper3 in outCitations[paper2]:
                    if paper3 in text.keys() and paper3 not in seen and paper3 not in outCitations[paper1]:
                        seen.add(paper3)
                        one_hop_count += 1
    print(str(total) + " papers")
    print(str(true_citation_count) + " cited pairs")
    print(str(one_hop_count) + " one hop pairs")


if __name__ == '__main__':
    main()
