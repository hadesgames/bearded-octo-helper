import pipeline
import ntext_parser

class NTextPipe(pipeline.Pipe):
    def process(self, text):
        return ntext_parser.parse(text)[0]
