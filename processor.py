import threading
import converter
import speach2text


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
                converter.WavToFlacPipe(),
                speach2text.Speach2TextPipe(self.rec)
        ]

    def run(self):
        for block in self.stream:
            self.pipeline(block)

    def pipeline(self, data):
        for pipe in self.pipeline_functions:
            data = pipe.process(data)
        return data

