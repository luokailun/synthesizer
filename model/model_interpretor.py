#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-02 21:30:12
# @Author  : Kailun Luo (luokl3@mail2.sysu.edu.cn)
# @Link    : https://sdcs.sysu.edu.cn
# @Version : $Id$

import os

import util_z3_model
from basic import context_operator
#from basic import util_z3
import itertools
import copy
import re
import random
'''
fun_list = []
preds_list = ['turn']
const_list = ['p2','p1','numStone']
'''

from basic import mylog as logging
logger = logging.getLogger(__name__)

'''
## ('0','0') -> (0,0)






def __parse_constraints(constraints, const_dict):
	constraint_dict = dict()
	for fun in constraints.keys():
		temp_list = list()
		for constraint in  constraints[fun]:
			if constraint.find(':')!=-1:
				for const, value in const_dict.iteritems():
					constraint = constraint.replace(const,str(value))
				mranges = constraint.split(':')
				#print mranges
				temp_list.append([str(e) for e in range(int(mranges[0]), int(mranges[1])+1)])
				#print temp_list
			else:
				temp_list.append(constraint.split(','))
		constraint_dict[fun] = list(itertools.product(*temp_list))
	return constraint_dict




def has_model(formula):
	#print '-----has_modelhas_model-----------'
	return not interpret_result(util_z3.check_sat(formula))
	

def get_sat_models(formula):
	return interpret(util_z3.check_sat(formula))[0]

'''



##############################################################################################################################



def ____gen_random_value(fun, fluent_sorts):
	fun_sort = fluent_sorts[fun][-1]
	value_list = context_operator.get_sort_symbols_dict()[fun_sort]
	ranNum = random.randint(0,len(value_list)-1)
	return value_list[ranNum]


def __get_default_fluents(fluents, fluent_sorts, universe, constraints=None):
	elem_list = __get_model_elements(fluents, constraints, universe)
	elem_value_list = [ (fun, paras, ____gen_random_value(fun, fluent_sorts)) for fun, paras in elem_list]
	return {"%s(%s)"%(fun,','.join(paras)) : value for fun, paras, value in elem_value_list}


def ____int_detect(mtuple):
	"""
		change '1' to 1
	"""
	return tuple(int(elem) if elem.isdigit() else elem for elem in mtuple)


def __name_relpace(paras, const_dict):
	"""
		change domain constants to SMT constants
	"""
	return ____int_detect(tuple([const_dict[para] if para in const_dict.keys() else para for para in paras ]))



def __trans_true_false(elems):
	for e,(fun, mtuple, value) in enumerate(elems):
		if value =="false":
			elems[e] = (fun, mtuple, 'False')
		elif value =="true":
			elems[e] =(fun, mtuple, 'True')
	return elems



def __get_model_elements(fluents, fluent_constraints=None, add_universe=None):
	fluent_sorts = context_operator.get_functions_sorts()
	fluent_constraints = {} if fluent_constraints is None else fluent_constraints
	#fluents = context_operator.get_fluents()
	
	if add_universe:
		sort_consts = add_universe
	else:
		sort_consts = context_operator.get_universe()
	#sort_consts = dict(context_operator.get_sort_symbols_dict())
	#if add_universe is not None:

	fluents_sorts = [(fluent, sorts[0:len(sorts)-1]) for fluent, sorts in fluent_sorts.iteritems() if fluent in fluents]

	#print fluent_constraints
	elem_list = list()
	for fluent_name, sorts in fluents_sorts:
		consts = [sort_consts[sort] if "%s@%s"%(fluent_name, e+1) not in fluent_constraints else fluent_constraints["%s@%s"%(fluent_name, e+1)] for e, sort in enumerate(sorts)]
		elem_list += [ (fluent_name, elem) for elem in list(itertools.product(*consts))]
	return elem_list


def ____fluent_in_model(fluent, lambda_funs, const_dict):
	return True if fluent in lambda_funs or fluent in const_dict.keys() else False
 

def __get_model_fluents(lambda_funs, const_dict, fluents):
	model_funs = [ fun.split('=')[0].strip() for fun in lambda_funs]
	return [fun for fun in fluents if ____fluent_in_model(fun, model_funs, const_dict)]


'''
number = r"\b\d+\b"
number_pattern = re.compile(number)

number_not_neg = r"[^-](\d+)\b"
number_not_neg_pattern  = re.compile(number_not_neg)


def __generate_num_universe(results):
	num1 = set(number_pattern.findall(''.join(results)))
	num2 = set(number_not_neg_pattern.findall(''.join(results)))
	nlist = list(num1&num2)
	return [ str(i) for i in range(int(min(nlist)),int(max(nlist))+1)]
'''


##############################################################################################################################

num_pattern = re.compile(r'\b\d+\b')


