
from model import model_checker
from basic import Util
from basic import context_operator
import conjunct_filter

from operator import itemgetter 
from itertools import groupby
import re
import itertools

##############################################################################################################################################################



def __refresh_vars(conjuct):
	"""
	delete redundant variables

	If k = (['X','Y'], ['Int','Int'],['! numStone() = N']) , 
	then __refresh_vars(k) will return  (['X'], ['Int'], ['! numStone() = X'])

	"""
	var_list, sort_list, pred_list = conjuct
	new_var_list, new_sort_list = list(),list()
	preds_str = '&'.join(pred_list)
	for e, var in enumerate(var_list):
		if re.search(r'\b%s\b'%var, preds_str):
			new_var_list.append(var)
			new_sort_list.append(sort_list[e])
	return (new_var_list, new_sort_list, pred_list)



def get_sat_subconjuncts(conjunct, model_list, length):
	"""
		(1) get sub-conjuncts of by dropping certain number (length) of predicates 
		(2) the sub-conjuncts should satisfy the model set

	"""
	var_list, sort_list, pred_list = conjunct
	subconjunct_list = list()
	if len(pred_list)<=length:
		return [([],[],[])]
	del_preds_list = list(itertools.combinations(pred_list,length))
	for del_preds in del_preds_list:
		rest_preds = list(set(pred_list) - set(list(del_preds)))
		if  model_list is None or model_checker.sat_conjunct(model_list, (var_list, sort_list, rest_preds)) is True:
			subconjunct_list.append( __refresh_vars((var_list, sort_list, rest_preds))) 
	return subconjunct_list


##############################################################################################################################################################




def to_formula(conjuct):
	"""
		transform a conjunct structure to the formula form
	"""
	var_list, sort_list, pred_list = conjuct
	if var_list !=list():
		add_pred_list = ['%s>=0'%(x) for e, x in enumerate(var_list) if sort_list[e] == 'Int']
		return "exists(%s)[%s]"%(','.join([ "%s:%s"%(var,sort) for var,sort in zip(var_list,sort_list)]), '&'.join(add_pred_list+pred_list))
	else:
		return '%s'%('&'.join(pred_list))




##############################################################################################################################################################


def __combine_conjunct(conjunctA, conjunctB, from_var_list, to_var_list):
	"""
		sub-procedure: merge two conjuncts into one by mapping variables from one conjunct to the other conjunct
	"""
	var_listA, sort_listA, pred_listA = conjunctA
	var_listB, sort_listB, pred_listB = conjunctB

	body_strB = '&'.join(pred_listB)
	replace_list = [(r'\b%s\b'%old_var, '_%s'%to_var_list[e]) for e, old_var in enumerate(from_var_list) ]
	new_body_strB = Util.repeat_do_function(Util.sub_lambda_exp, replace_list, body_strB)
	new_pred_listB = new_body_strB.replace('_','').split('&')

	new_var_listB = [ var for var in var_listB if var not in set(from_var_list)]
	new_sort_listB = [ sort_listB[e] for e, var in enumerate(var_listB) if var not in set(from_var_list) ]

	return (var_listA+new_var_listB, sort_listA+new_sort_listB, pred_listA+new_pred_listB)


#------------------------------------------------------------------------------------------------------------------------------



def ____get_var_mapping_tuples(var_listA, var_listB, share_var_num):
	"""
		sub-sub-procedure: mapping variable list B to variable list A
	"""
	to_vars_list = list(itertools.permutations(var_listA, share_var_num))
	from_vars_list = list(itertools.combinations(var_listB, share_var_num))
	#print list(to_vars_list)
	#print list(from_vars_list)
	var_mapping_tuple_list = [ (list(from_vars), list(to_vars))  for from_vars in from_vars_list for to_vars in to_vars_list ]
	return var_mapping_tuple_list



def ____get_var_mappings(sort_vars_dictA, sort_vars_dictB, max_var_num):
	"""
		sub-sub-procedure: determined how conjunctB's variables are mapped to conjunctA's
	"""
	# divide variables according to different sorts

	var_mapping_tuple_list = [([],[])]
	# for each sort, determined the mapping between two variable set
	for Asort, Avar_list in sort_vars_dictA.items():
		if Asort in sort_vars_dictB:
			min_share_vars_num = len(Avar_list) + len(sort_vars_dictB[Asort]) - max_var_num
			min_share = max([min_share_vars_num,0])
			max_share = min([len(Avar_list),len(sort_vars_dictB[Asort])])+1
			temp_tuple_list = sum([____get_var_mapping_tuples(Avar_list, sort_vars_dictB[Asort], n) \
				for n in range(min_share, max_share)], list())
			var_mapping_tuple_list = [(a+c,b+d) for (a,b) in var_mapping_tuple_list for (c,d) in temp_tuple_list ]	

	return [ (from_list, to_list) for from_list, to_list in var_mapping_tuple_list]



