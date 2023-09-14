#!/usr/bin/env python3.11
"""Get the most frequent words of some string."""
import re
import collections as col


def top_3_words(words):
    words = (i for i in re.split("[^a-z']+", words.lower()) if i and set(i) != {"'"})
    return [i[0] for i in col.Counter(words).most_common(3)]
