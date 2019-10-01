#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-19 22:56:01
# @Author  : Kailun Luo (luokl3@mail2.sysu.edu.cn)
# @Link    : https://sdcs.sysu.edu.cn
# @Version : $Id$

import os

from basic import context_operator
from basic import Util
import util_pred
import re

import itertools
from operator import itemgetter


#import mylog as logging
#logger = logging.getLogger(__name__)
#import modify2



fun_pattern_str = r"\w+"
fun_pattern = re.compile(fun_pattern_str)
math_functions = ['+', '%' ,'*']


##############################################################################################################################################################

'''
def __fluentTerm_filter_via_constraints(fluent_predicates, fluent_constraints):
	feature_list = [ (constraint.split('@')[0], constraint.split('@')[1])  for constraint in fluent_constraints.keys()]
	feature_dict = {"%s@%s"%(fun,index):(fun, r"%s\(%s\b"%(fun,'\s*,\s*'.join(['\s*\w+\s*']*(int(index)-1)+['#']))) for fun, index in feature_list}
	#print feature_dict
	filter_dict = dict()
	for key, (fun, feature) in feature_dict.iteritems():
		filter_dict[key] = (fun, [feature.replace('#',elem) for elem in fluent_constraints[key]])

	filter_list = filter_dict.values()

	new_pred_list = list()
	for pred in fluent_predicates:
		fun_name = fun_pattern.match(pred).group()
		#print fun_name
		flag_filter = False
		for fun, constraint_pattern_list in filter_list:
			if fun_name == fun:
				flag_filter = True
				for constraint_pattern in constraint_pattern_list:
					if re.match(constraint_pattern, pred) is not None:
						flag_filter = False
						break
		if flag_filter is False:
			new_pred_list.append(pred)
	return new_pred_list

'''

##############################################################################################################################################################
'''

def __gen_pred_from_file(filename):
	file = open(filename, 'r')
	preds = [eval(elem) for elem in file.readlines()]
	preds = preds + [ (var_list,sorts, '! '+body) for var_list,sorts, body in preds]
	return preds


zero_str = r"\b0\b"
zero_pattern = re.compile(zero_str)

def __del_zero(preds):
	return [ pred for pred in preds if zero_pattern.search(pred) is None ]

def __two_var_limited(preds):
	return [pred for pred in preds if len(var_pattern.findall(pred))<=2]

'''
##############################################################################################################################################################

'''
def ____gen_rel_pred_from_template(left_terms, right_terms, relations, template):
	temp0 = [template]
	temp1 = [t.replace('@rel', rel) for t in temp0 for rel in relations ] if relations else temp0
	#print '---1',temp1
	temp2 = [t.replace('@left', left) for t in temp1 for left in left_terms ] if left_terms else temp1
	#print '---2',temp2
	temp3 = [t.replace('@right', right) for t in temp2 for right in right_terms ] if right_terms else temp2
	#print '---3',temp3
	return list(set(temp3))


def ____get_var_terms(terms):
	return [elem for elem in terms if util_pred.is_var(elem)]



def ____get_terms_from_sort(fun_valuesort_list, t_sort, terms):
	fun_list = [ fun for fun, sort in fun_valuesort_list if sort == t_sort]
	return [elem for elem in terms if fun_pattern.search(elem).group(0) in fun_list]



def __gen_var_rel_pred(fun_valuesort_list, terms, relations, template, sort_list = None):
	"""

	@param fun_valuesort_list
	@terms 
	@relations
	@template
	@sort_list
	"""
	preds = list()
	if sort_list is None:
		sort_list = list(set([sort for fun, sort in fun_valuesort_list]))

	for t_sort in sort_list:
		mterms = ____get_terms_from_sort(fun_valuesort_list, t_sort, terms)
		var_terms = ____get_var_terms(mterms)
		if var_terms!=list():
			preds += ____gen_rel_pred_from_template(var_terms, var_terms, relations, template)
	return preds
'''




##############################################################################################################################################################
# generate predicates

