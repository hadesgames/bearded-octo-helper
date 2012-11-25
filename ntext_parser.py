"""
N(atural) Text Parser

To use the parser, call the method parse(string). The return value is a sentence tree
To test the type of sentence, use the .type field (the types are string values)
All sentences have a .type and a .subordinates, the latter being a list of sub-sentences

Subject Verb Object (main sentence) for ex. "Computer kill Alexandru Tache the ugly"
.type = "svo"
.subj = "Computer" (the name of the subject
.verb = "kill"     (the action)
.obj = ["Alexandru","Tache", "ugly"]  the list of nouns that compose the object. Articles are skipped

Time sentence (subordinate)  for ex. "at five o'clock" (o'clock is not compulsory)
.type = "time"
.val = "five"      the word used for the number

With sentence (subordinate) for ex. "with the title fried potatoes"
.type = "with"
.val = ["title","fried","potatoes"]    a list of everything but articles (are skipped). stops at eos or at first sub/coordination
"""


import nltk
#Convenience functions to use nltk tagging/chunking easly
def tag(string):
    text = nltk.word_tokenize(string)
    return nltk.pos_tag(text)

def chunk(tagged):
    return nltk.chunk.ne_chunk(tagged)

#Convenience checking functions on part of speech role. They are now generalizinf (eg: proper and improper nouns
#are checked by the same function
def is_noun(item):
    begin_tag = item[1][:2]
    return begin_tag == "NN"
def is_verb(item):
    begin_tag = item[1][:2]
    return begin_tag == "VB"
def is_conjunction(item):
    begin_tag = item[1]
    return begin_tag == "IN"
def is_number(item):
    tag = item[1]
    return tag == "CD"
def is_article(item):
    tag = item[1]
    return tag == "DT"
def is_and(item):
    tag = item[1]
    return tag == "CC"

#A stream class. Used to stream tokens in and read them one by one
class TokenStream(object):
    #Ls is a list
    def __init__(self,ls):
        self.position = 0
        self.ls = ls
    #Is end of stream
    def is_eos(self):
        return self.position >= len(self.ls)
    #Reads one token, advances the position
    def read_token(self):
        if (self.is_eos()):
            raise Exception("End of stream!")
        else:
            token = self.ls[self.position]
            self.position = self.position + 1
            return token
    #Pushes back the position in the stream by n places
    def push_back(self,num):
        val = self.position - num
        if val < 0:
            raise Exception("Can't push behind 0!")
        else:
            self.position = val
    def lookahead(self,num):
        val = self.position + num
        if val >= len(self.ls):
            #return ""
            raise Exception("Can't lookahead: end of stream reached")
        else:
            return self.ls[val]
    def read_noun(self):
        noun = self.read_token()
        if not is_noun(noun):
            raise Exception("Noun expected at %s" % (self.position-1))
        return noun
    def read_verb(self):
        verb = self.read_token()
        if not is_verb(verb):
            raise Exception("Verb expected at %s" % (self.position-1))
        return verb
    #Do I want to write a noun/adjective one?....
    def read_noun_sequence(self):
        read = list()
        while not self.is_eos():
            if is_article(self.lookahead(0)):
                self.skip_articles()
            elif is_noun(self.lookahead(0)):
                read.append(self.read_token()[0])
            else:
                break
        return read
    def skip_articles(self):
        while not self.is_eos() and is_article(self.lookahead(0)):
                self.read_token()
    def read_sequence(self):
        read = list()
        while not self.is_eos():
            if is_article(self.lookahead(0)):
                self.skip_articles()
            elif is_conjunction(self.lookahead(0)) or is_and(self.lookahead(0)):
                break
            else:
                read.append(self.read_token()[0])
        return read
#Just defining sentence object
class Sentence(object):
    def __init__(self):
        self.subordinates = list()

def parse_time_sentence(stream,time):
    #Eat the eventual o'clock
    if stream.lookahead(0)[0] == "o'clock":
        stream.read_token()
    sentence = Sentence()
    sentence.type = "time"
    sentence.val  = time[0]
    return sentence

#Parses subordinates that begin with at
def parse_at_subordinate(stream):
    item = stream.read_token()
    if is_number(item):
        return parse_time_sentence(stream,item)
    else:
        raise Exception("Unknown 'at' subordinate type")

def parse_with_subordinate(stream):
    read = stream.read_sequence()
    sentence = Sentence()
    sentence.type = "with"
    sentence.val = read
    return sentence

#Chooses wich subordinate super-type to use based on the conjunction
def parse_subordinate(stream):
    #Read the conjunction (past token)
    conjunction = stream.read_token()[0]
    if conjunction == "at":
        return parse_at_subordinate(stream)
    elif conjunction == "with":
        return parse_with_subordinate(stream)
    else:
        raise Exception("Unknown subordinate connector %s" %(conjunction))

def parse_subject_object_verb(stream,subject=None):
    if subject == None:
        subj = stream.read_noun()
    else:
        subj = subject
    verb = stream.read_verb()
    obj =  stream.read_noun_sequence()
    sentence = Sentence()
    sentence.type = "svo"
    sentence.subj = subj[0]
    sentence.verb = verb[0]
    sentence.obj  = obj
    keep_going = not stream.is_eos()
    while(keep_going):
        if is_conjunction(stream.lookahead(0)):
            sentence.subordinates.append(parse_subordinate(stream))
        else:
            break
        keep_going = not stream.is_eos()
    return sentence

def parse_tagged(tagged):
    stream = TokenStream(tagged)
    result_list = list()
    sentence = parse_subject_object_verb(stream)
    result_list.append(sentence)
    while not stream.is_eos():
        if is_and(stream.lookahead(0)):
            sentence = result_list[-1]
            stream.read_token()
            result_list.append(parse_subject_object_verb(stream,sentence.subj))
        else:
            result_list.append(parse_subject_object_verb(stream))
    return result_list
def parse(string):
    return parse_tagged(tag(string))
