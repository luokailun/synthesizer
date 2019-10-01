

import re

var_pattern_str = r"(?:\b[A-Z][\d]+\b)"
var_pattern = re.compile(var_pattern_str)
number_pattern_str = r"\b\d+\b"
number_pattern = re.compile(number_pattern_str)

symbol = r'%s|%s'%(var_pattern_str, number_pattern_str)
#symbol_pattern = re.compile(symbol)

expression = lambda x: '(?P<left>%s)\s*%s\s*(?P<mid>%s)\s*=\s*(?P<right>%s)'%(symbol,x,symbol,symbol)
modular_exp = expression('\%')
multiple_exp = expression('\*')
additive_exp = expression('\+')

modular_exp_pattern = re.compile(modular_exp)
multiple_exp_pattern = re.compile(multiple_exp)
additive_exp_pattern = re.compile(additive_exp)

##############################################################################################################################################################


def __filter_by_additive_property(math_pred_list, file_handler=None):
	"""
	delete predicates like x1+x2 =0
	"""
	del_math_pred_list = list()
	additive_pred_list = [ (var_list, sort_list, body) for var_list, sort_list, body in math_pred_list if body.find('+')!=-1]
	symbols_list = [ additive_exp_pattern.search(body).groups() for  (var_list, sort_list, body) in additive_pred_list ]

	for e, math_pred in enumerate(additive_pred_list):
		left, mid, right = symbols_list[e] 
		if right == '0': 
			del_math_pred_list.append(math_pred)

	if file_handler:
		file_handler.writelines('Delete Number(%s) \n %s \n\n'%(len(del_math_pred_list), '\n'.join([str(e) for e in del_math_pred_list])))

	return [pred for pred in math_pred_list if pred not in del_math_pred_list]



def __filter_by_multiple_property(math_pred_list, file_handler=None):
	"""
	delete predicates like x1*1 =x2, x3*1 = x4
	delete predicates like x*y =1,  x*y =2
	"""
	del_math_pred_list = list()
	multiple_pred_list = [ (var_list, sort_list, body) for var_list, sort_list, body in math_pred_list if body.find('*')!=-1]
	symbols_list = [ multiple_exp_pattern.search(body).groups() for  (var_list, sort_list, body) in multiple_pred_list ]

	for e, math_pred in enumerate(multiple_pred_list):
		left, mid, right = symbols_list[e] 
		if mid == '1': 
			del_math_pred_list.append(math_pred)
		elif not left.isdigit() and not mid.isdigit() and right.isdigit():
			del_math_pred_list.append(math_pred)

	if file_handler:
		file_handler.writelines('Delete Number(%s) \n %s \n\n'%(len(del_math_pred_list), '\n'.join([str(e) for e in del_math_pred_list])))

	return [pred for pred in math_pred_list if pred not in del_math_pred_list]



def __filter_by_modular_property(math_pred_list, file_handler=None):
	"""
	delete predicates like x % 1 = y
	delete predicates like x % 3 = 4
	"""
	del_math_pred_list = list()
	modular_pred_list = [ (var_list, sort_list, body) for var_list, sort_list, body in math_pred_list if body.find('%')!=-1]
	symbols_list = [ modular_exp_pattern.search(body).groups() for  (var_list, sort_list, body) in modular_pred_list ]

	for e, math_pred in enumerate(modular_pred_list):
		left, mid, right = symbols_list[e] 
		if mid == '1': 
			del_math_pred_list.append(math_pred)
		elif mid.isdigit() and right.isdigit() and int(mid)<= int(right):
			del_math_pred_list.append(math_pred)

	if file_handler:
		file_handler.writelines('Delete Number(%s) \n %s \n\n'%(len(del_math_pred_list), '\n'.join([str(e) for e in del_math_pred_list])))
	return [pred for pred in math_pred_list if pred not in del_math_pred_list]



def __filter_by_limited_constants(math_pred_list, file_handler=None):
	"""
	delete predicates like x-3 =1
	"""
	new_math_pred_list = list()
	del_math_pred_list = list()
	for math_pred in math_pred_list:
		var_list, sort_list, body = math_pred
		constants = number_pattern.findall(body)
		if len(constants)>=2 and body.find('%') ==-1:
			del_math_pred_list.append(math_pred)
		else:
			new_math_pred_list.append(math_pred)

	if file_handler:
		file_handler.writelines('Delete Number(%s) \n %s \n\n'%(len(del_math_pred_list), '\n'.join([str(e) for e in del_math_pred_list])))
	#print del_math_pred_list
	return new_math_pred_list




