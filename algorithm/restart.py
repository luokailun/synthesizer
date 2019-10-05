
#from formula import Fstructure

from formula import Fstructure
import scoring
import global_structure

##############################################################################################################################




def init_conjunct_storer():
	global_structure.STORER = ([], [])



def store_two_state_conjuncts(two_state_structure):
	"""
		store conjuncts for the two state structure
	"""
	s1, s2 = global_structure.STORER
	fstructure1, fstructure2 = two_state_structure
	conjunct_list1 = Fstructure.to_conjuncts(fstructure1)
	conjunct_list2 = Fstructure.to_conjuncts(fstructure2)

	s1.extend(conjunct_list1)
	s2.extend(conjunct_list2)



##############################################################################################################################


def restart(two_state_structure):
	"""
		setting to the initial structure and decrease the score of predicates
	"""
	fstructure1, fstructure2 = two_state_structure
	Goal = fstructure1[0]
	conjunct_list1, conjunct_list2 = global_structure.STORER
	pred_score_dict1 = Fstructure.get_pred_score_dict(fstructure1)
	pred_score_dict2 = Fstructure.get_pred_score_dict(fstructure2)

	new_pred_score_dict1 = scoring.decrease_preds_score(conjunct_list1, pred_score_dict1)
	new_pred_score_dict2 = scoring.decrease_preds_score(conjunct_list2, pred_score_dict2)

	fstructure1 = Fstructure.init(Goal,list(),list(), new_pred_score_dict1)
	fstructure2 = Fstructure.init(Goal,list(),list(), new_pred_score_dict2)

	return (fstructure1, fstructure2)
