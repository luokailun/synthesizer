

import re




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




def detect_varfree_conjuncts(conjunct_list, fluent_list):
	"""
		separate variable free conjuncts (conjuncts that have variable which is not related to any fluent)
	"""
	fluent_str = '|'.join([r'%s\('%fluent for fluent in fluent_list])
	fluent_pattern = re.compile(fluent_str)

	varfree_conjunct_list = [c for c in conjunct_list if __is_varfree_conjunct(c, fluent_pattern)]
	conjunct_list = [c for c in conjunct_list if not __is_varfree_conjunct(c, fluent_pattern)]
	
	#print varfree_conjunct_list
	#use this will largely increase the running time
	#conjunct_list = [c for c in conjunct_list if c not in varfree_conjunct_list]
	return varfree_conjunct_list, conjunct_list




