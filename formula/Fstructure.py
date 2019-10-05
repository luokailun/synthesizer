

###
# The form of Fstructure is: list[(A,B),...], where A is a conjunct, B is a list of models that satisfies A
#
# A conjunct is a tuple (P,Q,R) where P is a list of variable, Q is a list of sorts corresponding to P, and R is 
# a list of relation.
#
# A predicate is a tuple (P,Q,r) where P is a list of variable, Q is a list of sorts corresponding to P, and R is 
# a relation.
#
#



def init(formula, pos_model_list, conjunct_model_list, pred_score_dict):
	return (formula, pos_model_list, conjunct_model_list, pred_score_dict)

##############################################################################################################################

def to_conjuncts(fstructure):
	formula, pos_model_list, conjunct_model_list, pred_score_dict = fstructure
	return [ conjunct for (conjunct, model_list) in conjunct_model_list]

def to_conjunct_models(fstructure):
	formula, pos_model_list, conjunct_model_list, pred_score_dict = fstructure
	return conjunct_model_list



def get_pos_models(fstructure):
	formula, pos_model_list, conjunct_model_list, pred_score_dict = fstructure
	return pos_model_list


def get_pred_score_dict(fstructure):
	formula, pos_model_list, conjunct_model_list, pred_score_dict = fstructure
	return pred_score_dict


##############################################################################################################################

import Conjunct

def to_formula(fstructure):
	#print fstructure
	formula, pos_model_list, conjunct_model_list, pred_score_dict = fstructure
	conjunct_list = [ conjunct for (conjunct, model_list) in conjunct_model_list]
	if conjunct_list ==[]:
		return formula
	else:
		conjunct_str_list = list()
		for conjunct in conjunct_list:
			conjunct_str_list.append('!(%s)'%(Conjunct.to_formula(conjunct)))
		return "(%s)&%s"%(formula, '&'.join(conjunct_str_list))


def printer(fstructure):
	print_list = list()
	formula, pos_model_list, conjunct_model_list, pred_score_dict = fstructure

	print_list.append('#Goal:%s'%formula)
	print_list.append('#(+)model:\n  %s'%('\n  '.join([ str(m) for m in pos_model_list])))
	str_conjunct_models = '\n'.join([ "(%s):%s\n  %s"%(e,c, '\n  '.join([str(m) for m in m_list])) for e, (c, m_list) in enumerate(conjunct_model_list)])
	print_list.append('#conjuncts:\n%s'%str_conjunct_models)
	return '\n'.join(print_list)


##############################################################################################################################	


def delete_conjunct(fstructure, conjunct):
	formula, pos_model_list, conjunct_model_list, pred_score_dict = fstructure
	conjunct_model_list = [(c,m) for (c, m) in conjunct_model_list if c!=conjunct]
	return (formula, pos_model_list, conjunct_model_list, pred_score_dict)



def update(fstructure, replaced_conjunct_list, updated_conjunct, add_model_neg_list, add_model_pos_list):
	formula, pos_model_list, conjunct_model_list, pred_score_dict = fstructure

	updated_model_list = add_model_neg_list
	new_conjunct_model_list = list()

	for e, (conjunct, model_list) in enumerate(conjunct_model_list):
		if conjunct in replaced_conjunct_list:
			updated_model_list += model_list
		else:
			new_conjunct_model_list.append((conjunct, model_list))
	if updated_model_list!=[]:
		new_conjunct_model_list.append((updated_conjunct,updated_model_list))

	return (formula, pos_model_list+add_model_pos_list, new_conjunct_model_list, pred_score_dict)

##############################################################################################################################






'''
conjunctA = (['X3'], ['Int'], ['X3>2'])
conjunctB = (['X1','X2'], ['Int','_S1'], ['X1+X2>1','X1<1'])

fstructure = ('hello', list(), [(conjunctA, list()),(conjunctB, list()) ])
print to_formula(fstructure)
'''


