import json
import wikipediaapi
from nltk.corpus import wordnet as wn
from nltk import word_tokenize, sent_tokenize, pos_tag, FreqDist, bigrams, trigrams, FreqDist
from tqdm import tqdm

category = "animals"
wiki = wikipediaapi.Wikipedia('en')

with open(f"verbs_{category}.json") as f:
    verbs = json.load(f)

result = []
with open(f"../word_dictionary/{category}_definitions.json") as g:
    names = json.load(g)

    with tqdm(names, unit="name") as n_epoch:
        for name in n_epoch:
            word_summary = wiki.page(name).summary

            if word_summary == '':
                continue

            word_summary = pos_tag(word_tokenize(word_summary))
            wd_bg = bigrams(word_summary)

            for a,b in wd_bg:
                try:
                    if a[1].startswith('V') and wn.synsets(a[0], 'v')[0].lemma_names()[0] in verbs:
                        result.append(str((a[0], b[0])))
                except IndexError:
                    continue

fd = FreqDist(result)
bg_dict = dict(fd.most_common(20))

with open(f"./bigrams/bigrams_{category}.json", "w") as fp:
    json.dump(bg_dict, fp, indent=4)
