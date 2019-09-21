#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-25 16:26:29
# @Author  : Kailun Luo (luokl3@mail2.sysu.edu.cn)
# @Link    : https://sdcs.sysu.edu.cn
# @Version : $Id$

import os
from basic import Util
from basic import context_operator
from basic import pattern
import re
from operator import itemgetter #itemgetter用来去dict中的key，省去了使用lambda函数
from itertools import groupby
import copy
#import mylog as logging
#logger = logging.getLogger(__name__)

'''
unknown sort : sort_f@1, sort_f@2, sort_A@1, sort_A@2     
know sort :

sort equal: [sort_f@1,sort_f@2,sort_A@1]

SSA:
f(X,Y) = Z  ->   sort_f@1: [X] , sort_f@2: [Y]  sort_f:[Z]
A(K,M) ->   sort_A@1: [K], sort_A@2: [M]


formula  or formula and formula 
Expression: X+/*/|/|Y = K ->  X, Y, K is some sort        #[X,Y,K] -> [sort_f@1,sort_f@2,sort_A@1,INT]    

Predicate:    f(m,V)                                       [m,V] -> [sort_f@1: m] [sort_f@2: V]  
			  f(g(x,y),K+1)								   g(x,y) -> g[x, y] -> [sort_g@1:x] [sort_g@2:y]
			  		                                       f(g,K+1) -> [sort_f@1] 
function:                               


Poss:
A(m,M) ->   sort_A@1: [m], sort_A@2: [M]

'''


#math_expression = "[\+\-\*\|\>\<\%]"


def isMath(expression):
	return True if re.search(r'[\+\-\*\|\>\<]',expression) else False

def isConst(expression):
	return True if type(expression)==type("") and (re.match(pattern.str_const_name, expression.strip()) or expression.isdigit()) else False


def __get_sort_from_function(function):
	#print '!!!',function
	fun_name, fun_paras, fun_value = Util.parse_relation_or_function(function)
	para_list = Util.get_paras_from_str(fun_paras)

	#symbol_sort = [(symbol, (fun_name, pos+1)) for pos, symbol in enumerate(para_list) if not isMath(symbol)]
	#symbol_INT = sum([ __get_INTsymbol_from_expression(symbol) for pos, symbol in enumerate(para_list) if isMath(symbol)],[])
	symbol_sort = list()
	equal_symbols = list()
	for pos, symbol in enumerate(para_list):
		if not isMath(symbol):
			symbol_sort += [(symbol.strip(), (fun_name, pos+1))]
		else:
			symbol_INT, words = __get_INTsymbol_from_expression(symbol.strip())
			symbol_sort+=symbol_INT
			symbol_sort+=[(symbol.strip(), (fun_name, pos+1)) for symbol in words]
	return symbol_sort


def __get_INTsymbol_from_expression(expression):
	all_word = re.findall(r'\w+',expression)
	return [(word,'Int') for word in all_word], all_word


def __get_equalsymbol(equal_expresson):
	return [symbol.strip() for symbol in equal_expresson.split('=')]


def __get_sort_from_basic_expression(basic_exp):
	basic_exp = basic_exp.replace('!','')
	if re.search(r'[\+\-\*\|\>\<\%]',basic_exp):
		return __get_INTsymbol_from_expression(basic_exp)
	elif basic_exp.find("=")!=-1:
		return [], __get_equalsymbol(basic_exp)
	else:
		return [],[]


inner_function_pattern = re.compile(r"\s*(?P<fun>\w+)\([^\(\)]+\)")

def __get_sort_from_qf_formula(qf_formula):
	expressions = re.split(r'\&|\||\=\>', qf_formula)
	expressions = [Util.eliminate_unmatched(expression) for expression in expressions]
	#logger.debug("get sort from expressions: %s"%expressions)
	#print("get sort from expressions: %s"%expressions)
	for expression in expressions:
		#logger.debug("get sort from expression: %s"%expression)
		#print("get sort from expression: %s"%expression)
		while True:
			expression = Util.repeat_replace_inner_with_pattern(inner_function_pattern, __mrepl_getsort_exp, expression)
			new_expression = re.sub(r"\((?P<exp>[^\(\)]*)\)",r"\g<exp>",expression)
			if new_expression == expression:
				break
			else:
				expression = new_expression
		sort_symbol_list, symbol_group = __get_sort_from_basic_expression(expression)
		#logger.debug("get sort from basic expression: %s result: %s %s"%(expression,sort_symbol_list,symbol_group))
		context_operator.add_symbol_to_sort_list(sort_symbol_list)
		context_operator.add_symbols_equal_list(symbol_group)


def get_sort_from_symbols(symbol_list):
	pass


