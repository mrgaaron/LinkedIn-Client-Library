#! usr/bin/env python
import re, nltk

class TextualAnalyzer(object):
    def __init__(self, txt, source):
        self.sources = {}
        text = nltk.text.Text(txt)
        self.sources[source] = {}
        self.cfds = {}
        self.sources[source]['text'] = text
        self.sources[source]['collocations'] = text.collocations().split(';')
        self.sources[source]['freq_dist'] = text.vocab()
    
    def register(self, txt, source):
        if source not in self.sources.keys():
            text = nltk.text.Text(txt)
            self.sources[source] = {}
            self.sources[source]['text'] = text.tokens
            self.sources[source]['collocations'] = text.collocations().split(';')
            self.sources[source]['freq_dist'] = text.vocab()
        else:
            raise KeyError('Source already found in internal dictionary.  Please use a different source name.')
    
    def generate_cfd(self, srca, srcb):
        cdna = [(w, srca) for w in self.sources[srca]['text']]
        cdnb = [(w, srcb) for w in self.sources[srcb]['text']]
        cfdp = [cdnb + cdna]
        self.cfds[srca+ ', ' + srcb] = nltk.ConditionalFreqDist(cfdp)
    
    def tag(self, source, tagger=None):
        if not tagger:
            self.sources[source]['tagged'] = nltk.pos_tag(self.sources[source]['text'])
        else:
            self.sources[source]['tagged'] = tagger.tag(self.sources[source]['text'])
        
    def chunk(self, source, chunker=None):
        if not self.sources[source]['tagged']:
            self.tag(source)
        grammar = r"""
            NP: {<DT|PP>?<JJ.*>*<NN.*>}
                {<NNP>+}
            VP: {<JJ.*>?<RB>?<VB+><NN.*>*}
            """
        cp = nltk.RegexpParser(grammar)
        self.sources[source]['chunked'] = cp.parse(self.sources[source]['tagged'])
