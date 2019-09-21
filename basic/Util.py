 #!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-20 16:41:01
# @Author  : Kailun Luo (luokl3@mail2.sysu.edu.cn)
# @Link    : https://sdcs.sysu.edu.cn
# @Version : $Id$


import os
import re
import base64
#import context_operator
import json
import itertools

import sys
sys.path.append("..")
#import util_constraint





'''
s = "exists(K11:Int)[numStone()=K11+3]"
universe = {'Int': ['1', '0', '3', '2'], '_S1': [], '_S2': ['p2', 'p1'], 'Bool': ['True', 'False']}
print grounding_formula(s)
exit(0)

'''


from basic import context_operator
from basic import pattern



sub_lambda_exp = lambda x,y: re.sub(y[0],y[1],x)
replace_lambda_exp = lambda x,y: x.replace(y[0],y[1])
encode_pair_para = (['(',')',','],['[',']','#'])

# repeat to do function f with a list of arguments, initial argument is mbase
def repeat_do_function(f,args_list,mbase):
	return reduce(lambda x,y: f(x,y),args_list,mbase)



def endecode_string(my_str, old_symbols, new_symbols):
	return repeat_do_function(replace_lambda_exp, zip(old_symbols, new_symbols), my_str)


def __mrepl_encode(matched):
	match_str=matched.group()
	encoded_str=endecode_string(match_str, encode_pair_para[0], encode_pair_para[1])
	return encoded_str


def repeat_replace_inner_with_pattern(repeat_pattern, mrepl, my_str):
	while(True):
		encoded_str=repeat_pattern.sub(mrepl, my_str)
		my_str = encoded_str if my_str!=encoded_str else None
		if my_str is None:
			break	
	return encoded_str


def get_paras_from_str(para_str):
	#print para_str
	encoded_str = repeat_replace_inner_with_pattern(pattern.inner_parenth, __mrepl_encode, para_str)
	encoded_para_list = encoded_str.split(',')
	return [endecode_string(my_str, encode_pair_para[1], encode_pair_para[0]) for my_str in encoded_para_list]
	




def parse_relation(relation_str):
	#print relation_str
	match = pattern.fluent.match(relation_str)
	if match:
		if match.group(3):
			return match.group(1), match.group(2),match.group(3)
		else:
			return match.group(4), match.group(5),""
	else:
		return None, None, None


def parse_function(function_str):
	match = pattern.action.match(function_str)
	if match:
		return match.group(1), match.group(2),""
	else:
		return None, None, None

def parse_relation_or_function(mstr):
	a,b,c = parse_relation(mstr)
	if a==None:
		return parse_function(mstr)
	else:
		return a,b,c


def isVar(mstr):
	match = pattern.var.match(mstr)
	return True if match else False



encode_pair_forall = (['[',']'],['{','}'])
rename_pattern_str = r"(?:forall|exists)\((?P<var>[\w\:\s\d,_]+?)\)\[(?P<body>[^\[\]]+)\]"
rename_pattern = re.compile(rename_pattern_str)


def __mrepl_rename(match):
	#print "hello",match.group(0)
	old_var_list = match.group('var').split(',')
	old_var_list = [r'\b' + var + r'\b' for var in old_var_list]
	new_var_list = [context_operator.get_new_var() for e in range(0, len(old_var_list))]
	#print zip(old_var_list,new_var_list)
	rename_str = repeat_do_function(sub_lambda_exp, zip(old_var_list,new_var_list), match.group(0))
	#print rename_str
	encoded_rename_str = endecode_string(rename_str,encode_pair_forall[0], encode_pair_forall[1])
	return encoded_rename_str


def rename_forall(formula):
	#print rename_pattern.findall(s)
	encoded_formula = repeat_replace_inner_with_pattern(rename_pattern, __mrepl_rename, formula)
	return endecode_string(encoded_formula, encode_pair_forall[1], encode_pair_forall[0])


encode_pair_unmatch = (['(',')'],['{','}'])


def __mrepl_unmatch(matched):
	match_str=matched.group()
	encoded_str=endecode_string(match_str, encode_pair_unmatch[0], encode_pair_unmatch[1])
	return encoded_str


def eliminate_unmatched(m_str):
	m_str = repeat_replace_inner_with_pattern(pattern.inner_parenth, __mrepl_unmatch, m_str)
	m_str = m_str.replace('(',"").replace(')',"").replace('[',"").replace(']',"")
	return endecode_string(m_str, encode_pair_unmatch[1], encode_pair_unmatch[0])




def generate_function_feature(function_str):
	function_name, function_args_str, function_value= parse_relation_or_function(function_str)
	para_list = get_paras_from_str(function_args_str)
	function_feature = function_name + '_' + '_'.join(para_list)+'_'+function_value
	function_feature = re.sub(r'\s+', '', function_feature)
	return function_feature



