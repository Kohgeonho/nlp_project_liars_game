import wikipediaapi
from nltk.corpus import wordnet as wn
from nltk import word_tokenize, sent_tokenize, pos_tag, FreqDist
import json
from tqdm import tqdm

## For sentence generation
def category_verb_freq(category):
    '''
    :param category: Category of the game
    :return: returns frequency list of verbs frequently used when describing each of the categories' words. (from Wikipedia)
    '''

    with open(f"{category}_definitions.json", "r") as json_file:
        words_list = json.load(json_file).keys()
        wiki = wikipediaapi.Wikipedia('en')

        verbs = []

        with tqdm(words_list, unit="word") as word_list:
            for word in word_list:

                word_summary = wiki.page(word).summary

                if word_summary == '':
                    continue

                verb_list = [word for word, pos in pos_tag(word_tokenize(word_summary)) if pos.startswith("V") and word.isalpha()]

                ## Find original form of verb:
                for verb in verb_list:
                    try:
                        original_verb = [ss.lemma_names()[0] for ss in wn.synsets(verb) if ss.pos() == 'v'][0]
                        verbs.append(original_verb)
                    except IndexError:
                        continue

        fd = FreqDist(verbs)
        return dict(fd.most_common(20))

category = ["animals", "food", "jobs", "nations", "sports", "weapons"]

for c in category:
    with open(f"verbs_{c}.json", "w") as fp:
        print("Now processing:", c, "\n-------------------------")
        json.dump(category_verb_freq(c), fp, indent=4)
        fp.close()