


"""
	
	Xconjunct has the form \exists P1 or P2 or ... or Pn
	
	A Xconjunct structure has the form (X, Y, M-, M+), where 
		--- X is the Xconjucnt
		--- Y is a set of predicates
		--- M- is a set of models that X \models
		--- M+ is a set of models that X \nvDash

"""

from model import model_checker
from basic import context_operator
from operator import itemgetter 
from itertools import groupby
from basic import Util


##############################################################################################################################################################

def get_characteristic_conjuncts(conjunct_list, model_sat_list, model_unsat_list):
	"""
		main-procedure: return a conjunct list where every conjunct satisfies model_sat_list but falsifies model_unsat_list
	"""
	sat_conjunct_list = [conjunct for conjunct in conjunct_list if model_checker.sat_conjunct(model_sat_list, conjunct, '|')]
	return [conjunct for conjunct in sat_conjunct_list if model_checker.unsat_conjunct(model_unsat_list, conjunct, '|')]



def get_characteristic_conjunct_indexs(conjunct_list, model_sat_list, model_unsat_list):
	"""
		sub-procedure: return a conjunct index list where every conjunct satisfies model_sat_list but falsifies model_unsat_list
	"""
	sat_conjunct_list = [ (e, conjunct) for e, conjunct in enumerate(conjunct_list) if model_checker.sat_conjunct(model_sat_list, conjunct, '|')]
	return [ e for e, conjunct in sat_conjunct_list if model_checker.unsat_conjunct(model_unsat_list, conjunct, '|')]



##############################################################################################################################################################


def unify_conjuncts(conjunct_list):
	"""
	unify the variables in conjunct in the same rename way

	pred_list = [(['Y10', 'Y11', 'K11'], ['Int', 'Int', '_S1'], ['Y10 > Y11 and K11=empty'])]
	print __unify_conjuncts(pred_list)
	"""
	sorts = context_operator.get_sort_symbols_dict().keys()
	sort_var = {sort:chr(ord('U')+e) for e, sort in enumerate(sorts)} 

	new_conjunct_list = list()
	for (var_list, sort_list, pred_list) in conjunct_list:

		if var_list == list():
			new_conjunct_list.append((var_list, sort_list, pred_list))
			continue
		# first collect variables of the same sorted
		sort_dict = dict()
		sort_var_list = zip(sort_list, var_list)
		for k, g in groupby(sorted(sort_var_list, key=itemgetter(0)), key=itemgetter(0)):
			sort_dict[k] = list(zip(*list(g))[1])

		# replace old variables with new variables
		new_pred_str = '&'.join(pred_list)
		for sort, old_var_list in sort_dict.items():
			var_sym = sort_var[sort]
			# generate new variables for the same sort
			old_var_list = [r'\b%s\b'%(var) for var in old_var_list]
			new_var_list = ['%s%s'%(var_sym, str(e)) for e, var in enumerate(old_var_list)]
			new_pred_str = Util.repeat_do_function(Util.sub_lambda_exp, zip(old_var_list, new_var_list), new_pred_str)
			new_pred_list = new_pred_str.split('&')

		#print(new_var_list, sort_list, new_pred_list)
		new_conjunct_list.append((new_var_list, sort_list, new_pred_list))

	return new_conjunct_list

##############################################################################################################################################################


def __get_sat_subconjuncts(conjunct, model_list, length):
	"""
		sub-procedure:
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
			subconjunct_list.append( ____refresh_vars((var_list, sort_list, rest_preds))) 
	return subconjunct_list


def __refresh_vars(conjunct):
	"""
		sub-sub-procedure:	delete redundant variables

	If k = (['X','Y'], ['Int','Int'],['! numStone() = X']) , 
	then ____refresh_vars(k) will return  (['X'], ['Int'], ['! numStone() = X'])

	"""
	var_list, sort_list, pred_list = conjunct
	new_var_list, new_sort_list = list(),list()
	preds_str = '&'.join(pred_list)
	for e, var in enumerate(var_list):
		if re.search(r'\b%s\b'%var, preds_str):
			new_var_list.append(var)
			new_sort_list.append(sort_list[e])
	return (new_var_list, new_sort_list, pred_list)


def __combine(xconjunctA, xconjunctB):
	var_listA, sort_listA, pred_listA = xconjunctA
	var_listB, sort_listB, pred_listB = xconjunctB

	if var_listA == list() or var_listB == list():
		return (var_listA + var_listB, sort_listA + sort_listB, pred_listA + pred_listB)
	else:
		var_sort_dict = dict(zip(var_listA, sort_listA))
		var_sort_dict.update(dict(zip(var_listB, sort_listB)))
		var_list, sort_list = zip(*var_sort_dict.items())

		return (list(var_list), list(sort_list), pred_listA+ pred_listB)





def generate_conjunct(xconjunct, model_list, model_pos_list, basic_conjunct_list, LENGTH = 2):
	"""
		generate new conjunct list such that the new conjuncts characterize 
			(model_list vs model_pos_list)

		xconjunct \nvDash model_list => xconjunct \models model_list
		xconjunct \nvDash model_pos_list => xconjunct \nvDash model_pos_list
	"""
	if LENGTH == 0:
		return list()
	else:
		new_conjunct_list = [__combine(xconjunct, conjunct) for conjunct in basic_conjunct_list]
		sat_index_set = set(get_characteristic_conjunct_indexs(new_conjunct_list, model_list, model_pos_list))
		sat_conjunct_list = [new_conjunct_list[e] for e in range(0,len(new_conjunct_list)) if e in sat_index_set]
		unsat_conjunct_list = [new_conjunct_list[e] for e in range(0,len(new_conjunct_list)) if e not in sat_index_set]

		for unsat_conjunct in unsat_conjunct_list:
			sat_conjunct_list+= generate_conjunct(unsat_conjunct, model_list, model_pos_list, basic_conjunct_list, LENGTH-1)

		return sat_conjunct_list 



def P_update(xconjunct, model_list, model_neg_list, model_pos_list, basic_conjunct_list, LENGTH = 2):
	"""
		Exclude models 
		Note that basic_conjunct_list and xconjunct must be in an unified form
	"""
	basic_conjunct_list = set(get_characteristic_conjunct(basic_conjunct_list, [], model_list))

	# C = P1 \/ P2 \/ P3...  if there exists Pi \models M, then C \models M
	
	var_list, sort_list, pred_list = xconjunct
	pred_feature_set = set(sum([p_list for v_list, s_list, p_list in basic_conjunct_list],list()))
	new_pred_list = [pred for pred in pred_list if pred in pred_feature_set]
	sub_xconjunct = __refresh_vars((var_list, sort_list, new_pred_list))

	modified_len = LENGTH - (len(pred_list)- len(new_pred_list))
	sub_xconjunct_list = __get_sat_subconjuncts(sub_xconjunct, list(), modified_len) if modified_len>0 else [sub_xconjunct]

	new_conjunct_list = list()
	for sub_xconjunct in sub_xconjunct_list:
		new_conjunct_list += generate_conjunct(sub_xconjunct, model_neg_list, model_pos_list+model_list, LENGTH)

	return new_conjunct_list




#def N_update(xonjucnt, model_list, model_neg_list, model_pos_list, basic_conjunct_list, LENGTH =2 ):






	

