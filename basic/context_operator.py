#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-25 21:54:20
# @Author  : Kailun Luo (luokl3@mail2.sysu.edu.cn)
# @Link    : https://sdcs.sysu.edu.cn
# @Version : $Id$
   
import os
import global_context
import Util
#import sort_system
#import Util
#import re


def get_new_var():
	global_context.VAR_INDEX += 1
	return 'K'+ str(global_context.VAR_INDEX)



##########################################################################################




def get_symbol_to_sort_list():
	return global_context.SYMBOL_TO_SORT_LIST


def get_symbols_equal_list():
	return global_context.SYMBOLS_EQUAL_LIST


def add_symbol_to_sort_list(mlist):
	global_context.SYMBOL_TO_SORT_LIST += mlist


def add_symbols_equal_list(elem): 
	global_context.SYMBOLS_EQUAL_LIST.append(elem)


def set_symbol_to_sort_list(mlist):
	global_context.SYMBOL_TO_SORT_LIST = mlist


def set_symbols_equal_list(mlist): 
	global_context.SYMBOLS_EQUAL_LIST = mlist


def set_symbol_sorts_dict(mdict):
	global_context.SYMBOL_SORTS_DICT = mdict


def get_symbol_sorts_dict():
	return global_context.SYMBOL_SORTS_DICT


def set_sort_symbols_dict(mdict):
	global_context.SORT_SYMBOLS_DICT = mdict


def get_sort_symbols_dict():
	return global_context.SORT_SYMBOLS_DICT


def get_sorts():
	return global_context.SORT


def declare_sort(key,values):
	if key != "":
		global_context.SORT[key] = values
	else:
		global_context.SORT[global_context.SORT_NAME+str(global_context.SORT_INDEX)] = values
		global_context.SORT_INDEX+=1


def set_function_sorts(fun, sorts):
	global_context.FLUENT_SORT_DICT[fun] = sorts

def set_functions_sorts(m_dict):
	global_context.FLUENT_SORT_DICT = m_dict

def get_functions_sorts():
	return global_context.FLUENT_SORT_DICT


def add_predicate_sorts(p_dict):
	global_context.PREDICATE_SORT_DICT.update(p_dict)

def get_predicate_sorts():
	return global_context.PREDICATE_SORT_DICT


##########################################################################################


def get_axioms():
	return global_context.AXIOMS


def set_axiom(axiom_name, feature, var_list, formula):
	if var_list!=[]:
		var_list = [r'\b'+mvar+r'\b' for mvar in var_list]
		global_context.AXIOMS[axiom_name][feature] = lambda x: Util.repeat_do_function(Util.sub_lambda_exp, zip(var_list,x),formula)
	else:
		global_context.AXIOMS[axiom_name][feature] = formula
	# for stota
	#global_context.AXIOMS_STR[axiom_name][feature] = (axiom_name, feature, var_list, formula)


def find_axiom_with_feature(axiom_name, feature):
	axioms_features = global_context.AXIOMS[axiom_name].keys()
	for feature_pattern in axioms_features:
		match = feature_pattern.match(feature)
		if match:
			return global_context.AXIOMS[axiom_name][feature_pattern], match.groups()

	error_msg = "#ERROR:find_axiom_with_feature: can not find %s with %s in %s" %(feature, axiom_name, global_context.FEATURE_LIST)
	raise Exception(error_msg)



##########################################################################################


def add_zero_fluent(fluent_name):
	global_context.ZERO_FLUENT_SET.add(fluent_name)

def set_zero_fluent(fluents):
	global_context.ZERO_FLUENT_SET = fluents

def get_zero_fluents():
	return global_context.ZERO_FLUENT_SET



def add_actions(actions):
	global_context.ACTION_LIST.extend(actions)
	global_context.ACTION_LIST = list(set(global_context.ACTION_LIST))

def add_fluents(fluents):
	global_context.FLUENT_LIST.extend(fluents)
	global_context.FLUENT_LIST = list(set(global_context.FLUENT_LIST))

def get_actions():
	return global_context.ACTION_LIST

def get_fluents():
	return global_context.FLUENT_LIST



def add_feature(feature):
	global_context.FEATURE_LIST.append(feature)

def get_feature():
	return global_context.FEATURE_LIST



def add_predicates(p_list):
	global_context.PREDICATES.extend(p_list)

def get_predicates():
	return global_context.PREDICATES



def set_rigid_functions(f_list):
	global_context.RIGID_FUNCTION = f_list

def get_rigid_functions():
	return global_context.RIGID_FUNCTION

##########################################################################################



def add_nregx_function_patterns(pattern_list):
	global_context.NREGX_FUNCTION_PATTERNS.extend(pattern_list)

def get_nregx_function_patterns():
	return global_context.NREGX_FUNCTION_PATTERNS


def get_function_regress_lambda():
	return global_context.FUNCTION_LAMBDA_REGRESS 

def set_function_regress_lambda(lambda_exp):
	global_context.FUNCTION_LAMBDA_REGRESS = lambda_exp



def get_predicate_regress_lambda():
	return global_context.PREDICATE_LAMBDA_REGRESS 

def set_predicate_regress_lambda(lambda_exp):
	global_context.PREDICATE_LAMBDA_REGRESS = lambda_exp


##########################################################################################


def get_z3_header():
	return global_context.Z3_HEADER

def set_z3_header(z3_head_str):
	global_context.Z3_HEADER = z3_head_str



##########################################################################################


def get_template_order():
	return global_context.TEMPLATE

def set_template_order(order):
	global_context.TEMPLATE = order


##########################################################################################
# for regression

def use_local_dict():
	global_context.LOCAL_DICT = dict()

def update_local_dict(m_dict):
	global_context.LOCAL_DICT.update(m_dict)

def get_local_dict():
	return global_context.LOCAL_DICT

def get_global_action():
	return global_context.ACTION#'take(1,a,f(x)+3)'

def set_global_action(action):
	global_context.ACTION = action

##########################################################################################
# from transformation to SMT format

def get_replace_list():
	return global_context.RPLIST

def clear_replace_list():
	global_context.RPLIST = list()
	global_context.RP_INDEX =0


def add_replace_list(elem):
	repl = "RP%s"%str(global_context.RP_INDEX)
	global_context.RP_INDEX+=1
	global_context.RPLIST.append((r"\b%s\b"%repl, elem))
	return repl

##########################################################################################	


def get_state_constraints():
	return global_context.DOMAIN_SC

def set_state_constraints(sc):
	global_context.DOMAIN_SC = sc

##########################################################################################

def get_current_model():
	return global_context.MODEL

def set_current_model(model):
	global_context.MODEL = model

##########################################################################################

'''
#get_symbol_to_sort_list()
set_symbols_equal_list("1")
print get_symbols_equal_list()

set_symbol_to_sort_list(['1'])
print get_symbol_to_sort_list()
'''
