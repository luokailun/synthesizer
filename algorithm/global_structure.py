


"""
	A tuple: (A_list, B_list), where A B list are conjuncts
"""

CONJUNCT_STORER = (list(),list())


"""
	A dict
	keys: 'type': P or N denoting whether P update or N update
		  'q1': (fstructure, [c1, c2, ...]), 
		  		where each c1 stores
		  			(1) a model need to do update
		  			(2) an adjacent conjunct dict 
		  			(3) an adjacent conjunct scoring dict
		  'q2': similar to 'q1'
"""

CHOICE = dict()
CHOICE['type'] = None
CHOICE['q1'] = None
CHOICE['q2'] = None
