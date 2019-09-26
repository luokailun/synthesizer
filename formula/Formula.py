#######################################################################################################################################

from basic import Util
import re

quantifier_pattern = re.compile(r"(?:(forall|exists))\s*\(([\w:,\s\d_]+)\)\[([^\[\]]+)\]")
most_inner_pattern = re.compile(r'\(([^\(\)]+)\)')
entailment_pattern = re.compile(r'(?P<head>.+?)=>(?P<body>(?:.(?!=>))+.)')
encode_pair = (['(',')','[',']'],['#','$','{','}'])

def ____eliminate_entailment(formula):
	old_formula = ""
	while old_formula!=formula:
		old_formula = formula
		formula = re.sub(entailment_pattern,"not #\g<head>$ or \g<body>",old_formula, 1)
	#print '---return',formula
	return formula


def ____mrepl_entailment_inner(mathched):
	#print mathched.groups()
	return "#%s$"%____eliminate_entailment(mathched.group(1))


def __eliminate_bracket(formula):
	old_formula = ""
	while old_formula!=formula:
		old_formula = formula
		#print '1',formula
		formula = Util.repeat_replace_inner_with_pattern(most_inner_pattern, ____mrepl_entailment_inner, old_formula) 
		#print '2',formula
	return ____eliminate_entailment(formula)



def __mrepl_entailment_quantifier(matched):
	#print matched.groups()
	formula = __eliminate_bracket(matched.group(3))
	return Util.endecode_string("%s(%s)[%s]"%(matched.group(1),matched.group(2),formula), encode_pair[0], encode_pair[1])


def entailment_eliminate(formula):
	old_formula = ""
	while old_formula!=formula:
		old_formula = formula
		formula = Util.repeat_replace_inner_with_pattern(quantifier_pattern, __mrepl_entailment_quantifier, old_formula)
	return Util.endecode_string(__eliminate_bracket(formula),encode_pair[1],encode_pair[0])

