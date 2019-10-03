

###
# 
#
#
#
#

import re
from model import model_checker
from basic import Util
from basic import context_operator

from operator import itemgetter 
from itertools import groupby

import itertools

##############################################################################################################################################################

def to_formula(conjuct):
	var_list, sort_list, pred_list = conjuct
	if var_list !=list():
		add_pred_list = ['%s>=0'%(x) for e, x in enumerate(var_list) if sort_list[e] == 'Int']
		return "exists(%s)[%s]"%(','.join([ "%s:%s"%(var,sort) for var,sort in zip(var_list,sort_list)]), '&'.join(add_pred_list+pred_list))
	else:
		return '%s'%('&'.join(pred_list))



##############################################################################################################################################################
#k1 = (['X1','X2'], ['Int','Int'],['! numStone() = X1']) 

def __refresh_vars(conjuct):
	var_list, sort_list, pred_list = conjuct
	new_var_list, new_sort_list = list(),list()
	preds_str = '&'.join(pred_list)
	for e, var in enumerate(var_list):
		if re.search(r'\b%s\b'%var, preds_str):
			new_var_list.append(var)
			new_sort_list.append(sort_list[e])
	return (new_var_list, new_sort_list, pred_list)

#print refresh_vars(k1) -> (['X1'], ['Int'], ['! numStone() = X1'])


##############################################################################################################################################################


def get_sat_subconjuncts(conjunct, model_list, length):
	var_list, sort_list, pred_list = conjunct
	subconjunct_list = list()
	#del_preds_list = sum([ list(itertools.combinations(body_list,length)) for length in range(1,length+1) if len(body_list)>=length],[])
	if len(pred_list)<=length:
		return [([],[],[])]
	del_preds_list = list(itertools.combinations(pred_list,length))
	for del_preds in del_preds_list:
		rest_preds = list(set(pred_list) - set(list(del_preds)))
		#rest_body = ' and '.join(rest_preds)
		if rest_preds == [] or model_list is None or model_checker.sat_conjunct(model_list, (var_list, sort_list, rest_preds)) is True:
			subconjunct_list.append( __refresh_vars((var_list, sort_list, rest_preds))) 
	return subconjunct_list


##############################################################################################################################################################

# rename the variables in the conjunct

def rename(conjunct):
	var_list, sort_list, pred_list = conjunct

	new_var_list = [context_operator.get_new_var() for i in var_list]
	rename_var_list = [r'\b' + elem + r'\b' for elem in var_list]

	body_str = "%s"%("&".join(pred_list))
	#print var_body_str
	new_body_str =Util.repeat_do_function(Util.sub_lambda_exp, zip(rename_var_list,new_var_list), body_str)
	#print var_body_str
	new_pred_list =  new_body_str.split('&')

	return (new_var_list, sort_list, new_pred_list)



##############################################################################################################################################################



def __get_sort_vars_dict(var_list, sort_list):
	sort_dict = dict()
	sort_list = zip(sort_list, var_list)
	for k, g in groupby(sorted(sort_list, key=itemgetter(0)), key=itemgetter(0)):
		sort_dict[k] = list(zip(*list(g))[1])
	return sort_dict



def __get_combined_conjunct(conjunctA, conjunctB, vars_repl_tuple):
	#print 'aaa',conjunctA, conjunctB, vars_repl_tuple
	var_listA, sort_listA, pred_listA = conjunctA
	var_listB, sort_listB, pred_listB = conjunctB
	be_repl_var_list,  repl_var_list = vars_repl_tuple


	body_strB = '&'.join(pred_listB)
	replace_list = [(r'\b%s\b'%old_var, '_%s'%repl_var_list[e]) for e, old_var in enumerate(be_repl_var_list) ]
	new_body_strB = Util.repeat_do_function(Util.sub_lambda_exp, replace_list, body_strB)
	new_pred_listB = new_body_strB.replace('_','').split('&')


	new_var_listB, new_sort_listB = list(), list()
	for e, var in enumerate(var_listB):
		if var not in be_repl_var_list:
			new_var_listB.append(var)
			new_sort_listB.append(sort_listB[e])


	return (var_listA+new_var_listB, sort_listA+new_sort_listB, pred_listA+new_pred_listB)



def ____get_combine_vars_tuples(varA_list, varB_list, share_var_num):
	#return  [zip(tuple(var_list), pattern) for pattern in patterns]
	repl_vars_list = list(itertools.permutations(varA_list, share_var_num))
	be_repl_vars_list = list(itertools.combinations(varB_list, share_var_num))
	#print list(repl_vars_list)
	#print list(be_repl_vars_list)
	vars_repl_tuple_list = [ (list(be_repl_vars), list(repl_vars))  for be_repl_vars in be_repl_vars_list for repl_vars in repl_vars_list ]

	return vars_repl_tuple_list


def __get_repl_vars_tuples(var_listA, sort_listA, var_listB, sort_listB, max_var_num):

	sort_vars_dictA = __get_sort_vars_dict(var_listA, sort_listA)
	sort_vars_dictB = __get_sort_vars_dict(var_listB, sort_listB)

	#print sort_vars_dictA
	#print sort_vars_dictB
	#print '!!!!'
	vars_repl_tuple_list = [([],[])]
	part_vars_repl_tuple_list = list()

	for Asort, Avar_list in sort_vars_dictA.iteritems():
		if Asort in sort_vars_dictB:
			min_share_vars_num = len(Avar_list) + len(sort_vars_dictB[Asort]) - max_var_num
			#print min_share_vars_num
			min_share_vars_num = max([min_share_vars_num,0])

			part_vars_repl_tuple_list = list()
			for length in range(min_share_vars_num, min([len(Avar_list),len(sort_vars_dictB[Asort])])+1):
				part_vars_repl_tuple_list += ____get_combine_vars_tuples(Avar_list, sort_vars_dictB[Asort], length)

		vars_repl_tuple_list = [(a+c,b+d) for (a,b) in vars_repl_tuple_list for (c,d) in part_vars_repl_tuple_list ]	

	return vars_repl_tuple_list


## note: merge two conjuncts into one, 
##       with the limitation of maximal number of variables for every sort for the new conjunct

def combine_conjunct(conjunctA, conjunctB, max_var_num):
	var_listA, sort_listA, pred_listA = conjunctA
	var_listB, sort_listB, pred_listB = conjunctB

	#new_conjunct_str_list = ['%s#%s#%s'%('&'.join(varB_list),'&'.join(sort_listB), '&'.join(predB_list))] 

	vars_repl_tuple_list = __get_repl_vars_tuples(var_listA, sort_listA, var_listB, sort_listB, max_var_num)

	#print '!!!!',vars_repl_tuple_list
	return [ __get_combined_conjunct(conjunctA, conjunctB, vars_repl_tuple) for vars_repl_tuple in vars_repl_tuple_list]


##############################################################################################################################################################

## return a conjunct list where every conjunct satisfies model_sat_list but falsifies model_unsat_list

def get_target_conjuncts(conjunct_list, model_sat_list, model_unsat_list):
	#exit(0)
	sat_conjunct_list = [conjunct for conjunct in conjunct_list if model_checker.sat_conjunct(model_sat_list, conjunct)]
	return [conjunct for conjunct in sat_conjunct_list if model_checker.unsat_conjunct(model_unsat_list, conjunct)]



##############################################################################################################################################################