s="forall(X,Y)[(X=1 or X=2 or X=3) and (Y=1 or Y=2 or f(Y)=3) and m(g(X),(X-1)) > 1+X => num(X)=num(Y)] and turn(P) = true and color(blue)"



def __mrepl_getsort_exp(matched):
	#fun_pos_symbols, equal_sorts = __get_sort_from_function(matched.group())
	fun_pos_symbols = __get_sort_from_function(matched.group())
	#logger.debug("get sort from function: %s result: %s"%(matched.group(),fun_pos_symbols))
	##print "---hello-------",fun_pos_symbols
	context_operator.add_symbol_to_sort_list(fun_pos_symbols)
	#context_operator fun_pos_symbols
	#get_symbol_to_sort_listequal_symbols_list.append(equal_symbols)
	return matched.group('fun')+"()"


def __mrepl_getsort_fol(matched):
	formula_body = matched.group('body')
	#logger.debug("get sort from qf formula:%s\n"%formula_body)
	#print "get sort from qf formula:%s\n"%formula_body
	__get_sort_from_qf_formula(formula_body)
	return ""

		   
def generate_sort_from_formula(formula):
	#logger.debug("get sort from formula:%s\n"%formula)
	#print "get sort from formula:%s\n"%formula
	formula = Util.repeat_replace_inner_with_pattern(Util.rename_pattern, __mrepl_getsort_fol,formula)
	__get_sort_from_qf_formula(formula)
	

def __merge_equal_lists(equal_symbols_list):
	'''
	symbols_sets = [set(mlist) for mlist in equal_symbols_list]
	while True:
		symbol_sets_update=[]
		for symbol_set in symbols_sets:	'''
	#print equal_symbols_list

	a = [list(set(elem)) for elem in equal_symbols_list]
	b = len(a)
	for i in range(b):
	    for j in range(b):
	    	#print "begin---", i,j, a[i],a[j]
	    	if j == [] or i==[]:
	    		continue
	        x = list(set(a[i]+a[j]))
	        y = len(a[j])+len(a[i])
	        if i == j:
	        	#print "break-------",a[i],a[j]
	        	break
	        elif len(x) < y:
	        	a[i] = x
	        	a[j] = []
	    	#print a
	return [i for i in a if i != []]
#x = list(set(a[i]+a[j]))
#y = len(a[j])+len(a[i])
#['INT', 'INT', ('m', 2), 'INT', ('f', 1), ('num', 1), ('g', 1), 'INT', ('m', 2), 'INT', ('num', 1)] ['num']

def __get_equal_sorts(symbol_list):
	symbol_sorts = context_operator.get_symbol_sorts_dict()
	#print "-----symobs to sorts:", symbol_sorts
	#print "-----equal symbols list:", symbol_list
	if set(symbol_list)& set(symbol_sorts.keys()) ==set():
		return symbol_list
	else:
		return sum([symbol_sorts[symbol] for symbol in symbol_list if symbol in symbol_sorts.keys()],[])
	'''
	print "--------------------", symbol_list
	print "--------------------",[ symbol for symbol in symbol_list if symbol not in symbol_sorts.keys()]
	return sum([symbol_sorts[symbol] for symbol in symbol_list if symbol in symbol_sorts.keys()],[])
	'''


#[('Y', ('f', 1)), ('X', ('g', 1)), ('g', ('m', 1)), ('X-1', ('m', 2)), ('m', 'INT'), ('1', 'INT'), ('X', 'INT'), 
#('X', ('num', 1)), ('Y', ('num', 1)), ('P', ('turn', 1)), ('blue', ('color', 1))]



#[['f', 'm', '1', '3', '2', 'Y', 'X'], ['num'], ['turn', 'true']]


def discover_sorts():
	#symbols_with_same_sort = __merge_equal_lists(context_operator.get_symbols_equal_list())
	#context_operator.set_symbols_equal_list(symbols_with_same_sort)

	########get two dict()
#打横打树
	symbol_sorts_list = context_operator.get_symbol_to_sort_list()
#print symbol_sorts_list
	symbol_sorts_dict = dict()
	for k, g in groupby(sorted(symbol_sorts_list, key=itemgetter(0)), key=itemgetter(0)):
		 symbol_sorts_dict[k] = [ elem[1] for elem in list(g)]
    #set1
	context_operator.set_symbol_sorts_dict(symbol_sorts_dict)

	sort_symbols_dict = dict()
	for k, g in groupby(sorted(symbol_sorts_list, key=itemgetter(1)), key=itemgetter(1)):
		 sort_symbols_dict[k] = [ elem[0] for elem in list(g)]
	#set2
	context_operator.set_sort_symbols_dict(sort_symbols_dict)

