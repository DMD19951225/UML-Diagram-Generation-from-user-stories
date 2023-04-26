import spacy
from spacy import displacy
import pandas as pd
from spacy.matcher import Matcher
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load('en_core_web_sm')

STOP_WORDS.add("able")
if 'make' in STOP_WORDS:
    STOP_WORDS.remove("make")

doc = nlp("Overall, the system should aim to optimize operations, reduce waste, and provide an exceptional dining experience for customers.")

displacy.render(doc, style="dep", jupyter=True)
for tok in doc:
    print(tok.text, "...", tok.pos_, "...", tok.dep_)

tokens = [token.text for token in doc]
print(tokens)

#Creating and updating our list of filtered tokens using list comprehension

filtered = [token.text for token in doc if token.text.isalpha() == True]

print(filtered)

new_doc= ' '.join(filtered)
new_doc = nlp(new_doc)
print(new_doc)

df = pd.DataFrame(columns=['text', 'lemma', 'pos', 'tag', 'dep'])
for token in new_doc:
    df = df.append({'text': token.text, 'lemma': token.lemma_, 'pos': token.pos_, 'tag': token.tag_, 'dep': token.dep_}, ignore_index=True)
print(df)

df2 = pd.DataFrame(columns=['text', 'lemma', 'pos', 'tag', 'dep', 'is_stop'])
for token in doc:
    df2 = df2.append({'text': token.text, 'lemma': token.lemma_, 'pos': token.pos_, 'tag': token.tag_, 'dep': token.dep_, 'is_stop': token.is_stop}, ignore_index=True)
print(df2)

for token in doc:
    ancestors = [t.text for t in token.ancestors]
    children = [t.text for t in token.children]
    print(token.text, "\t",
          token.pos_, "\t", token.dep_, "\t",
          ancestors, "\t", children)


def find_root_of_sentence(doc):
    root_token = None
    for token in doc:
        if (token.dep_ == "ROOT"):
            root_token = token
    return root_token

root_token = find_root_of_sentence(doc)
print(root_token)

def find_other_verbs(doc, root_token):
    other_verbs = []
    for token in doc:
        ancestors = list(token.ancestors)
        if (token.pos_ == "VERB" and token.dep_ != "ROOT"):
            other_verbs.append(token.text)
    return other_verbs

other_verbs = find_other_verbs(new_doc, root_token)
print(other_verbs)

def get_entities(sentence):
    actor = []
    verbe = []
    isFirst = True
    # isThere = True

    for tok in nlp(sentence):
        if (tok.tag_ == "NN" or tok.tag_ == "NNS") and isFirst == True:
            isFirst = False
            actor.append(tok.text)
        if tok.tag_ == "VB" or tok.tag_ == "VBP" or tok.tag_ == "VBN" or tok.tag_ == "VBD" or tok.tag_ == "VBG" or tok.tag_ == "VBZ":
            verbe.append(tok.text)
        if tok.text not in actor:
            if tok.tag_ == "NN" or tok.tag_ == "NNS":
                verbe.append(tok.text)

    # return actor, verbe
    return [actor, verbe]


actor, verbe = get_entities(doc)
verbe = ' '.join(verbe)
verbe = nlp(verbe)
filtered_verbe = [token.text for token in verbe if token.is_stop == False]
if root_token.text in filtered_verbe:
    filtered_verbe.remove(root_token.text)
print(actor)
print(filtered_verbe)

terms = []
for word in filtered_verbe:
    if word in other_verbs:
        terms.append([word])
    else:
        if len(terms) == 0:
            terms.append([])
        terms[-1].append(word)
print(terms)

for i in range(len(other_verbs)):
    terms[i] = ' '.join(terms[i])

print(terms)

def get_relation(sent):

  doc = nlp(sent)

  # Matcher class object
  matcher = Matcher(nlp.vocab)

  #define the pattern
  pattern = [{'DEP':'ROOT'},
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},
            {'POS':'ADJ','OP':"?"}]

  matcher.add("matching_1", [pattern])

  matches = matcher(doc)
  k = len(matches) - 1

  span = doc[matches[k][1]:matches[k][2]]

  return(span.text)

print(get_relation(doc))


f = open("UML.puml", "w")
f.write("@startuml\n")
f.write("rectangle Actor{\n")
f.write("actor " + actor[0] + " as c\n")
f.write("}\n")
f.write("rectangle UseCase{\n")
for i in range(len(other_verbs)):
    f.write("usecase " + '"' + terms[i] + '"' + " as uc" + str(i+1) + "\n")
f.write("}\n")

for i in range(len(other_verbs)):
    f.write("c " + "-->" + " uc" + str(i+1) +"\n")

f.write("@enduml")