def ____get_sort_vars_dict(conjunct):
	"""
		sub-sub-procedure: divide variables according to different sorts
	"""
	var_list, sort_list, pred_list = conjunct
	sort_dict = dict()
	sort_list = zip(sort_list, var_list)
	for k, g in groupby(sorted(sort_list, key=itemgetter(0)), key=itemgetter(0)):
		sort_dict[k] = list(zip(*list(g))[1])
	return sort_dict



def __generate_conjunct_mappings(conjunct_listA, conjunct_listB, MAX_VAR):
	"""
		sub-procedure: generate mappings that determine how two conjuncts combine together (about variables)
	"""
	# for each sub-conjunct, first divide variables according to different sorts
	sort_vars_dict_listA = [____get_sort_vars_dict(conjunctA) for conjunctA in conjunct_listA]
	sort_vars_dict_listB = [____get_sort_vars_dict(conjunctB) for conjunctB in conjunct_listB]

	# get mappings on how to combine variables between two conjuncts
	conjunct_mapping_list = [ (conjunct_listA[i], ____get_var_mappings(a, b, MAX_VAR), conjunct_listB[j]) \
		for i, a in enumerate(sort_vars_dict_listA) for j, b in enumerate(sort_vars_dict_listB) ]
	conjunct_mapping_list = [ (s, from_list, to_list, b) for s, m_list, b in conjunct_mapping_list for from_list, to_list in m_list ]
	return conjunct_mapping_list


#------------------------------------------------------------------------------------------------------------------------------

def __rename(conjunct):
	"""
		rename the variables in the conjunct
	"""

	var_list, sort_list, pred_list = conjunct
	if var_list == list():
		return conjunct

	new_var_list = [ 'G%s'%e for e in range(0, len(var_list))]
	rename_var_list = [r'\b' + elem + r'\b' for elem in var_list]

	body_str = "%s"%("&".join(pred_list))
	new_body_str =Util.repeat_do_function(Util.sub_lambda_exp, zip(rename_var_list,new_var_list), body_str)
	new_pred_list =  new_body_str.split('&')

	return (new_var_list, sort_list, new_pred_list)



#------------------------------------------------------------------------------------------------------------------------------




def __get_character_conjuncts(conjunct_list, model_sat_list, model_unsat_list):
	"""
		sub-procedure: return a conjunct list where every conjunct satisfies model_sat_list but falsifies model_unsat_list
	"""
	sat_conjunct_list = [conjunct for conjunct in conjunct_list if model_checker.sat_conjunct(model_sat_list, conjunct)]
	return [conjunct for conjunct in sat_conjunct_list if model_checker.unsat_conjunct(model_unsat_list, conjunct)]



def __get_character_conjunct_indexs(conjunct_list, model_sat_list, model_unsat_list):
	"""
		sub-procedure: return a conjunct index list where every conjunct satisfies model_sat_list but falsifies model_unsat_list
	"""
	sat_conjunct_list = [ (e, conjunct) for e, conjunct in enumerate(conjunct_list) if model_checker.sat_conjunct(model_sat_list, conjunct)]
	return [ e for e, conjunct in sat_conjunct_list if model_checker.unsat_conjunct(model_unsat_list, conjunct)]


#------------------------------------------------------------------------------------------------------------------------------