def __filter_by_duplicate_vars(math_pred_list, file_handler=None):
	"""
	delete predicates like X +1 =X
	"""
	new_math_pred_list = list()
	del_math_pred_list = list()
	for math_pred in math_pred_list:
		var_list, sort_list, body = math_pred
		all_vars = var_pattern.findall(body)
		if len(list(set(all_vars))) < len(all_vars):
			del_math_pred_list.append(math_pred)
		else:
			new_math_pred_list.append(math_pred)

	if file_handler:
		file_handler.writelines('Delete Number(%s) \n %s \n\n'%(len(del_math_pred_list), '\n'.join([str(e) for e in del_math_pred_list])))
	#print '\n'.join([str(e) for e in del_math_pred_list])
	return new_math_pred_list



def filter_by_math_property(math_pred_list, file_handler=None):

	new_pred_list = __filter_by_duplicate_vars(math_pred_list, file_handler)
	new_pred_list = __filter_by_limited_constants(new_pred_list, file_handler)
	new_pred_list = __filter_by_modular_property(new_pred_list, file_handler)
	new_pred_list = __filter_by_multiple_property(new_pred_list, file_handler)
	new_pred_list = __filter_by_additive_property(new_pred_list, file_handler)

	return new_pred_list


'''
m_list = [(['Y10', 'Y11'], ['Int', 'Int'], '! Y10 + Y11 = 2'),
(['Y10', 'Y11'], ['Int', 'Int'], '! Y10 * Y11 = 2'),
(['Y10', 'Y11'], ['Int', 'Int'], '! Y10 * Y11 = 0'),
(['Y10', 'Y11'], ['Int', 'Int'], '! Y10 * Y11 = 1'),
(['Y10', 'Y11', 'Y12'], ['Int', 'Int', 'Int'], '! Y10 + Y11 = Y12'),
(['Y10', 'Y11', 'Y12'], ['Int', 'Int', 'Int'], '! Y10 % Y11 = Y12'),
(['Y10', 'Y11'], ['Int', 'Int'], '! Y10 + 3 = Y11'),
(['Y10', 'Y11', 'Y12'], ['Int', 'Int', 'Int'], '! Y10 * Y11 = Y12'),
(['Y10', 'Y11'], ['Int', 'Int'], '! Y10 * 2 = Y11'),
(['Y10', 'Y11'], ['Int', 'Int'], '! Y10 % 4 = Y11'),
(['Y10', 'Y11'], ['Int', 'Int'], '! Y10 % 4 = 4'),
(['Y10', 'Y11'], ['Int', 'Int'], '! Y10 % 1 = Y11'),
(['Y10', 'Y11'], ['Int', 'Int'], '! Y10 + 4 = Y11'),
(['Y10', 'Y11'], ['Int', 'Int'], '! Y10 * 4 = Y11'),
(['Y10', 'Y11'], ['Int', 'Int'], '! Y10 + 2 = Y11'),
(['Y10', 'Y11'], ['Int', 'Int'], '! Y10 * 1 = Y11')]

print filter_by_math_property(m_list)
'''

##############################################################################################################################################################


def __get_unused_mathsymbols(file_name):
	math_symbols = ['+','-','*','%']
	with open('./input/%s'%(file_name),"read") as sc_file:
		full_txt = " ".join(sc_file.readlines())
		return [sym for sym in math_symbols if full_txt.find(sym)==-1]


def __filter_by_matched_symbols(pred_list, symbols):
	delete_pred_list = [(var_list, sorts, body) for (var_list, sorts, body) in pred_list for sym in symbols if body.find(sym)!=-1]
	return [pred for pred in pred_list if pred not in delete_pred_list]


def filter_by_unused_mathsymbols(file_name, pred_list):
	unused_symbols = __get_unused_mathsymbols(file_name)
	# if - is used, then we use '+'.
	if '+' in unused_symbols and '-' not in unused_symbols:
		unused_symbols.pop('+')
	return __filter_by_matched_symbols(pred_list, unused_symbols)



##############################################################################################################################################################

'''

def __delete_unknown_predicates(fluent_predicates):
	return [ (var_list, sorts, body) for var_list ,sorts, body in fluent_predicates if body.find('unknown')==-1]

def __delete_last_preds(com_preds):
	#??? delete_preds = [(var_list, sorts, body) for (var_list, sorts, body) in com_preds if body.find('last')!=-1 and (body.find('>=')!=-1 or body.find('>')!=-1)]
	delete_preds = [(var_list, sorts, body) for (var_list, sorts, body) in com_preds if body.find('last')!=-1]
	#print delete_preds
	return [pred for pred in com_preds if pred not in delete_preds]


def reduce_num_fluent_preds(com_preds):
	com_preds = __delete_unknown_predicates(com_preds)
	com_preds = __delete_last_preds(com_preds)
	return com_preds

'''
##############################################################################################################################################################

