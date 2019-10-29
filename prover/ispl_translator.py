
'''
Agent Environment
    Obsvars:
        numberStone: 1..3;
        turn_p1: Boolean;
        turn_p2: Boolean;
    end Obsvars
    Actions = {none};
    Protocol:
        Other: {none};
    end Protocol
    Evolution:
    ssa:
    end Evolution
end Agent

Evaluation
	Tianjiwin if Environment.a>Environment.b and Environment.a+Environment.b=3;
	Kingwin if Environment.a<Environment.b and Environment.a+Environment.b=3;
	Tianjinotwin if Environment.a<=Environment.b;
end Evaluation

InitStates
	Environment.a=0 and Environment.b=0 and Tianji.state=HML and King.state=HML;
end InitStates
'''




from basic import context_operator
import itertools 
from regression import atomic_regress
from formula import Formula
from basic import Util
from basic import simplify
import re

##############################################################################################################


def __get_useless_actions(action_list, poss_list):
	poss_str = ' '.join(poss_list)
	actions = [ action for action in action_list if re.search(r"\b%s\b"%action, poss_str) is None]
	return actions

def __delete_useless_updates(update_list, useless_action_list):
	action_str = '|'.join([r"\b%s\b"%action for action in useless_action_list])
	updates = [update for update in update_list if re.search(action_str, update) is None]
	return updates


##############################################################################################################

illgal_pattern1 = re.compile(r"(?P<exp>\d+\s*(?:=|>|<)\s*\d+)")
illgal_pattern2 = re.compile(r"(?P<exp>\d+\s*(?:>=|<=)\s*\d+)")

'''
def __del_illgal_exp(formula):
	return re.sub(illgal_pattern, lambda x: str(eval(x.group('exp').replace('=','=='))), formula)
'''

def ____ispl_simplify(formula, eq_symbol):
	#print 'aaa',formula
	formula = re.sub(illgal_pattern1, lambda x: str(eval(x.group('exp').replace('=','=='))), formula)
	formula = re.sub(illgal_pattern2, lambda x: str(eval(x.group('exp'))), formula)
	#print 'bbb',formula
	formula = simplify.simplify(formula).replace(" ",'')
	#print 'ccc',formula
	if formula == 'true':
		return "%s=%s"%(eq_symbol, eq_symbol)
	else:
		return formula


##############################################################################################################


#, r'\bnot\b'

#encode_ispl =(['\|','&', '=>', r'\bnot\b' ],[' or ', ' and ', '->','!'])
encode_ispl =(['|','&', '=>', '~' ],[' or ', ' and ', '->', '!'])

def ____to_ispl_logic(formula):
	#print  zip(encode_ispl[0], encode_ispl[1])
	#return Util.repeat_do_function(Util.sub_lambda_exp, zip(encode_ispl[0], encode_ispl[1]), formula)
	#return Util.repeat_do_function(Util.sub_lambda_exp, zip(encode_ispl[0], encode_ispl[1]), formula)
	return Util.endecode_string(formula, encode_ispl[0], encode_ispl[1])

def ____to_ispl_preds(formula, pred_list):
	new_pred_list = ['%s=true'%(pred) for pred in pred_list] 
	return Util.endecode_string(formula, pred_list, new_pred_list)


def ____add_env(formula, fluent_list):
	new_fleunt_list = ['Environment.%s'%(fluent) for fluent in fluent_list]
	return Util.endecode_string(formula, fluent_list, new_fleunt_list)
	#return formula

def ____to_ispl_vars(formula, fluent_list, ispl_fluent_list):
	return Util.endecode_string(formula, fluent_list, ispl_fluent_list)


def __get_ispl_formula(formula, model, fluent_tuple_list):
	#print formula
	ispl_fluent_list = ['%s_%s'%(f,'_'.join(para_list)) for f, para_list, sort in fluent_tuple_list]
	fluent_list = ['%s(%s)'%(f,','.join(para_list)) for f, para_list, sort in fluent_tuple_list]
	pred_fluent_list = ['%s(%s)'%(f,','.join(para_list)) for f, para_list, sort in fluent_tuple_list \
			if f in context_operator.get_predicates()]


	formula = Formula.transform_entailment(formula)
	formula = ____add_env(formula, fluent_list)
	#print formula
	formula = Formula.grounding(formula, model)
	#print formula
	formula = ____ispl_simplify(formula, 'Environment.Action')
	#print formula
	# add back zero fluent
	formula = ____handle_0arity_fluents(formula)
	formula = ____to_ispl_preds(formula, pred_fluent_list)
	#print formula
	#formula = ____add_env(formula, fluent_list)
	#print formula
	formula = Util.endecode_string(formula, fluent_list, ispl_fluent_list)
	#formula = ____ispl_simplify(formula, 'Environment.Action')
	#print formula
	formula = ____to_ispl_logic(formula)
	#print formula
	#print 
	return formula


