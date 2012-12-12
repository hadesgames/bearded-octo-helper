from parser import Parser
from pprint import pprint
from pyparsing import *
#import ipdb

def passer(*args, **kwargs):
    pass


class RuleDatabase(object):
    def __init__(self):
        self.dict = {}

    def __getitem__(self, name):
        if not name in self.dict:
            self.dict[name] = Forward()
        return self.dict[name]

    def __contains__(self, name):
        return name in self.dict

    def __setitem__(self, name, value):
        if name in self.dict:
            self.dict[name] << value
        else:
            self.dict[name] = value

        self.dict[name].setParseAction(lambda s, loc, toks: {"value": toks})


class Interpreter:
    def __init__(self, jsgf=None, file_handler=None):
        self.parser = Parser(self)
        self.db = RuleDatabase()
        self.public_rules = set()

        if file_handler:
            self.jsgf = self.compute_grammar(file_handler.read())
        else:
            self.jsgf = self.compute_grammar(jsgf)

    def interpret(self, string, rules=None):
        if rules is None:
            rules = self.public_rules

        for rule in rules:
            if rule in self.db:
                try:
                    res = self.db[rule].parseString(string)
                    return res[0]
                except ParseException:
                    pass

        raise Exception("No matching grammar rule")

    def compute_grammar(self, string):
        return self.parser.parse(string)

    def __getattr__(self, name):
        print "Interpreter doesn't have function \"%s\"" % name
        return passer

    def parse_token(self, s, loc, toks):
        res = Literal(toks[0])
        res.setParseAction(lambda s: {"value": toks[0]})
        return res

    def parse_rule_ref(self, s, loc, toks):
        return self.db[toks[0]]

    def parse_rule_def(self, s, loc, toks):
        if len(toks) == 3 and toks[0] == "public":
            toks = toks[1:]
            self.public_rules.add(toks[0])

        self.db[toks[0]] = toks[1]

    def parse_optional_exp(self, s, loc, toks):
        return Optional(toks[0])

    def parse_and_op(self, s, loc, toks):
        toks = toks[0]  # No clue why

        return reduce(lambda x, y: x + y, toks)

    def parse_or_op(self, s, loc, toks):
        toks = toks[0]  # No clue why

        return reduce(lambda x, y: x | y, toks)

    def parse_zero_or_more_op(self, s, loc, toks):
        toks = toks[0]

        return ZeroOrMore(toks[0])

    def parse_one_or_more_op(self, s, loc, toks):
        toks = toks[0]

        return OneOrMore(toks[0])

    def parse_tag_op(self, s, loc, toks):
        toks = toks[0]

        def add_tag(m_s, m_loc, m_toks):
            if len(m_toks) == 0:
                return m_toks

            m_toks = m_toks[0]
            if "tags" in m_toks:
                m_toks["tags"].append(toks[1])
            else:
                m_toks["tags"] = [toks[1]]

            return m_toks

        toks[0].addParseAction(add_tag)

        return toks[0]

if __name__ == "__main__":
    y = Interpreter(file_handler=open("test2.jsgf", "r"))
    pprint(y.db.dict)
    #pprint(y.jsgf)
    pprint(y.interpret("bla kkt laba ceai de prune"))






