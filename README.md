# mcgenerator

A web app which uses a Markov chain to generate text.

A Markov chain is a process where state changes only depend on the current state
and state changes are probabilistic.

## Data structure description

The Markov chain is represented as a Python dictionary. The key of the dictionary
is a word, and the value is another dictionary where the key is a word and the value
is the number of times that word follows. The following example shows training the
model on two sentences that are almost the same, with the exception of 1 change, the
name following the word "is".  You'll see that for the "is" entry in the dictionary,
there are 2 items, each with a count of 1, while the other words "my" and "name", both
have counts of 2 for their subsequent words.

### Examples of the data structure used

```python
In [1]: import mcgenerator

In [2]: g = mcgenerator.Generator()

In [3]: g.read_sentence("my name is derek.")

In [4]: g.read_sentence("my name is wisong.")

In [5]: g.next_word_count
Out[5]: 
{'is': {'derek.': 1, 'wisong.': 1}, 
 'my': {'name': 2}, 
 'name': {'is': 2}}
```

Additionally, once the model has been trained, the probabilities need to be computed.

Here, you'll see that the counts have been replaced by the probabilities of the
subsequent words.

```python
In [6]: g.calculate_probabilities()

In [7]: g.next_word_fraction
Out[7]:
{'is': {'derek.': 0.5, 'wisong.': 0.5},
 'my': {'name': 1.0},
 'name': {'is': 1.0}}
```

To generate the following word, given a start word, one must pick a  word and then
perform a weighted random draw from the dictionary of probabilities to obtain the
next word. This process is then reapeated using the randomly selected word as the
new starting word until you have made a sentence of your desired length.

In this example, I choose the word "is" to begin, get its dictionary of following
words with their probabilities, and perform a few draws to demonstrate the randomness
of the draw.

```python
In [8]: prob = g.next_word_fraction['is']

In [9]: prob
Out[9]: {'derek.': 0.5, 'wisong.': 0.5}

In [10]: mcgenerator.weighted_random(prob)
Out[10]: 'wisong.'

In [11]: mcgenerator.weighted_random(prob)
Out[11]: 'wisong.'

In [12]: mcgenerator.weighted_random(prob)
Out[12]: 'derek.'

In [13]: mcgenerator.weighted_random(prob)
Out[13]: 'derek.'

In [14]: mcgenerator.weighted_random(prob)
Out[14]: 'wisong.'
```

In this implementation, the words that define the start and end of a sentence are actually
taken from the start and end words of the sentences used to train the model. The first and
last words from each sentence trained with are placed into special lists. The process of
generating a new sentence is as follows:

1. randomly (uniformly, no weighting involved) pick a word from the list of start words
2. using the start word, draw the next word(s) using the methods described above until a
   word which has been used to end a sentence is encountered.

Here is an example of training on more sentences, and then generating a few new sentences.

Note that after training more sentences (using the read_sentence function), I must calculate 
the probabilities again before generating new sentences

```python
In [15]: g.read_sentence("my cat's name is luna")

In [16]: g.read_sentence("it is snowy outside")

In [17]: g.read_sentence("what time is it")

In [18]: g.read_sentence("how much wood could a woodchuck chuck")

In [19]: g.read_sentence("this is a markov chain application")

In [20]: g.read_sentence("a hammer is a useful tool")

In [21]: g.read_sentence("i like to write python code")

In [22]: g.calculate_probabilities()

In [23]: g.generate_sentence()
Out[23]: 'how much wood could a useful tool'

In [24]: g.generate_sentence()
Out[24]: 'my name is a woodchuck chuck'

In [25]: g.generate_sentence()
Out[25]: 'a useful tool'

In [26]: g.generate_sentence()
Out[26]: 'this is snowy outside'

In [27]: g.generate_sentence()
Out[27]: 'i like to write python code'

In [28]: g.generate_sentence()
Out[28]: 'how much wood could a useful tool'

In [29]: g.generate_sentence()
Out[29]: 'a markov chain application'

In [30]: g.generate_sentence()
Out[30]: 'what time is a woodchuck chuck'

In [31]: g.generate_sentence()
Out[31]: 'how much wood could a useful tool'

In [32]: g.generate_sentence()
Out[32]: 'a markov chain application'

In [33]: g.generate_sentence()
Out[33]: 'my name is snowy outside'

In [34]: g.generate_sentence()
Out[34]: 'a woodchuck chuck'

In [35]: g.generate_sentence()
Out[35]: "my cat's name is wisong."

In [36]: g.generate_sentence()
Out[36]: 'it'

In [37]: g.generate_sentence()
Out[37]: 'what time is it'

In [38]: g.generate_sentence()
Out[38]: 'my name is a woodchuck chuck'

```
