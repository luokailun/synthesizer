import os
from operator import itemgetter
import util_pred_formula
import re
import util_cache
import util_pred
import util_pred_model
from operator import itemgetter 
from itertools import groupby 
from basic import context_operator

var_pattern = re.compile(r'\w\d+')
'''
def __unify_vars(var_list, pred):
	replace_var = 'W'
	e = 0
	for var in var_list:
		if pred.find(var)!=-1:
			pred = pred.replace(var, replace_var+str(e))
			e+=1
	return pred
'''

#s = "Y11 * 4 = Y11"

def __unify_vars(pred):
	replace_var = 'W'
	mvars = var_pattern.findall(pred)
	#print mvars
	for e, var in enumerate(mvars):
		pred = pred.replace(var, replace_var+str(e),1)
	return pred
#print __unify_vars(s)

def init_preds_base_score(pred_list):
	return { __unify_vars(pred): 0 for var_list, sorts, pred in pred_list}


##############################################################################################################################################################

def __compute_pred_score(pred, base_score_dict):
	#print '--',pred
	#print base_score_dict
	elems = pred.split(' and ')
	return sum([base_score_dict[__unify_vars(elem)] for elem in elems ], 0)



def compute_preds_score(pred_list, pred_dict, base_score_dict):
	return { pred: __compute_pred_score(pred, base_score_dict) for pred in pred_list}



def sort_preds(pred_score_dict):
	return [ pred for pred, score in sorted(pred_score_dict.items(), key=itemgetter(1), reverse=True)]


##############################################################################################################################################################


def get_sort_pred_list_org(com_pred_list, base_score_dict):
	pred_dict = { pred: (var_list, sorts) for var_list, sorts, pred in com_pred_list}
	pred_score_dict = compute_preds_score(pred_dict.keys(), pred_dict, base_score_dict)
	pred_list = sort_preds(pred_score_dict)
	return [(pred_dict[pred][0], pred_dict[pred][1], pred) for pred in pred_list]
	


def get_sort_pred_list(pred_list, pred_dict, base_score_dict):
	pred_score_dict = compute_preds_score(pred_list, pred_dict, base_score_dict)
	return sort_preds(pred_score_dict)


##############################################################################################################################################################
#f = "((  row(1)=1 and row(2)=0   ) => (  row(1) = 1 and row(2)=0 and ! turn(p1)               ))  and {! (exists(X0:Int)[$X0>=0 and $len() = X0 and X0 % 3 = 1])} and {! (exists(X0:Int)[$X0>=0 and $mrow() = X0 and ! row(1) = X0])}"
#pred_score_dict = {'mrow() = W0':0, '! row(1) = W0':2}


def minus_pred_score_dict(formula, pred_score_dict):
	formula = util_pred_formula.delete_prefix(formula)
	conjuncts = util_pred_formula.from_formula_to_conjuncts(formula)
	com_preds = [ util_pred_formula.from_conjunct_to_pred(conjunct.strip('!').strip()) for conjunct in conjuncts]
	preds = sum([ pred.split(' and ') for var_list, sorts, pred in com_preds ],[])

	for pred in preds:
		pred_feature = __unify_vars(pred)
		pred_score_dict[pred_feature] = pred_score_dict[pred_feature]-1
		#print '---------------'
		#print pred_score_dict[pred_feature]
	return pred_score_dict

'''
preds = [(['X1'],['Int'],'X1>1'), (['X1','X2'], ['Int','Int'],'fun(X1, X2)=0')]

pred_list = ['X1>1 and fun(X1, X2)=0']
pred_dict2 = {'X1>1 and fun(X1, X2)=0': (['X1', 'X2'], ['Int','Int'])}
m = {'fun(W0, W1)=0': 1, 'W0>1': 2}
mdict = init_preds_base_score(preds)
k = compute_preds_score(pred_list, pred_dict2, m)
k.update(m)
print sort_preds(k)
'''
##############################################################################################################################################################


'''
def sort_and_get_pred(conjunct_list, vars_sorts_dict, base_score_dict, model_set_neg, model_set_pos):
	#print 
	#print conjunct_list
	#print vars_sorts_dict
	#print base_score_dict
	#print

	pred_score_dict = compute_preds_score(conjunct_list, vars_sorts_dict, base_score_dict)
	for score, group_preds in groupby(sorted(pred_score_dict.iteritems(), key=itemgetter(1), reverse=True), key=itemgetter(1)):
		#print '------', list(group_preds)
		pred_model_num_list = [ (pred, util_pred_model.count_models_sat_pred(model_set_neg, vars_sorts_dict[pred][0], vars_sorts_dict[pred][1], pred) ) for pred,num in  list(group_preds)]
		num_sort_pred_list = (sorted(pred_model_num_list, key=itemgetter(1), reverse=True))
		#print
		#print '---------------'
		#print len(model_set_neg)
		#print num_sort_pred_list
		#print '--------------'
		#print
		for pred, num in num_sort_pred_list:
			com_pred = (vars_sorts_dict[pred][0], vars_sorts_dict[pred][1], pred)
			if util_pred.__math_ground_check(com_pred, model_set_pos) is True and util_cache.has_choice(pred) is False:
				util_cache.add_conjunct_choice(pred)
				return com_pred
	return None

'''

