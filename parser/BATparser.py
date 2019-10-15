#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-14 20:56:19
# @Author  : Kailun Luo (luokl3@mail2.sysu.edu.cn)
# @Link    : https://sdcs.sysu.edu.cn
# @Version : $Id$

 
import os
import re
from operator import itemgetter #itemgetter用来去dict中的key，省去了使用lambda函数
from itertools import groupby #itertool还包含有其他很多函数，比如将多个list联合起来。。
import json

#import Util
#import context_operator
#import sort_system
#import util_z3

#import  mylog as logging
#logger = logging.getLogger(__name__)
#print rename(s)







#def __get_predicates(sort_consts, fluent):


    		
#eval("apply(__parse_Init,[('Init', '', ' numStone >0  '), ('Init', '', ' turn(p1) and !turn(p2)    ')])")
#exit(0)




#parser("./takeaway.sc")
#print "-----",context_operator.get_axioms()['init']

 #(Poss\(|SSA\(|Init\(|End\(|Win\()




from basic import pattern
from basic import Util
from basic import context_operator
import sort_system


#when replace 'and' with '&', both 'notlogic_pattern_str1' and 'notlogic_pattern_str2' is not possible.
#notlogic_pattern_str1 = r"(?:(?:(?<!and)(?<!or)(?<!=>).(?!and)(?!or)(?!=>))+)"
#notlogic_pattern_str2 = r"(?:(?:(?<!\&)(?<!\|)(?<!=>).(?!\&)(?!\|)(?!=>))+)"

notlogic_pattern_str = r"[^\&\|!=]+"
fluent_pattern_lambda_exp = lambda x: r"(?:"+ "|".join(x)+ ")\s*=\s*"+notlogic_pattern_str 
predicate_pattern_lambda_exp = lambda x: r"(?:"+ "|".join(x)+ ")"


nregxfun_pattern_str_pre = r""+'(?P<pre>.?)\s*(?P<fun>'
nregxfun_pattern_str_pos = '\([^\(\)]*\))\s*(?P<pos>=>|.)' 



def __generate_nregx_function_patterns(fluents):
	nregxfun_pattern_str_list = [nregxfun_pattern_str_pre+ fun+ nregxfun_pattern_str_pos for fun in fluents]
	#print nregxfun_pattern_str_list
	nreg_fluent_pattern_list = [re.compile(pattern_str) for pattern_str in nregxfun_pattern_str_list ]
	return nreg_fluent_pattern_list

def __generate_fun_regress_lambda(functions, function_sorts):
	#print [fluent+"\("+','.join(["(.*?)"]*(len(function_sorts[fluent])-1))+"\)" for fluent in functions ]
	return re.compile(fluent_pattern_lambda_exp([fluent+"\("+','.join(["(.*?)"]*(len(function_sorts[fluent])-1))+"\)" for fluent in functions ]))

def __generate_pred_regress_lambda(predicates, function_sorts):
	#print [predicate+"\("+','.join(["(.*?)"]*len(function_sorts[predicate]))+"\)" for predicate in predicates ]
	return re.compile(predicate_pattern_lambda_exp([predicate+"\("+','.join(["(.*?)"]*len(function_sorts[predicate]))+"\)" for predicate in predicates ]))

###########################################################################################

def __get_rigid_functions(rule_list, fluent_list):

	ssas = [(paras, formula) for name, paras, formula in rule_list if name == 'SSA' ]
	rigid_str_list = [ formula for fluent_action, formula in ssas if re.match('%s,pi\('%(formula.replace('(','\(').replace(')','\)')), fluent_action)]
	rigid_str = ' '.join(rigid_str_list)
	rigid_function_list = [fluent for fluent in fluent_list if re.search(r'\b%s\b'%fluent, rigid_str)]

	return rigid_function_list



###########################################################################################



def __generate_predicates(fluent_list, symbols):
	return [fluent for fluent in fluent_list if fluent not in symbols]

