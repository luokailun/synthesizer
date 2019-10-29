


from formula import Fstructure
from formula import Conjunct
from model import model_checker
import scoring
import backtrack
import copy

from formula import conjunct_filter
from basic import context_operator


def __update_adjacent_conjuncts(fstructure, conjunct, adjacent_list):
	"""
		adding the conjunct with its adjacent conjuncts if they are absent
	"""
	conjunct_structure_list = Fstructure.get_conjunct_structure(fstructure)
	flag_update, neg_model_list = False, None

	for c, m_list, adj_list in conjunct_structure_list:
		if conjunct == c and adj_list is None:
			flag_update = True
			neg_model_list = m_list
	if flag_update:
		new_conjunct_structure = (conjunct, neg_model_list, adjacent_list)
		fstructure = Fstructure.delete_conjuncts(fstructure, [conjunct])
		fstructure = Fstructure.add_conjuncts(fstructure, [new_conjunct_structure])
	return fstructure



def __generate_new_conjuncts(model_neg_list, model_pos_list, atomic_pred_list, LENGTH):
	"""
		generate new conjuncts of limited length

	"""
	print('****** Generate new conjuncts')
	return sum([ Conjunct.generate_conjuncts([([],[],[])], model_neg_list, model_pos_list, atomic_pred_list, l) \
		for l in range(1, LENGTH+1)], list())




def N_update(fstructure, model_minus_list, atomic_pred_list, LENGTH=2):
	
	"""
		 Modify certain conjunct in the fstructure to exclude the model.
		 Note the fstructure can be translated as:  Goal & !(C1 & C2 & C3 ...), 
			where each Ci is of the form exists(X1,X2,...)[P1 & P2 &...].
		
		 @param model_minus_list 		the models need to be excluded
		 @param atomic_pred_list	the set of predicates used to modify conjuncts
	"""
	# get predicates' score for conjunct selection
	pred_score_dict = Fstructure.get_pred_score_dict(fstructure)
	# get the set of conjunct C1, C2,...
	conjunct_list = Fstructure.to_conjuncts(fstructure)
	# get the set of conjunct C1, C2... with M1, M2, where each Mi is a set of models that satisfy Ci
	conjunct_structure_list = Fstructure.get_conjunct_structure(fstructure)
	# get the set of positive models that falsify each conjunct
	model_pos_list = Fstructure.get_pos_models(fstructure)
	# used for possible backtrack
	fstructure_copy = copy.deepcopy(fstructure)

	candicate_conjuncts_list = list()
	for e, (conjunct, model_neg_list, adjacent_list) in enumerate(conjunct_structure_list):
		# first check whether the adjacent_list is None,  if so generate adjacent conjuncts for the new new conjunct
		adjacent_list = Conjunct.generate_adjacent_conjuncts(conjunct, model_neg_list, model_pos_list, atomic_pred_list, LENGTH) if adjacent_list is None else adjacent_list
		# update structure if generating new adjacent conjuncts 
		fstructure = __update_adjacent_conjuncts(fstructure, conjunct, adjacent_list)
		# used for possible backtrack
		fstructure_copy = __update_adjacent_conjuncts(fstructure_copy, conjunct, adjacent_list)
		# filter adjacent conjuncts by using the model
		candicate_conjuncts_list += Conjunct.get_characteristic_conjuncts(adjacent_list, model_minus_list, [])
	# generate new conjuncts of length 2
	candicate_conjuncts_list += __generate_new_conjuncts(model_minus_list, model_pos_list, atomic_pred_list, LENGTH)
	# sort and get one modified conjunct and replace the old one.
	scoring_conjunct_dict = scoring.compute_conjuncts_score(candicate_conjuncts_list, pred_score_dict)
	updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict, model_pos_list)
	
	if updated_conjunct is None:
		print('\n***** Long update ***** \n')
		candicate_conjuncts_list =  Conjunct.generate_conjuncts([([],[],[])], model_minus_list, model_pos_list, atomic_pred_list, 3)
		if candicate_conjuncts_list ==list():
			print('***** Local update fails ')
			return None
		else:
			scoring_conjunct_dict = scoring.compute_conjuncts_score(candicate_conjuncts_list, pred_score_dict)
			updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict, model_pos_list)
	"""
		modify the fstructure by the updated_conjunct
	"""
	# find the conjunct that need to be replaced
	old_conjunct_list = Fstructure.find_repl_conjuncts(fstructure, updated_conjunct)
	print('***** Change %s ---> %s \n'%(' and '.join([Conjunct.to_formula(c) for c in old_conjunct_list]), Conjunct.to_formula(updated_conjunct)))
	# find the negative models for the new updated conjunct
	updated_model_list = model_minus_list + Fstructure.get_update_model_list(fstructure, old_conjunct_list, updated_conjunct)
	fstructure = Fstructure.delete_conjuncts(fstructure, old_conjunct_list )
	fstructure = Fstructure.add_conjuncts(fstructure, [(updated_conjunct, updated_model_list, None)])
	# store the choice for possible backtrack
	backtrack.store_choice(fstructure_copy, [(model_minus_list, scoring_conjunct_dict)])
	return fstructure



