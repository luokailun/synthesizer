


from formula import Fstructure
from formula import Conjunct
from model import model_checker
import scoring
import copy

from formula import conjunct_filter
from basic import context_operator


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




def __generate_new_conjuncts(model_neg, model_pos_list, atomic_pred_list, LENGTH):
	"""
	generate new conjuncts of limited length

	"""
	return sum([ Conjunct.generate_conjuncts([([],[],[])], [model_neg], model_pos_list, atomic_pred_list, l) \
		for l in range(1, LENGTH+1)], list())



def __generate_adjacent_conjuncts(conjunct, model_neg_list, model_pos_list, atomic_pred_list, LENGTH):
	"""
 		first generate sub-conjuncts of the conjunct 
 		then combine each sub-conjunct with each basic conjunct to generate modified conjuncts

 		@param conjunct 		the conjunct need to be modified
	"""

	candicate_conjunct_list = list()
	var_list, sorts, pred_list = conjunct

	mrange = LENGTH+1 if len(pred_list)>1 else 2
	# mlen means how many predicates should be replaced
	# get all the sub-conjuncts of the modified mlen
	subconjunct_list = sum([Conjunct.get_sat_subconjuncts(conjunct, model_neg_list, mlen) for mlen in range(1,mrange)],[])
	print('------Number of sub-conjunct (%s)\n'%(len(subconjunct_list)))
	for e, subconjunct in enumerate(subconjunct_list):
		print('(B%s)-----Generate conjuncts for %s'%(e, Conjunct.to_formula(subconjunct)))
		# if a sub-conjunct unsat certain positive model, then this positive model will be unsat by conjuncts modified 
		# 		based on the sub-conjunct. So we do not need to check it any more
		sat_model_pos_list =  model_checker.get_sat_models(model_pos_list, subconjunct) if subconjunct != ([], [], []) else model_pos_list
		#subconjunct = Conjunct.rename(subconjunct)
		candicate_conjunct_list += Conjunct.generate_conjuncts([subconjunct], model_neg_list, sat_model_pos_list, atomic_pred_list, LENGTH)
		print("")
	return candicate_conjunct_list





def N_update(fstructure, model_minus, atomic_pred_list, LENGTH=2):
	"""
		 Modify certain conjunct in the fstructure to exclude the model.
		 Note the fstructure can be translated as:  Goal & !(C1 & C2 & C3 ...), 
			where each Ci is of the form exists(X1,X2,...)[P1 & P2 &...].
		
		 @param model_minus 		the model need to be excluded
		 @param atomic_pred_list	the set of predicates used to modify conjuncts
	"""
	# get predicates' score for conjunct selection
	pred_score_dict = Fstructure.get_pred_score_dict(fstructure)
	# get the set of conjunct C1, C2,...
	conjunct_list = Fstructure.to_conjuncts(fstructure)
	# get the set of conjunct C1, C2... with M1, M2, where each Mi is a set of models that satisfy Ci
	conjunct_model_list = Fstructure.to_conjunct_models(fstructure)
	# get the set of positive models that falsify each conjunct
	model_pos_list = Fstructure.get_pos_models(fstructure)

	candicate_conjuncts_dict = dict()
	for e, (conjunct, model_neg_list) in enumerate(conjunct_model_list):
		print('(A%s)**** Generate adjacent conjuncts for  %s'%(e, Conjunct.to_formula(conjunct)))
		new_model_neg_list = [model_minus]+model_neg_list
		# generate candidate conjuncts by modifying the conjunct with the set of predicates
		candicate_conjuncts_dict[e] = __generate_adjacent_conjuncts(conjunct, new_model_neg_list, model_pos_list, atomic_pred_list, LENGTH)
	# generate new conjuncts of length 2
	candicate_conjuncts_dict['new'] = __generate_new_conjuncts(model_minus, model_pos_list, atomic_pred_list, LENGTH)
	#print candicate_conjuncts_dict['new']
	
	# sort and get one modified conjunct from C and replace the old one.
	scoring_conjunct_dict = scoring.compute_conjuncts_score(sum(candicate_conjuncts_dict.values(),[]), pred_score_dict)
	updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict, model_pos_list)

	del candicate_conjuncts_dict['new']
	old_conjunct_list = __find_repl_conjuncts(candicate_conjuncts_dict, conjunct_list, updated_conjunct)

	print('***** Change %s ---> %s \n'%(' and '.join([Conjunct.to_formula(c) for c in old_conjunct_list]), Conjunct.to_formula(updated_conjunct)))

	return Fstructure.update(fstructure, old_conjunct_list, updated_conjunct, [model_minus], [])


	#new_conjunct = util_pred_score.sort_and_get_conjunct(candicate_conjuncts_dict.values(), pred_score_dict)


def P_update(fstructure, model_plus, atomic_pred_list, LENGTH=2):

	pred_score_dict = Fstructure.get_pred_score_dict(fstructure)
	conjunct_model_list = Fstructure.to_conjunct_models(fstructure)
	model_pos_list = Fstructure.get_pos_models(fstructure)
	#candicate_conjuncts_dict = dict()
	new_model_pos_list = model_pos_list + [model_plus]

	#print conjunct_model_list

	for num, (conjunct, model_neg_list) in enumerate(conjunct_model_list):
		print('(A%s)**** Generate adjacent conjuncts for  %s'%(num, Conjunct.to_formula(conjunct)))
		candicate_conjunct_list = __generate_adjacent_conjuncts(conjunct, model_neg_list, new_model_pos_list, atomic_pred_list, LENGTH)

		if candicate_conjunct_list == list():
			updated_conjunct = None
		else:
			scoring_conjunct_dict = scoring.compute_conjuncts_score(candicate_conjunct_list, pred_score_dict)
			updated_conjunct = scoring.get_min_score_conjunct(scoring_conjunct_dict, new_model_pos_list)

		if updated_conjunct is None:
			fstructure = Fstructure.delete_conjunct(fstructure, conjunct)
			print('****** Delete conjunct %s \n'%( Conjunct.to_formula(conjunct)))
		else:
			print('****** Change %s ---> %s \n'%(Conjunct.to_formula(conjunct), Conjunct.to_formula(updated_conjunct)))
			fstructure = Fstructure.update(fstructure, [conjunct], updated_conjunct, [], [])

	return Fstructure.update(fstructure, [], [], [], [model_plus])








