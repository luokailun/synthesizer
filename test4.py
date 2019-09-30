




d = {1:[2,3], 2:[3,4]}

def get_min_score_conjunct(scoring_dict, unsat_model_list):

	while scoring_dict.keys()!=list():
		min_score = min(scoring_dict.keys())
		print min_score
		conjunct = scoring_dict[min_score].pop(0)
		print 'c',conjunct
		if scoring_dict[min_score] == list():
			scoring_dict.pop(min_score)
		if conjunct ==1:
			return conjunct
	return None


print get_min_score_conjunct(d, list())
print d