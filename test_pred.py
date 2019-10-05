


from parser import BATparser
from formula import predicate_filter
BATparser.parser('takeaway.sc')
#BATparser.parser('new_chomp2N.sc')


from formula import Predicate

#Predicate.generate_preds('takeaway.sc')


#print [e for e in range(0,3) if not None]




def decrease(pred_score_dict):
	k=3
	for e in range(1,2):
		pred_score_dict[e] = k
	pred_score_dict = {2,3}

k = {1:2,2:3}
print decrease(k)
print k


def hello(mt):
	s1, s2 = mt
	s1 = list()
	return mt
k=([1],[2])
print hello(k)
print k



