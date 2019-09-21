#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-29 17:15:05
# @Author  : Kailun Luo (luokl3@mail2.sysu.edu.cn)
# @Link    : https://sdcs.sysu.edu.cn
# @Version : $Id$
 
import os
from basic import my_parser
from basic import Util
from basic import regress
import counterexample
import abstraction
import predicate
from basic import context_operator
import sys
sys.setrecursionlimit(100000)
#from basic import util_transiform
from basic import util_z3
import json
import FSA
import util_pred_formula
import util_pred_score
import util_cache
import util_constraint
from basic import util_trans_smt
import time
import heuristic
import modify2
import modify3
import modify4


import mylog as logging
logger = logging.getLogger(__name__)


                          


##############################################################################################################################################################




 


##############################################################################################################################################################		


def __combine(X1,X2):
	#X1 = { q: util_formula.decode_pred_formula(X1[q]) for q in X1.keys()}
	#X2 = { q: util_formula.decode_pred_formula(X2[q]) for q in X2.keys()}
	return {q: "( %s ) and ( %s )" %(X1[q], X2[q]) for q in X1.keys() }


def __mergeModelSet(Mset1, Mset2):
	return  {q : Util.del_redundant_dict(Mset1[q]+Mset2[q]) for q in Mset1.keys()}


##############################################################################################################################################################


def abstract(X, Mset, Ln, Lq, Lcm, Lscore, Preds, flag_backtract):
	X_new = dict()
	for q in X.keys():
		context_operator.set_current_state(q)
		if Mset[q]!=list():
			X_new[q] = abstraction.abstract_state(q, X[q], Mset[q], Ln[q], Lq[q], Lcm[q], None, Lscore[q], Preds, flag_backtract)
			if X_new[q] is None:
				#return False, X, util_pred_score.minus_pred_score_dict(X[q], Lscore[q]) 
				return False, X, q
	#return True, {q: X_new[q] if q in X_new.keys() else X[q] for q in X.keys() }, dict()
	return True, {q: X_new[q] if q in X_new.keys() else X[q] for q in X.keys() }, q


##############################################################################################################################################################
#k = {u'states': [u'q_1', u'q_2'], u'starting_state': u'q_1', u'transitions': {u'q_2': [{u'q_1': u'pi(X:Int)[take(p2,X)]'}], u'q_1': [{u'q_2': u'pi(X:Int)[(numStone()-X)%4=0?;take(p1,X)]'}]}, 'state_succ_label': {u'q_2': [u'pi(X:Int)[take(p2,X)]'], u'q_1': [u'pi(X:Int)[(numStone()-X)%4=0?;take(p1,X)]']}, 'state_succ': {u'q_2': [u'q_1','q_1'], u'q_1': [u'q_2']}}


#print __compoute_abs_order(k)

##----- abandon(2018.7.15)
'''
def __propergation(q, q_formula, X, Lcm, models_neg, fsa):
	for p, sucessors in fsa['state_succ'].iteritems():
		if q in sucessors:
			X[p], Lcm[p], models_neg[p] = abstraction.delete_via_models(p, q, X[p], q_formula, Lcm[p], models_neg[p], fsa)
	return X, Lcm, models_neg
'''		 

def refine(X, L, Ln, Lp, Lcm, Lscore, fsa, Preds, flag_backtrack):
	state_order = [ q for q in __compoute_abs_order(fsa) if L[q]!=list()] 
	for q in state_order:
		context_operator.set_current_state(q)
		print 
		print "@--------refine state[%s] with formula %s"%(q, X[q])
		print "@--------new p-counterexamples %s"%L[q]
		print "@--------old p-counterexamples %s"%Lp[q]
		print "@--------old n-counterexamples %s"%Ln[q]
		X[q] = abstraction.refine_state(q, X[q], L[q], Ln[q], Lp[q], Lcm[q], Lscore[q], Preds, flag_backtrack)
		print "@--------results %s"%X[q]
		#print '#--------before propogation: %s'%X
		#X, Lcm, Ln= __propergation(q, X[q], X, Lcm, Ln, fsa)
		#print '#--------after propogation: %s'%X
	#return {q: X_new[q] if q in X_new.keys() else X[q] for q in X.keys() }, L

	return True, X, dict()


