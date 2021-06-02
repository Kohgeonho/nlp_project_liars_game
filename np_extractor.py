import nltk
from nltk import word_tokenize
import json

chunk_rule = r"""
    NP: {<N.*><IN><NNP>}
        {<DT|PR.*>?<RB|PR.?>?<JJ|PR.?>*<N.*>+} 
        {<DT><RB><NP>}
        {<N.*><JJ><NN>*}
        {<N.*><VBG><NN>*}
        {<J.*>*<NN>*}
        {<JJ>+<NN>+}
    P:  {<IN>}
    V:  {<V.*>}
    PP: {<P><PR.?>?<NP>}
    VP: {<V> <NP|PP>*}
"""

def leaves(tree):
    for subtree in tree.subtrees(filter=lambda x: x.label() == 'NP'):
        yield subtree.leaves()

def definition_NPs(category, word):

    '''
    :param category: category of the game (singular)
    :param word: word that is being searched

    :return:
    definition, NPS
    definition: raw string of definition
    NPS: Noun Phrases extracted
    '''

    category_file = f"word_dictionary/{category}_definitions.json"

    with open(category_file, "r") as json_file:
        word_dict = json.load(json_file)

    definition = word_dict[word]
    return extract_NPs(definition)

def extract_NPs(sentence):
    sent = nltk.pos_tag(word_tokenize(sentence))
    cp = nltk.RegexpParser(chunk_rule)
    chunked = cp.parse(sent)
    NPS = [leaf for leaf in leaves(chunked)]
    return sentence, NPS

def NP_compare(definitions, des_NP):

    Noun = 0
    Adj = 0
    
    for def_NP in definitions:
        for word, tag in des_NP:
            if tag.startswith('NN'):
                if word in [w for w, _ in def_NP]:
                    Noun += 1 
            if not tag.startswith('DT'):
                if word in [w for w, _ in def_NP]:
                    Adj += 1

    if Noun and Adj:
        return True
    return False