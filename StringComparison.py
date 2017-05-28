# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import unicodedata


def remove_polish_letters(uniS):
	return str(unicodedata.normalize('NFKD', str(uniS)).encode('ascii', 'ignore'))


def letter_pairs(s):
	num_pairs = len(s) - 1
	pairs = []
	for i in range(0, num_pairs):
		pairs.append(s[i:i + 2])
	return pairs


def word_letter_pairs(s):
	all_pairs = []
	words = s.split(" ")
	for w in words:
		pairs_in_word = letter_pairs(w)
		for p in pairs_in_word:
			all_pairs.append(p)
	return all_pairs


def similarity(s1, s2):
	pairs1 = word_letter_pairs(s1.upper())
	pairs2 = word_letter_pairs(s2.upper())

	intersection = 0
	union = len(pairs1) + len(pairs2)

	for i in pairs1:
		for j in pairs2:
			if i == j:
				intersection += 1
				pairs2.remove(j)
				break
	return ((2.0 * intersection) / union) * 100.
