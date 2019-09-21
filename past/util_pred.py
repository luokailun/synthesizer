#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-06 21:28:17
# @Author  : Kailun Luo (luokl3@mail2.sysu.edu.cn)
# @Link    : https://sdcs.sysu.edu.cn
# @Version : $Id$
from memory_profiler import profile
import gc  
import os
from basic import progress
from basic import Util
from basic import context_operator
from basic import util_z3
import counterexample

import util_pred_model
import util_pred_score
import util_pred_filter
import util_constraint

import itertools
from operator import itemgetter 
from itertools import groupby
import copy
import re
import mylog as logging
import util_pred_formula
logger = logging.getLogger(__name__)

conjunct_pattern = re.compile("\{.+?\}")
PREFIX_LENGTH = 2
PRED_LENGTH = 2
MAX_NUM = 11


def __add_prefix(pred):
	var_list, sorts, body = pred
	add_body = body
	bound_list = context_operator.get_bound()
	for e, sort in enumerate(sorts):
		if sort =='Int':
			#prefix = '%s>0 and ! %s>len()'%(var_list[e], var_list[e])
			#prefix = '%s>=0'%(var_list[e])
			prefix = " and ".join(bound_list)%tuple(itertools.repeat(var_list[e], len(bound_list)))
			add_body = "%s and %s"%(prefix, add_body)
	return (var_list, sorts, add_body)


##############################################################################################################################################################

def __math_ground_check(pred, unsat_models):
	print 'math ground check-------',pred
	universe = dict(context_operator.get_sort_symbols_dict())
	universe['Int'] = [ str(e) for e in range(0, MAX_NUM+1)]
	pred = __add_prefix(pred)
	return util_pred_model.models_unsat_math_pred(unsat_models, pred, universe)


def __get_not_true_pred(pred_list, unsat_models):
	for pred in pred_list:
		#if counterexample.interpret_result(util_z3.imply('true', __pred_to_formula(pred))) is False and __math_ground_check(pred, unsat_models) is True:
		if __math_ground_check(pred, unsat_models) is True:
			return pred
	return None

##############################################################################################################################################################

def __compress_to_dict(pred_list):
	return {body: (var_list, sorts) for var_list, sorts, body in pred_list}


def compress(pred_list):
	pred_dict = context_operator.get_pred_dict()
	new_dict = {body: (var_list, sorts) for var_list, sorts, body in pred_list}
	pred_dict.update(new_dict)
	return new_dict.keys()


def decompress(pred_body_list):
	pred_dict = context_operator.get_pred_dict()
	return [ (pred_dict[body][0], pred_dict[body][1], body) for body in pred_body_list]

##############################################################################################################################################################



def __str_to_pred(pred_str):
	com_pred = pred_str.split('#')
	return com_pred[0].split('_'), com_pred[1].split('_'), com_pred[2].split('_'), com_pred[3].split('_')



def __pred_to_str(pred):
	var_list, sorts, prefix, body = pred
	var_str = '_'.join(var_list)
	sort_str = '_'.join(sorts)
	prefix_str = '_'.join(prefix)
	body_str = '_'.join(body)
	return "%s#%s#%s#%s"%(var_str, sort_str, prefix_str, body_str)


def __preds_to_strs(pred_list):
	return [ __pred_to_str(pred) for pred in pred_list] 


#pred = (['X1','X2'], ['Int','Int'], 'X1+X2=0')



#print __pred_to_formula(pred)

##############################################################################################################################################################
#k1 = (['X1','X2'], ['Int','Int'],[], ['! numStone() = X1'])

def del_compred_var(com_pred):
	var_list, sorts, body_str = com_pred
	new_var_list, new_sorts = list(),list()
	for e, var in enumerate(var_list):
		if re.findall(r'\b%s\b'%var, body_str)!=list():
			new_var_list.append(var)
			new_sorts.append(sorts[e])
	return (new_var_list, new_sorts, body_str)
#print del_compred_var(k1)


##############################################################################################################################################################
'''
body = "row(X1) = 2 and X1 % 4 = X2"
vars_sorts = (['X2','X1'],['Int','Int'])
pred_sort_dict = {'row(X) = 2':True, 'X % 4 = X':False}
'''
#preds = ['a and b and c', 'b and c and d', 'a and c and b']

'''
def __isFilter_redundant(preds):
	print 
	print preds
	print 
	pred_dict = {pred: True for pred in preds}
	pred_set = set()
	for pred in preds:
		if pred not in pred_set:
			pred_set.update([ ' and '.join(elem) for elem in itertools.permutations(pred.split(' and '))])
		else:
			pred_dict[pred] = False
	return [pred for pred in preds if pred_dict[pred] is True]
'''