def P_update(fstructure, model_plus_list, atomic_pred_list, LENGTH=2):
	"""
	"""
	pred_score_dict = Fstructure.get_pred_score_dict(fstructure)
	conjunct_structure_list = Fstructure.get_conjunct_structure(fstructure)
	model_pos_list = Fstructure.get_pos_models(fstructure)

	new_model_pos_list = model_pos_list + model_plus_list
	# used for possible backtrack
	fstructure_copy, choice_copy = copy.deepcopy(fstructure), list()
	
	for num, (conjunct, model_neg_list, adjacent_list) in enumerate(conjunct_structure_list):
		# first check whether we need to update the conjunct by the new model
		if model_checker.unsat_conjunct_math(model_plus_list, conjunct) is False:
			# first check whether the adjacent_list is None,  if so generate adjacent conjuncts for the new new conjunct
			adjacent_list = Conjunct.generate_adjacent_conjuncts(conjunct, model_neg_list, model_pos_list, atomic_pred_list, LENGTH) if adjacent_list is None else adjacent_list
			# update structure if generating new adjacent conjuncts 
			fstructure = __update_adjacent_conjuncts(fstructure, conjunct, adjacent_list)
			fstructure_copy = __update_adjacent_conjuncts(fstructure_copy, conjunct, adjacent_list)
			# filter the adjacent adjacent conjuncts by the positive model
			candicate_conjunct_list = Conjunct.get_characteristic_conjuncts(adjacent_list, [], model_plus_list)
			scoring_conjunct_dict = scoring.compute_conjuncts_score(candicate_conjunct_list, pred_score_dict)
			updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict, new_model_pos_list)
			# store the choice for possible backtrack
			choice_copy.append((model_plus_list, scoring_conjunct_dict))

			if updated_conjunct is None:
				print('****** Delete conjunct %s \n'%( Conjunct.to_formula(conjunct)))
				fstructure = Fstructure.delete_conjuncts(fstructure, [conjunct])
			else:
				print('****** Change %s ---> %s \n'%(Conjunct.to_formula(conjunct), Conjunct.to_formula(updated_conjunct)))
				fstructure = Fstructure.delete_conjuncts(fstructure, [conjunct])
				fstructure = Fstructure.add_conjuncts(fstructure, [(updated_conjunct, model_neg_list, adjacent_list)])
		else:
		# else mark that this conjunct does not need to do update
			choice_copy.append((model_plus_list, None))
	# store the choice for possible backtrack
	backtrack.store_choice(fstructure_copy, choice_copy)
	return Fstructure.add_positive_models(fstructure, model_plus_list)








