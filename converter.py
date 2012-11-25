import wave
import pipeline
import tempfile
import subprocess
import os


class RawToWavPipe(pipeline.Pipe):
    def __init__(self, rec):
        self.rec = rec

    def process(self, data):
        _, fn = tempfile.mkstemp(suffix=".wav")
        wf = wave.open(fn, "wb")

        wf.setnchannels(self.rec.channels)
        wf.setsampwidth(self.rec.samplewidth)
        wf.setframerate(self.rec.rate)

        wf.writeframes(data)
        wf.close()

        return fn


class WavToFlacPipe(pipeline.Pipe):
    def process(self, fn):
        new_fn = fn.replace('.wav', '.flac')
        err = subprocess.call(['flac', fn, '-o', new_fn])
        if err:
            raise Exception(err)
        os.unlink(fn)
        print new_fn
        return new_fn

