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


var_pattern_str = r"(?:\b[A-Z][\d]+\b)"
var_pattern = re.compile(var_pattern_str)
fun_pattern_str = r"\w+"
fun_pattern = re.compile(fun_pattern_str)

#math_functions = [('+',['Int','Int']), ('-',['Int','Int']), ('%',['Int','Int']), ('/',['Int','Int'])]
math_functions = ['+', '-', '%', '/','*']
#math_relations = ['>']

##############################################################################################################################################################


def __find_var(pred):
	var_list =[ var for var in var_pattern.findall(pred) if var not in context_operator.get_predicates() ]
	return (var_list, pred)


def __is_var(pred):
	if var_pattern.search(pred):
		return True
	else:
		return False


def __find_var_sort(var_list, sort_consts):
	return [ sort for var in var_list for sort, consts in sort_consts.iteritems() if var in consts ]

##############################################################################################################################################################


def __compress(xlist, ylist):
	#print xlist, ylist
	mxlist, mylist = list(),list()
	for e in range(0,len(xlist)):
		if xlist[e] not in mxlist:
			mxlist.append(xlist[e])
			mylist.append(ylist[e])
	#print mxlist,mylist
	return (mxlist, mylist)



def __replace_var(var_str, t, var):
	for new_var in t:
		var_str = re.sub(var+r'\b',new_var, var_str, 1)
	return var_str


def __replace_body(old_list, new_list, body):
	old_list = [ r'\b'+elem+r'\b' for elem in old_list]
	return Util.repeat_do_function(lambda x,y: re.sub(y[0],y[1],x,1), zip(old_list, new_list),body)


def __recolour(mtuple, colors,var):
	n = 0
	mdict = dict()
	mlist = list()
	for e,elem in enumerate(mtuple):
		if elem in mdict.keys():
			mlist.append(var+str(mdict[elem]))
		else:
			mlist.append(var+str(colors[n]))
			mdict[elem] = colors[n]
			n+=1
	return tuple(mlist)


def __gen_template(num, var):
	var = var.replace('X','Y')
	templates =  list(itertools.product(range(0,num), repeat=num))
	templates = [ __recolour(elem,range(0,num),var) for elem in templates]
	return list(set(templates))


def __devars(pred):
	var_list, sort_list, body  = pred
	if var_list == list():
		return [pred]
	visited = list()
	var_template_list = ['#'.join(var_list)]

	for var in var_list:
		num = var_list.count(var)
		if var in visited or num ==1:
			continue
		else:
			visited.append(var)
			templates = __gen_template(num, var)
			var_template_list = [ __replace_var(var_str, t, var) for var_str in var_template_list for t in templates ]
	temp_pred_list = [(t.split('#'), sort_list, body) for t in var_template_list ]
	temp_pred_list = [( __compress(new_var_list, sort_list), __replace_body(var_list, new_var_list,body)) for (new_var_list, sort_list,body) in temp_pred_list ]
	
	return [ (var_list, sorts, body) for (var_list, sorts),body in temp_pred_list]

#print 'final!!!!',__devars((['X','X','X'], ['Int','Int','Int'], 'hello'))
##############################################################################################################################################################


def __gen_term(fun_sorts, sort_consts):
	fun_terms = list()
	for fluent_name, sorts in fun_sorts:
		consts = [sort_consts[sort] for sort in sorts]
		fun_terms += [ "%s(%s)"%(fluent_name, ','.join(list(elem))) for elem in list(itertools.product(*consts))]

	return fun_terms


def __gen_pred(pred_sorts, sort_consts):
	preds = list()
	for fluent_name, sorts in pred_sorts:
		consts = [sort_consts[sort] for sort in sorts]
		preds += [ "%s(%s)"%(fluent_name, ','.join(list(elem))) for elem in list(itertools.product(*consts))]
	return preds