def ____gen_elem_from_template(consts, mvars, functions, relations, template):
	temp0 = [template]
	temp1 = [t.replace('@rel', rel) for t in temp0 for rel in relations ] if relations else temp0
	temp2 = [t.replace('@fun', fun) for t in temp1 for fun in functions ] if functions else temp1
	temp3 = [t.replace('@var', var) for t in temp2 for var in mvars ] if mvars else temp2
	temp4 = [t.replace('@const', const) for t in temp3 for const in consts ] if consts else temp3
	return list(set(temp4))



def __gen_pred_from_template(sort, functions, relations, sort_consts, template):
	consts = sort_consts[sort]
	mvars = [ elem for elem in consts if util_pred.is_var(elem)]
	consts = [ elem for elem in consts if elem not in mvars]
	return ____gen_elem_from_template(consts, mvars, functions, relations, template)



def __gen_equal_pred_from_template(fun_valuesort_list, terms, sort_consts, template):
	preds = list()
	for fun, sort in fun_valuesort_list:
		mterms = [elem for elem in terms if fun_pattern.search(elem).group(0)==fun]
		preds += __gen_pred_from_template(sort, mterms, ['='], sort_consts, template)
	return preds


def __gen_fluent_pred(pred_parasorts_list, sort_consts):
	preds = list()
	for fluent_name, sorts in pred_parasorts_list:
		consts = [sort_consts[sort] for sort in sorts]
		preds += [ "%s(%s)"%(fluent_name, ','.join(list(elem))) for elem in list(itertools.product(*consts))]
	return preds


##############################################################################################################################################################
# generate terms


def __get_math_term_from_template(sort, functions, sort_consts, template):
	consts = sort_consts[sort]
	consts = [elem for elem in consts if elem!='0']
	mvars = [ elem for elem in consts if util_pred.is_var(elem)]
	consts = [ elem for elem in consts if elem not in mvars]	
	return ____gen_elem_from_template(consts, mvars, functions, None, template)



def __gen_fluent_term(fun_parasorts_list, sort_consts):
	fluent_terms = list()
	for fluent_name, sorts in fun_parasorts_list:
		consts = [sort_consts[sort] for sort in sorts]
		fluent_terms += [ "%s(%s)"%(fluent_name, ','.join(list(elem))) for elem in list(itertools.product(*consts))]

	return fluent_terms


##############################################################################################################################################################


