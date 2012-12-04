import threading
import converter
import speach2text
import ntext_pipe
import hands_pipe
import utils
import sphinx


def run(rec):
    thread = ProcessorThread(rec, name="Processor Thread")
    thread.start()
    return thread


class ProcessorThread(threading.Thread):
    def __init__(self, rec, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.stream = rec.sound_blocks()
        self.rec = rec
        self.pipeline_functions = self.create_pipeline()


    def create_pipeline(self):
        return [
                converter.RawToWavPipe(self.rec),
                sphinx.SphinxPipe(),
                #converter.WavToFlacPipe(),
                #speach2text.Speach2TextPipe(self.rec),
                #ntext_pipe.NTextPipe(),
                #hands_pipe.HandsPipe()
                utils.DebugPipe()
        ]

    def run(self):
        for block in self.stream:
            self.pipeline(block)

    def pipeline(self, data):
        for pipe in self.pipeline_functions:
            data = pipe.process(data)
        return data