# turnp1 = false if (Player1.Action = takep1_1) and Player2.Action = none;
# turnp2 = true  if (Player1.Action = takep1_1) and Player2.Action = none;
# turnp1 = true  if (Player2.Action = takep2_1) and Player1.Action = none;
# turnp2 = false if (Player2.Action = takep2_1) and Player1.Action = none;

turn_list = [
			'turn(p1) = false if ! Player1.Action = none and Player2.Action = none;', 
			'turn(p2) = true  if ! Player1.Action = none and Player2.Action = none;', 
			'turn(p1) = true if ! Player2.Action = none and Player1.Action = none;', 
			'turn(p2) = false if ! Player2.Action = none and Player1.Action = none;', 
			]


def ____handle_0arity_fluents(elem):
	zero_arity_fluents = context_operator.get_zero_fluents()
	old_strs = [r'\b'+str(fluent)+r'\b' for fluent in zero_arity_fluents]
	replaces = [fluent+'()' for fluent in zero_arity_fluents]
	return Util.repeat_do_function(Util.sub_lambda_exp, zip(old_strs,replaces), elem)


def __get_ispl_update(fluent_tuple_list, p1_action_tuple_list, p2_action_tuple_list, model):

	universe, assignment, default_value = model
	ispl_fluent_list = ['%s_%s'%(f,'_'.join(para_list)) for f, para_list, sort in fluent_tuple_list]
	fluent_list = ['%s(%s)'%(f,','.join(para_list)) for f, para_list, sort in fluent_tuple_list]

	predicates = context_operator.get_predicates()
	fun_fluent_list = [('%s(%s)'%(f,','.join(para_list)), sort) for f, para_list, sort in fluent_tuple_list if f not in predicates]
	pred_fluent_list = ['%s(%s)'%(f,','.join(para_list)) for f, para_list, sort in fluent_tuple_list if f in predicates and f!='turn']
	#print fun_fluent_list
	#print pred_fluent_list
	fluent_value_list = sum([list(itertools.product([fluent],universe[sort])) \
		for fluent, sort in fun_fluent_list] ,[])
	fluent_value_list = ['%s=%s'%(fluent,value) for fluent, value in fluent_value_list]
	fluent_value_list.extend(pred_fluent_list)


	ispl_p1_action_list = ['Player1.Action = %s%s'%(a,'_'.join(para_list)) for a, para_list in p1_action_tuple_list]
	p1_action_list = ['%s(%s)'%(a,','.join(para_list)) for a, para_list in p1_action_tuple_list]
	ispl_p2_action_list = ['Player2.Action = %s%s'%(a,'_'.join(para_list)) for a, para_list in p2_action_tuple_list]
	p2_action_list = ['%s(%s)'%(a,','.join(para_list)) for a, para_list in p2_action_tuple_list]

	action_pair_list = [(a,b) for a, b in zip(p1_action_list+p2_action_list, ispl_p1_action_list+ispl_p2_action_list)]
	update_pair_list = [ (a,b,c) for a, (b,c) in itertools.product(fluent_value_list, action_pair_list)]
	update_pair_list = [ (fluent, atomic_regress.poss_or_ssa(action, fluent), ispl_action) \
						for fluent, action, ispl_action in update_pair_list]
	# transform (=>) to (not or)
	update_pair_list = [ (a, Formula.transform_entailment(b), c) for a, b, c in update_pair_list]
	update_pair_list = [ (a, Formula.grounding(b,model), c) for a, b, c in update_pair_list]
	update_pair_list = [ (a, ____ispl_simplify(b,'Estate'), c) for a, b, c in update_pair_list]
	# simply will eliminate () in 0arity fluent, here we add back to it
	update_pair_list = [ (a, ____handle_0arity_fluents(b),c) for a, b, c in update_pair_list]
	#update_pair_list = [ (a, b, c) for a, b, c in update_pair_list if b is not None]

	pred_fluent_list = ['%s(%s)'%(f,','.join(para_list)) for f, para_list, sort in fluent_tuple_list if f in predicates]
	# add =true to each predicates
	update_pair_list = [ (fluent, ____to_ispl_preds(update, pred_fluent_list), ispl_action) for fluent, update, ispl_action in  update_pair_list]

	fun_update_pair_list = [ (fluent, update, ispl_action) for fluent, update, ispl_action in  update_pair_list if fluent not in pred_fluent_list and update !='false'] 
	pred_update_pair_list = [ (fluent, update, ispl_action) for fluent, update, ispl_action in  update_pair_list if fluent in pred_fluent_list] 

	update_list = ['%s if (%s) and %s;'%(fluent, update, ispl_action) for fluent, update, ispl_action in  fun_update_pair_list ]
	update_list += ['%s=true if (%s) and %s;'%(fluent, update, ispl_action) for fluent, update, ispl_action in  pred_update_pair_list if update !='false' ]
	update_list += ['%s=false if !(%s) and %s;'%(fluent, update, ispl_action) for fluent, update, ispl_action in  pred_update_pair_list if update !='false' ]
	update_list += ['%s=false if %s;'%(fluent, ispl_action) for fluent, update, ispl_action in  pred_update_pair_list if update =='false' ]
	update_list += turn_list
	
	update_list = [ Util.endecode_string(formula, fluent_list, ispl_fluent_list) for formula in update_list]
	update_list = [ ____to_ispl_logic(formula) for formula in update_list]

	#return '\n    '.join(update_list)
	return update_list