def __generate_predicate_sorts(predicates, functions_sorts):
	#print predicates, functions_sorts
	return { pred :sorts[0: len(sorts)-1] for pred, sorts in functions_sorts.iteritems() if pred in predicates}


def __get_funs_sorts(funs):
	fun_sorts_dict = dict()
	for fun in funs:
		fun_sorts_dict[fun] = sort_system.get_function_sort(fun)
	return fun_sorts_dict


def __get_sort_const_with_fluents(sort_consts, fluent):
	#print sort_consts , fluent
	for key in sort_consts.keys():
		sort_consts[key] = [ elem for elem in sort_consts[key] if elem not in fluent]
	return sort_consts

###########################################################################################

######################
###### NOTICE
######################
#f(X) =Y , X,Y can be variable or constant 
#f(X) = k(Y) can be changed, for example:
#contains(P) = volunn(P), take(P',P) <=> contains(P)+ contains(P')> volunn(P) can be rewrite as
#contains(P) = Y, take(P',P) <=> Y=volunn(P) and  contains(P)+ contains(P')> volunn(P)

def __parse_Basic(*tuples):
	#print tuples
	pass

def __parse_Win(*tuples):
	for mtuple in tuples:
	#'numStone=Y, take(P,X)' -> [numStone=Y, take(P,X)]
		formula = mtuple[2]
		name_list, feature_list, var_list = ____get_features_vars(mtuple[1])
		#print name_list, feature_list, var_list
		feature = ____generate_feature_pattern(feature_list, var_list)
		context_operator.set_axiom("win",feature, var_list, formula)
		#print feature

	#print tuples


def __parse_End(*tuples):
	#print tuples
	for mtuple in tuples:
		formula = mtuple[2]
		context_operator.set_axiom("end","",[], formula)


def __parse_Init(*tuples):
	#print tuples
	formulas = list()
	for mtuple in tuples:
		formulas.append(mtuple[2])
	context_operator.set_axiom("init", "" , [], "&".join(formulas))


def __parse_Poss(*tuples): #(('Poss', 'take(P,X)', ' num_stone>=X and (X=1 or X=2 or X=3)       and turn(P)    '),)
	#print tuples
	for mtuple in tuples:
		#'numStone=Y, take(P,X)' -> [numStone=Y, take(P,X)]
		formula = mtuple[2]
		#print '----',mtuple[1]
		name_list, feature_list, var_list = ____get_features_vars(mtuple[1])
		feature = ____generate_feature_pattern(feature_list, var_list)
		context_operator.add_actions([name for name in name_list if name.strip()!="pi"])
		#print '-------',feature, name_list, feature_list, var_list
		context_operator.set_axiom("poss",feature, var_list, formula)



def ____get_features_vars(m_str):
	#print '1111',m_str
	feature_list = list()
	var_list = list()
	names_list = list()
	functions = Util.get_paras_from_str(m_str)
	for function in functions:
		fun_name, fun_para, fun_value = Util.parse_relation_or_function(function)
		var_list+= [mvar for mvar in Util.get_paras_from_str(fun_para)+[fun_value] if Util.isVar(mvar) ] 
		feature_list.append(Util.generate_function_feature(function))
		names_list.append(fun_name)
	return names_list, feature_list, var_list


def ____generate_feature_pattern(feature_list, var_list):
	#print feature_list, var_list
	feature = '_'.join(feature_list)
	replace_pattern_list = ['_'+mvar+'_' for mvar in var_list]
	#print replace_pattern_list
	replace_pattern_list = zip(replace_pattern_list, ['_(.+?)_']*(len(replace_pattern_list)))
	#print replace_pattern_list
	feature = Util.repeat_do_function(Util.replace_lambda_exp, replace_pattern_list, feature).replace("pi_","")
	#print "--feature for pattern--",feature,feature.replace("pi_","")
	context_operator.add_feature((feature_list, var_list,feature))
	return re.compile(feature)  #handle pi(A) which means A is variable


