


# model is a tuple (U, S) where U is universe and S is an assignment

def to_formula(model):
	universe, assignment = model
	formula_list = list()
	for key,value in assignment.iteritems():
		if value is True or str(value) == 'True':
			formula_list.append(key)
		elif value is False or str(value) == 'False':
			formula_list.append('!%s'%key)
		else:
			formula_list.append('%s=%s'%(key,value))
	return '&'.join(formula_list)

################################################################################################################################################
'''
M1 =({'_S1': [ 'p1', 'p2'], 'Int': ['1', '0', '3', '2', '6', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': 'False', 'numStone()': '4', 'turn(p2)': 'True'})
M2 = ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '5', '4'], 'Bool': ['True', 'False']}, {'numStone()': '4', 'turn(p1)': 'False',  'turn(p2)': 'True'})

print model_equivalent(M1, M2)
print is_lager_model(M1, M2)
'''



def model_equivalent(M1, M2):
	universe1, assignment1 = M1
  	universe2, assignment2 = M2
  	if cmp(assignment1, assignment2) == 0:
  		return True
  	else:
  		return False


def is_lager_model(M1, M2):
	universe1, assignment1 = M1
  	universe2, assignment2 = M2
  	temp1 = max([ int(e) for e in universe1['Int']])
  	temp2 = max([ int(e) for e in universe2['Int']])
  	return temp1>temp2




