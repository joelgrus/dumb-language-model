from collections import defaultdict
import random

import streamlit as st
import spacy
from spacy_streamlit import process_text

st.title("Dumb Language Model")

with open('sonnets.txt') as f:
    TEXT = f.read()

START = "<@@START>"
END = "<@@END>"

text = st.text_area("training text", value=TEXT)

# Split on double new lines
paragraphs = text.split("\n\n")

docs = [process_text('en_core_web_sm', paragraph)
        for paragraph in paragraphs]

n = st.radio("n-grams", [1, 2, 3], index=0)

# Generate Transitions
transitions = defaultdict(list)

for doc in docs:
    words = [token.text for token in doc]

    # can't slice a deque, so just use a list
    q = [START]

    for word in words:
        q.append(word)
        # can't slice a queue
        prv = tuple(q[:-1])
        nxt = q[-1]
        transitions[prv].append(nxt)

        if len(q) > n:
            q = q[1:]

    # Now we have the last n words, which transition to END
    prv = tuple(q)
    transitions[prv].append(END)

generate = st.button("generate")

if generate:
    output = [START]

    while True:
        prv = tuple(output[-n:])
        word = random.choice(transitions[prv])
        output.append(word)
        if word == END:
            break

    out_text = ' '.join(output[1:-1])
    for line in out_text.split("\n"):
        st.write(line)