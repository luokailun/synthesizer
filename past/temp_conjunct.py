def ______construct_sort_vars_dict(pred_list):
	#print pred_list
	return {body:__gen_sort_vars(var_list,sorts) for (var_list, sorts, body) in pred_list }


def ____combine_preds(base_preds, add_preds, models_sat, models_unsat, pred_score_dict, filter_set, pred_sort_dict):

	#print '1------',base_preds
	print '#########-------combine---------'
	print '#########base: %s'%(base_preds if len(base_preds)==1 else len(base_preds))
	print '#########', models_sat
	print '#########', models_unsat
	#print '#########-------combine---------'

	#__combine(pred_b, pred_b) for pred_b, pred_b in if __filter(a,b,filter_set)
	sort_vars_dict = ______construct_sort_vars_dict(base_preds+add_preds)
	new_preds_dict = dict()
	print '#########(2)'
	if base_preds == [([],[],"")]:
		new_preds_dict = __compress_to_dict(add_preds)
		print '######### *[base_preds is empty:]'
		print '#########(3)'
	else:
		##### ????(check??) The __isFilter_redundant function should be confirmed again
		#####
		new_pairs = [ (a,b) for (a,b) in itertools.product(base_preds, add_preds) if __isFilter_no_common_sort(a, b) is False]
		print '######### *[new_pair_len:]',len(new_pairs)
		print '#########(3)'
		for a, b in new_pairs:
			util_pred.gen_var_preds(a, b, sort_vars_dict, new_preds_dict)

	#k = [ __gen_var_preds(a, b, sort_vars_dict, new_preds_dict) for a, b in new_pairs ]
	print '#########(4)'

	new_com_preds = new_preds_dict.keys()
	print '######### *[new gen_com_preds: num=%s]'%(len(new_com_preds))
	new_com_preds = __filter_redundant(new_com_preds)
	print '######### *[after delete redundant num = %s]'%len(new_com_preds)
	if filter_set!=set():
		new_com_preds = __filter_via_filter_set(new_com_preds, filter_set)
		print '######### *[after delete via filter set num = %s]'%len(new_com_preds)

	new_com_preds_filt = util_pred_filter.filter_by_isNotUnsat(new_com_preds)
	print '######### *[after delete via positive model filter set num = %s]'%len(new_com_preds_filt)

	new_preds = [ elem for elem in new_com_preds_filt if __isFilter_free_var(new_preds_dict[elem], elem, pred_sort_dict) is False ]
	print '######### *[after delete free var, new_preds: num=%s]'%len(new_preds)
	free_var_preds = list(set(new_com_preds_filt) - set(new_preds))
	notUnsat_preds = list(set(new_com_preds) - set(new_com_preds_filt))
	#print '#########free_preds: len=%s'%len(free_var_preds)
	print '#########(5)'

	#new_preds = [ (new_preds_dict[pred][0], new_preds_dict[pred][1], pred) for pred in new_preds]
	#new_preds = [  (a,b) for base_pred in base_preds for add_pred in add_preds for (a,b) in  __connect_var(base_pred, add_pred) if not __filter_no_common_sort(base_pred, add_pred) ]
	#new_preds = [ __combine(a, b) for (a,b) in new_preds if not __filter(a,b,filter_set) ] 
	#print 'new:', len(new_preds)#,new_preds
	sat_preds = __get_sat_preds(new_preds, new_preds_dict, models_sat)
	# model_sat_preds = [ util_pred_model.preds_sat_model(model, new_preds, new_preds_dict) for model in models_sat]
	print '#########(6)'
	#model_sat_preds_compress = [ compress(pred_list) for pred_list in model_sat_preds]
	#sat_preds_compress = reduce(lambda x,y: set(x) & set(y), model_sat_preds_compress, model_sat_preds_compress[0])
	#print '6'

	#sat_preds = list(reduce(lambda x,y: set(x) & set(y), model_sat_preds, model_sat_preds[0]))
	print '#########(7)'
	print '######### sat:', len(sat_preds)#,sat_preds
	#sat_preds = decompress(sat_preds_compress)

	sat_preds_filter = util_pred_filter.filter_by_isUnsat(sat_preds)
	print '######### *[sat preds after filter: num = %s]'%len(sat_preds_filter)#,sat_preds
	if models_unsat!=[]:
		#model_unsat_preds = [ util_pred_model.preds_unsat_model(model, sat_preds_filter, new_preds_dict) for model in models_unsat]
		#unsat_preds = list(reduce(lambda x,y: set(x) & set(y), model_unsat_preds, model_unsat_preds[0]))
		unsat_preds = __get_unsat_preds(sat_preds_filter, new_preds_dict, models_unsat)
	else:
		unsat_preds = sat_preds_filter
	#unsat_preds_compress = reduce(lambda x,y: set(x) & set(y), model_unsat_preds_compress, model_unsat_preds_compress[0])
	#unsat_preds = decompress(unsat_preds_compress)
	print '######### *[check unsat preds = %s]'%len(unsat_preds)
	
	untarget_preds = list((set(free_var_preds) | set(sat_preds_filter)| set(notUnsat_preds)) - set(unsat_preds))
	filter_preds = set(new_preds) - set(sat_preds)
	final_unsat_preds = list((set(sat_preds)- set(sat_preds_filter)) | set(unsat_preds))

	util_pred_filter.addto_isUnsat(unsat_preds)
	util_pred_filter.addto_isNotUnsat(set(sat_preds_filter) - set(unsat_preds))
	#logger.debug("~~~~~~~find target pred: \n%s"%final_unsat_preds)

	print '######### *[final candidate preds = %s]'%len(final_unsat_preds)
	return untarget_preds, final_unsat_preds, filter_preds, new_preds_dict




