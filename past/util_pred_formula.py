import os
import re
from basic import Util
import util_pred
import itertools
import util_pred_model
import util_pred_formula
from basic import context_operator


conjunct_pattern = re.compile(r"{(.+?)}")
prefix_pattern = re.compile(r"\$.+?\$")
equal_pattern = re.compile(r"\s*(?P<left>[\w\d,\(\)]+)\s*=\s*(?P<right>\w\d+)")
replace_patten = re.compile(r"\s*!?\s*(?P<left>[\w\d,\(\)]+)\s*(?:>=|=|>)\s*(?P<right>[\w\d]+)")





def decode_pred_formula(pred_formula):
	pred_formula = pred_formula.replace('{','').replace('}','')
	pred_formula = pred_formula.replace('$','').replace('$','')
	return pred_formula


def delete_prefix(pred_formula):
	return prefix_pattern.sub("", pred_formula)


def pred_to_formula(pred):
	#print pred
	var_list, sorts, body = pred
	if var_list == list():
		return body
	else:
		int_vars = [var for e, var in enumerate(var_list) if sorts[e] =='Int']
		#int_vars_fol =' and '.join([ "%s>0 and %s<=len()"%(var, var) for var in int_vars])
		bound_list = context_operator.get_bound()
		int_vars_fol =' and '.join([ " and ".join(bound_list)%tuple(itertools.repeat(var, len(bound_list))) for var in int_vars])
		int_vars_fol ='$%s and $'%int_vars_fol if int_vars_fol!="" else int_vars_fol

		var_sort_list = [ '%s:%s'%(var_list[e],sorts[e]) for e in range(0,len(var_list))]
		return "exists(%s)[%s%s]"%(','.join(var_sort_list), int_vars_fol,body)



def from_conjuncts_to_formula(conjunct_list):
	return ' and '.join(["{%s}"%conjunct for conjunct in conjunct_list])



#f = "{! (exists(X1:Int)[$X1>=0 and $row(X1) = 2 and ! row(2) = X1])}"

def from_formula_to_conjuncts(formula):
	#print formula
	#formula = prefix_pattern.sub("",formula)
	return conjunct_pattern.findall(formula)

#print from_formula_to_conjuncts(f)



def from_conjunct_to_pred(conjunct):
	match = Util.rename_pattern.search(conjunct)
	if match:
		vars_sorts = match.group('var').split(',')
		vars_sorts = zip(*sum([],[ (var_sort.split(':')[0], var_sort.split(':')[1]) for var_sort in vars_sorts]))
		vars_sorts = [ list(elem) for elem in vars_sorts]
		var_list, sorts = vars_sorts[0], vars_sorts[1]
		#preds = [  elem.strip().lstrip('(').rstrip(')') for elem in match.group('body').split('and')]
		#prefix = [ pred for pred in preds if not __find_fluent(pred)]
		#body = [ pred for pred in preds if pred not in prefix]
		body = match.group('body').strip()
	else:
		var_list, sorts, body = [],[], Util.strip_kuohao(conjunct.strip())
		#body = [  elem.strip().lstrip('(').rstrip(')') for elem in conjunct.split('and')]
	return (var_list, sorts, body)


##############################################################################################################################################################


f= "((  row(1)=1 and row(2)=0   ) => (  row(1) = 1 and row(2)=0 and ! turn(p1)               )) and \
{! (exists(X0:Int)[$X0>=0 and $! row(X0) = 1 and row(1) = X0])} and \
{! (exists(X0:Int)[$X0>=0 and $row(2) = X0 and X0 > 1])} and \
{! (exists(X0:Int)[$X0>=0 and $len() = X0 and X0 > 3])}"



def __find_rep_var_preds(var, var_preds):
	rep_dict = dict()
	for pred in var_preds:
		match = equal_pattern.match(pred)
		if match is not None and match.group('right')==var and pred.count(var) ==1:
			rep_dict[pred] = match.group('left')
	return rep_dict

#print __fine_rep_var_preds('X0', mlist)


def __find_math(pred):
	if pred.find('%')!=-1: #or pred.find('-')!=-1 or pred.find('+')!=-1 or pred.find('/')!=-1 or pred.find('*')!=-1:
		return True
	else:
		return False

def __simplify_preds(var_list, preds):
	math_pred = [ pred for pred in preds if __find_math(pred) is True]
	preds = list(set(preds) - set(math_pred))
	for var in var_list:
		var_preds = [pred for pred in preds if pred.find(var)!=-1]
		rep_pred_dict = __find_rep_var_preds(var, var_preds)
		if rep_pred_dict == dict():
			continue
		be_rep_preds = list(set(var_preds) - set(rep_pred_dict.keys()))
		new_preds = [ pred.replace(var, rep_fun) for pred in be_rep_preds for key, rep_fun in rep_pred_dict.iteritems()]
		new_preds += [ "%s = %s"%elem for elem in itertools.combinations(rep_pred_dict.values(),2)]
		preds = list((set(preds) - set(var_preds)) | set(new_preds))
	return preds+math_pred
	#exit(0)


def __del_compred_var(com_pred):
	var_list, sorts, body_str = com_pred
	new_var_list, new_sorts = list(),list()
	for e, var in enumerate(var_list):
		if re.findall(r'\b%s\b'%var, body_str)!=list():
			new_var_list.append(var)
			new_sorts.append(sorts[e])
	return (new_var_list, new_sorts, body_str)

#f = "{! (exists(X0:Int,Y11:Int)[ mrow() = Y11 and ! X0 + 1 = Y11 and ! Y11 % 4 >= X0 and ! row(X0) = 0 and len() = X0])}"
# and \

def simplify(pred_formula):
	#print '---',pred_formula
	conjuncts = from_formula_to_conjuncts(pred_formula)
	#print conjuncts
	#print 'input',pred_formula
	for conjunct in conjuncts:
		m_conjunct = delete_prefix(conjunct)
		var_list, sorts, body = from_conjunct_to_pred(m_conjunct.strip('!').strip())
		elems = body.split(' and ')
		#print elems, body
		pred_str =' and '.join(__simplify_preds(var_list, elems))
		pred = __del_compred_var((var_list, sorts, pred_str))
		formula = pred_to_formula(pred)
		pred_formula = pred_formula.replace(conjunct, '! (%s)'%formula)
	#print 'output',pred_formula
	#print 
	return decode_pred_formula(pred_formula)


#print simplify(f)
##############################################################################################################################################################


def is_sublist(mlistA, mlistB):
	for mA in mlistA:
		if mA not in mlistB:
			return False
	return True



def detect_redundant_conjuncts(conjunct_list, conjunct_model_dict, new_repl_conjunct, model_set_neg):
	#print
	#print conjunct_list
	#print conjunct_model_dict
	#print new_repl_conjunct
	#print model_set_neg
	#print
	com_pred = from_conjunct_to_pred(util_pred_formula.delete_prefix(new_repl_conjunct.strip('!').strip()))
	model_list = util_pred_model.get_models_sat_pred(model_set_neg, com_pred)
	decode_conjuncts = [Util.strip_kuohao(util_pred_formula.delete_prefix(conjunct).lstrip('!').strip()) for conjunct in conjunct_list]

	redundant_conjunct_list = list()
	for e, conjunct in enumerate(decode_conjuncts):
		if is_sublist(conjunct_model_dict[conjunct], model_list) is True:
			redundant_conjunct_list.append(conjunct)
	return redundant_conjunct_list



##############################################################################################################################################################












