from nltk.util import ngrams
import random
import re


def most_probable_word(dict_key, i=0):
    return sorted(corpus[dict_key].items(), key=lambda x: -x[1])[i][0]


def random_first_and_second(source):
    return random.choice(source).split()


trigrams = ngrams(open(input(), 'r', encoding='utf-8').read().split(), 3)
corpus = {}
for trigram in trigrams:
    key = f'{trigram[0]} {trigram[1]}'
    corpus.setdefault(key, {})
    corpus[key].setdefault(trigram[2], 0)
    corpus[key][trigram[2]] += 1

p = re.compile(r'^[A-Z]')
capital_letters = [word for word in list(corpus.keys()) if p.match(word)]

first, second = random_first_and_second(capital_letters)
while re.match(r'.+(\.|!|\?)$', first):
    first, second = random_first_and_second(capital_letters)

for _ in range(10):
    sentence = [first, second]

    while True:
        previous = f'{sentence[-2]} {sentence[-1]}'
        word = most_probable_word(previous)
        sentence.append(word)
        if re.match(r'.+(\.|!|\?)$', word) and len(sentence) >= 5:
            break

    print(f'{sentence[0].capitalize()} {" ".join(sentence[1:])}')

    first, second = random_first_and_second(capital_letters)
    while re.match(r'.+(\.|!|\?)$', first):
        first, second = random_first_and_second(capital_letters)
