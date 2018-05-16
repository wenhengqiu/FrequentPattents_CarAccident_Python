#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Usage: 
    $ python hw2.py
'''

import pandas as pd
from collections import defaultdict, OrderedDict
import operator

# Read Data from input file
def readData(path):
    list = []
    carAccident = pd.read_excel(path)
    for h in carAccident.values:
        list.append(tuple(h))
    carAccidentTuple = tuple(list)
    return carAccidentTuple

# Computes the frequenceies of a sequence of sequences and stored as a dictionary {key:frequecies} .
def get_frequencies(transactions):
    frequencies = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            frequencies[item] += 1
    return frequencies

# Sort Transactions by frequency
def _sort_transactions_by_freq(transactions, key_func, reverse_int=False, reverse_ext=False, sort_ext=True):
    key_seqs = [{key_func(i) for i in sequence} for sequence in transactions]
    frequencies = get_frequencies(key_seqs)

    asorted_seqs = []
    for key_seq in key_seqs:
        if not key_seq:
            continue
        # Sort each transaction (infrequent key first)
        l = [(frequencies[i], i) for i in key_seq]
        l.sort(reverse=reverse_int)
        asorted_seqs.append(tuple(l))
    # Sort all transactions. Those with infrequent key first, first
    if sort_ext:
        asorted_seqs.sort(reverse=reverse_ext)

    return (asorted_seqs, frequencies)
# :param rinput: the input of the algorithm. Must come from 'get_relim_input'
def relim(rinput, min_support=2):
    fis = set()
    report = {}
    _relim(rinput, fis, report, min_support)
    return report

def _get_key_map(frequencies):
    l = [(frequencies[k], k) for k in frequencies]
    l.sort(reverse=True)
    key_map = OrderedDict()
    for i, v in enumerate(l):
        key_map[v] = i
    return key_map

def _new_relim_input(size, key_map):
    i = 0
    l = []
    for key in key_map:
        if i >= size:
            break
        l.append(((0, key), []))
        i = i + 1
    return l

#returns a data structure used as the input of the relim algorithm.
def get_relim_input(transactions, key_func=None):

    # Data Structure
    # relim_input[x][0] = (count, key_freq)
    # relim_input[x][1] = [(count, (key_freq, )]
    #
    # in other words:
    # relim_input[x][0][0] = count of trans with prefix key_freq
    # relim_input[x][0][1] = prefix key_freq
    # relim_input[x][1] = lists of transaction rests
    # relim_input[x][1][x][0] = number of times a rest of transaction appears
    # relim_input[x][1][x][1] = rest of transaction prefixed by key_freq

    if key_func is None:
        def key_func(e):
            return e

    (asorted_seqs, frequencies) = _sort_transactions_by_freq(transactions, key_func)
    key_map = _get_key_map(frequencies)

    relim_input = _new_relim_input(len(key_map), key_map)
    for seq in asorted_seqs:
        if not seq:
            continue
        index = key_map[seq[0]]
        ((count, char), lists) = relim_input[index]
        rest = seq[1:]
        found = False
        for i, (rest_count, rest_seq) in enumerate(lists):
            if rest_seq == rest:
                lists[i] = (rest_count + 1, rest_seq)
                found = True
                break
        if not found:
            lists.append((1, rest))
        relim_input[index] = ((count + 1, char), lists)
    return (relim_input, key_map)

def _relim(rinput, fis, report, min_support):
    (relim_input, key_map) = rinput
    n = 0
    a = relim_input
    while len(a) > 0:
        item = a[-1][0][1]
        s = a[-1][0][0]
        if s >= min_support:
            fis.add(item[1])
            report[frozenset(fis)] = s
            b = _new_relim_input(len(a) - 1, key_map)
            rest_lists = a[-1][1]

            for (count, rest) in rest_lists:
                if not rest:
                    continue
                k = rest[0]
                index = key_map[k]
                new_rest = rest[1:]
                # Only add this rest if it's not empty!
                ((k_count, k), lists) = b[index]
                if len(new_rest) > 0:
                    lists.append((count, new_rest))
                b[index] = ((k_count + count, k), lists)
            n = n + 1 + _relim((b, key_map), fis, report, min_support)
            fis.remove(item[1])

        rest_lists = a[-1][1]
        for (count, rest) in rest_lists:
            if not rest:
                continue
            k = rest[0]
            index = key_map[k]
            new_rest = rest[1:]
            ((k_count, k), lists) = a[index]
            if len(new_rest) > 0:
                lists.append((count, new_rest))
            a[index] = ((k_count + count, k), lists)
        a.pop()
    return n
def mine_assoc_rules(isets, min_support=2, min_confidence=0.5):
    rules = []
    visited = set()
    for key in sorted(isets, key=lambda k: len(k), reverse=True):
        support = isets[key]
        if support < min_support or len(key) < 2:
            continue

        for item in key:
            left = key.difference([item])
            right = frozenset([item])
            _mine_assoc_rules(left, right, support, visited, isets, min_support, min_confidence, rules)
    return rules


def _mine_assoc_rules(
        left, right, rule_support, visited, isets, min_support,
        min_confidence, rules):
    if (left, right) in visited or len(left) < 1:
        return
    else:
        visited.add((left, right))

    support_a = isets[left]
    confidence = float(rule_support) / float(support_a)
    if confidence >= min_confidence:
        rules.append((left, right, rule_support, confidence))
        # We can try to increase right!
        for item in left:
            new_left = left.difference([item])
            new_right = right.union([item])
            _mine_assoc_rules(new_left, new_right, rule_support, visited, isets, min_support, min_confidence, rules)
            
path = 'data.xlsx'
carAccidentTuple = readData(path)
carAccident = pd.read_excel('data.xlsx')

relim_input = get_relim_input(carAccidentTuple)
#Find out frequent patterns
item_sets = relim(relim_input, min_support=1000)

sort_item_sets = sorted(item_sets.items(), key=operator.itemgetter(1))



f=open('FP_1000.txt','w', encoding='utf-8')
for i in sort_item_sets:
    f.write((str(i[0])+' :'+str(i[1])+'\n'))
f.close()

rules = mine_assoc_rules(item_sets, min_support=1000, min_confidence=0.5)

f=open('AR_1000.txt','w',encoding='utf-8')
for i in rules:
    f.write(str(i)+'\n')
f.close()