def generate_conjuncts(subconjunct_list, model_neg_list, model_pos_list, atomic_pred_list, LENGTH, MAX_VAR=3):
	"""
		main-procedure: generate conjuncts based on the sub-conjunct and a set of predicates, 
		the new conjuncts should be under the limitation of maximal number of variables for every sort.

		@param	model_neg_list		the set of models that should new conjuncts satisfy
		@param	model_pos_list		the set of models that should new conjuncts falsify
		@param	LENGTH 				the length of growth for the new conjuncts
		@param 	MAX_VAR 			the maximal number of variables for each sort

		Two stage generation: internal step and final step.
		(1) Internal step: gradually combine sub-conjunct with one more predicate to form longer sub-conjunct 
			and check whether it satisfies the requirement (satisfies all negative models).
		(2) Final step:
			First,divide conjuncts into four categories: 
				A. pure math conjuncts (PM)			--- has variables and all are free
				B. free variable conjuncts (FV) 	--- has variables but some are free, some are not free
				C. not-free variable conjuncts (NFV)--- has variables but all are not free
				D. no variable conjuncts (NV)		--- has no variables
			Second, generate conjuncts according to their categories: 
			-- PM: FV + NFV  (can combine PM with FV or with NFV)
			-- FV: FV + NFV
			-- NFV: PM + FV + NFV + NV 
			-- NV: NFV + NV
			(because we want to reduce the number of conjuncts that are PM, FV)
	"""
	# generate basic conjuncts (only one predicate in a conjunct)
	basic_conjunct_list = [(var_list, sort_list, [pred]) for var_list, sort_list, pred in atomic_pred_list]
	# get those satisfy all negative models
	basic_conjunct_list = __get_character_conjuncts(basic_conjunct_list, model_neg_list, [])

	subconjunct_list = [ __rename(c) for c in  subconjunct_list ]
	# (1) Internal step:
	failure_set = set()
	for step in range(1, LENGTH):

		# generate mappings that determine how two conjuncts combine together
		conjunct_mapping_list = __generate_conjunct_mappings(subconjunct_list, basic_conjunct_list, MAX_VAR)
		# filter mappings that previously fail
		conjunct_mapping_list = conjunct_filter.filter_by_pre_failure(conjunct_mapping_list, failure_set)
		# use mappings to construct new conjuncts
		conjunct_list  =  [ __combine_conjunct(s, b, from_list, to_list) for s, from_list, to_list, b in conjunct_mapping_list]
		print('------Step %s: number of sub-conjunct (%s)'%(step, len(conjunct_list)) )
		# get those conjuncts (index) satisfying all negative models
		sat_conjunct_index_list = __get_character_conjunct_indexs(conjunct_list, model_neg_list, [])
		# from index to conjunct
		subconjunct_list = [ __rename(conjunct_list[e]) for e in sat_conjunct_index_list]
		print('------Step %s: number of sub-conjunct after MC (%s)'%(step, len(subconjunct_list)) )
		# generate failure set
		fail_mapping_list = [conjunct_mapping_list[e] for e in range(0,len(conjunct_mapping_list)) if e not in set(sat_conjunct_index_list)]
		failure_set |= conjunct_filter.build_failure_set(fail_mapping_list)

	# (2) Final step:
	fluent_list = context_operator.get_fluents()
	PM_slist, FV_slist, NFV_slist, NV_slist = conjunct_filter.categorize_conjuncts(subconjunct_list, fluent_list)
	PM_blist, FV_blist, NFV_blist, NV_blist = conjunct_filter.categorize_conjuncts(basic_conjunct_list, fluent_list)

	conjunct_mapping_list = __generate_conjunct_mappings(PM_slist + FV_slist, FV_blist + NFV_blist, MAX_VAR)
	conjunct_mapping_list += __generate_conjunct_mappings(NFV_slist, PM_blist + FV_blist + NFV_blist + NV_blist, MAX_VAR)
	conjunct_mapping_list += __generate_conjunct_mappings(NV_slist,  NFV_blist + NV_blist, MAX_VAR)
	print('------Step %s: number of mappings (%s)'%(LENGTH, len(conjunct_mapping_list)) )
	conjunct_mapping_list = conjunct_filter.filter_by_pre_failure(conjunct_mapping_list, failure_set)
	print('------Step %s: number of mappings after filter (%s)'%(LENGTH, len(conjunct_mapping_list)) )
	conjunct_list  =  [ __combine_conjunct(s, b, from_list, to_list) for s, from_list, to_list, b in conjunct_mapping_list]
	print('------Step %s: number of conjunct (%s)'%(LENGTH, len(conjunct_list)) )
	conjunct_list = conjunct_filter.filter_by_varfree(conjunct_list, fluent_list)
	print('------Step %s: number of conjunct after free-var filter (%s)'%(LENGTH, len(conjunct_list)) )
	conjunct_list = __get_character_conjuncts(conjunct_list, model_neg_list, model_pos_list)
	print('------Step %s: number of conjunct after MC (%s)'%(LENGTH, len(conjunct_list)) )

	return conjunct_list



