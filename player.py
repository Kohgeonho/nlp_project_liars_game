from word_association import WordTable

class Liar():
    def __init__(self, topic, suggestions, players=3, play_num=3):

        self.topic = topic
        self.suggestions = suggestions
        self.players = players
        self.play_num = play_num
        self.round = 1

        self.keywords = []
        self.wordtable = WordTable(category=topic, wordlist=suggestions)

    def resetTable(self):
        self.wordtable.resetScore()

    def myTurn(self):

        sorted_score = sorted(self.wordtable.score.items() , key = lambda x:x[1], reverse=True)
        SWS = self.wordtable.SWS
        DEF = self.wordtable.DEF
        score = self.wordtable.score

        candidates = []
        liar_keywords = {}

        for i in range(5):
            for NP in DEF[sorted_score[i][0]]['NPs']:
                candidates += [word for word, tag in NP if tag.startswith('NN') or tag.startswith('JJ')]
            candidates += [word for word in SWS[sorted_score[i][0]] if SWS[sorted_score[i][0]][word][1] == 0]

        for c in candidates:
            liar_keywords[c] = sum(SWS[word][c][0] * score[word] for word in score)

        sorted_keywords = sorted(liar_keywords.items(), key=lambda x: x[1], reverse=True)
        liar_sentence = [word 
                         for word, s in sorted_keywords 
                         if word not in self.topic and word not in self.wordtable.score and word not in self.keywords][:3]
        print(f'{self.play_num}: ', ', '.join(liar_sentence))

    def others(self, description):
        self.keywords += self.wordtable.sentenceScore(description)

    def endofGame(self):
        self.wordtable.plot()
        print("The answer is {}.".format(max(self.wordtable.score, key=lambda x: self.wordtable.score[x])))

class Player():
    def __init__(self, topic, suggestions, answer, players, play_num):

        self.topic = topic
        self.suggestions = suggestions
        self.answer = answer
        self.players = players
        self.play_num = play_num
        self.keywords = []

        self.liarscore = {}
        for i in range(1, players+1):
            if i != play_num:
                self.liarscore[i] = 0
        self.wordtable = WordTable(category=topic, wordlist=suggestions)
    
    def resetTable(self):
        self.wordtable.resetScore()

    def myTurn(self):
        
        SWS = self.wordtable.SWS
        DEF = self.wordtable.DEF
        score = self.wordtable.score

        candidates = []
        player_keywords = {}

        for NP in DEF[self.answer]['NPs']:
            candidates += [word for word, tag in NP if tag.startswith('NN') or tag.startswith('JJ')]
        candidates += [word for word in SWS[self.answer] if SWS[self.answer][word][1] == 0]

        for c in candidates:
            player_keywords[c] = sum(SWS[word][c][0] for word in score)

        sorted_keywords = sorted(player_keywords.items(), key=lambda x: x[1], reverse=True)
        player_sentence = [word 
                           for word, s in sorted_keywords 
                           if word not in self.topic and word not in self.wordtable.score and word not in self.keywords][:3]
        print(f'{self.play_num}: ', ', '.join(player_sentence))

    def others(self, description, player):
        self.wordtable.resetScore()
        self.keywords += self.wordtable.sentenceScore(description)
        
        for word in self.wordtable.score:
            self.liarscore[player] += self.wordtable.score[word] - self.wordtable.score[self.answer]

    def endofGame(self):
        print("Liar is player{}".format(max(self.liarscore)))