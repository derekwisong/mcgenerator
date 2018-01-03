from __future__ import division
import random
from collections import Counter

def dict_to_pct(x):
    return {i:j/sum(x.values()) for (i,j) in x.items()}

def ranges(dictionary):
    # convert words to percentages
    d = dict_to_pct(dictionary)
    s = sorted(d.items(), key=lambda x:x[1])
    v = 0
    n = {}

    for word, pct in s:
        r = (v, v + pct)
        n[word] = r
        v = r[1]

    return n

def draw(ranges):
    r = random.random()

    for word, (start, end) in  ranges.items():
        if r >= start and r < end:
            break

    return word


class Generator(object):
    def __init__(self):
        self.next_words = {}
        self.next_ranges = {}
        self.start_words = set()
        self.end_words = set()

    def read_items(self, items):
        for i in range(len(items) - 1):
            item = items[i]
            next_item = items[i + 1]

            if i == 0:
                self.start_words.add(item)

            if i == len(items) - 2:
                self.end_words.add(next_item)

            if item not in self.next_words:
                self.next_words[item] = {next_item: 1}
                continue
            else:
                next_words = self.next_words[item]

                if next_item not in next_words:
                    next_words[next_item] = 1
                else:
                    next_words[next_item] += 1

    def read_sentence(self, sentence):
        items = sentence.split()
        self.read_items(items)

    def build_ranges(self):
        self.next_ranges = {word: ranges(next_words) for (word, next_words) in self.next_words.items()}

    def generate(self, length=None):
        generated = []

        if len(self.start_words) == 0:
            return generated

        word = random.choice(tuple(self.start_words))
        generated.append(word)

        while word not in self.end_words:
            if length and len(generated) >= length:
                break

            word = draw(self.next_ranges[word])
            generated.append(word)

        return generated

    def generate_sentence(self, length=None):
        return " ".join(self.generate(length=length))

    @staticmethod
    def from_file(filename):
        generator = Generator()

        with open(filename, 'r') as f:
            for line in f:
                generator.read_sentence(line.strip())

        generator.build_ranges()
        return generator

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        filename = "quotes2.txt"
        num = 20
    else:
        filename = sys.argv[1]
        num = int(sys.argv[2])

    g = Generator.from_file(filename)
    
    for i in range(num):
        print("{0: >5}.  {1}".format(i + 1, g.generate_sentence()))
