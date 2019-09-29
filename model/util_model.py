


# model is a tuple (U, S) where U is universe and S is an assignment

def to_formula(model):
	universe, assignment = model
	formula_list = list()
	for key,value in assignment.iteritems():
		if value is True:
			formula_list.append(key)
		elif value is False:
			formula_list.append('!%s'%key)
		else:
			formula_list.append('%s=%s'%(key,value))
	return '&'.join(formula_list)