def __get_pred_length(pred):
	return len(pred.split(' and '))



def sort_and_get_pred(conjunct_list, vars_sorts_dict, base_score_dict, model_set_neg, model_set_pos):
	#print 
	#print conjunct_list
	#print vars_sorts_dict
	#print base_score_dict
	#print
	if context_operator.get_action_function()=='quantifier_first':
		quantiferFree_conjunct_list = [conjunct for conjunct in conjunct_list if vars_sorts_dict[conjunct]==([],[])]
		quantifer_conjunct_list = [conjunct for conjunct in conjunct_list if conjunct not in quantiferFree_conjunct_list]


		pred_score_dict = compute_preds_score(quantifer_conjunct_list, vars_sorts_dict, base_score_dict)
		for score, group_preds in groupby(sorted(pred_score_dict.iteritems(), key=itemgetter(1), reverse=True), key=itemgetter(1)):
			#print '------', list(group_preds)
			pred_len_list = [ (pred, __get_pred_length(pred)) for pred, num in list(group_preds) ]

			sort_length_group =  groupby(sorted(pred_len_list, key=itemgetter(1), reverse=False), key=itemgetter(1))
			for length, sub_group_preds in sort_length_group:
				pred_model_num_list = [ (pred, util_pred_model.count_models_sat_pred(model_set_neg, vars_sorts_dict[pred][0], vars_sorts_dict[pred][1], pred) ) for pred, num in  list(sub_group_preds)]
				num_sort_pred_list = (sorted(pred_model_num_list, key=itemgetter(1), reverse=True))
				for pred, num in num_sort_pred_list:
					com_pred = (vars_sorts_dict[pred][0], vars_sorts_dict[pred][1], pred)
					if util_cache.has_choice(pred) is False and util_pred.__math_ground_check(com_pred, model_set_pos) is True:
						util_cache.add_conjunct_choice(pred)
						return com_pred


		pred_score_dict = compute_preds_score(quantiferFree_conjunct_list, vars_sorts_dict, base_score_dict)
		for score, group_preds in groupby(sorted(pred_score_dict.iteritems(), key=itemgetter(1), reverse=True), key=itemgetter(1)):
			#print '------', list(group_preds)
			pred_len_list = [ (pred, __get_pred_length(pred)) for pred, num in list(group_preds) ]
			sort_length_group =  groupby(sorted(pred_len_list, key=itemgetter(1), reverse=False), key=itemgetter(1))
			for length, sub_group_preds in sort_length_group:
				pred_model_num_list = [ (pred, util_pred_model.count_models_sat_pred(model_set_neg, vars_sorts_dict[pred][0], vars_sorts_dict[pred][1], pred) ) for pred, num in  list(sub_group_preds)]
				num_sort_pred_list = (sorted(pred_model_num_list, key=itemgetter(1), reverse=True))
				for pred, num in num_sort_pred_list:
					com_pred = (vars_sorts_dict[pred][0], vars_sorts_dict[pred][1], pred)
					if util_cache.has_choice(pred) is False and util_pred.__math_ground_check(com_pred, model_set_pos) is True :
						util_cache.add_conjunct_choice(pred)
						return com_pred
	
	else:
		pred_score_dict = compute_preds_score(conjunct_list, vars_sorts_dict, base_score_dict)
		for score, group_preds in groupby(sorted(pred_score_dict.iteritems(), key=itemgetter(1), reverse=True), key=itemgetter(1)):
			#print '------', list(group_preds)
			pred_len_list = [ (pred, __get_pred_length(pred)) for pred, num in list(group_preds) ]

			#sort_length_group =  groupby(sorted(pred_len_list, key=itemgetter(1), reverse=False), key=itemgetter(1))
			#for length, sub_group_preds in sort_length_group:
			#	pred_model_num_list = [ (pred, util_pred_model.count_models_sat_pred(model_set_neg, vars_sorts_dict[pred][0], vars_sorts_dict[pred][1], pred) ) for pred, num in  list(sub_group_preds)]
			#	num_sort_pred_list = (sorted(pred_model_num_list, key=itemgetter(1), reverse=True))
			len_sort_pred_list = (sorted(pred_len_list, key=itemgetter(1), reverse=False))
			for pred, num in len_sort_pred_list:
				com_pred = (vars_sorts_dict[pred][0], vars_sorts_dict[pred][1], pred)
				if util_cache.has_choice(pred) is False and util_pred.__math_ground_check(com_pred, model_set_pos) is True:
					util_cache.add_conjunct_choice(pred)
					return com_pred
	return None
##############################################################################################################################################################