'''
def __isFilter_redundant(com_predA, com_predB):
	var_list1, sorts1, body1 = com_predA
	var_list2, sorts2, body2 = com_predB
	for var in var_list1:
		body1 = body1.replace(var, 'W')
	for var in var_list2:
		body2 = body2.replace(var, 'W')	
	if body1.find(body2) == -1:
		return False
	else:
		return True

'''
'''
# has function????
def __filter(base_pred, add_pred, filter_set):
	var_list1, sorts1, body1 = base_pred
	var_list2, sorts2, body2 = add_pred

	body = body1.split(' and ')+[body2]
	feature_list = list()
	for length in range(2, len(body)+1):
		feature_list += list(itertools.permutations(body,length))

	feature_set = set([ '_'.join(prefix+list(elem)) for elem in feature_list])
	return  True if feature_set & filter_set!=set() else False

'''

def __filter_redundant(preds):
	pred_dict = {pred: True for pred in preds}
	pred_set = set()
	for pred in preds:
		pred_feature_set = set([ ' and '.join(elem) for elem in itertools.permutations(pred.split(' and '))])
		if pred_feature_set & pred_set == set():
			pred_set.add(pred)
	return list(pred_set)


#print __isFilter_redundant(preds)

def __isFilter_free_var(vars_sorts, body, pred_sort_dict):
	var_list, sorts = vars_sorts
	mbody = body
	for var in var_list:
		mbody = mbody.replace(var,'X')
	mbody = mbody.split(' and ')

	fluent_part = ' '.join([ pred for e, pred in enumerate(body.split(' and ')) if pred_sort_dict[mbody[e]] is True])
	for var in var_list:
		if fluent_part.find(var)==-1:
			return True
	return False

#print 'hello',__isFilter_free_var(vars_sorts, body, pred_sort_dict)


def __isFilter_no_common_sort(base_pred, add_pred):
	var_list1, sorts1, body1 = base_pred
	var_list2, sorts2, body2 = add_pred
	return True if not (sorts1==[] and sorts2==[]) and set(sorts1) & set(sorts2) == set() else False

#pred_list = ['a and b and c', 'a and d']
#filter_set = set([('a','b')])

def __filter_via_filter_set(pred_list, filter_set):
	pred_dict = dict()
	for pred in pred_list:
		elems = pred.split(' and ')
		feature_set = set()
		for length in range(2, len(elems)+1):
			feature_set.update(itertools.permutations(elems,length))
		#print feature_set
		if feature_set & filter_set == set():
			pred_dict[pred] = True
		else:
			pred_dict[pred] = False
	return [pred for pred in pred_dict.keys() if pred_dict[pred] is True]

#print '----'
#print __filter_via_filter_set(pred_list, filter_set)

#pred_list = ['a and b']
def __add_filter_elems(pred_list):
	filter_set = set()
	for pred in pred_list:
		elems = pred.split(' and ')
		filter_set.update(itertools.permutations(elems,len(elems)))
	return filter_set

#print __add_filter_elems(pred_list)


##############################################################################################################################################################




#P1=(['X'], ['Int'], 'xpos() = 0') 
#P2=(['Y'], ['Int'], '! LeftTurn()')

#print __combine(P1, P2, dict())




#only allow two variable






#var_list = ['X1','X2','X3','X4']
#sorts = ['Int','S1','Int','Int']
#print __gen_sort_vars(var_list, sorts)


##############################################################################################################################################################



'''
k1 = (['X1'], ['Int'], 'numStone() = X1')
k2 = (['X1', 'X2'],['Int','Int'],'X1 > X2')


sorts_vars_dict = dict()
sorts_vars_dict[k1[2]] = __gen_sort_vars(k1[0],k1[1])
sorts_vars_dict[k2[2]] = __gen_sort_vars(k2[0],k2[1])
#print sorts_vars_dict
print __gen_var_preds(k1, k2, sorts_vars_dict)
'''
##############################################################################################################################################################






##############################################################################################################################################################

def __get_sat_preds(preds, pred_dict, models_sat):
	for model in models_sat:
		preds = util_pred_model.preds_sat_model(model, preds, pred_dict) 
	return preds


def __get_unsat_preds(preds, pred_dict, models_unsat):
	for model in models_unsat:
		preds = util_pred_model.preds_unsat_model(model, preds, pred_dict) 
	return preds


##############################################################################################################################################################



##############################################################################################################################################################


def __create_score_dict(fluent_preds, model_preds):
	return dict()