def genPreds(constraints=dict()):

	fluent_sorts = context_operator.get_functions_sorts()
	sort_consts = context_operator.get_sort_symbols_dict()
	functions =  list(set(context_operator.get_fluents())- set(context_operator.get_predicates()))
	predicates = context_operator.get_predicates()


	fun_parasorts_list = [(fluent, sorts[0:len(sorts)-1]) for fluent, sorts in fluent_sorts.iteritems() if fluent in functions]
	fun_valuesort_list = [(fluent, sorts[len(sorts)-1]) for fluent, sorts in fluent_sorts.iteritems() if fluent in functions]
	pred_parasorts_list = [(fluent, sorts[0:len(sorts)-1]) for fluent, sorts in fluent_sorts.iteritems() if fluent in predicates]
	sort_consts = {sort:consts+['X'+str(e)] for e,(sort,consts) in enumerate(sort_consts.iteritems())}

	
	# generate terms like x+1 from template "@var @fun @const", where the first is variable,  the second is math function 
	# the third is constant 
	math_terms = __get_math_term_from_template( 'Int', math_functions, sort_consts, "@var @fun @const")
	# generate terms like x+x
	math_terms += __get_math_term_from_template( 'Int', math_functions, sort_consts, "@var @fun @var")
	# generate terms like cell(x,x)
	fluent_terms = __gen_fluent_term(fun_parasorts_list, sort_consts)
	#fluent_terms = __fluentTerm_filter_via_constraints(fluent_terms, constraints)

	# generate predicates like x>1, x>=1, x=1
	math_var_predicates = __gen_pred_from_template('Int', [], ['>','>=','='], sort_consts, "@var @rel @const")
	# generate predicates like x>x, x>=1, x=1
	math_var_predicates += __gen_pred_from_template('Int', [], ['>','>=','='], sort_consts, "@var @rel @var")
	# generate predicates like x%2=1
	math_var_predicates += __gen_pred_from_template('Int', math_terms, ['='], sort_consts, "@fun @rel @const")
	# generate predicates like x+1 = x
	math_var_predicates += __gen_pred_from_template('Int', math_terms, ['='], sort_consts, "@fun @rel @var")

	# generate fluent predicates like turn(p1)
	fluent_predicates = __gen_fluent_pred(pred_parasorts_list, sort_consts)

	# generate fluent predicates by combining fluent terms with constants or variables under certain relation (e.g.,=,>=)
	const_funs = [ fun+"()" for fun in context_operator.get_zero_fluents() if fun in context_operator.get_fluents() if fun not in predicates]
	fluent_predicates += __gen_equal_pred_from_template(fun_valuesort_list, fluent_terms , sort_consts, "@fun @rel @const")
	fluent_predicates += __gen_equal_pred_from_template(fun_valuesort_list, fluent_terms , sort_consts, "@fun @rel @var")
	fluent_predicates += __gen_pred_from_template('Int', const_funs , ['>=','>'], sort_consts, "@fun @rel @var")

	#print __gen_var_rel_pred(fun_valuesort_list, fluent_terms, ['='], "@left @rel @right")
	#print __gen_var_rel_pred(fun_valuesort_list, fluent_terms, ['>=', '>'], "@left @rel @right", ['Int'])
	#exit(0)

	#fluent_predicates += __two_var_limited(__del_zero(__gen_var_rel_pred(fun_valuesort_list, fluent_terms, ['='], "@left @rel @right")))
	##print __two_var_limited(__del_zero(__gen_var_rel_pred(fun_valuesort_list, fluent_terms, ['='], "@left @rel @right")))
	#print '4',fluent_predicates
	#fluent_predicates += __two_var_limited(__del_zero(__gen_var_rel_pred(fun_valuesort_list, fluent_terms, ['>=', '>'], "@left @rel @right", ['Int'])))
	##print  __gen_var_rel_pred(fun_valuesort_list, fluent_terms, ['>=', '>'], "@left @rel @right", ['Int'])
	#print '5',fluent_predicates
	
	math_var_predicates = [ util_pred.find_var(pred) for pred in math_var_predicates] 
	fluent_predicates = [ util_pred.find_var(pred) for pred in fluent_predicates]
	#print '6',fluent_predicates
	math_var_predicates = [  (var_list, util_pred.find_var_sort(var_list, sort_consts), pred) for var_list,pred in math_var_predicates]
	fluent_predicates = [ (var_list, util_pred.find_var_sort(var_list, sort_consts), pred) for var_list,pred in fluent_predicates]
	#print '7',fluent_predicates


	math_var_predicates = sum([ util_pred.devars(pred) for pred in math_var_predicates],[])
	fluent_predicates = sum([ util_pred.devars(pred) for pred in fluent_predicates],[])

	math_var_predicates += [(var_list,sorts, "! "+body) for (var_list,sorts, body) in math_var_predicates ]
	fluent_predicates += [(var_list,sorts, "! "+body) for (var_list,sorts, body) in fluent_predicates ]


	return math_var_predicates, fluent_predicates


##############################################################################################################################################################

import predicate_filter

def generate_preds(file_name, constraints=dict()):
	with open('./temp/pred_info','write') as sc_temp:
		math_var_predicates, fluent_predicates = genPreds()
		math_var_predicates = predicate_filter.filter_by_unused_mathsymbols(file_name, math_var_predicates)
		sc_temp.writelines('Before filter: Math Preds: %s Fluent Preds: %s \n'%(len(math_var_predicates),len(fluent_predicates) ))
		math_var_predicates = predicate_filter.filter_by_math_property(math_var_predicates, sc_temp)
		sc_temp.writelines('After filter: Math Preds: %s Fluent Preds: %s \n'%(len(math_var_predicates),len(fluent_predicates)))
		sc_temp.writelines('\n'.join([str(e) for e in math_var_predicates]))
		sc_temp.writelines('\n\n')
		sc_temp.writelines('\n'.join([str(e) for e in fluent_predicates]))
		sc_temp.close()

		return math_var_predicates, fluent_predicates

