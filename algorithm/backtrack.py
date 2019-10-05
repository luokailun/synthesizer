

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


def init_choice(fstructure1, fstructure2, update_type):
	"""
	"""
	global_structure.CHOICE = dict()
	global_structure.CHOICE['type'] = update_type
	global_structure.CHOICE['q1'] = (copy.deepcopy(fstructure1), list())
	global_structure.CHOICE['q2'] = (copy.deepcopy(fstructure2), list())


def store_choice(fstructure, model, candicate_conjuncts_dict, scoring_conjunct_dict):

	if cmp(global_structure.CHOICE['q1'][0], fstructure) == 0:
		global_structure.CHOICE['q1'][1].append((model, candicate_conjuncts_dict, scoring_conjunct_dict))
	elif cmp(global_structure.CHOICE['q2'][0], fstructure) == 0:
		global_structure.CHOICE['q2'][1].append((model, candicate_conjuncts_dict, scoring_conjunct_dict))
	else:
		print '???'
		print fstructure
		print 
		print global_structure.CHOICE['q1'][0]
		print
		print global_structure.CHOICE['q2'][0]
		print('WAHT????')
		exit(0)

##############################################################################################################################


def __find_repl_conjuncts(candicate_conjuncts_dict, conjunct_list, target_conjunct):
	"""
		find conjuncts that need to be replaced by the new conjunct
		@param	candicate_conjuncts_dict	storing all the adjacent conjuncts
		@param	conjunct_list 				the original conjuncts
		@param	target_conjunct 			the new conjunct
	"""
	repl_conjunct_list = list()
	for (e, elist) in candicate_conjuncts_dict.iteritems():
		if target_conjunct in elist:
			repl_conjunct_list.append(conjunct_list[e])
	return repl_conjunct_list




def backtrack():
	org_fstructure1, choice_list1 =  global_structure.CHOICE['q1']
	org_fstructure2, choice_list2 =  global_structure.CHOICE['q2']
	fstructure1 = copy.deepcopy(org_fstructure1)
	fstructure2 = copy.deepcopy(org_fstructure2)
	if global_structure.CHOICE['type'] == 'N':
		#for key, structure in global_structure.CHOICE.items():
		#	if key!='type' and structure!=list():
		if choice_list1!=list():
			model_pos_list = Fstructure.get_pos_models(fstructure1)
			model_minus, candicate_conjuncts_dict, scoring_conjunct_dict = choice_list1.pop(0)

			updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict, model_pos_list)
			store_choice(org_fstructure1, model_minus, candicate_conjuncts_dict, scoring_conjunct_dict)

			old_conjunct_list = __find_repl_conjuncts(candicate_conjuncts_dict, Fstructure.to_conjuncts(fstructure1), updated_conjunct)
			print('***** Change %s ---> %s \n'%(' and '.join([Conjunct.to_formula(c) for c in old_conjunct_list]), Conjunct.to_formula(updated_conjunct)))
			fstructure1 = Fstructure.update(fstructure1, old_conjunct_list, updated_conjunct, [model_minus], [])

		if choice_list2!=list():
			model_pos_list = Fstructure.get_pos_models(fstructure2)
			model_minus, candicate_conjuncts_dict, scoring_conjunct_dict = choice_list2.pop(0)

			updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict, model_pos_list)
			store_choice(org_fstructure2, model_minus, candicate_conjuncts_dict, scoring_conjunct_dict)

			old_conjunct_list = __find_repl_conjuncts(candicate_conjuncts_dict, Fstructure.to_conjuncts(fstructure2), updated_conjunct)
			print('***** Change %s ---> %s \n'%(' and '.join([Conjunct.to_formula(c) for c in old_conjunct_list]), Conjunct.to_formula(updated_conjunct)))
			fstructure2 = Fstructure.update(fstructure2, old_conjunct_list, updated_conjunct, [model_minus], [])

		return (fstructure1, fstructure2)

	if global_structure.CHOICE['type'] == 'P':
		if choice_list1!=list():
			model_plus, candicate_conjuncts_dict, scoring_conjunct_dict = choice_list1.pop(0)
			conjunct_model_list = Fstructure.to_conjunct_models(fstructure1)
			model_pos_list = Fstructure.get_pos_models(fstructure1)

			new_model_pos_list = model_pos_list + [model_plus]
			for num, (conjunct, model_neg_list) in enumerate(conjunct_model_list):
				updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict, new_model_pos_list)
				# store the choice for possible backtrack
				store_choice(org_fstructure1, model_plus, None, scoring_conjunct_dict)
				print('****** Change %s ---> %s \n'%(Conjunct.to_formula(conjunct), Conjunct.to_formula(updated_conjunct)))
				fstructure1 = Fstructure.update(fstructure1, [conjunct], updated_conjunct, [], [])

			fstructure1 = Fstructure.update(fstructure1, [], [], [], [model_plus])

		if choice_list2!=list():
			model_plus, candicate_conjuncts_dict, scoring_conjunct_dict = choice_list2.pop(0)
			conjunct_model_list = Fstructure.to_conjunct_models(fstructure2)
			model_pos_list = Fstructure.get_pos_models(fstructure2)

			new_model_pos_list = model_pos_list + [model_plus]
			for num, (conjunct, model_neg_list) in enumerate(conjunct_model_list):
				updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict, new_model_pos_list)
				# store the choice for possible backtrack
				store_choice(org_fstructure2, model_plus, None, scoring_conjunct_dict)
				print('****** Change %s ---> %s \n'%(Conjunct.to_formula(conjunct), Conjunct.to_formula(updated_conjunct)))
				fstructure2 = Fstructure.update(fstructure2, [conjunct], updated_conjunct, [], [])

			fstructure2 = Fstructure.update(fstructure2, [], [], [], [model_plus])

		return (fstructure1, fstructure2)

	