def __get_ispl_poss(action_tuple_list, model, fluent_tuple_list):
	#feature_list = Util.get
	#context_operator.get

	ispl_fluent_list = ['%s_%s'%(f,'_'.join(para_list)) for f, para_list, sort in fluent_tuple_list]
	fluent_list = ['%s(%s)'%(f,','.join(para_list)) for f, para_list, sort in fluent_tuple_list]
	ispl_action_list = ['%s%s'%(a,'_'.join(para_list)) for a, para_list in action_tuple_list]
	action_list = ['%s(%s)'%(a,','.join(para_list)) for a, para_list in action_tuple_list]

	pred_fluent_list = ['%s(%s)'%(f,','.join(para_list)) for f, para_list, sort in fluent_tuple_list \
				if f in context_operator.get_predicates()]

	action_poss_list = [ atomic_regress.poss_or_ssa(action) for action in action_list ]
	#exit(0)
	action_poss_list = [ Formula.transform_entailment(poss) for poss in action_poss_list ]
	action_poss_list = [ ____add_env(poss, fluent_list) for poss in action_poss_list ]
	action_poss_list = [ Formula.grounding(poss, model) for poss in action_poss_list ]
	action_poss_list = [ ____ispl_simplify(poss, 'state') for poss in action_poss_list]
	action_poss_list = [ ____handle_0arity_fluents(poss) for poss in action_poss_list]
	action_poss_list = [ ____to_ispl_preds(poss, pred_fluent_list) for poss in action_poss_list ]
	action_poss_list = [ ____to_ispl_vars(poss, fluent_list, ispl_fluent_list) for poss in action_poss_list]
	#action_poss_list = [ ____ispl_simplify(poss, 'state') for poss in action_poss_list]
	action_poss_list = [ ____to_ispl_logic(poss) for poss in action_poss_list]
	action_poss_list = [ "%s:{%s};"%(poss, ispl_action_list[e]) for e, poss in enumerate(action_poss_list) if poss !='false']
	
	#return '\n    '.join(action_poss_list)
	return action_poss_list

##############################################################################################################


def __get_ispl_actions(action_tuple_list):
	return [ '%s%s'%(a,'_'.join(para_list)) for a, para_list in action_tuple_list]



def __get_actions(universe, player):
	actions = context_operator.get_actions()
	action_sorts_list = [ (f, sort_list) for f, sort_list in  context_operator.get_functions_sorts().iteritems() if f in actions]
	p_sort = [sort for sort, consts in context_operator.get_sort_symbols_dict().iteritems() if player in consts].pop()


	action_tuple_list = list()
	for a, sort_list in action_sorts_list:
		paras_list = itertools.product(*[ universe[s] if s!=p_sort else [player] for s in sort_list[0: len(sort_list)-1] ])
		action_tuple_list.extend([(a,paras) for paras in paras_list ])

	return action_tuple_list



def __get_ispl_vars(fluent_tuple_list, universe):

	ispl_var_list = list()	

	Int_list = [int(s) for s in universe['Int'] ]
	for f, paras, sort in fluent_tuple_list:
		if sort =='Bool':
			ispl_type = 'boolean'
		elif sort =='Int':
			ispl_type = '%s..%s'%(str(min(Int_list)),str(max(Int_list)))
		else:
			ispl_type = '{%s}'%(','.join(universe[sort]))
		ispl_var_list.append('%s_%s:%s;'%(f, '_'.join(paras), ispl_type))

	#return '\n    '.join(ispl_var_list)
	return ispl_var_list



