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

token = QuotedString(quoteChar='"', escChar='\\') | CharsNotIn(";=|*+<>()[]{}/")
token = token.setResultsName("Token")

real_number = Combine(Word(nums) + Optional(Literal('.') + Word(nums)))
weight = Literal('/').suppress() + real_number + Literal('/').suppress()
weight = weight.setResultsName("Weight")


# TODO: The tag is just a hack
tag = Literal('{').suppress() + Word(alphanums) + Literal('}').suppress()
tag = tag.setResultsName("Tag")

rule_ref = Literal('<').suppress() + rule_name + Literal('>').suppress()


"""
    Defining an expression. God help us.
"""
weight_op = weight
one_or_more_op = Literal('+')
zero_or_more_op = Literal('*')
tag_op = tag
and_op = White()
or_op = Literal('|')


operand = rule_ref | token

expression = operatorPrecedence(operand,
    [
     (weight_op, 1, opAssoc.RIGHT),
     (tag_op, 1, opAssoc.LEFT),
     (zero_or_more_op, 1, opAssoc.LEFT),
     (one_or_more_op, 1, opAssoc.LEFT),
     (and_op, 2, opAssoc.LEFT),
     (or_op, 2, opAssoc.LEFT)]
    )

"""
    Defining rest of the complex structures
"""
grammar = Keyword("grammar") + rule_name
grammar = grammar.setResultsName('Grammar')


rule_def = Optional(Keyword("public")) + rule_ref + Literal("=") + expression
rule_def = rule_def.setResultsName("Rule Definition")


entry = (grammar | header | rule_def) + Literal(";")


pprint(list(entry.scanString(open("test.jsgf", "r").read())))
