#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-13 16:36:12
# @Author  : Kailun Luo (luokl3@mail2.sysu.edu.cn)
# @Link    : https://sdcs.sysu.edu.cn
# @Version : $Id$

import os

from basic import Util
from basic import context_operator
import re
#import util_transiform


most_inner_pattern = re.compile(r'\([^\(\)]+\)')


math_sym_first = re.compile(r'(?:(\w+)\s*(\*)\s*(\w+))|(?:(\w+)\s*(\/)\s*(\w+))|(?:(\w+)\s*(mod)\s*(\w+))')
math_sym_second = re.compile(r'(?:(\w+)\s*(\+)\s*(\w+))|(?:(\w+)\s*(\-)\s*(\w+))')
math_pred = re.compile(r'(?:(\w+)\s*(<=)\s*(\w+))|(?:(\w+)\s*(>=)\s*(\w+))|(?:(\w+)\s*(<)\s*(\w+))|(?:(\w+)\s*(>)\s*(\w+))|(?:(\w+)\s*(=)\s*(\w+))')
#logic_conn1 = re.compile(r'(not)\s*(\w+)(?!not\s*)')
logic_conn1 = re.compile(r'(not)\s*(?!not)(\w+)')
logic_conn2 = re.compile(r'(\w+)\s*(and)\s*(\w+)')
logic_conn3 = re.compile(r'(\w+)\s*(or)\s*(\w+)')
logic_conn4 = re.compile(r'(\w+)\s*(=>)\s*(\w+)')
logic_conn5 = re.compile(r'(\w+)\s*(<=>)\s*(\w+)')

quantifier_pattern = re.compile(r"(?:(forall|exists))\s*\(([\w:,_]+)\)\[([^\(\)\[\]]+)\]")
##
##
# repeat most inner (exp):  
#	handle (exp)  
#		 exp:   basic expression    
#					math:   (1) * / mod  (2) + -         
#				    math predicate:    <= >=  <  >  =
# 		 		    logical connector ! &  |  => 
#
#	handle fluent(L1,L1,L1)   -> (fluent L1 L1 L1)
#	
#
#



def __mrepl_math(matched):
	match_list = [ elem for elem in matched.groups() if elem]
	##print 'aaaa',match_list
	#s= "
	###print s
	return context_operator.add_replace_list("(%s %s %s)"%(match_list[1], match_list[0], match_list[2]))


def __mrepl_logic_not(matched):
	match_list = [ elem for elem in matched.groups() if elem]
	##print 'bbbb',match_list
	return context_operator.add_replace_list("(%s %s)"%(match_list[0], match_list[1]))


def __mrepl_no_inner_formula(matched):
	if matched.group().find(':')!=-1:
		return matched.group()
	formula = matched.group().lstrip('(').rstrip(')')
	#print "---before innerformula", formula
	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = math_sym_first.sub(__mrepl_math, formula, 1)
	#print '1111',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = math_sym_second.sub(__mrepl_math, formula, 1)
	#print '2222',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = math_pred.sub(__mrepl_math, formula, 1)
	#print '2222',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = logic_conn1.sub(__mrepl_logic_not, formula)
	#print '3333',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = logic_conn2.sub(__mrepl_math, formula, 1)
	#print '4444',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = logic_conn3.sub(__mrepl_math, formula, 1)
	#print '5555',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = logic_conn4.sub(__mrepl_math, formula, 1)
	#print '6666',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = logic_conn5.sub(__mrepl_math, formula, 1)
	#print '7777',formula
	#print "----after,innerformula",formula
	return formula




def __mrepl_fluent(matched):
	match_list = [ elem for elem in matched.groups() if elem]
	##print match_list
	if len(match_list)==1 or match_list[1]=="":
		return match_list[0]
	else:
		paras = match_list[1].split(',')
		#paras = [ "(%s %s)"%(para.split(':')[0], para.split(':')[1]) for para in paras]
		fluent_str = "(%s %s)"%(match_list[0], ' '.join(paras))    #[ "(%s %s)"%(para.split(':')[0], para.split(':')[1]) for para in paras]
		return context_operator.add_replace_list(fluent_str)



def __mrepl_quntifier(matched):
	paras = matched.group(2).split(',')
	var_str = " ".join([ "(%s %s)"%(para.split(':')[0], para.split(':')[1]) for para in paras])
	formula = re.sub(r'.*', __mrepl_no_inner_formula, matched.group(3).strip())
	return context_operator.add_replace_list("(%s (%s) %s)"%(matched.group(1), var_str, formula))


def __logicSym_to_smtSym(formula):
	formula = formula.replace('!',' not ').replace('%',' mod ').replace('&',' and ').replace('|', ' or ')
	return Util.repeat_do_function(Util.sub_lambda_exp, [(r'\bFalse\b','false'), (r'\bTrue\b','true')] ,formula)


def get_smt_body(formula):
	#print '-----need to tans formula is:', formula
	formula = __logicSym_to_smtSym(formula)
	fluents = context_operator.get_fluents()
	fluent_sub = '|'.join([r"(?:(%s)\(([\w,\s]*)\))"%fun for fun in fluents])
	#print fluents
	fluent_sub_pattern = re.compile(fluent_sub)

	temp_formula = ""
	while temp_formula!= formula:
		temp_formula = formula
		#formula = fluent_sub_pattern.sub(__mrepl_fluent, formula)
		formula = Util.repeat_replace_inner_with_pattern(fluent_sub_pattern, __mrepl_fluent, formula)
		#print "repl_fluent---",formula
		#formula = Util.repeat_replace_inner_with_pattern(most_inner_pattern, __mrepl_no_inner_formula, formula)
		formula = most_inner_pattern.sub(__mrepl_no_inner_formula, formula)
		#print "inner_pattern---",formula
		formula = Util.repeat_replace_inner_with_pattern(quantifier_pattern, __mrepl_quntifier, formula)
		#formula = quantifier_pattern.sub(__mrepl_quntifier, formula)
	formula = re.sub(r'.*', __mrepl_no_inner_formula, formula)

	repl_list = context_operator.get_replace_list()
	repl_list.reverse()
	#print repl_list
	formula = Util.repeat_do_function(Util.sub_lambda_exp, repl_list, formula)
	#print formula
	context_operator.clear_replace_list()
	return formula







