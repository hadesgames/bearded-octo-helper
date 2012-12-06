from pyparsing import *
from pprint import pprint

"""
    Header Definition
"""
header = Literal("#") + Word(". " + alphanums)
header = header.setResultsName("Header")


"""
    Definition of basic elements
"""
rule_name = Word(alphanums + '._')
rule_name = rule_name.setResultsName("Rule")

token = QuotedString(quoteChar='"', escChar='\\') | CharNotIn(" ;=|*+<>()[]{}/")
token = token.setResultsName("Token")

rule_ref = Literal('<') + rule_name + Literal('>')

"""
    More complex structures
"""


grammar = Keyword("grammar") + rule_name
grammar = grammer.setResultsName('Grammar')


rule_def = Optional(Keyword("public")) + rule_ref + Literal("=") + expression
rule_def = rule_def.setResultsName("Rule Definition")



entry = (grammar | header | rule_def) + Literal(";")


pprint(list(entry.scanString(open("test.jsgf", "r").read())))