def __parse_SSA(*tuples):
	#print tuples
	'''
	divide_pattern_str = r"(?P<fun>[\w]+)(?P<para>(?:\(.*?\))?)\s*(?:=\s*(?P<value>(?:"+var_pattern_str+"|"+const_pattern_str+")))?"# (?:" + const_pattern_str +"|"+ var_pattern_str+ "))?,"
	divide_pattern = re.compile(divide_pattern_str)
	for mtuple in tuples:
		match = re.match(divide_pattern,mtuple[2])
		print match
	'''
	#generate ssa[key]
	for mtuple in tuples:
		#'numStone=Y, take(P,X)' -> [numStone=Y, take(P,X)]

		formula = mtuple[2]

		#print var_list
		name_list, feature_list, var_list = ____get_features_vars(mtuple[1])
		#print name_list, feature_list, var_list
		feature_pattern = ____generate_feature_pattern(feature_list, var_list)
		actions = [name for e, name in enumerate(name_list) if e % 2 ==1  and name.strip()!="pi"]
		fluents = [name for e, name in enumerate(name_list) if e % 2 == 0 ]
		context_operator.add_actions(actions)
		context_operator.add_fluents(fluents)

		#print feature
		context_operator.set_axiom("ssa", feature_pattern, var_list, formula)
		#print formula
		#print context_operator.get_axioms()['ssa'][feature](['b','c','d'])
		

m = (('SSA', 'numStone(m) =Y , take(P,X)', '     Y = numStone -X    '),)
#__parse_SSA(m)
#print __parse

########################################################################################################################


addsort_pattern_str = r"(?P<head>(?:forall|exists))\((?P<var>[\w\:\s\d,]+?)\)(?P<body>\[[^\[\]]+\])"
addsort_pattern  = re.compile(addsort_pattern_str)


def ______mrepl_addsort_forall(matched):
	sort_dict = context_operator.get_symbol_sorts_dict()
	var_list = matched.group("var").split(",")
	var_sort_list = [ var+":"+sort_dict[var] for var in var_list]
	var_sort_str = ",".join(var_sort_list)
	var_sort_str = matched.group("head")+ "(" + var_sort_str+ ")" + matched.group('body')
	return Util.endecode_string(var_sort_str, Util.encode_pair_forall[0], Util.encode_pair_forall[1])


def ____add_sort_forall(rule_list):
	for e,rule in enumerate(rule_list):
		new_formula = Util.repeat_replace_inner_with_pattern(addsort_pattern, ______mrepl_addsort_forall, rule[2])
		new_formula = Util.endecode_string(new_formula, Util.encode_pair_forall[1], Util.encode_pair_forall[0])
		rule_list[e] = (rule[0],rule[1], new_formula)
	return rule_list



def ____rename_rule_vars(rule_list, varlist_list):
	#rename free varable

	for e, rename_var_list in enumerate(varlist_list):
		#print "rename##########:", rename_var_list
		new_var_list = [context_operator.get_new_var() for i in rename_var_list]
		#print "new_var#########",new_var_list 
		rename_var_list = [r'\b' + elem + r'\b' for elem in rename_var_list]
		temp_rule =Util.repeat_do_function(Util.sub_lambda_exp, zip(rename_var_list,new_var_list),rule_list[e][1]+"#"+rule_list[e][2])
		#print "temp_rule ~~~~~~~~>:", temp_rule
		#print Util.rename_forall(temp_rule.split('&')[1])
		rule_list[e] = (rule_list[e][0], temp_rule.split('#')[0], Util.rename_forall(temp_rule.split('#')[1]))
	return rule_list


# elements in rule_list: (axiom_name, ['']|[fluent,action]|[action], formula)


def ____get_vars_from_relationlist_list(relationlist_list):
	return [____get_vars_from_relations(relation_list) for relation_list in relationlist_list]

