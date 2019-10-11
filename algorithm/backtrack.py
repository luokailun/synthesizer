

'''
	cStructure: 
	(fstructure1, [scoring_conjunct_dict, scoring_conjunct_dict,...]])
	(fstructure2, [scoring_conjunct_dict, scoring_conjunct_dict,...])

'''

import scoring
from formula import Fstructure
from formula import Conjunct
import copy
import global_structure
import restart
#restart.store_two_state_conjuncts(two_state_structure)


def init_choice():
	"""
	"""
	global_structure.CHOICE['type'] = ""
	global_structure.CHOICE['q1'] = False
	global_structure.CHOICE['q2'] = False



def store_choice(fstructure, choice_stucture):

	if global_structure.CHOICE['q1'] is True:
		global_structure.CHOICE['q1'] = (fstructure, choice_stucture)
	elif global_structure.CHOICE['q2'] is True:
		global_structure.CHOICE['q2'] = (fstructure, choice_stucture)
	else:
		print '???'
		print 
		print global_structure.CHOICE['q1']
		print
		print global_structure.CHOICE['q2']
		print('WAHT????')
		exit(0)


def set_update(update_type, update_state):
	global_structure.CHOICE['type']  = update_type
	global_structure.CHOICE[update_state] = True


##############################################################################################################################



def __backtrack_P_update(fstructure, choice_list):
	conjunct_structure_list = Fstructure.get_conjunct_structure(fstructure)
	model_pos_list = Fstructure.get_pos_models(fstructure)
	# store the choice for possible backtrack
	fstructure_copy = copy.deepcopy(fstructure)
	new_choice_list = list()
	for e, (conjunct, model_neg_list, adj_list) in enumerate(conjunct_structure_list):
		model_plus_list, scoring_conjunct_dict = choice_list[e]
		if model_plus_list is None:
			new_choice_list.append((None, None))
		else:
			new_model_pos_list = model_pos_list + model_plus_list
			updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict, new_model_pos_list)
			new_choice_list.append((model_plus_list, scoring_conjunct_dict))
			if updated_conjunct is None:
				print('****** Delete conjunct %s \n'%( Conjunct.to_formula(conjunct)))
				fstructure = Fstructure.delete_conjuncts(fstructure, [conjunct])
			else:
				fstructure = Fstructure.delete_conjuncts(fstructure, [conjunct])
				fstructure = Fstructure.add_conjuncts(fstructure, [(updated_conjunct, model_neg_list, None)])
				print('****** Change %s ---> %s \n'%(Conjunct.to_formula(conjunct), Conjunct.to_formula(updated_conjunct)))

	store_choice(fstructure_copy, new_choice_list)
	return Fstructure.add_positive_models(fstructure, model_plus_list)




def __backtrack_N_update(fstructure, choice_list):
	model_pos_list = Fstructure.get_pos_models(fstructure)
	model_minus_list, scoring_conjunct_dict = choice_list.pop(0)
	updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict, model_pos_list)
	# store for backtrack
	fstructure_copy = copy.deepcopy(fstructure)
	store_choice(fstructure_copy, [(model_minus_list, scoring_conjunct_dict)])
	# find the conjunct that need to be replaced
	print "('***** Find update conjunct: %s"%(str(updated_conjunct))
	old_conjunct_list = Fstructure.find_repl_conjuncts(fstructure, updated_conjunct)
	print('***** Change %s ---> %s \n'%(' and '.join([Conjunct.to_formula(c) for c in old_conjunct_list]), Conjunct.to_formula(updated_conjunct)))
	# find the negative models for the new updated conjunct
	updated_model_list = model_minus_list + Fstructure.get_update_model_list(fstructure, old_conjunct_list, updated_conjunct)
	fstructure = Fstructure.delete_conjuncts(fstructure, old_conjunct_list )
	fstructure = Fstructure.add_conjuncts(fstructure, [(updated_conjunct, updated_model_list, None)])
	return fstructure




def backtrack(two_state_structure):

	fstructure1, fstructure2 = two_state_structure

	if global_structure.CHOICE['type'] == 'N':
		apply_function = __backtrack_N_update
	elif global_structure.CHOICE['type'] == 'P':
		apply_function = __backtrack_P_update
	else:
		print('Error for backtrack!!!')
		exit(0)

	# redo for state q1
	if global_structure.CHOICE['q1'] is False:
		print('q1 does not need to backtrack')
	elif global_structure.CHOICE['q1'] is True:
		print('Error for backtrack!!!')
		exit(0)
	else:
		
		fstructure1_bk, choice_list1 =  global_structure.CHOICE['q1']
		set_update(global_structure.CHOICE['type'], 'q1')
		# redoing N/P update again by updating 
		fstructure1 = apply_function(fstructure1_bk, choice_list1)
	# redo for state q2
	if global_structure.CHOICE['q2'] is False:
		print('q2 does not need to backtrack')
	elif global_structure.CHOICE['q2'] is True:
		print('Error for backtrack!!!')
		exit(0)
	else:
		fstructure2_bk, choice_list2 =  global_structure.CHOICE['q2']
		set_update(global_structure.CHOICE['type'], 'q2')
		# redoing N/P update again by updating 
		fstructure2 = apply_function(fstructure2_bk, choice_list2)
	# record for possible restart
	restart.store_two_state_conjuncts((fstructure1, fstructure2))
	return (fstructure1, fstructure2)