#print "#sort_symbols_dict:",sort_symbols_dict

	#add symbols and merge
	symbols_with_same_sort = __merge_equal_lists(context_operator.get_symbols_equal_list()+sort_symbols_dict.values())
	#set3
	context_operator.set_symbols_equal_list(symbols_with_same_sort)

	equal_sorts_list = [__get_equal_sorts(equal_symbols) for equal_symbols in symbols_with_same_sort]
	#print equal_sorts_list
	equal_sorts_list = __merge_equal_lists(equal_sorts_list)

	#print "hello!!!!!",get_unknown_symbols_or_subsorts(symbol_sorts_list, symbols_with_same_sort,1)
	#print "helloQ!!!!!!!", symbols_with_same_sort
	#print equal_sorts_list
	#exit(0)
	return equal_sorts_list

#print "symbol_to_sort:\n", context_operator.get_symbol_to_sort_list()
#print "equal_symbols:\n ", context_operator.get_symbols_equal_list()
#print "symbol_to_sorts:\n", symbol_sorts_dict
#print "detected equal sorts:\n", equal_sorts_list



# if constant symbol 

#"('X-1', ('m', 2))" ->  [INT, ('m',2)]      case  "sorts" merge
#"('g', ('m', 1))"   ->  [g]                case "constants" nothing
#                     -> [g, ('m', 1)]     case "sorts" merge ? YES



#def get_unknown_symbols_or_subsorts(symbol_sorts_list, known_equal_symbols,num):
#	unknown_symbols = [symbol[num] for symbol in symbol_sorts_list if symbol[num] not in sum(known_equal_symbols,[])]
#	return unknown_symbols

#print "unknown_symbols: ", get_unknown_symbols_or_subsorts(symbol_sorts_list,symbols_with_same_sort,0)
#print "unknown_subsorts: ",get_unknown_symbols_or_subsorts(symbol_sorts_list,equal_sorts_list,1)


def __get_sort_constants(symbol_to_sort):
	#print symbol_to_sort
	sort_keys = list(set(symbol_to_sort.values()))
	#print symbol_to_sort.items()
	sort_constants_dict = dict()
	for sort_key in sort_keys:
		sort_constants_dict[sort_key] = [key for key, value in symbol_to_sort.iteritems() if value == sort_key and isConst(key) ]
	return sort_constants_dict
	#print context_operator.get_sorts()
	#exit(0)


def generate_new_sorts(sorts_list):
	for elem in sorts_list:
		if 'Int' in elem:
			context_operator.declare_sort('Int', elem)
		else:
			context_operator.declare_sort("", elem)
	sorts = context_operator.get_sorts()
	subsort_to_sort = { key: value for value in sorts.keys() for key in sorts[value]}
	symbol_to_sort ={ key:subsort_to_sort[values[0]] for key, values in context_operator.get_symbol_sorts_dict().iteritems()}
	#print "@test-----------subsort_to_sort",subsort_to_sort
	#print "@test-----------symbol_to_sort",symbol_to_sort


	
	symbols = context_operator.get_symbols_equal_list()
	add_symbolsort_dict = dict()
	for symbol, sort in symbol_to_sort.iteritems():
		for elem_list in symbols:
			if symbol in elem_list:
				add_symbolsort_dict.update({elem: sort for elem in elem_list})

	symbol_to_sort.update(add_symbolsort_dict)
	#[context_operator.declare_sort("", elem) for elem in unknown_symbols]
	#print "222",symbol_to_sort
	symbol_to_sort.update(subsort_to_sort)
	#print "333", symbol_to_sort
	context_operator.set_symbol_sorts_dict(symbol_to_sort)

	sort_constants = __get_sort_constants(symbol_to_sort)
	#sort_constants.update(__get_add_sort_constants(context_operator.get_sorts()))
	context_operator.set_sort_symbols_dict(sort_constants)

	

#sort = [[('m', 1)], [('turn', 1)], [('color', 1)], ['INT', ('m', 2), ('g', 1), ('num', 1), ('f', 1)]]
#sort = [['num'], ['turn', 'true'], [('m', 1)], [('turn', 1)], [('color', 1)], ['INT', ('m', 2), ('g', 1), ('num', 1), ('f', 1)]]

'''
generate_sort_from_formula(s)
equal_sort_list = discover_sorts()
generate_new_sorts(equal_sort_list)
print context_operator.get_symbol_sorts_dict()
'''

#print context_operator.get_sorts()

#print context_operator.get_symbols_equal_list()
'''
print "-------------------"
print context_operator.get_symbol_sorts_dict()
print "-------------------"
print context_operator.get_sort_symbols_dict()
'''

