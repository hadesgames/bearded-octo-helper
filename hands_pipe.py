import pipeline
import hands.verbs

class HandsPipe(pipeline.Pipe):
    def process(self, sentence):
        if sentence.verb in hands.verbs.verbs:
            hands.verbs.verbs[sentence.verb](sentence)