def get_default_value(elem_list, scope, const_dict, anti_const_dict):
	"""
		get default value for fluents who have parameters of Int sort

		@param elem_list 		elements like ('Ch', ('1', '1'))
		@param scope 			the scope for executing lambda expression
		@param const_dict 		from domain constants to SMT constants
		@param anti_const_dict 	from SMT constants to domain constants
	"""
	default_num = '9999'
	elem_list = [ (fun, num_pattern.sub(default_num, ','.join(paras))) for fun, paras in elem_list]
	elem_list = list(set([(fun, para_str) for fun, para_str in elem_list if para_str.find(default_num)!=-1 ]))
	elem_list = [(fun, tuple(para_str.split(','))) for fun, para_str in elem_list]

	elem_value_list = [ (fun, paras, apply(eval(fun,scope), __name_relpace(paras, const_dict))) for fun, paras in elem_list]
	elem_value_list = [ (fun, paras, anti_const_dict[value]) if value in anti_const_dict.keys() else (fun, paras, value) for (fun, paras, value) in elem_value_list  ]

	default_value = {("%s\(%s\)"%(fun,','.join(paras))).replace(default_num, '\d+') : str(value) for fun, paras, value in elem_value_list}
	
	return default_value





##############################################################################################################################


def interpret_model(results, max_value=99999):
	#print results
	#context_operator.set_counterexample_result(results)
	lambda_funs = util_z3_model.get_fun(results)
	#print lambda_funs
	# a dict maps constants to SMT constants
	const_dict = util_z3_model.get_const(results)
	#print const_dict
	#print const_dict
	#print '----------',context_operator.get_sort_symbols_dict()

	universe = copy.deepcopy(context_operator.get_sort_symbols_dict())
	min_num = min([int(e) for e in universe['Int']])
	max_num = max([int(e) for e in universe['Int']])
	universe['Int'] = [str(e) for e in range(min_num,max_num+1)]
	#universe['Int'] =  list(set(universe['Int'] +__generate_num_universe(str(lambda_funs)+str(const_dict))))
	#print universe['Int']
	# get fluent names from the interpretation
	fluents = __get_model_fluents(lambda_funs, const_dict, context_operator.get_fluents()) 
	#Predicates is also included because they can be seen as two-value (true/false) functions.

	scope = dict()
	for fun in lambda_funs:
		exec(fun,scope)

	fluent_sorts = context_operator.get_functions_sorts()

	#constraints = __parse_constraints(domain_constraints, const_dict)??
	flag = True
	value_constraints = list()
	while flag is True and value_constraints == list():
		flag = False
		#elem_list = __get_model_elements(fluents, context_operator.get_fluent_constraint())
		#generate parameters for fluents
		elem_list = __get_model_elements(fluents, add_universe=universe)
		const_symbols = sum(universe.values(),[])
		# set non-constant fluent, lile xlen, numStone
		elem_value_list = [ (fun, tuple(), value) for fun, value in const_dict.items() if fun in fluents]
		# transform SMT true/false to 'True'/'False'
		elem_value_list = __trans_true_false(elem_value_list)
		elem_value_list += [ (fun, paras, apply(eval(fun,scope), __name_relpace(paras, const_dict))) for fun, paras in elem_list if fun not in const_dict.keys()]

		# transform SMT constants to constant symbols
		anti_const_dict = { value:key for key,value in const_dict.items() if key not in fluents and key in const_symbols and not isinstance(value,int) and not value.isdigit()}
		elem_value_list = [ (fun, paras, anti_const_dict[value]) if value in anti_const_dict.keys() else (fun, paras, value) for (fun, paras, value) in elem_value_list  ]
		#########################
		for e, (fun, paras, value) in enumerate(elem_value_list):
			fun_sort = fluent_sorts[fun][-1]
			## ???????
			if str(value) not in universe[fun_sort]:
				flag = True
				if int(value)<0:
					logger.info('ERROR: model has negative value \n %s'%results)
					exit(0)
				if fun_sort == 'Int' and int(value)>max_value:
					#print 'Hello'
					value_constraints.append("%s(%s)"%(fun,','.join(paras)))
				elif fun_sort == 'Int':
					#print 'C'
					min_num = min([int(e) for e in universe['Int']])
					universe[fun_sort] = [str(e) for e in range(min_num,value+1)]
				else:
					#print 'D'
					universe[fun_sort].append(str(value))


	if value_constraints!=list():
		return False, value_constraints
	else:
		model = {"%s(%s)"%(fun,','.join(paras)) : str(value) for fun, paras, value in elem_value_list}

		lack_fluents =  [fun for fun in context_operator.get_fluents() if fun not in fluents ]
		complete_part = __get_default_fluents(lack_fluents, fluent_sorts, universe)
		model.update(complete_part)

		"""
			get default value for fluents who have parameters of Int sort
		"""
		default_value  = get_default_value(elem_list, scope, const_dict, anti_const_dict)

		""" 
		"""
		return True, (universe, model, default_value)


##############################################################################################################################


def interpret_result(result, M_MAX_VALUE=99999):
	#print result
	#print
	if result[0] == 'sat\n':
		return False
	elif result[0] == 'unsat\n':
		return True
	elif result[0] == 'unknown\n':
		return 'UNKNOWN'
	else:
		logger.error(result)
		print result
		exit(0)






	