def __get_fluents(universe):
	fun_sorts_dict = context_operator.get_functions_sorts()
	fun_fluent_list = [f for f in context_operator.get_fluents() if f ]
	fun_sorts_list  = [ (f, fun_sorts_dict[f]) for f in fun_fluent_list]

	fluent_tuple_list = list()
	for f, sort_list in fun_sorts_list:
		paras_list = itertools.product(*[ universe[s] for s in sort_list[0: len(sort_list)-1] ])
		fluent_tuple_list.extend([(f,paras, sort_list[-1]) for paras in paras_list ])

	return fluent_tuple_list



##############################################################################################################


ispl = 'Semantics=SA;\n\
Agent Environment\n\
  Obsvars:\n\
	  %s\n\
  end Obsvars\n\
  Vars:\n\
  	Estate: {none};\n\
  end Vars\n\
  Actions = {none};\n\
  Protocol: Other: {none}; end Protocol \n\
  Evolution: \n\
	  %s \n\
  end Evolution \n\
end Agent\n \
\n\
Agent Player1\n\
  Vars:\n\
  	state: {none};\n\
  end Vars\n\
  Actions = {%s};\n\
  Protocol:\n\
	  %s \n\
	  Other: {none};\n\
  end Protocol \n\
  Evolution: \n\
	  state = none if state = none; \n\
  end Evolution \n\
end Agent\n \
\n\
Agent Player2\n\
  Vars:\n\
  	state: {none};\n\
  end Vars\n\
  Actions = {%s};\n\
  Protocol:\n\
	  %s \n\
	  Other: {none};\n\
  end Protocol \n\
  Evolution: \n\
	  state = none if state = none; \n\
  end Evolution \n\
end Agent\n \
\n\
Evaluation \n\
	goal if %s; \n\
end Evaluation \n\
\n\
InitStates \n \
	%s;\n\
end InitStates \n\
\n\
Groups \n\
	%s; \n\
end Groups \n\
\n\
Formulae \n \
	%s; \n\
end Formulae \n\
'
#%(ispl_vars, ispl_updates, p1_actions, p1_poss, p2_actions, p2_poss, win_property, init)


def to_ispl(model, init, goal, players, modal_operator):
	"""
	players: a list containing p1, p2
	modal_operator: G or F
	"""
	universe, assignment, default_value = model

	fluent_tuple_list  = __get_fluents(universe)
	ispl_vars = __get_ispl_vars(fluent_tuple_list, universe)

	p1_action_tuple_list = __get_actions(universe, 'p1')
	p2_action_tuple_list = __get_actions(universe, 'p2')
	ispl_p1_actions = __get_ispl_actions(p1_action_tuple_list)
	ispl_p2_actions = __get_ispl_actions(p2_action_tuple_list)

	ispl_p1_actions_poss = __get_ispl_poss(p1_action_tuple_list, model, fluent_tuple_list)
	ispl_p2_actions_poss = __get_ispl_poss(p2_action_tuple_list, model, fluent_tuple_list)


	ispl_updates = __get_ispl_update(fluent_tuple_list, p1_action_tuple_list, p2_action_tuple_list, model)

	### simplify domains by deleting useless actions and updates
	useless_actions = __get_useless_actions(ispl_p1_actions+ispl_p2_actions, ispl_p1_actions_poss+ispl_p2_actions_poss)
	ispl_p1_actions = list(set(ispl_p1_actions) - set(useless_actions))
	ispl_p2_actions = list(set(ispl_p2_actions) - set(useless_actions))
	if useless_actions!=list():
		ispl_updates = __delete_useless_updates(ispl_updates, useless_actions)
	

	ispl_vars = '\n    '.join(ispl_vars)
	ispl_p1_actions = ','.join(ispl_p1_actions+['none'])
	ispl_p2_actions = ','.join(ispl_p2_actions+['none'])
	ispl_p1_actions_poss = '\n    '.join(ispl_p1_actions_poss)
	ispl_p2_actions_poss = '\n    '.join(ispl_p2_actions_poss)
	ispl_updates = '\n    '.join(ispl_updates)

	ispl_win_property = __get_ispl_formula(goal, model, fluent_tuple_list)

	ispl_init = __get_ispl_formula(init, model, fluent_tuple_list)
	#print ispl_init
	#print util_model.to_formula(model)
	player_dict = {'p1':"Player1", 'p2':'Player2'}
	groups = "g1 = {%s}"%(','.join([player_dict[p] for p in players]))

	formula = "<g1>%s goal"%(modal_operator)

	return ispl%(ispl_vars, ispl_updates, ispl_p1_actions, ispl_p1_actions_poss, ispl_p2_actions, ispl_p2_actions_poss, \
		ispl_win_property, ispl_init, groups, formula)

	#print ispl_vars_str
	#print ispl_p1_actions_str
	#print ispl_p2_actions_str
	#print ispl_p1_actions_poss
	#print ispl_p2_actions_poss





