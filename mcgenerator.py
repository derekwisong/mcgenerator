from __future__ import division
import random


def make_triples(item_list):
    """
    Generate triples from a list of items.
    :param item_list: A list of items, such as ['a', 'big', 'dog']
    :return: a list of triples
    """
    if len(item_list) < 3:
        return

    for i in range(len(item_list) - 2):
        yield (item_list[i], item_list[i+1], item_list[i+2])


def counts_to_fractions(count_dict):
    """
    Convert a dictionary of word -> count to fractions that the word is used.
    > dict_to_pct({'abc': 12, 'def': 24})
    > {'abc': 0.3333333333333333, 'def': 0.6666666666666666}
    :param count_dict: word count dict
    :return: dict of fractions
    """
    return {i: j/sum(count_dict.values()) for (i, j) in count_dict.items()}


def weighted_random(weight_dict):
    """
    Given a dictionary of weighted choices where the key is an item to be chosen and the value is the weight, draw
    a random sample.
    :param weight_dict: dict of items to weights {'a': 0.5, 'b': 0.5}
    :return: A value randomly chosen by weight
    """
    rand_val = random.random()
    total = 0

    for k, v in weight_dict.items():
        total += v

        if rand_val <= total:
            return k

    raise Exception("Unable to draw a weighted random value")


class Generator(object):
    def __init__(self):
        self.next_word_count = {}
        self.next_word_fraction = {}
        self.start_words = set()
        self.end_words = set()

    def add_item(self, item, next_item):
        if item not in self.next_word_count:
            self.next_word_count[item] = {next_item: 1}
            return
        else:
            next_words = self.next_word_count[item]

            if next_item not in next_words:
                next_words[next_item] = 1
            else:
                next_words[next_item] += 1

    def read_items(self, items):
        for i in range(len(items) - 1):
            item = items[i]
            next_item = items[i + 1]

            if i == 0:
                self.start_words.add(item)

            if i == len(items) - 2:
                self.end_words.add(next_item)

            self.add_item(item, next_item)

    def read_sentence(self, sentence):
        items = sentence.split()
        self.read_items(items)

    def calculate_probabilities(self):
        self.next_word_fraction = {word: counts_to_fractions(next_words)
                                   for (word, next_words) in self.next_word_count.items()}

    def generate(self, length=None):
        generated = []

        if len(self.start_words) == 0:
            return generated

        word = random.choice(tuple(self.start_words))
        generated.append(word)

        while word not in self.end_words:
            if length and len(generated) >= length:
                break

            word = weighted_random(self.next_word_fraction[word])
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

        generator.calculate_probabilities()
        return generator


class TupleGenerator(Generator):

    def read_items(self, items):
        triples = make_triples(items)

        for item1, item2, item3 in triples:
            self.add_item((item1, item2), item3)

    def generate(self, length=20):
        # pick 2 random seed words
        seed = random.randint(0, len(self.next_word_count) - 1)
        word1, word2 = list(self.next_word_count.keys())[seed]
        words = [word1, word2]

        for i in range(length):
            next_word = weighted_random(self.next_word_fraction[(word1, word2)])
            word1, word2 = word2, next_word
            words.append(word2)

        return words


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        training_file = "data/quotes2.txt"
        num = 20
    else:
        training_file = sys.argv[1]
        num = int(sys.argv[2])

    g = Generator.from_file(training_file)
    
    for _ in range(num):
        print("{0: >5}.  {1}".format(_ + 1, g.generate_sentence()))