def __gen_elem_from_template(consts, mvars, functions, relations, template):
	temp0 = [template]
	temp1 = [t.replace('@rel', rel) for t in temp0 for rel in relations ] if relations else temp0
	temp2 = [t.replace('@fun', fun) for t in temp1 for fun in functions ] if functions else temp1
	temp3 = [t.replace('@var', var) for t in temp2 for var in mvars ] if mvars else temp2
	temp4 = [t.replace('@const', const) for t in temp3 for const in consts ] if consts else temp3
	return list(set(temp4))


def __gen_term_from_template(sort, functions, sort_consts, template):
	consts = sort_consts[sort]
	consts = [elem for elem in consts if elem!='0']
	mvars = [ elem for elem in consts if __is_var(elem)]
	consts = [ elem for elem in consts if elem not in mvars]	
	return __gen_elem_from_template(consts, mvars, functions,None ,template)


def __gen_pred_from_template(sort, functions, relations, sort_consts, template):
	consts = sort_consts[sort]
	mvars = [ elem for elem in consts if __is_var(elem)]
	consts = [ elem for elem in consts if elem not in mvars]
	return __gen_elem_from_template(consts, mvars, functions, relations, template)



def __gen_equal_pred_from_template(fun_value_sort, terms, sort_consts, template):
	preds = list()
	for fun, sort in fun_value_sort:
		mterms = [elem for elem in terms if fun_pattern.search(elem).group(0)==fun]
		preds += __gen_pred_from_template(sort, mterms, ['='], sort_consts, template)
	return preds


def __gen_pred_from_file(filename):
	file = open(filename, 'r')
	preds = [eval(elem) for elem in file.readlines()]
	preds = preds + [ (var_list,sorts, '! '+body) for var_list,sorts, body in preds]
	return preds


##############################################################################################################################################################

def __gen_rel_pred_from_template(left_terms, right_terms, relations, template):
	temp0 = [template]
	temp1 = [t.replace('@rel', rel) for t in temp0 for rel in relations ] if relations else temp0
	#print '---1',temp1
	temp2 = [t.replace('@left', left) for t in temp1 for left in left_terms ] if left_terms else temp1
	#print '---2',temp2
	temp3 = [t.replace('@right', right) for t in temp2 for right in right_terms ] if right_terms else temp2
	#print '---3',temp3
	return list(set(temp3))


def __get_terms_from_sort(fun_value_sort, t_sort, terms):
	fun_list = [ fun for fun, sort in fun_value_sort if sort == t_sort]
	return [elem for elem in terms if fun_pattern.search(elem).group(0) in fun_list]


def __get_var_terms(terms):
	return [elem for elem in terms if __is_var(elem)]


def __gen_var_rel_pred(fun_value_sort, terms, relations, template, sort_list = None):
	preds = list()
	if sort_list is None:
		sort_list = list(set([sort for fun, sort in fun_value_sort]))

	for t_sort in sort_list:
		mterms = __get_terms_from_sort(fun_value_sort, t_sort, terms)
		var_terms = __get_var_terms(mterms)
		if var_terms!=list():
			preds += __gen_rel_pred_from_template(var_terms, var_terms, relations, template)
	return preds
##############################################################################################################################################################

zero_str = r"\b0\b"
zero_pattern = re.compile(zero_str)

def __del_zero(preds):
	return [ pred for pred in preds if zero_pattern.search(pred) is None ]

def __two_var_limited(preds):
	return [pred for pred in preds if len(var_pattern.findall(pred))<=2]


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



##############################################################################################################################################################

