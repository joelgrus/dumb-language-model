from collections import defaultdict
import random

import streamlit as st
import spacy
from spacy_streamlit import process_text

st.title("Dumb Language Model")

st.markdown("""
Back before GPT-3 and all that we used to make our own language models
by hand, barefoot in the snow, uphill both ways, etc etc. 
This right here is a really dumb
[n-gram language model](https://en.wikipedia.org/wiki/N-gram#n-gram_models).

The pre-filled corpus is all of Shakespeare's sonnets, 
which means it will generate nonsense that looks like poetry.
Of course, one man's "nonsense that looks like poetry" is another man's poetry.

If you want to put in your own text, know that the code assumes that 
blank lines are paragraph dividers, and that the generation code stops
when it generates such a divider. This seemed like a good way to generate
a "poem worth" of material.

If you want to see the small amount of code behind this, it's
[on GitHub](https://github.com/joelgrus/dumb-language-model).
""")

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