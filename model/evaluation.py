

import operator
import re

word_pattern = re.compile(r'\w+')
sym_pattern = re.compile(r'[^\w\s\(\)]+')
op_dict = {'>': operator.gt, '==': operator.eq, '>=':operator.ge, '+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.div, '%': operator.mod }


def eval_expression(expression, value_dict):
	#print expression, value_dict
	words = word_pattern.findall(expression)
	symbols = sym_pattern.findall(expression)
	neg, pos, left_value, op= False,0, None, None
	#print
	#print expression
	for sym in symbols:
		#print words,"current position[%s]"%pos,words[pos],sym
		if sym == '!':
			#print 'A'
			neg = True
		elif sym == '==' or sym == '>=' or sym == '>':
			#print 'B'
			op, left_value, pos = sym, words[pos], pos+1
			#left_value = var_dict[left_value] if left_value in var_dict else left_value
		elif sym == '&':
			#print 'C'
			right_value, pos =  words[pos], pos+1
			if op is not None:
				#right_value = var_dict[right_value] if right_value in var_dict else right_value
				left_value = int(left_value) if left_value.isdigit() else left_value
				right_value = int(right_value) if right_value.isdigit() else right_value
				true_value = op_dict[op](left_value,right_value)
				#print '#return %s'%true_value
			else:
				true_value = value_dict[right_value]

			true_value = not true_value if neg is True else true_value
			if true_value is False:
				return False
			else:
				neg, op = False, None
		else:
			#print 'D'
			left, right, pos = words[pos], words[pos+1], pos+1
			#left = var_dict[left] if left in var_dict else left
			#right = var_dict[right] if right in var_dict else right
			left = int(left) if left.isdigit() else left
			right = int(right) if right.isdigit() else right
			words[pos] = str(op_dict[sym](left,right))
			#print '#return %s'%words[pos]

	right_value, pos =  words[pos], pos+1
	#print left_value, right_value, op
	if op is not None:
		#right_value = var_dict[right_value] if right_value in var_dict else right_value
		left_value = int(left_value) if left_value.isdigit() else left_value
		right_value = int(right_value) if right_value.isdigit() else right_value
		true_value = op_dict[op](left_value,right_value)
		#print left_value, right_value, true_value
	else:
		true_value = value_dict[right_value]

	true_value = not true_value if neg is True else true_value
	if true_value is False:
		return False
	else:
		return True


