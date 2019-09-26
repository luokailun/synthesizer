


from formula import Fstructure
from formula import Conjunct
from model import model_checker
import scoring
import copy


def __find_repl_conjuncts(candicate_conjuncts_dict, conjunct_list, target_conjunct):
	repl_conjunct_list = list()
	for (e, elist) in candicate_conjuncts_dict.iteritems():
		if target_conjunct in elist:
			repl_conjunct_list.append(conjunct_list[e])
	return repl_conjunct_list


# first generate sub-conjuncts C of conjunct 
# then combine each conjunct c1 in C with each conjunct c2 in base_conjunct_list to generate modified conjuncts

def __get_repl_candidate_conjuncts(conjunct, model_neg_list, model_pos_list, base_conjunct_list):

	candicate_conjunct_list = list()
	var_list, sorts, pred_list = conjunct

	mrange = 3 if len(pred_list)>1 else 2
	for mlen in range(1,mrange):
		subconjunct_list = Conjunct.get_sat_subconjuncts(conjunct, model_neg_list, mlen)

		for subconjunct in subconjunct_list:
			if subconjunct != ([], [], []):
				sat_model_pos_list =  model_checker.get_sat_models(model_pos_list, subconjunct)
				subconjunct = Conjunct.rename(subconjunct)
			else:
				sat_model_pos_list = model_pos_list
			combined_conjunct_list = sum([Conjunct.combine_conjunct(subconjunct,c,3) for c in base_conjunct_list],[])
			candicate_conjunct_list += Conjunct.get_target_conjuncts(combined_conjunct_list, model_neg_list, sat_model_pos_list)

	return candicate_conjunct_list



def __get_target_conjuncts_from_preds( model_neg_list, model_pos_list, atomic_pred_list, length):
	#math_pred_list, fluent_pred_list = atomic_pred_list
	conjunct_list = [(var_list, sort_list, [pred]) for var_list, sort_list, pred in atomic_pred_list]

	base_conjunct_list = Conjunct.get_target_conjuncts(conjunct_list, model_neg_list, model_pos_list)
	target_conjunct_list = copy.deepcopy(base_conjunct_list)
	for n in range(2,length+1):
		temp_conjunct_list = [Conjunct.rename(conjunct) for conjunct in target_conjunct_list]
		combined_conjunct_list = sum([Conjunct.combine_conjunct(c1,c2,3) for c1 in temp_conjunct_list for c2 in base_conjunct_list],[])
		#print combined_conjunct_list
		#exit(0)
		target_conjunct_list += Conjunct.get_target_conjuncts(combined_conjunct_list, model_neg_list, model_pos_list)
		
	return target_conjunct_list


### note the fstructure can be translated as:  Goal & !(C1 & C2 & C3 ...), where each Ci is exists(variables)[P1 & P2 &...].

def N_update(fstructure, model_minus, atomic_pred_list, LENGTH=2):
	pred_score_dict = Fstructure.get_pred_score_dict(fstructure)
	# get the set of conjunct C1, C2,...
	conjunct_list = Fstructure.to_conjuncts(fstructure)
	# get the set of conjunct C1, C2... with M1, M2, where each Mi is a set of models that satisfy Ci
	conjunct_model_list = Fstructure.to_conjunct_models(fstructure)
	model_pos_list = Fstructure.get_pos_models(fstructure)

	candicate_conjuncts_dict = dict()
	for e, (conjunct, model_neg_list) in enumerate(conjunct_model_list):
		new_model_neg_list = [model_minus]+model_neg_list
		# generate a set K of conjuncts of limited length (l=2) from predicates
		base_conjunct_list = __get_target_conjuncts_from_preds(new_model_neg_list, list(), atomic_pred_list, LENGTH)
		# generate candidate modified conjuncts C by modifying the conjunct with the set of conjuncts K
		candicate_conjuncts_dict[e] = __get_repl_candidate_conjuncts(conjunct, new_model_neg_list, model_pos_list, base_conjunct_list)
	candicate_conjuncts_dict['new'] = __get_target_conjuncts_from_preds([model_minus], model_pos_list , atomic_pred_list, LENGTH)
	#print candicate_conjuncts_dict['new']
	
	# sort and get one modified conjunct from C and replace the old one.
	#print '@@@@;',fstructure
	#print '@@@@;',model_minus

	scoring_conjunct_dict = scoring.compute_conjuncts_score(sum(candicate_conjuncts_dict.values(),[]), pred_score_dict)
	updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict)

	del candicate_conjuncts_dict['new']
	replaced_conjunct_list = __find_repl_conjuncts(candicate_conjuncts_dict, conjunct_list, updated_conjunct)

	return Fstructure.update(fstructure, replaced_conjunct_list, updated_conjunct, [model_minus], [])


	#new_conjunct = util_pred_score.sort_and_get_conjunct(candicate_conjuncts_dict.values(), pred_score_dict)

def P_update(fstructure, model_plus, atomic_pred_list, LENGTH=2):

	pred_score_dict = Fstructure.get_pred_score_dict(fstructure)
	conjunct_model_list = Fstructure.to_conjunct_models(fstructure)
	model_pos_list = Fstructure.get_pos_models(fstructure)
	#candicate_conjuncts_dict = dict()
	new_model_pos_list = model_pos_list + [model_plus]

	#print conjunct_model_list

	for e, (conjunct, model_neg_list) in enumerate(conjunct_model_list):
		base_conjunct_list = __get_target_conjuncts_from_preds(model_neg_list, list(), atomic_pred_list, LENGTH)
		#candicate_conjuncts_dict[e] = __get_repl_candidate_conjuncts(conjunct, model_neg_list, new_model_pos_list, base_conjunct_list)
		candicate_conjunct_list = __get_repl_candidate_conjuncts(conjunct, model_neg_list, new_model_pos_list, base_conjunct_list)

		#print 'candidate', candicate_conjunct_list
		if candicate_conjunct_list == list():
			fstructure = Fstructure.delete_conjunct(fstructure, conjunct)
		else:
			scoring_conjunct_dict = scoring.compute_conjuncts_score(candicate_conjunct_list, pred_score_dict)
			#print scoring_conjunct_dict
			updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict)
			fstructure = Fstructure.update(fstructure, [conjunct], updated_conjunct, [], [])

	return Fstructure.update(fstructure, [], [], [], [model_plus])








