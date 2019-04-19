#! /usr/bin/env python3

import json
from typing import Set

import spacy
from spacy.lang.en import English
import statistics
from tqdm import tqdm

PAPERS: str = "../dataset/papers.json"


def main():
    nlp = spacy.load("en_core_web_sm")
    tokenizer = English().Defaults.create_tokenizer(nlp)
    ids = []
    abstracts = []
    titles = []
    out_citations = []
    with open(PAPERS, 'r') as f:
        for line in tqdm(f):
            ids.append(json.loads(line)['id'])
            abstracts.append(json.loads(line)['paperAbstract'])
            titles.append(json.loads(line)['title'])
            out_citations.append(json.loads(line)['outCitations'])

    train_ids, dev_ids, test_ids = (ids[:int(0.8 * len(ids))],
                        ids[int(0.8 * len(ids)): int(0.9 * len(ids))],
                        ids[int(0.9 * len(ids)):])
    train, dev, test = (abstracts[:int(0.8 * len(abstracts))],
                        abstracts[int(0.8 * len(abstracts)): int(0.9 * len(abstracts))],
                        abstracts[int(0.9 * len(abstracts)):])
    train_title, dev_title, test_title = (titles[:int(0.8 * len(titles))],
                                          titles[int(0.8 * len(titles)): int(0.9 * len(titles))],
                                          titles[int(0.9 * len(titles)):])
    train_out_citations, dev_out_citations, test_out_citations = (out_citations[:int(0.8 * len(out_citations))],
                                          out_citations[int(0.8 * len(out_citations)): int(0.9 * len(out_citations))],
                                          out_citations[int(0.9 * len(out_citations)):])

    train_token_rows = [set(get_tokens(tokenizer, paper)) for paper in train]

    eval_score = []
    for i, dev_row in enumerate(test):
        rankings = []
        dev_tokens = set(get_tokens(tokenizer, dev_row))
        for index, train_tokens in enumerate(train_token_rows):
            rankings.append((jaccard_similarity(dev_tokens, train_tokens), index))
        rankings.sort(key=lambda x: x[0], reverse=True)
        # paper_titles = get_relevant_papers(rankings[:10], train_title)
        top_10_rankings = rankings
        out_citations = test_out_citations[i]
        if len(out_citations) == 0:
            continue
        ranking_ids = get_ids(top_10_rankings, train_ids)
        for out_citation in out_citations:
            if out_citation in ranking_ids:
                eval_score.append(1.0/ (ranking_ids.index(out_citation) + 1))
                print(eval_score)
        # print(out_citations)
        # print(test_title[i])
        # print(list(paper_titles))
    print(eval_score)
        # similarity_sum += sum(r[0] for r in rankings[:10])
    # print(similarity_sum)
    print(statistics.mean(eval_score))


def jaccard_similarity(a, b):
    if not a and not b:
        return 0
    c = a & b
    return len(c) / (len(a) + len(b) - len(c))


def get_tokens(tokenizer, paper: str) -> Set[str]:
    tokens = tokenizer(paper.lower())
    return {token.lemma_ for token in tokens if token.is_alpha and not token.is_stop}


def get_relevant_papers(rankings, train_title):
    titles = [];
    for rank, index in rankings:
        titles.append(train_title[index])
    return titles


def get_ids(rankings, train_ids):
    ids = []
    for rankings, index in rankings:
        ids.append(train_ids[index])
    return ids


# def evaluation_metric

if __name__ == '__main__':
    main()
