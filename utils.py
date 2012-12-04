import pipeline

class DebugPipe(pipeline.Pipe):
    def process(self, data):
        print data