def __model_progress(state_models, fsa):
	L = {q: list() for q in fsa['states']}
	print '~~~~~',L
	for state, model in state_models:
		L_new = FSA.fsa_model_progress(state, model, fsa)
		print '~~~~~~~',L_new
		L = __mergeModelSet(L, L_new)
		print '~~~~~~~',L
	return L

##############################################################################################################################################################

def __simply_formula(formula):
	#return util_pred_formula.simplify(formula)
	return util_pred_formula.decode_pred_formula(formula)

def simplify(X):
	#print '!!!!!!!!!!!!!!!!!',X
	return {q: __simply_formula(X[q]) for q in X.keys()}

def __load_state_constaints(domain_name):
	with open("state_constraint","r") as fp_fsa:
		mdict = json.load(fp_fsa)[domain_name]
		context_operator.set_state_constraints(mdict['sc'])
		context_operator.set_unknown(mdict['unknown'])
		context_operator.set_bound(mdict['bound'])
		context_operator.set_action_function(mdict['action_function'])
		context_operator.set_template_order(mdict['template'])


def __before_verify(domain_name, player, mdir):
	my_parser.parser("./%s/"%mdir+domain_name+".sc", mdir) 
	fsa = FSA.load_fsa_from_file("./%s/"%mdir+domain_name+".fsa")
	__load_state_constaints(domain_name)
	#print context_operator.get_functions_sorts()
	#print context_operator.get_predicate_sorts()

	Init = context_operator.get_axioms()['init']['']
	#print '----------',Init
	lambda_fun, para_list = context_operator.find_axiom_with_feature('win', Util.generate_function_feature(player+'()'))
	Win = lambda_fun(para_list)
	End = context_operator.get_axioms()['end']['']
	#print Goal
	return Init, fsa, "( %s ) => ( %s )"% (End, Win)


def __set_filter_set(states):
	for q in states:
		context_operator.set_pos_model_filter(q, set(), set())


def __set_conjunct_cache(states):
	for q in states:
		context_operator.set_conjunct_cache(q, dict(), dict())


def __init_conjunct_constraint_cache(states):
	for q in states:
		context_operator.init_conjunct_constraint_cache(q)


def __get_choice_reset_states(states, fsa):
	succ_states = sum([ fsa['state_succ'][q] for q in states],[])
	return list(set(fsa['states'])- set(states)- set(succ_states))

def __init_base_pred_constraint_dict(Preds, fluent_constraints):
	pred_constraints= util_constraint.gen_pred_constraint_dict(Preds[1], fluent_constraints)
	pred_constraints.update({body:dict() for var_list, sorts, body in Preds[0]})
	context_operator.set_base_pred_constraint_dict(pred_constraints)