# get function sorts e.g.,  supose f(int ,int ) -> int     =>    input : f   output:   [int, int, int]

def get_function_sort(function_name):
	#print function_name
	symbol_sort = context_operator.get_symbol_sorts_dict()
	#print symbol_sort
	function_sorts = [symbol_sort[fun_para] for fun_para in symbol_sort.keys() if type(fun_para) == type(tuple()) and fun_para[0].strip() == function_name.strip()]	
	function_sorts = sorted(function_sorts, key=itemgetter(1))	

	if function_name in symbol_sort.keys():
		function_sorts.append(symbol_sort[function_name])
	else:
		function_sorts.append('Bool')
	return function_sorts



def get_fun_value_sort(function):
	fun_name, fun_var, fun_value = Util.parse_relation_or_function(function)
	return context_operator.get_symbol_sorts_dict()[fun_name]






def __find_var_sort_from_expression(symbol, expression, symbol_sort=""): #expression without quantifier and logical connection (and or =>)

	#print symbol, expression
	symbol_sort = context_operator.get_symbol_sorts_dict() if symbol_sort=="" else None
	symbols = re.findall(r"\w+",expression)

	symbol2 = copy.copy(symbol)
	symbol1 = symbol.encode('utf-8') if isinstance(symbol, unicode) else symbol.decode('utf-8')

	#print [symbol2]
	#print [symbol1]
	#print symbols
	if symbol1 not in symbols and symbol2 not in symbols:
		return None
	#if symbol not in symbols:
	#	raise Exception('No such vars in expression!%s %s'%(symbol, expression))
	#symbol_sort = context_operator.get_symbol_sorts_dict()
	para_pattern_str = r"(?P<fun>\w+)\((?P<body>[^\(\)]*?"+ symbol +"[^\(\)]*?)\)"
	value_pattern_str = r"(?P<fun>\w+)\(.*?\)\s*=\s*" + symbol
	para_pattern = re.compile(para_pattern_str)
	value_pattern = re.compile(value_pattern_str)

	match1 = para_pattern.search(expression)
	match2 = value_pattern.search(expression)
	if match1:
		#if match.group('fun') !="":
		#print "heloo1"
		symbols = [elem.strip() for elem in match1.group('body').split(',')]
		para_list = [ (e, elem.find(symbol)) for e,elem in enumerate(symbols)]
		pre_sort = [ (match1.group('fun'), index+1) for index, signal in para_list if signal!=-1 ][0]

	elif match2:
		#print "hello2"
		#print match2.group()
		pre_sort = match2.group('fun')
	elif re.search(r'[\+\-\*\/\>\<\%]|\>\=|\<\=',expression):
			return 'Int'
	else:
		# numStone = Y find Y is numStone's sort
		#symbols = [elem for elem in symbols if elem !=symbol]
		#return None if symbols == [] else (symbol_sort[symbols.pop()] if symbol_sort!=None else symbols.pop())
		#raise Exception('can not match any sort in expression!%s %s'%(symbol, expression))
		#logger.info('can not match any sort in expression!%s %s'%(symbol, expression))
		return None

	return symbol_sort[pre_sort] if symbol_sort else pre_sort


def __mrepl_var_sort(matched):

	var_list = [var.strip() for var in matched.group('vars').split(',')]
	action_list = [action.strip() for action in matched.group('actions').split(';')]

	#print '#######',var_list, action_list
	vars_sorts = [ (X, __find_var_sort_from_expression(X, action)) for X in var_list for action in action_list if action.find(X)!=-1 ]
	#print '#######@@@',vars_sorts
	vars_sorts = list(set([(var,sort) for var, sort in vars_sorts if sort !=None ]))
	add_sort_var_list = [ var for (var, sort) in vars_sorts]
	if len(vars_sorts)> len(var_list):
		print vars_sorts
		Errormsg = "#ERROR-----get_vars_sorts_from_program:"+matched+"(sort conflict!):"
		raise Exception(Errormsg)
	vars_sorts_str = ",".join([var+":"+sort for var, sort in vars_sorts]+ [var for var in var_list if var not in add_sort_var_list])
	#vars_sorts_str = ",".join([var+":"+sort for var, sort in vars_sorts])
	return "pi("+ vars_sorts_str + ")[" + matched.group('actions') + "]"


pi_action_pattern_str = r"pi\((?P<vars>.+?)\)\s*\[(?P<actions>.+?)\]"
pi_action_pattern = re.compile(pi_action_pattern_str)

def add_program_vars_sorts(program):
	#print program
	return pi_action_pattern.sub(__mrepl_var_sort, program)
	













