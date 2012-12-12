from pyparsing import *


class Parser:
    def __init__(self, interpreter, handlers={}):
        self.interpreter = interpreter
        self.handlers = handlers
        self.parser = self._construct_parser()

    def get_handler(self, name):
        if name in self.handlers:
            return self.handlers[name]

        return getattr(self.interpreter, name)

    def parse(self, string):
        return list(self.parser.scanString(string))

    def _construct_parser(self):
        """
            Header Definition
        """
        header = Literal("#").suppress() + Word(". " + alphanums)
        header = header.setResultsName("Header")
        header.setParseAction(self.get_handler("parse_header"))

        """
            Definition of basic elements
        """
        rule_name = Word(alphanums + '._')
        rule_name = rule_name.setResultsName("Rule")

        token = QuotedString(quoteChar='"', escChar='\\') | CharsNotIn(";=|*+<>()[]{}/\" ")
        token = token.setResultsName("Token")
        token.setParseAction(self.get_handler("parse_token"))

        real_number = Combine(Word(nums) + Optional(Literal('.') + Word(nums)))
        weight = Literal('/').suppress() + real_number + Literal('/').suppress()
        weight = weight.setResultsName("Weight")

        # TODO: The tag is just a hack
        tag = Literal('{').suppress() + Word(alphanums) + Literal('}').suppress()
        tag = tag.setResultsName("Tag")

        rule_ref = Literal('<').suppress() + rule_name + Literal('>').suppress()

        #Creating separate parse action for when the rule_ref is used in expressions
        rule_ref_exp = rule_ref.copy()
        rule_ref_exp.setParseAction(self.get_handler("parse_rule_ref"))

        """
            Defining an expression. God help us.
        """
        weight_op = weight
        one_or_more_op = Literal('+')
        zero_or_more_op = Literal('*')
        tag_op = tag
        and_op = White().suppress()
        or_op = Literal('|').suppress()

        expression = Forward()

        optional_expression = Literal('[').suppress() + expression + Literal(']').suppress()
        optional_expression = optional_expression.setResultsName("Optional")
        optional_expression.setParseAction(self.get_handler("parse_optional_exp"))

        operand = rule_ref_exp | token | optional_expression

        expression << operatorPrecedence(operand,
            [
             (weight_op, 1, opAssoc.RIGHT, self.get_handler("parse_weight_op")),
             (tag_op, 1, opAssoc.LEFT, self.get_handler("parse_tag_op")),
             (zero_or_more_op, 1, opAssoc.LEFT, self.get_handler("parse_zero_or_more_op")),
             (one_or_more_op, 1, opAssoc.LEFT, self.get_handler("parse_one_or_more_op")),
             (and_op, 2, opAssoc.LEFT, self.get_handler("parse_and_op")),
             (or_op, 2, opAssoc.LEFT, self.get_handler("parse_or_op"))]
            )

        """
            Defining rest of the complex structures
        """
        grammar = Keyword("grammar") + rule_name
        grammar = grammar.setResultsName('Grammar')

        import_pattern = Keyword("import") + rule_name
        import_pattern = import_pattern.setResultsName('Import')

        rule_def = Optional(Keyword("public")) + rule_ref + \
                   Literal("=").suppress() + expression
        rule_def = rule_def.setResultsName("Rule Definition")
        rule_def.setParseAction(self.get_handler("parse_rule_def"))

        comment = (Literal('//') + SkipTo(LineEnd(), include=True)) | \
                  (Literal('/*') + SkipTo('*/', include=True))
        comment = comment.setResultsName('Comment')

        entry = ((grammar | import_pattern | header | rule_def) + Literal(";").suppress()) | comment

        return entry