def verify(domain_name, player, mdir):
	Init, fsa, Goal = __before_verify(domain_name, player, mdir)
	math_symbols = modify2.get_useless_math_symbols(domain_name, mdir)
	#fluent_constraints = {'cell@1':['1','2']}
	#fluent_constraints = {'Ch@1':['0','1','2']}
	fluent_constraints = dict()
	action_constraints = dict()
	#action_constraints = {'eat@2':['1','2'], 'eat@4':['1','2']}
	#action_constraints = {'eat@2':['1','2']}
	context_operator.set_fluent_constraint(fluent_constraints)
	context_operator.set_action_constraint(action_constraints)

	Preds = predicate.genPreds(fluent_constraints)

	print Preds
	exit(0)
	Preds = (modify2.deleteUselessMath(Preds[0], math_symbols), modify4.deleteLast(Preds[1]))

	num_pred =len(Preds[0])+len(Preds[1])
	num_abs =0
	num_ref =0
	num_bak =0
	num_re =0
	print
	print '--------------------'
	print len(Preds[0])+len(Preds[1])
	print 
	#print Preds[0]

	#print Preds[0]
	#print Preds[1]
	#exit(0)
	pred_score_dict = util_pred_score.init_preds_base_score(Preds[0]+Preds[1])
	#Preds = (Preds[0], predicate.predicate_filter_via_constraints(Preds[1]), fluent_constraints)
	#fluent_constraints = dict()
	#print Preds[1]
	#print len(Preds[0]+Preds[1])
	#exit(0)
	__init_conjunct_constraint_cache(fsa['states'])
	__init_base_pred_constraint_dict(Preds, fluent_constraints)

	Ln = { state : list() for state in fsa['states'] }
	Lp = { state : list() for state in fsa['states'] }
	Lcm = {state : dict() for state in fsa['states'] }
	Lscore = {state: dict(pred_score_dict) for state in fsa['states']}
	__set_filter_set(fsa['states'])
	__set_conjunct_cache(fsa['states'])
	modify2.init_history_store(fsa['states'])
	modify3.init_refine_conjuncts_back(fsa['states'])
	
	X = {q: "(%s)"%Goal for q in fsa['states']}
	X_sim = X
	Mset, n = dict(), 1
	while n>0:
		logger.info("\n------------begin-%s---------"%n)
		#X_next = __combine(X_sim, FSA.fsa_regress(X_sim,fsa))
		X_next = FSA.fsa_regress(X_sim,fsa)
		logger.info('#formula label after-regress--%s'%X_next)
		backtrack_list = list()
		flag = True
		flag_out_loop = True
		while not label_imply(X_sim, X_next, fsa, Mset, backtrack_list):
			modify2.add_history_store(X)
			if backtrack_list!=list():
				num_backtract +=1
				'''
				if num_backtract>=5:
					print '---------------adjust score of preds:'
					modify2.minus_pred_score_dict(fsa['states'], Lscore)
					print
					print "restart"
					print Lscore
					print
					X = {q: "(%s)"%Goal for q in fsa['states']}
					X_sim = simplify(X)
					Ln = { state : list() for state in fsa['states'] }
					Lp = { state : list() for state in fsa['states'] }
					Lcm = {state : dict() for state in fsa['states']}
					__set_filter_set(fsa['states'])
					__set_conjunct_cache(fsa['states'])
					__init_conjunct_constraint_cache(fsa['states'])
					modify2.init_history_store(fsa['states'])
					X_next = FSA.fsa_regress(X_sim,fsa)
					logger.info('#formula label after-regress--%s'%X_next)
					backtrack_list = list()
					num_re+=1
					flag_out_loop=False
					continue
				'''

				X, Mset, Ln, Lp, Lcm, results = util_cache.reset_from_state_cache()
				states = __get_choice_reset_states(backtrack_list, fsa)
				util_cache.reset_choices(states)
				context_operator.set_counterexample_result(results)
				flag_backtract = True
				num_bak+=1
				print '***********------------reset-----------------:'
				print X
				print '***********------------reset-----------------'
				if flag_out_loop is True:
					#print 
					#print '----------------hallowork'
					#print 
					#time.sleep(3)
					break
			else:
				num_backtract = 0
				print '***********------------set cache-----------------:'
				print X
				print '***********------------set cache-----------------'
				flag_backtract = False
				util_cache.add_to_state_cache(X, Mset, Ln, Lp, Lcm, context_operator.get_counterexample_result())
				util_cache.reset_choices(fsa['states'])
			backtrack_list = list()
			flag_out_loop = False
			Mset, ill_state_models = abstraction.check_models_legal(Init, Mset, fsa)
			if ill_state_models == []:
				flag, X, state = abstract(X, Mset, Ln, Lp, Lcm, Lscore, Preds, flag_backtract)
				X_sim = simplify(X)
				#X_next = __combine(X_sim, FSA.fsa_regress(X_sim,fsa))
				Ln = __mergeModelSet(Ln, Mset)
				num_abs+=1
			else:
				L = __model_progress(ill_state_models,fsa)
				flag, X, qscore = refine(X, L, Ln, Lp, Lcm, Lscore, fsa, Preds, flag_backtract)
				X_sim = simplify(X)
				#X_next = __combine(X_sim, FSA.fsa_regress(X_sim,fsa))
				Lp = __mergeModelSet(Lp, L)
				num_ref+=1
			print '\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
			for q,f in X.iteritems():
				print q,f.replace(Goal,"")
			print '#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
			flag_backtract = False
			if flag is False:
				print '---------------adjust score of preds:'
				modify2.minus_pred_score_dict(fsa['states'], Lscore)
				print
				print "restart"
				print Lscore
				print
				X = {q: "(%s)"%Goal for q in fsa['states']}
				X_sim = simplify(X)
				Ln = { state : list() for state in fsa['states'] }
				Lp = { state : list() for state in fsa['states'] }
				Lcm = {state : dict() for state in fsa['states']}
				__set_filter_set(fsa['states'])
				__set_conjunct_cache(fsa['states'])
				__init_conjunct_constraint_cache(fsa['states'])
				modify2.init_history_store(fsa['states'])
				X_next = FSA.fsa_regress(X_sim,fsa)
				logger.info('#formula label after-regress--%s'%X_next)
				backtrack_list = list()
				num_re+=1
				#Lscore.update(qscore)
				#exit(0)
			else:
				#X_next = __combine(X_sim, FSA.fsa_regress(X_sim,fsa))
				X_next = FSA.fsa_regress(X_sim,fsa)

		n=n+1
		modify2.add_history_store(X)
		if flag:
			if flag_backtract is False:
				util_cache.add_to_state_cache(X, Mset, Ln, Lp, Lcm, context_operator.get_counterexample_result())
				util_cache.reset_choices(fsa['states'])
			else:
				X_sim = simplify(X)
			flag_out_loop = True
			M =  __imply_get_model(Init, X_sim[fsa['starting_state']])
			logger.info("\n####return counterexample: %s" %M)
			if M is not True:
				#del_flag, formula, conjuncts = heuristic.delete_heuristic(Init, X[fsa['starting_state']])
				del_flag = False
				if del_flag is not True:
					L = FSA.fsa_model_progress(fsa['starting_state'],M, fsa)
					flag, X, qscore = refine(X, L, Ln, Lp, Lcm, Lscore, fsa, Preds, flag_backtract)
					Lp = __mergeModelSet(Lp, L)
					num_ref+=1
				else:
					X[fsa['starting_state']] = formula
					context_operator.set_current_state(fsa['starting_state'])
					util_cache.remove_cache_if_exits(conjuncts)

				X_sim = simplify(X)
				print '--------- refine result:', X
			else:
				print "success!!"
				print num_pred
				print num_abs
				print num_ref
				print num_bak
				print num_re
				return "yes"


def main():
	verify("new_chompNN","p1", "game_domains")

#(assert (forall ((X Int) (Y Int) (W Int) (Z Int)) (=> (and (and (and (= lastx X) (= lasty Y)) (>= W X)) (>= Z Y)) (not (Ch W Z)))))

if __name__ == '__main__':
	from basic import context_operator
	from cProfile import Profile
	prof = Profile()
	prof.runcall(main)
	prof.print_stats()

'''
if __name__ == "__main__":
       import profile
       profile.run("foo()")
'''

#(['Z10', 'Z11', 'Z12'], ['Int', 'Int', 'Int'], 'Z10 = Z11 + Z12')
#(['Z10', 'Z11', 'Z12'], ['Int', 'Int', 'Int'], 'Z10 = Z11 * Z12')



