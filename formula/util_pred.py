

def __delete_unknown_predicates(fluent_predicates):
	return [ (var_list, sorts, body) for var_list ,sorts, body in fluent_predicates if body.find('unknown')==-1]

def __delete_last_preds(com_preds):
	#??? delete_preds = [(var_list, sorts, body) for (var_list, sorts, body) in com_preds if body.find('last')!=-1 and (body.find('>=')!=-1 or body.find('>')!=-1)]
	delete_preds = [(var_list, sorts, body) for (var_list, sorts, body) in com_preds if body.find('last')!=-1]
	#print delete_preds
	return [pred for pred in com_preds if pred not in delete_preds]

def __get_useless_math_symbols(domain_name):
	math_symbols = ['+','-','*','%','/']
	with open('./input/%s.sc'%(domain_name),"read") as sc_file:
		full_txt = " ".join(sc_file.readlines())
		return [sym for sym in math_symbols if full_txt.find(sym)==-1]


def __deleteUselessMath(com_preds, math_symbols):
	delete_preds = [(var_list, sorts, body) for (var_list, sorts, body) in com_preds for sym in math_symbols if body.find(sym)!=-1]
	return [pred for pred in com_preds if pred not in delete_preds]



def reduce_num_math_preds(domain_name, com_preds):
	useless_symbols = __get_useless_math_symbols(domain_name)
	return __deleteUselessMath(com_preds, useless_symbols)


def reduce_num_fluent_preds(com_preds):
	com_preds = __delete_unknown_predicates(com_preds)
	com_preds = __delete_last_preds(com_preds)
	return com_preds





##############################################################################################################################################################