def __get_satisfied_conjuncts(base_pred, pre_preds, fluent_preds, models_sat, models_unsat, pred_score_dict, filter_set, pred_sort_dict, length=2):
	mvar_list, msorts, mbody = base_pred if base_pred is not None else ([],[],"")

	fluents = context_operator.get_fluents()
	fluent_flag = __detect_fluents(mbody, fluents)

	base_preds, LENGTH = [ (mvar_list, msorts, mbody)], length
	add_preds = fluent_preds if fluent_flag is False else fluent_preds+pre_preds

	sat_pred_list = list()
	sat_pred_dict = dict()
	
	while LENGTH>0:
		# new_unsat_preds is the combined predicates fail to unsat some the models_unsat
		# new_sat_preds is the combined predicates satisfy the two conditions
		print '#######---*[begin base pred [%s] with length(%s)]'%(base_pred, LENGTH)
		new_untarget_preds, new_candidate_preds, new_filter_set, pred_temp_dict = ____combine_preds(base_preds, add_preds, models_sat, models_unsat, pred_score_dict, filter_set, pred_sort_dict)
		print '#######---*[new generate candidate pred num =%s]'%len(new_candidate_preds)
		base_preds = [ (pred_temp_dict[pred][0], pred_temp_dict[pred][1], pred) for pred in new_untarget_preds ]
		add_preds, LENGTH = fluent_preds+pre_preds, LENGTH-1
		filter_set |= __add_filter_elems(new_filter_set)
		sat_pred_list.extend(new_candidate_preds)
		new_candidate_preds = set(new_candidate_preds)
		sat_pred_dict.update({pred: vars_sorts for pred, vars_sorts in pred_temp_dict.iteritems() if pred in new_candidate_preds})

	return sat_pred_list, sat_pred_dict



def __gen_pred_sort_dict(pre_preds, fluent_preds):
	pred_sort_dict = dict()
	for var_list, sort, body in pre_preds:
		for var in var_list:
			body = body.replace(var,'X')
		pred_sort_dict[body] = False

	for var_list, sort, body in fluent_preds:
		for var in var_list:
			body = body.replace(var,'X')
		pred_sort_dict[body] = True
	return pred_sort_dict



def combine_with_preds(subconjunct, model_neg_list, model_pos_list, atomic_pred_list, length):
	#print '----------------'
	pre_pred_list, fluent_pred_list = atomic_pred_list
	pred_sort_dict = __gen_pred_sort_dict(pre_pred_list, fluent_pred_list)

	####[constraint]
	#context_operator.set_pred_constraint_dict(copy.deepcopy(context_operator.get_base_pred_constraint_dict()))
	#if base_pred is not None:
	#	constraints = util_constraint.gen_pred_constraint_dict([base_pred], context_operator.get_fluent_constraint())
	#	context_operator.add_pred_constraint_dict(constraints)
	#####

	########## delete unsat preds

	model_preds = [ util_pred_model.preds_sat_model_org(model, fluent_pred_list) for model in models_sat] 
	model_preds_compress = [ util_pred.compress(pred_list) for pred_list in model_preds]
	#print '---',model_preds_compress
	union_preds = set(model_preds_compress[0])
	for e in range(1, len(model_preds_compress)):
		union_preds = union_preds & set(model_preds_compress[e])
	union_preds = util_pred.decompress(union_preds)

	########

	if union_preds!=[]:
		#print '1,-----', base_pred

		sat_pred_list, sat_pred_dict = __get_satisfied_conjuncts(subconjunct, pre_pred_list, union_preds, models_sat, models_unsat, pred_score_dict, set(), pred_sort_dict, length)
		####constraint
		pred_constraint_dict = util_constraint.filter_pred_constraint(sat_pred_list)
		#context_operator.set_pred_constraint_dict(pred_constraint_dict)
		context_operator.add_pred_constraint_sum_dict(pred_constraint_dict)
		#####
		return sat_pred_list, sat_pred_dict
	else:
		return [], {}

		