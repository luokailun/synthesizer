import os
from basic import context_operator
import itertools


m_list = ['a and b and c', 'a and b', 'c and b']
filter_not_unsat = set([('b','c')])


def filter_by_isNotUnsat(new_com_preds, filter_not_unsat=None):
	state = context_operator.get_current_state()
	filter_unsat, filter_not_unsat = context_operator.get_pos_model_filter(state)
	m_list = list()
	for pred in new_com_preds:
		elems = pred.split(' and ')
		feature_set = set(itertools.permutations(elems, len(elems)))
		#print feature_set
		if feature_set & filter_not_unsat == set():
			m_list.append(pred)
	return m_list

#print filter_by_pos_model_isNotFilter(m_list, filter_not_unsat)


def filter_by_isUnsat(new_com_preds, filter_not_unsat=None):
	state = context_operator.get_current_state()
	filter_unsat, filter_not_unsat = context_operator.get_pos_model_filter(state)
	m_list = list()
	for pred in new_com_preds:
		elems, feature_set = pred.split(' and '), set()
		for length in range(1, len(elems)+1):
			feature_set.update(itertools.permutations(elems, length))
		#print feature_set
		if feature_set & filter_unsat == set():
			m_list.append(pred)
	return m_list



def addto_isNotUnsat(pred_list):
	state = context_operator.get_current_state()
	pred_list = [tuple(pred.split(' and ')) for pred in pred_list]
	context_operator.update_pos_model_filter(state,list(), pred_list)


def addto_isUnsat(pred_list):
	state = context_operator.get_current_state()
	pred_list = [tuple(pred.split(' and ')) for pred in pred_list]
	context_operator.update_pos_model_filter(state, pred_list, list())

