#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-28 12:39:09
# @Author  : Kailun Luo (luokl3@mail2.sysu.edu.cn)
# @Link    : https://sdcs.sysu.edu.cn
# @Version : $Id$



import os
from basic import context_operator
from parser import sort_system
#import util_transiform
import util_trans_smt

from basic import mylog as logging
logger = logging.getLogger(__name__)



def __generate_head():
	head_str =""
	sorts = list(context_operator.get_sorts().keys())
	#print ["(declare-sort "+sort for sort in sorts]
	head_str+= "&".join(["(declare-sort "+ sort + ")" for sort in sorts if sort !="Int"])

	functions = context_operator.get_fluents()
	functions_sorts = [sort_system.get_function_sort(fun) for fun in functions]
	#print functions_sorts
	functions_sorts = [ "("+" ".join(sorts[0:len(sorts)-1])+") "+ sorts[len(sorts)-1]  for sorts in functions_sorts]
	sorts_consts = context_operator.get_sort_symbols_dict()
	#print functions, functions_sorts
	#print ["(declare-sort "+ sort + ")" for sort in sorts]
	head_str+= "&".join(["(declare-fun "+ fun + functions_sorts[e]+ ")" for e, fun in enumerate(functions)])
	head_str+= "&".join(["(declare-const "+ const +" "+sort+ ")" for sort in sorts_consts.keys() for const in sorts_consts[sort] if sort!="Int"] )
	
	return head_str


def check_sat(formula):
	return imply(formula, 'false')


#(assert (not (= (row 1) 404))) (assert (not (= (row 2) 404)))
def imply(formula1, formula2, add_head=""):
	logger.debug("#checking imply:\n f1:%s\n f2:%s"%(formula1, formula2))
	formula = "( %s ) => ( %s )" % (formula1 , formula2)
	sc_formula = context_operator.get_state_constraints()

	with open("./z3_input/smt_input","write") as input_file:
		#print "-------",encoded_formula
		#smt_body = util_transiform.decode_formula(util_prolog.get_smt_format_body(encoded_formula))
		#formula = "( turn(p1) and !turn(p2)) and len(1)" 
		#print formula
		smt_body = util_trans_smt.get_smt_body(formula)
		smt_head = "\n".join(__generate_head().split('&')) +  add_head+ sc_formula
		smt_str = '\n%s (assert (not %s ))\n(check-sat)\n(get-model)' %(smt_head, smt_body)
		#logger.debug("smt_format:\n %s"%smt_str)
		#print smt_str
		#(assert (> len 0) )
		input_file.writelines(smt_str)

		cmd = "z3 -smt2 ./z3_input/smt_input"
		input_file.close()
		return os.popen(cmd).readlines()






