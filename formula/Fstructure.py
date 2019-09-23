

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



def init(formula, pos_model_list, conjunct_model_list):
	return (formula, pos_model_list, conjunct_model_list)



def to_conjuncts(fstructure):
	formula, pos_model_list, conjunct_model_list = fstructure
	return [ conjunct for (conjunct, model_list) in conjunct_model_list]

def to_conjunct_models(fstructure):
	formula, pos_model_list, conjunct_model_list = fstructure
	return conjunct_model_list


def to_formula(fstructure):
	formula, pos_model_list, conjunct_model_list = fstructure
	conjunct_list = [ conjunct for (conjunct, model_list) in conjunct_model_list]
	if conjunct_list ==[]:
		return formula
	else:
		conjunct_str_list = list()
		for (var_list, sort_list, pred_list) in conjunct_list:
			if var_list !=list():
				conjunct_str_list.append("!exists(%s)[%s]"%(','.join([ "%s:%s"%(var,sort) for var,sort in zip(var_list,sort_list)]), \
					'&'.join(pred_list)))
			else:
				conjunct_str_list.append('!(%s)'%('&'.join(pred_list)))
		return "(%s)&%s"%(formula, '&'.join(conjunct_str_list))



def get_pos_models(fstructure):
	formula, pos_model_list, conjunct_model_list = fstructure
	return pos_model_list



def delete_conjunct(fstructure, conjunct):
	formula, pos_model_list, conjunct_model_list = fstructure
	conjunct_model_list = [(c,m) for (c, m) in conjunct_model_list if c!=conjunct]
	return (formula, pos_model_list, conjunct_model_list)




def update(fstructure, replaced_conjunct_list, updated_conjunct, add_model_neg_list, add_model_pos_list):
	formula, model_pos_list, conjunct_model_list = fstructure

	updated_model_list = add_model_neg_list
	new_conjunct_model_list = list()

	for e, (conjunct, model_list) in enumerate(conjunct_model_list):
		if conjunct in replaced_conjunct_list:
			updated_model_list += model_list
		else:
			new_conjunct_model_list.append((conjunct, model_list))
	if updated_model_list!=[]:
		new_conjunct_model_list.append((updated_conjunct,updated_model_list))

	return (formula, model_pos_list+add_model_pos_list, new_conjunct_model_list)


'''
conjunctA = (['X3'], ['Int'], ['X3>2'])
conjunctB = (['X1','X2'], ['Int','_S1'], ['X1+X2>1','X1<1'])

fstructure = ('hello', list(), [(conjunctA, list()),(conjunctB, list()) ])
print to_formula(fstructure)
'''