def ____get_vars_from_relations(relation_list):
	if relation_list ==[""]:
		return list()
	var_list = list()
	for relation in relation_list:
		fun_name, fun_para, fun_value = Util.parse_relation(relation)
		fun_name2, fun_para2, fun_value2 = Util.parse_function(relation)
		if fun_name == None and fun_name2 == None:
			print '~~~~~~(ERROR):', relation
			error_message = "#Error-----when parsing str %s-----Util.parse_relation: Exist" %relation
			raise Exception(error_message)
		if fun_name == None:
			fun_name, fun_para, fun_value = fun_name2, fun_para2, fun_value2
		var_list+= [ mvar for mvar in Util.get_paras_from_str(fun_para)+[fun_value] if Util.isVar(mvar) ] 
	return var_list


def ____handle_0arity_fluents(rule_list, zero_arity_fluents):
	old_strs = [r'\b'+str(fluent)+r'\b' for fluent in zero_arity_fluents]
	replaces = [fluent+'()' for fluent in zero_arity_fluents]
	for e, rule in enumerate(rule_list):
		relations = Util.repeat_do_function(Util.sub_lambda_exp, zip(zero_arity_fluents,replaces),rule[1])
		formula = Util.repeat_do_function(Util.sub_lambda_exp, zip(zero_arity_fluents,replaces),rule[2])
		rule_list[e] = (rule[0], relations, formula)
	return rule_list 


def ____get_0arity_functions(function_list):
	zero_arity_fluents = list()
	for function in function_list:
		if function.split('=')[0].find('(')==-1: # it's f = X or f or f = g(Y) where f is zero-para function
			matched = pattern.symbol.match(function)
			if matched:
				zero_arity_fluents.append(matched.group())
			else:
				print "#EOROR(__parse_SSA|Poss): name error when parsing function: ",function
	return list(set(zero_arity_fluents))


def ____get_relations_from_rules(rule_list):
	return sum([ Util.get_paras_from_str(rule[1]) for rule in rule_list if rule[1]!=""],[])


def ____get_relationlist_list_from_rules(rule_list):
	return [ Util.get_paras_from_str(rule[1]) for rule in rule_list]


def __pre_parse(rule_list):
	
	relation_list = ____get_relations_from_rules(rule_list)
	zero_arity_fluents = ____get_0arity_functions(relation_list)
	rule_list = ____handle_0arity_fluents(rule_list, zero_arity_fluents)

	relationlist_list = ____get_relationlist_list_from_rules(rule_list)
	varlist_list = ____get_vars_from_relationlist_list(relationlist_list)
	rule_list =  ____rename_rule_vars(rule_list, varlist_list)

	#return rule_list
	#exit(0)

	context_operator.set_zero_fluent(zero_arity_fluents)
	#print "hello", rule_list

	for rule in rule_list:
		functions = Util.get_paras_from_str(rule[1])
		[ sort_system.generate_sort_from_formula(item) for item in functions+[rule[2]]]

	equal_sort_list = sort_system.discover_sorts()
	sort_system.generate_new_sorts(equal_sort_list)
	#print context_operator.get_symbol_sorts_dict()
	#print context_operator.get_sort_symbols_dict()
	#print context_operator.get_sorts()
	#logger.info("after detecting sort: %s\n %s\n %s\n"%(context_operator.get_symbol_sorts_dict(), context_operator.get_sort_symbols_dict(),context_operator.get_sorts()) )

	#print context_operator.get_sorts()
	#print
	#print context_operator.get_symbol_sorts_dict()
	#print
	#print context_operator.get_sort_symbols_dict()
	rule_list = ____add_sort_forall(rule_list)
	#print rule_list
	return rule_list


########################################################################################################################


def __load_state_constaints(domain_name):
	with open("./input/state_constraint","r") as fp_fsa:
		mdict = json.load(fp_fsa)[domain_name]
		context_operator.set_state_constraints(mdict['sc'])



