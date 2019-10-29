

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


def ____detect_only_delete(fstructure, new_fstructure):
	"""
		detect only delete action occur after backtrack
	"""
	conjunct_list = Fstructure.to_conjuncts(fstructure)
	new_conjunct_list = Fstructure.to_conjuncts(new_fstructure)

	if len(new_conjunct_list) == len(conjunct_list):
		return False
	else:
		for conjunct in new_conjunct_list:
			if conjunct not in conjunct_list:
				return False
	return True


def __backtrack_P_update(fstructure, choice_list):
	conjunct_structure_list = Fstructure.get_conjunct_structure(fstructure)
	model_pos_list = Fstructure.get_pos_models(fstructure)
	# store the choice for possible backtrack
	fstructure_copy = copy.deepcopy(fstructure)
	new_choice_list = list()
	for e, (conjunct, model_neg_list, adj_list) in enumerate(conjunct_structure_list):
		model_plus_list, scoring_conjunct_dict = choice_list[e]
		if scoring_conjunct_dict is None:
			new_choice_list.append((model_plus_list, None))
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
	# check whether there is only "delete" operation was occurred such that the new and old fstructure is the same
	if ____detect_only_delete(fstructure_copy, fstructure) is True:
		print "----------P update backtrack fails (only delete)-------------\n"
		return None
	else:
		fstructure =  Fstructure.add_positive_models(fstructure, model_plus_list)
		return fstructure




def __backtrack_N_update(fstructure, choice_list):
	model_pos_list = Fstructure.get_pos_models(fstructure)
	model_minus_list, scoring_conjunct_dict = choice_list.pop(0)
	#print 'bbbbbbbtttttt', scoring_conjunct_dict
	updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict, model_pos_list)
	if updated_conjunct is not None:
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
	else:
		print "----------N update backtrack fails-------------\n"
		return None




def backtrack(two_state_structure):

	fstructure1, fstructure2 = two_state_structure

	# previously do N update or P update
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
		# how to detect similar update???	
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
		'''
		# how to detect similar update???
		if cmp(fstructure2_bk, fstructure2) == 0:
			print "\n-------------Similar update! do restart!\n"
			fstructure2 = None
		else:
			fstructure2 = fstructure2_bk
		'''

	# if the backtrack is not failed
	if fstructure1 is not None and fstructure2 is not None:
		# record for possible restart
		restart.store_two_state_conjuncts((fstructure1, fstructure2))
	return (fstructure1, fstructure2)


