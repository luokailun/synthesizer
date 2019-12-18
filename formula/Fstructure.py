

"""
The form of Fstructure is a tuple (F1, F2, F3, F4), where:
	F1 is a goal formula
	F2 is a set of positive models
	F3 is a set of conjuncts with the corresponding negative models and adjacent conjuncts (we call conjunct structure)
	F4 is a set of predicates with score

A conjunct is a tuple (P,Q,R) where P is a list of variable, Q is a list of sorts corresponding to P, 
and R is a list of relation.

A predicate is a tuple (P,Q,r) where P is a list of variable, Q is a list of sorts corresponding to P, 
and R is a relation.

"""



def init(formula, pos_model_list, conjunct_structure_list, pred_score_dict):
	return (formula, pos_model_list, conjunct_structure_list, pred_score_dict)

##############################################################################################################################

import Conjunct

def to_formula(fstructure):
	#print fstructure
	formula, pos_model_list, conjunct_structure_list, pred_score_dict = fstructure
	conjunct_list = [ conjunct for (conjunct, model_list, adjacent_list) in conjunct_structure_list]
	if conjunct_list ==[]:
		return formula
	else:
		conjunct_str_list = list()
		for conjunct in conjunct_list:
			conjunct_str_list.append('!(%s)'%(Conjunct.to_formula(conjunct)))
		return "(%s)&%s"%(formula, '&'.join(conjunct_str_list))


def to_formula_list(fstructure):
	"""
	return a list of formula
	"""
	formula, pos_model_list, conjunct_structure_list, pred_score_dict = fstructure
	conjunct_list = [ conjunct for (conjunct, model_list, adjacent_list) in conjunct_structure_list]
	formula_list = [formula]
	if conjunct_list ==[]:
		return formula_list
	else:
		for conjunct in conjunct_list:
			formula_list.append('!(%s)'%(Conjunct.to_formula(conjunct)))
		return formula_list


def to_conjuncts(fstructure):
	formula, pos_model_list, conjunct_structure_list, pred_score_dict = fstructure
	return [ conjunct for (conjunct, model_list, adjacent_list) in conjunct_structure_list]


def get_conjunct_structure(fstructure):
	formula, pos_model_list, conjunct_structure_list, pred_score_dict = fstructure
	return conjunct_structure_list



def get_pos_models(fstructure):
	formula, pos_model_list, conjunct_structure_list, pred_score_dict = fstructure
	return pos_model_list


def get_pred_score_dict(fstructure):
	formula, pos_model_list, conjunct_structure_list, pred_score_dict = fstructure
	return pred_score_dict


##############################################################################################################################

from basic import format_output

def printer(fstructure):
	print_list = list()
	formula, pos_model_list, conjunct_structure_list, pred_score_dict = fstructure
	print_list.append('#Goal:%s'%formula)
	print_list.append('#(+)model:\n  %s\n%s'%('\n  '.join([ str(m) for m in pos_model_list]), 
		format_output.format_outputs(pos_model_list, 'Ch')))
	str_conjunct_models = '\n'.join([ "(%s):%s\n  %s\n%s"%(e,c, '\n  '.join([str(m) for m in m_list]), 
		 format_output.format_outputs(m_list, 'Ch') ) for e, (c, m_list, adj_list) in enumerate(conjunct_structure_list)])
	print_list.append('#conjuncts:\n%s'%str_conjunct_models)
	return '\n'.join(print_list)


##############################################################################################################################	



def delete_conjuncts(fstructure, conjunct_list):
	formula, pos_model_list, conjunct_structure_list, pred_score_dict = fstructure
	conjunct_structure_list = [ (c ,m_list, adj_list) for (c ,m_list, adj_list) in conjunct_structure_list if c not in conjunct_list]
	return (formula, pos_model_list, conjunct_structure_list, pred_score_dict)


def add_conjuncts(fstructure, conjunct_structures):
	formula, pos_model_list, conjunct_structure_list, pred_score_dict = fstructure
	conjunct_structure_list.extend(conjunct_structures)
	return fstructure


##############################################################################################################################

def get_update_model_list(fstructure, old_conjunct_list, new_conjunct):
	"""
		merge all the models that come from conjuncts need to be modified
	"""
	conjunct_structure_list = get_conjunct_structure(fstructure)
	updated_model_list = list()
	for conjunct, model_list, adjacent_list in conjunct_structure_list:
		if conjunct in old_conjunct_list:
			updated_model_list += model_list
	return updated_model_list


##############################################################################################################################

def find_repl_conjuncts(fstructure, target_conjunct):
	"""
		find conjuncts that need to be replaced by the new conjunct
		@param	conjunct_structure_list	    storing tuple of conjunct, negative models and all the adjacent conjuncts
		@param	target_conjunct 			the new conjunct
	"""
	conjunct_structure_list = get_conjunct_structure(fstructure)
	repl_conjunct_list = list()
	for (c, m_list, adj_list) in conjunct_structure_list:
		if target_conjunct in adj_list:
			repl_conjunct_list.append(c)
	return repl_conjunct_list


##############################################################################################################################

def add_positive_models(fstructure, model_list):
	formula, pos_model_list, conjunct_structure_list, pred_score_dict = fstructure
	pos_model_list.extend(model_list)
	return fstructure

##############################################################################################################################






'''
conjunctA = (['X3'], ['Int'], ['X3>2'])
conjunctB = (['X1','X2'], ['Int','_S1'], ['X1+X2>1','X1<1'])

fstructure = ('hello', list(), [(conjunctA, list()),(conjunctB, list()) ])
print to_formula(fstructure)
'''


