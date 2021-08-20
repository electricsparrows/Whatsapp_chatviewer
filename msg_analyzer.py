# This module processes message content only.

import nltk
from nltk.corpus import stopwords
#nltk.download()

msg1 = "don't think u had hallucinations cuz i witnessed ur situation and saw nothing except trembling and muscles atonia"

msg2 = "I don't think so. Don't think it's doable"

stop_words = {"u", "do", "i", "ur", "and"}

#probably split into sentences first
word_tokens = nltk.word_tokenize(msg1)
filtered = [w for w in word_tokens if not w in stop_words]
tagged = nltk.pos_tag(filtered)
print(tagged)
print()

def get_nouns(tagged_list):
    noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
    return [w for w in tagged_list if w[1] in noun_tags]

print(get_nouns(tagged))


def summarize(msgs: list):
    """
    :param msgs: list of message references
    :return:
    """
    #return start and end date,
    #no. of messages
    return

#tokenizer: string --> list of tokens

#part of Speech tagger: list of tokens --> list of two-tuples

#get noun set

#get verb set

def get_unigrams(text):
    return text.split()

def get_bigrams(text):
    bag = get_unigrams(text)
    res = []
    #pop off the first two and append
    while len(bag) != 0:
        if len(bag) > 1:
            res.append(" ".join(bag[:2]))
            bag.pop(0)
            bag.pop(0)
        else:
            res.append(bag.pop())
    return res