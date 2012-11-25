import pipeline
import urllib2
import json
import os


class Speach2TextPipe(pipeline.Pipe):
    def __init__(self, rec):
        self.rec = rec

    def process(self, fn):

        url = "https://www.google.com/speech-api/v1/recognize?client=chromium&lang=en-us"
        flac = open(fn, "rb").read()

        header = {'Content-type': 'audio/x-flac; rate=%s' % self.rec.rate}

        req = urllib2.Request(url, flac, header)
        data = urllib2.urlopen(req).read()

        result = json.loads(data)

        response = result["hypotheses"][0]["utterance"]
        print response

        os.unlink(fn)

        return response