#mbody = "! row(2) = X1"
#fluents = ['turn', 'len', 'row']

def __detect_fluents(mbody, fluents):
	for fluent in fluents:
		if re.findall(r'\b%s\b'%fluent, mbody)!=[]:
			return True
	return False
#print '!',__detect_fluents(mbody, fluents)





##############################################################################################################################################################
#print util_pred_formula.from_formula_to_conjuncts('aaa')







def ______combine(pred, add_pred, new_preds_dict):
	var_list, sorts, body = pred
	m_var_list, m_sorts, m_body = add_pred
	vars_sorts = zip(*list(set(zip(var_list, sorts)+zip(m_var_list,m_sorts))))
	new_preds_dict[body+' and '+m_body] = (list(vars_sorts[0]), list(vars_sorts[1]))
	return ""


def ____gen_combined_pred_constraint_dict(com_pred, add_pred, devar_pred_list):
	var_list, sorts, body = com_pred
	mvar_list, msorts, mbody = add_pred
	pred_constraint_dict = context_operator.get_pred_constraint_dict()
	base_pred_constraint_dict = context_operator.get_base_pred_constraint_dict()
	add_pred_constraints = base_pred_constraint_dict[mbody]

	for add_var_list, add_sorts, add_body in devar_pred_list:
		var_match_dict = {mvar_list[e]:add_var for e, add_var in enumerate(add_var_list) }
		new_pred_key = body+ ' and '+add_body
		add_constraints = { var_match_dict[key]: value for key, value in add_pred_constraints.iteritems()}
		pred_constraint_dict[new_pred_key] = copy.deepcopy(pred_constraint_dict[body])
		pred_constraint_dict[new_pred_key].update(add_constraints)


def ____gen_new_combined_pred_dict(pred, add_pred, de_var_pred_list, new_preds_dict):
	if de_var_pred_list ==[]:
		var_list, sorts, body = pred
		mvar_list, msorts, mbody = add_pred
		new_preds_dict[body+' and '+mbody] = (var_list, sorts)
	else:
		for de_var_pred in de_var_pred_list:
			______combine(pred, de_var_pred, new_preds_dict)


def ____from_str_to_pred(var_body_str, sorts):
	temp = var_body_str.replace('_','').split('#')
	return (temp[0].split('$'), sorts, temp[1])


def ____replace_var_body(mstr, replace_list):
	replace_list = [(r'\b%s\b'%old_var, '_%s'%new_var) for (new_var, old_var) in replace_list]
	new_str = reduce(lambda x,y: re.sub(y[0],y[1],x), replace_list, mstr)
	return new_str


def ____de_vars(var_list, old_var_list):
	if len(var_list) < len(old_var_list):
		patterns = list(itertools.permutations(old_var_list))
		var_list = var_list + old_var_list[len(var_list)::]
		return  [zip(tuple(var_list), pattern) for pattern in patterns]
	else:
		patterns = list(itertools.permutations(var_list))
		return [zip(pattern, old_var_list) for pattern in patterns]			



def __from_sort_to_varPreds(sorts_vars_one, sorts_vars_two, pred, add_pred, new_preds_dict):
	var_list, sorts, body = pred
	m_var_list, m_sorts, m_body = add_pred

	if var_list ==[] and m_var_list==[]:
		de_var_pred_list = []
	else:
		replace_list = ['$%s#%s'%('$'.join(m_var_list),''m_body)]
		for sort, vars_one in sorts_vars_one.iteritems():
			if sort not in sorts_vars_two:
				continue
			var_templates = ____de_vars(vars_one, sorts_vars_two[sort])
			#print var_templates
			replace_list = [ ____replace_var_body(replace_part, template) for template in var_templates for replace_part in replace_list]

		de_var_pred_list = [ ____from_str_to_pred(mstr, m_sorts) for mstr in replace_list]
	####[constraints]
	____gen_combined_pred_constraint_dict(pred, add_pred, de_var_pred_list)
	####
	____gen_new_combined_pred_dict(pred, add_pred, de_var_pred_list, new_preds_dict)
	#return [ __combine(pred, de_var_pred, new_preds_dict) for de_var_pred in de_var_pred_list]



def gen_var_preds(pred, add_pred, sort_vars_dict, new_preds_dict):
	var_list, sorts, body = pred
	sorts_vars_one = sort_vars_dict[body]
	#for add_pred in pred_list:
	add_var_list, add_sorts, add_body = add_pred
	sorts_vars_two = sort_vars_dict[add_body]

	__from_sort_to_varPreds(sorts_vars_one, sorts_vars_two, pred, add_pred, new_preds_dict)