def genPreds(domain_file, constraints=dict()):

	fluent_sorts = context_operator.get_functions_sorts()
	sort_consts = context_operator.get_sort_symbols_dict()
	functions =  list(set(context_operator.get_fluents())- set(context_operator.get_predicates()))
	predicates = context_operator.get_predicates()


	fun_sorts = [(fluent, sorts[0:len(sorts)-1]) for fluent, sorts in fluent_sorts.iteritems() if fluent in functions]
	fun_value_sorts = [(fluent, sorts[len(sorts)-1]) for fluent, sorts in fluent_sorts.iteritems() if fluent in functions]
	pred_sorts = [(fluent, sorts[0:len(sorts)-1]) for fluent, sorts in fluent_sorts.iteritems() if fluent in predicates]
	sort_consts = {sort:consts+['X'+str(e)] for e,(sort,consts) in enumerate(sort_consts.iteritems())}


	math_terms = __gen_term_from_template( 'Int', math_functions, sort_consts, "@var @fun @const")
	fun_terms = __gen_term(fun_sorts, sort_consts)
	fun_terms = __fluentTerm_filter_via_constraints(fun_terms, constraints)

	#print fun_terms
	preds = __gen_pred(pred_sorts, sort_consts)

	math_var_predicates = __gen_pred_from_template('Int', [], ['>'], sort_consts, "@var @rel @const")
	math_var_predicates += __gen_pred_from_template('Int', math_terms, ['='], sort_consts, "@fun @rel @const")
	math_var_predicates += __gen_pred_from_template('Int', math_terms, ['=','>'], sort_consts, "@fun @rel @var")

	#math_fluent_sort = [(fluent,sort) for fluent, sort in fun_value_sorts if sort =='Int']
	const_funs = [ fun+"()" for fun in context_operator.get_zero_fluents() if fun in context_operator.get_fluents() if fun not in predicates]
	fluent_predicates = __gen_equal_pred_from_template(fun_value_sorts, fun_terms , sort_consts, "@fun @rel @const")
	#print '1',fluent_predicates
	fluent_predicates += __gen_equal_pred_from_template(fun_value_sorts, fun_terms , sort_consts, "@fun @rel @var")
	#print '2',fluent_predicates
	fluent_predicates += __gen_pred_from_template('Int', const_funs , ['>=','>'], sort_consts, "@fun @rel @var")
	#print '3',fluent_predicates

	fluent_predicates += __two_var_limited(__del_zero(__gen_var_rel_pred(fun_value_sorts, fun_terms, ['='], "@left @rel @right")))
	##print __two_var_limited(__del_zero(__gen_var_rel_pred(fun_value_sorts, fun_terms, ['='], "@left @rel @right")))
	#print '4',fluent_predicates
	fluent_predicates += __two_var_limited(__del_zero(__gen_var_rel_pred(fun_value_sorts, fun_terms, ['>=', '>'], "@left @rel @right", ['Int'])))
	##print  __gen_var_rel_pred(fun_value_sorts, fun_terms, ['>=', '>'], "@left @rel @right", ['Int'])
	#print '5',fluent_predicates
	
	#math_fluent_predicates = gen_pred_from_templa*te()
	math_var_predicates = [ __find_var(pred) for pred in math_var_predicates] 
	fluent_predicates = [ __find_var(pred) for pred in fluent_predicates+preds]
	#print '6',fluent_predicates
	math_var_predicates = [  (var_list,__find_var_sort(var_list, sort_consts), pred) for var_list,pred in math_var_predicates]
	fluent_predicates = [ (var_list,__find_var_sort(var_list, sort_consts), pred) for var_list,pred in fluent_predicates]
	#print '7',fluent_predicates
	#print len(fluent_predicates)
	#exit(0)

	math_var_predicates = sum([ __devars(pred) for pred in math_var_predicates],[])
	fluent_predicates = sum([ __devars(pred) for pred in fluent_predicates],[])

	math_var_predicates += [(var_list,sorts, "! "+body) for (var_list,sorts, body) in math_var_predicates ]
	fluent_predicates += [(var_list,sorts, "! "+body) for (var_list,sorts, body) in fluent_predicates ]

	#math_var_predicates = __gen_pred_from_file(context_operator.get_template_order())
	#fluent_predicates = delete_unknown_predicates(fluent_predicates)

	math_preds = util_pred.reduce_num_math_preds('new_chomp2N', math_var_predicates)
	fluent_preds = util_pred.reduce_num_fluent_preds(fluent_predicates)

	return math_preds, fluent_preds


'''
from basic import my_parser
my_parser.parser("./game_domains/takeaway.sc")

print genPreds()
'''

