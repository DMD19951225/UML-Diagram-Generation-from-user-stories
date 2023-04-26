import spacy
from spacy import displacy
import pandas as pd
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load('en_core_web_sm')

STOP_WORDS.add("able")
if 'make' in STOP_WORDS:
    STOP_WORDS.remove("make")

doc = nlp("Users should be able to update credit card info on payment screen, add items to carts, and pay for items.")

displacy.render(doc, style="dep", jupyter=True)
for tok in doc:
    print(tok.text, "...", tok.pos_, "...", tok.dep_)

new_doc = []
for tok in doc:
    new_doc.append(tok.lemma_)
new_doc = ' '.join(new_doc)
new_doc = nlp(new_doc)
print(new_doc)

df = pd.DataFrame(columns=['text', 'pos', 'tag', 'dep'])
for token in new_doc:
    df = df.append({'text': token.text, 'pos': token.pos_, 'tag': token.tag_, 'dep': token.dep_}, ignore_index=True)
print(df)

for token in doc:
    ancestors = [t.text for t in token.ancestors]
    children = [t.text for t in token.children]
    print(token.text, "\t",
          token.pos_, "\t", token.dep_, "\t",
          ancestors, "\t", children)

actor = []
isFirst = True

for tok in nlp(new_doc):
    if (tok.tag_ == "NN" or tok.tag_ == "NNS" or tok.tag_ == "NNP") and isFirst == True:
        isFirst = False
        actor.append(tok.text)

print(actor)

def get_subject_phrase(doc):
    for token in doc:
        if ("subj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]


def get_object_phrase(doc):
    middle = 0
    for token in doc:
        if ("dobj" in token.dep_):
            subtree = list(token.subtree)
            for i in range(len(subtree)):
                if subtree[i].pos_ == 'ADP':
                    middle = subtree[i].i
            start = subtree[0].i
            end = subtree[-1].i + 1

            for tok in token.ancestors:
                if tok.pos_ == "VERB":
                    method = tok
                break;

            method = str(method) + " " + str(doc[start:middle])
            method = nlp(method)

            return [method, doc[(middle + 1):end]]


def get_class_after_preposition(doc):
    terms = []
    for i in range(len(doc)):
        if doc[i].text == 'of' or doc[i].text == 'for' or doc[i].text == 'to':
            if doc[i + 1].pos_ == 'NOUN':
                for tok in doc[i].ancestors:
                    if tok.pos_ == "VERB":
                        terms.append([tok])
                    break;
                terms[-1].append(doc[i + 1])

    return terms

subject= get_subject_phrase(new_doc)
obt = get_object_phrase(new_doc)
other_classes = get_class_after_preposition(new_doc)
print("Subject:", subject)
print("Direct object:", obt)
print("Other classes:", other_classes)

classes = []
# if get_subject_phrase(new_doc).text not in actor:
#         classes.append(subject)
if obt != None:
        classes.append(obt)
for term in other_classes:
        classes.append(term)

print("Extracted classes are as follows.")
print(classes)

tmp_part = classes
classes = []
for part in tmp_part:
    temp_part = []
    for term in part:
        temp_part.append(term.text.replace(' ', '_'))
    classes.append(temp_part)
print(classes)

f = open("classUML.puml", "w")
f.write("@startuml\n")
f.write("hide circle\n")
f.write("skinparam classFontStyle bold\n")

for i in range(len(classes)):
    f.write("class " + str(classes[i][1]) + "{\n")
    f.write(str(classes[i][0]) + "()" + "\n")
    f.write("}\n")

f.write("@enduml")