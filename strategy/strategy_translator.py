
"""

	Intuitively, a strategy is a "sub" transition system which is generate from a situation calculus model

	-- domain (universe)
	-- initial model  
	-- strategy tree

	nodes {1: model, 2: model}
	structure {1: [1,2,3], 3:[4,5,6]}
	win nodes [0,1,3,4]
	MCMAS strategy like the following:


Formula number 1: (<g1>G goal), is TRUE in the model
  The following is a witness for the formula: 
   < 0 1 > 
   < 1 2 > 
   < 1 3 > 
   < 1 4 > 
   < 1 5 > 
   < 1 6 > 
   < 4 7 > 
   < 6 7 > 
   < 2 8 > 
   < 3 8 > 
   < 5 5 > 
   < 8 4 > 
   < 8 9 > 
   < 8 5 > 
   < 7 5 > 
   < 9 7 > 
  States description: 
------------- State: 0 -----------------
Agent Environment
  Ch0_0 = true
  Ch0_1 = true
  Ch0_2 = true
  Ch0_3 = true
  Ch0_4 = false
  Ch1_0 = true
  Ch1_1 = true
  Ch1_2 = true
  Ch1_3 = true
  Ch1_4 = false
  Ch2_0 = true
  Ch2_1 = false
  Ch2_2 = false
  Ch2_3 = false
  Ch2_4 = false
  Ch3_0 = false
  Ch3_1 = false
  Ch3_2 = false
  Ch3_3 = false
  Ch3_4 = false
  Ch4_0 = false
  Ch4_1 = false
  Ch4_2 = false
  Ch4_3 = false
  Ch4_4 = false
  turnp1 = true
  turnp2 = false
  xlen = 4
  ylen = 4
Agent Player1
  state = none
Agent Player2
  state = none
----------------------------------------
------------- State: 1 -----------------
Agent Environment
  Ch0_0 = true
  Ch0_1 = true
  Ch0_2 = false
  Ch0_3 = false
  Ch0_4 = false
  Ch1_0 = true
  Ch1_1 = true
  Ch1_2 = false
  Ch1_3 = false
  Ch1_4 = false
  Ch2_0 = true
  Ch2_1 = false
  Ch2_2 = false
  Ch2_3 = false
  Ch2_4 = false
  Ch3_0 = false
  Ch3_1 = false
  Ch3_2 = false
  Ch3_3 = false
  Ch3_4 = false
  Ch4_0 = false
  Ch4_1 = false
  Ch4_2 = false
  Ch4_3 = false
  Ch4_4 = false
  turnp1 = false
  turnp2 = true
  xlen = 4
  ylen = 4
Agent Player1
  state = none
Agent Player2
  state = none
----------------------------------------
------------- State: 2 -----------------"
"""



import re
def ____get_model(model_txt):
	"""
		from MCMAS state representation to our model representation
	"""
	pred_list = model_txt.replace('true','True').replace('false', 'False').split('#')
	# delete Estate
	pred_list = [pred for pred in pred_list if pred.find('Estate') == -1]
	fluent_pattern = re.compile(r"(?P<fluent>[\w\d]+?)_(?P<para>[\w\d_]*?)=(?P<value>[\w\d]+)")
	pred_list = [pred for pred in pred_list if pred!=""]

	pred_list = [ fluent_pattern.search(pred) for pred in pred_list]
	#print '!!!!',pred_list
	fluent_tuple_list = [ (match.group('fluent'), match.group('para').split('_'), match.group('value')) for match in  pred_list]
	assignment = { "%s(%s)"%(fluent,','.join(paras)): value for fluent, paras, value in fluent_tuple_list}
	return assignment



def __get_node_models(link_dict, result, universe, default_value):
	"""
		exact  detailed states representation in MCMAS result
	"""
	node_list = link_dict.keys()
	node_model_dict = dict()
	for node in node_list:
		model_pattern = re.compile(r"State:\s*%s.+?Agent Environment(.+?)Agent Player1"%(node))
		model_txt = model_pattern.search(result)
		# Estate is a key word we use as a spurious variable in MCMAS
		node_model_dict[node] = (universe, ____get_model(model_txt.group(1).replace(" ","")), default_value)

	return node_model_dict



def __get_win_nodes(start_node, link_dict):
	"""
		get those nodes winning by the player 
	"""
	win_nodes =  list()
	visit_nodes = list()

	win_flag = True
	current_nodes = [start_node]
	# if there is node that has not been visited
	while set(visit_nodes) != set(link_dict.keys()):
		if win_flag is True:
			win_nodes += current_nodes

		win_flag = not win_flag
		visit_nodes += current_nodes
		current_nodes = sum([link_dict[node] for node in current_nodes],[])

	return list(set(win_nodes))


def construct_strategy(result, universe, default_value):
  	"""
  		from the result returned by MCMAS to construct the model with universe and default value
  	"""
  	tree_pattern = re.compile(r"The following is a witness for the formula:(.+?)States description:")
  	link_pattern = re.compile(r"<\s*(\d+)\s*(\d+)\s*>")
  	result = ''.join(result).replace('\n',"#")
  	m = tree_pattern.search(result)
  	tree_str = m.group(1)
  	link_list = link_pattern.findall(tree_str)
  	# generate tree link structure
  	link_dict = dict()
  	for left, right in link_list:
	  	if left in link_dict:
	  	  	link_dict[left].append(right)
	  	else:
	  	  	link_dict[left] = [right]
  	# it may contains redundant????
  	link_dict = {key: list(set(value)) for key, value in link_dict.items()}

  	win_node_list = __get_win_nodes('0', link_dict)
  	node_model_dict = __get_node_models(link_dict, result, universe, default_value)

  	strategy_structure = dict()
  	strategy_structure['domain'] = universe
  	#strategy_structure['init_model'] = model
  	strategy_structure['strategy'] = (node_model_dict, link_dict, win_node_list)
  	return strategy_structure