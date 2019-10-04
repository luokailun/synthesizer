

import re
from basic import pattern
import random

var_pattern = re.compile(r'[A-Z]\d+')


def __unify_vars(pred):
	replace_var = 'W'
	mvars = var_pattern.findall(pred)
	#print mvars
	for e, var in enumerate(mvars):
		pred = pred.replace(var, replace_var+str(e),1)
	return pred
#print __unify_vars(s)

##############################################################################################################################################################

def init_preds_base_score(pred_list):
	return { __unify_vars(pred): -1 for var_list, sorts, pred in pred_list} 


##############################################################################################################################################################

def __compute_conjunct_score(conjunct, pred_score_dict):
	#print conjunct
	var_list, sort_list, pred_list = conjunct
	return sum([pred_score_dict[__unify_vars(pred)] for pred in pred_list],0)



def compute_conjuncts_score(conjunct_list, pred_score_dict):
	scoring_dict = dict()
	for conjunct in conjunct_list:
		score = __compute_conjunct_score(conjunct, pred_score_dict)
		if score in scoring_dict:
			scoring_dict[score].append(conjunct)
		else:
			scoring_dict[score] = [conjunct]
	return scoring_dict
	
##############################################################################################################################################################

'''
def get_min_score_conjunct(scoring_dict, unsat_model_list):
	min_score = min(scoring_dict.keys())
	min_conjunct_list = scoring_dict[min_score]
	#ranNum = random.randint(0,len(min_conjunct_list)-1)
	#target_conjunct = min_conjunct_list[ranNum]
	target_conjunct = min_conjunct_list[0]
	min_conjunct_list.remove(target_conjunct)
	if scoring_dict[min_score] == list():
		scoring_dict.pop(min_score)
	return target_conjunct
'''

	#ranNum = random.randint(0,len(min_conjunct_list)-1)
	#target_conjunct = min_conjunct_list[ranNum]

from model import model_checker
#from model import model_interpretor
#from prover import z3prover
#from formula import Conjunct


def get_min_score_conjunct(scoring_dict, unsat_model_list):
	while scoring_dict.keys()!=list():
		min_score = max(scoring_dict.keys())
		conjunct = scoring_dict[min_score].pop(0)
		if scoring_dict[min_score] == list():
			scoring_dict.pop(min_score)
		#if model_interpretor.interpret_result(z3prover.check_unsat('!(%s)'%(Conjunct.to_formula(conjunct)))) is False:
		if model_checker.unsat_conjunct_math(unsat_model_list, conjunct):
			return conjunct
	return None

##############################################################################################################################################################




