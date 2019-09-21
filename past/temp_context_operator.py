


def set_MPDtree(state, trees):
	if state in global_context.PDTREE.keys():
		global_context.PDTREE[state].extend(trees)
	else:
		global_context.PDTREE[state] = list()
		global_context.PDTREE[state].extend(trees)

def get_MPDtree(state):
	if state in global_context.PDTREE.keys():
		return global_context.PDTREE[state]
	else:
		return None
		
def get_MPDtree_states():
	return global_context.PDTREE.keys()













def set_universe(universe):
	global_context.UNIVERSE = universe

def get_universe():
	return global_context.UNIVERSE






def set_current_model(model):
	global_context.MODEL = model

def get_current_model():
	return global_context.MODEL
'''
def set_abstract_state(state_list):
	global_context.ABS_STATE = state_list

def get_abstract_state():
	return global_context.ABS_STATE


def get_preds():
	return global_context.PREDS

def set_preds(m_list):
	global_context.PREDS = m_list

def add_preds(m_list):
	global_context.PREDS.extend(m_list)
'''




def get_pred_dict():
	return global_context.PRED_DICT

def set_pred_dict(mdict):
	global_context.PRED_DICT = mdict

def update_pred_dict(mdict):
	global_context.PRED_DICT.update(mdict)



def get_pos_model_filter(state):
	#print "----",state
	return global_context.FILTER_UNSAT[state], global_context.FILTER_NOT_UNSAT[state]

def update_pos_model_filter(state, updateA, updateB):
	global_context.FILTER_UNSAT[state].update(updateA)
	global_context.FILTER_NOT_UNSAT[state].update(updateB)


def set_pos_model_filter(state, updateA=None, updateB=None):
	if updateA is not None:
		global_context.FILTER_UNSAT[state] = set(updateA)
	if updateB is not None:
		global_context.FILTER_NOT_UNSAT[state] = set(updateB)


def get_current_state():
	return global_context.CURRENT_STATE

def set_current_state(state):
	global_context.CURRENT_STATE = state



def get_conjunct_cache(state):
	return global_context.CONJUNCT_CACHE[state] 


def set_conjunct_cache(state, conjunct_dict, vars_sorts):
	global_context.CONJUNCT_CACHE[state] = (conjunct_dict, vars_sorts)


def add_conjunct_cache(state, conjunct_dict, vars_sorts):
	#print global_context.CONJUNCT_CACHE
	#print cache
	global_context.CONJUNCT_CACHE[state][0].update(conjunct_dict)
	global_context.CONJUNCT_CACHE[state][1].update(vars_sorts)


#def init_state_cache(states):
#	for q in states:


def set_state_cache(X, Mset, Ln, Lp, Lcm, result):
	global_context.STATE_CACHE = (X, Mset, Ln, Lp, Lcm, result)


def get_state_cache():
	return global_context.STATE_CACHE

def set_conjunct_choice(state, choice_set):
	global_context.CONJUNCT_CHOICE[state] = choice_set


def get_conjunct_choice(state):
	return global_context.CONJUNCT_CHOICE[state]

def add_conjunct_choice(state, choice):
	global_context.CONJUNCT_CHOICE[state].add(choice)


def set_fluent_constraint(fluent_constraints):
	global_context.FLUENT_CONSTRAINT = fluent_constraints

def get_fluent_constraint():
	return global_context.FLUENT_CONSTRAINT


def set_pred_constraint_dict(pred_constraint_dict):
	global_context.PRED_CONSTRAINT_DICT = pred_constraint_dict

def get_pred_constraint_dict():
	return global_context.PRED_CONSTRAINT_DICT

def add_pred_constraint_dict(pred_constraint_dict):
	global_context.PRED_CONSTRAINT_DICT.update(pred_constraint_dict)


def set_base_pred_constraint_dict(pred_constraint_dict):
	global_context.BASE_PRED_CONSTRAINT_DICT = pred_constraint_dict

def get_base_pred_constraint_dict():
	return global_context.BASE_PRED_CONSTRAINT_DICT


def get_conjunct_constraint_cache(state):
	return global_context.CONJUNCT_CONSTRAINT_CACHE[state]


def set_conjunct_constraint_cache(state, conjunct, conjunct_constraint_dict):
	global_context.CONJUNCT_CONSTRAINT_CACHE[state][conjunct] = conjunct_constraint_dict


def init_conjunct_constraint_cache(state):
	global_context.CONJUNCT_CONSTRAINT_CACHE[state] = dict()


def get_pred_constraint_sum_dict():
	return global_context.PRED_CONSTRAINT_SUM_DICT

def set_pred_constraint_sum_dict(pred_constraint_dict):
	global_context.PRED_CONSTRAINT_SUM_DICT = pred_constraint_dict

def add_pred_constraint_sum_dict(pred_constraint_dict):
	global_context.PRED_CONSTRAINT_SUM_DICT.update(pred_constraint_dict)


def get_action_constraint():
	return global_context.ACTION_CONSTRAINT

def set_action_constraint(action_constraint):
	global_context.ACTION_CONSTRAINT = action_constraint


def set_counterexample_result(results):
	global_context.RESULT = results

def get_counterexample_result():
	return global_context.RESULT

def get_re_progress_flag():
	return global_context.FLAG_REPROGRESS

def set_re_progress_flag_true():
	global_context.FLAG_REPROGRESS = True

def set_re_progress_flag_false():
	global_context.FLAG_REPROGRESS = False

def set_reprogress_universe(universe):
	global_context.UNIVERSE_REPROGRESS = universe

def get_reprogress_universe():
	return global_context.UNIVERSE_REPROGRESS

def get_del_conjunct_list():
	return global_context.DEL_CONJUNCT_LIST

def set_del_conjunct_list(conjunct_list):
	global_context.DEL_CONJUNCT_LIST = conjunct_list

def add_del_conjunct_list(elem):
	global_context.DEL_CONJUNCT_LIST.append(elem)
	

def get_state_constraints():
	return global_context.MY_SC
def get_unknown():
	return global_context.MY_UNKNOWN


def set_state_constraints(sc):
	global_context.MY_SC = sc
def set_unknown(unknown):
	global_context.MY_UNKNOWN = unknown

def set_bound(bound):
	global_context.BOUND = bound

def get_bound():
	return global_context.BOUND


def get_candidates_from_cache(state):
	return global_context.CANDICATE_CACHE[state]

def set_candidates_to_cache(state, candicates, vars_sorts):
	global_context.CANDICATE_CACHE[state] = (candicates, vars_sorts)


def get_history_conjuncts(state):
	return global_context.HISTORY_CONJUNCTS[state]

def add_history_conjuncts(state, conjuncts):
	global_context.HISTORY_CONJUNCTS[state].update(conjuncts)


def set_history_conjuncts(state, conjuncts):
	global_context.HISTORY_CONJUNCTS[state] = conjuncts


def get_refine_candidate_conjuncts(state, conjunct):
	return global_context.BACK_REFINE_CONJUNCTS[state][conjunct]

def set_refine_candidate_conjuncts(state, conjunct, conjunct_list, var_sort_dict):
	global_context.BACK_REFINE_CONJUNCTS[state][conjunct] = (conjunct_list, var_sort_dict)

def init_refine_candidate_conjuncts(states):
	for state in states:
		global_context.BACK_REFINE_CONJUNCTS[state] = dict()

def get_action_function():
	return global_context.SCORE_FUNCTION_ACTION

def set_action_function(order):
	global_context.SCORE_FUNCTION_ACTION= order