def parser(filename):
	with open('./input/%s'%filename,"read") as sc_file, open('./input/default_axioms.sc',"read") as basic_file,\
	open('./temp/game_rule_info','write') as sc_temp:
		full_txt = " ".join(sc_file.readlines()).replace("\n"," ").replace("\t"," ")
		full_txt +=" ".join(basic_file.readlines()).replace("\n"," ").replace("\t"," ")+";"
		full_txt = full_txt.replace(' and ','&').replace(' or ','|').replace(' ',"")
		#logger.debug(full_txt)

		rule_list = pattern.rule3.findall(full_txt)+pattern.rule4.findall(full_txt)+pattern.rule5.findall(full_txt)

		sc_temp.writelines('\n'.join([str(elem) for elem in rule_list]))
		
		rule_list = __pre_parse(rule_list)


		sc_temp.writelines('\n')
		sc_temp.writelines('\n\n')
		sc_temp.writelines('\n'.join([str(elem) for elem in rule_list]))
		
		for k, g in groupby(sorted(rule_list, key=itemgetter(0)), key=itemgetter(0)):
			m_group = list(g)
		 	#print "-------",k, m_group
			eval("apply(__parse_" + k + "," + str(m_group) + ")")

		rigid_function_list = __get_rigid_functions(rule_list, context_operator.get_fluents())
		context_operator.set_rigid_functions(rigid_function_list)

		predicates = __generate_predicates(context_operator.get_fluents(), context_operator.get_symbol_sorts_dict().keys())
		fun_fluents = [fluent for fluent in  context_operator.get_fluents() if fluent not in predicates]

		#print context_operator.get_feature()
		sc_temp.writelines('\n\n')
		sc_temp.writelines('feature pattern for regression:\n')
		sc_temp.writelines('\n'.join([str(elem) for elem in context_operator.get_feature()]))
		#exit(0)
		sc_temp.writelines('\n')
		sc_temp.writelines('\n actions:'+str(context_operator.get_actions()))
		sc_temp.writelines('\n fluents:'+str(context_operator.get_fluents()))
		sc_temp.writelines('\n 0arity-fluents:'+str(context_operator.get_zero_fluents()))
		sc_temp.writelines('\n predicates:'+str(predicates))
		sc_temp.writelines('\n functional fluents:'+str(fun_fluents))
		sc_temp.writelines('\n rigid functions:'+str(context_operator.get_rigid_functions()))

		
		#logger.debug("\n actions :%s \n fluents %s"%(context_operator.get_actions(), context_operator.get_fluents()))
		#print sort_system.get_function_sort('numStone')
		#print context_operator.get_sort_symbols_dict()
		sort_const = __get_sort_const_with_fluents(context_operator.get_sort_symbols_dict(), context_operator.get_fluents())
		sort_const["Bool"] = ['True','False']
		sort_funs =  __get_funs_sorts(context_operator.get_fluents()+context_operator.get_actions())
		sort_preds = __generate_predicate_sorts(predicates, sort_funs)
		
		sc_temp.writelines('\n')
		sc_temp.writelines('\n sort for constants:'+str(sort_const))
		sc_temp.writelines('\n sort for functions:'+str(sort_funs))
		sc_temp.writelines('\n sort for predicates:'+str(sort_preds))


		context_operator.set_sort_symbols_dict(sort_const)
		context_operator.set_functions_sorts(sort_funs)
		context_operator.add_predicates(predicates)
		context_operator.add_predicate_sorts(sort_preds)

		context_operator.add_nregx_function_patterns(__generate_nregx_function_patterns(fun_fluents))
		#print z3_header
		context_operator.set_function_regress_lambda(__generate_fun_regress_lambda(fun_fluents, sort_funs))
		context_operator.set_predicate_regress_lambda(__generate_pred_regress_lambda(predicates, sort_preds))
		#exit(0)

		domain_name = filename.split('.')[0]
		__load_state_constaints(domain_name)

		#context_operator.set_z3_header(util_z3.generate_head())
		#exit(0)	

