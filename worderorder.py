#!/usr/local/bin/python3
# -*- encoding:utf-8 -*-

'''
    汉字语序识别
'''

import jieba

from itertools import permutations

def get_all_possible_word(str):
    word_list = list(permutations(str))
    for i in range(len(word_list)):
        word_list[i] = ''.join(word_list[i])
    return word_list

def sort_dict_by_key(dic):
    return [(k, dic[k]) for k in sorted(dic.keys())]

def dicts(filename):
    with open(filename,encoding='UTF-8') as f:
        array_lines = f.readlines()
    Dict = {}
    for line in array_lines:
        line = line.strip()
        listFromLine = line.split()
        Dict[listFromLine[0]] = int(listFromLine[1])
    return Dict

def find_longest(list):
    l = 0
    index = 0
    for i, word in enumerate(list):
        if len(word) > l:
            l = len(word)
            index = i
    return index

if __name__ == "__main__":
    strs = '机算计术技'
    possible_words = []
    for word in get_all_possible_word(strs):
        seg_list = jieba.lcut(word, cut_all=True)
        index = find_longest(seg_list)
        if len(seg_list[index]) == len(strs):
            possible_words.append(seg_list[index])
    if len(possible_words) == 1:
        print(possible_words[0])
    elif len(possible_words) > 1:
        word_dict = dicts(r'E:\soft\python\Lib\site-packages\jieba\dict.txt')
        possible_dict = {}
        for possible_word in possible_words:
            possible_dict[word_dict[possible_word]] = possible_word
        sorteds = sort_dict_by_key(possible_dict)
        print(sorteds)
    else:
        print( "暂时无法识别" )  