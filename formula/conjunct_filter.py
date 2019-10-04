

import re
import cPickle as pickle


########################################################################################################################


def __is_varfree_conjunct(conjunct, fluent_pattern):
	"""
		tell whether the conjunct has free variable (do not correlate to any fluent)
	"""
	var_list, sort_list, pred_list = conjunct
	fluent_conjunct_str = '&'.join([pred for pred in pred_list if fluent_pattern.search(pred)])
	for var in var_list:
		if fluent_conjunct_str.find(var) == -1:
			return True
	return False




def detect_varfree_conjunct_index(conjunct_list, fluent_list):
	"""
		separate variable free conjuncts (conjuncts that have variable which is not related to any fluent)
	"""
	fluent_str = '|'.join([r'%s\('%fluent for fluent in fluent_list])
	fluent_pattern = re.compile(fluent_str)

	varfree_conjunct_index_list = [e for e, c in enumerate(conjunct_list) if __is_varfree_conjunct(c, fluent_pattern)]
	#conjunct_list = [c for c in conjunct_list if not __is_varfree_conjunct(c, fluent_pattern)]

	#print varfree_conjunct_list
	#use this will largely increase the running time
	#conjunct_list = [c for c in conjunct_list if c not in varfree_conjunct_list]
	return varfree_conjunct_index_list


def filter_by_varfree(conjunct_list, fluent_list):
	"""
		filter conjuncts which have free variables  (conjuncts that have variable which is not related to any fluent)
	"""
	fluent_str = '|'.join([r'%s\('%fluent for fluent in fluent_list])
	fluent_pattern = re.compile(fluent_str)

	return [c for c in conjunct_list if not __is_varfree_conjunct(c, fluent_pattern)]


########################################################################################################################


def build_failure_set(mapping_list):
	return set([ pickle.dumps((f_list, t_list, b)) for s, f_list, t_list, b in mapping_list])



def filter_by_pre_failure(mapping_list, failure_set):
	if failure_set == set():
		return mapping_list
	else:
		feature_list = [ pickle.dumps((f_list, t_list, b)) for s, f_list, t_list, b in mapping_list]
		return [ m for e, m in enumerate(mapping_list) if feature_list[e] not in failure_set ]


########################################################################################################################



def categorize_conjuncts(conjunct_list, fluent_list):
	"""
	divide conjuncts into four categories: 
		A. pure math conjuncts (PM)			--- has variables and all are free
		B. free variable conjuncts (FV) 	--- has variables but some are free, some are not free
		C. not-free variable conjuncts (NFV)--- has variables but all are not free
		D. no variable conjuncts (NV)		--- has no variables

	"""
	NV_index_list = [ e for e, (var_list, sort_list, pred_list) in enumerate(conjunct_list) if var_list ==list()]
	NV_list = [conjunct_list[e] for e in NV_index_list]

	conjunct_list = [ conjunct_list[e] for e in range(0, len(conjunct_list)) if e not in set(NV_index_list)]

	fluent_str = '|'.join([r'%s\('%fluent for fluent in fluent_list])
	fluent_pattern = re.compile(fluent_str)
	PM_index_list = [ e for e, (var_list, sort_list, pred_list) in enumerate(conjunct_list) if not fluent_pattern.search('&'.join(pred_list))]
	PM_list = [conjunct_list[e] for e in PM_index_list]

	conjunct_list = [ conjunct_list[e] for e in range(0, len(conjunct_list)) if e not in set(PM_index_list)]

	FV_index_list = detect_varfree_conjunct_index(conjunct_list, fluent_list)
	FV_list = [conjunct_list[e] for e in FV_index_list]

	NFV_list = [conjunct_list[e] for e in range(0, len(conjunct_list)) if e not in set(FV_index_list)]

	return PM_list, FV_list, NFV_list, NV_list




########################################################################################################################