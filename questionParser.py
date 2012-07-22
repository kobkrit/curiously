#!/usr/bin/python
from corenlp import *
corenlp = StanfordCoreNLP()  # wait a few minutes...

question = "When is the independence day?"
parsed = corenlp.parse(question)
print parsed