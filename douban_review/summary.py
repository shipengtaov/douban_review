#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import path
import re
import random
import string

from argparse import ArgumentParser

import gensim
import jieba


stopwords = open(path.join(path.dirname(path.abspath(__file__)), 'stop_words.txt'), 'rb')

def cut_texts(texts):
    """中文分词
    """
    result = []
    for text in texts:
        seg = jieba.cut(text)
        result.append(list(seg))
    return result

# 需要转换的标点
transform_puncs = {
    u"，": ",",
    u"。": ".",
    u"？": "?",
    u"！": "!",
    u"（": "(",
    u"）": ")",
    u"《": "<",
    u"》": ">",
    u"／": "/",
    u"、": ",",
    u"－": "-",
    u"＝": "=",
}

# 映射：sample_id -> 中文
sample_id_to_chinese = dict()

def transform_texts(texts):
    """中文转换为英文
    """
    global sample_id_to_chinese

    result = []
    for seg in texts:
        tmp = []
        for i in seg:
            i = i.strip()
            if i in transform_puncs:
                tmp.append(transform_puncs[i])
                continue

            if i in sample_id_to_chinese:
                sample_id = sample_id_to_chinese[i]
            else:
                sample_id = random_letters(sample_id_to_chinese.keys())
                sample_id_to_chinese[sample_id] = i
            tmp.append(sample_id)

        result.append(' '.join(tmp))

    return result

def random_letters(samples, length=10):
    """生成唯一字符串
    """
    while True:
        sample = random.sample(string.letters[26:], length)
        if sample not in samples:
            break
    return ''.join(sample)

#-----------------------------------------------------------------------------#

def do_summary(file, word_count=100):
    """执行 summary
    """
    with open(file, 'rb') as f:
        texts = [i.strip() for i in f.readlines()]

    print "cutting..."
    cutted = cut_texts(texts)
    print "transforming..."
    transformed = transform_texts(cutted)
    print "summarizing..."
    summarized = gensim.summarization.summarize(' '.join(transformed), word_count=word_count, split=False)
    
    summary = u''
    for s in summarized.split():
        s = s.strip()
        if s in sample_id_to_chinese:
            summary += sample_id_to_chinese[s]
        else:
            summary += s
    print summary

def list_files():
    """列出所有已保存的评论文件
    """
    print "Available files:"
    for i in os.listdir(path.join(path.dirname(path.dirname(path.abspath(__file__))), 'files')):
        if i.startswith('.'):
            continue
        print ' '*8, i

def main():
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', help=u"保存评论的文件名")
    parser.add_argument('-l', '--list', action="store_true", help=u"查看所有评论文件")
    parser.add_argument('-c', '--word-count', type=int, default=100, help=u"how many words will the output contain?")
    args = parser.parse_args()

    if args.list:
        list_files()
    elif args.file:
        do_summary(path.join(
            path.dirname(path.dirname(path.abspath(__file__))),
            'files',
            args.file
        ), args.word_count)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

