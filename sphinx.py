import pipeline

hmmd = '/usr/share/pocketsphinx/model/hmm/wsj1'
lmd = '/usr/share/pocketsphinx/model/lm/wsj/wlist5o.3e-7.vp.tg.lm.DMP'
dictd = '/usr/share/pocketsphinx/model/lm/wsj/wlist5o.dic'
dictd = 'test.dict'

import pocketsphinx as ps


class SphinxPipe(pipeline.Pipe):
    def process(self, filename):
        rec = ps.Decoder(hmm=hmmd, lm=lmd, dict=dictd, samprate='16000', jsgf="test.jsgf")
        fh = open(filename, "rb")
        fh.seek(44)

        rec.decode_raw(fh)

        return rec.get_hyp()


