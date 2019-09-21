#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-23 15:57:26
# @Author  : Kailun Luo (luokl3@mail2.sysu.edu.cn)
# @Link    : https://sdcs.sysu.edu.cn
# @Version : $Id$




VAR_INDEX = 0

##########################################################################################


SORT_INDEX = 1
SORT_NAME = "_S"
SORT = dict()
  
SYMBOL_TO_SORT_LIST = list()
SYMBOLS_EQUAL_LIST = list()

SORT_SYMBOLS_DICT = dict()
SYMBOL_SORTS_DICT = dict()

FLUENT_SORT_DICT = dict()
PREDICATE_SORT_DICT = dict()

##########################################################################################

AXIOMS = dict()
AXIOMS['ssa'] = dict()
AXIOMS['poss'] = dict()
AXIOMS['win'] = dict()
AXIOMS['init'] = dict()
AXIOMS['end'] = dict()


##########################################################################################

ZERO_FLUENT_SET = set()
FEATURE_LIST = list()

ACTION_LIST = list()
FLUENT_LIST = list()
PREDICATES = list()


##########################################################################################

NREGX_FUNCTION_PATTERNS = list()
FUNCTION_PATTERNS = list()

FUNCTION_LAMBDA_REGRESS = None
PREDICATE_LAMBDA_REGRESS = None


##########################################################################################

Z3_HEADER =""

##########################################################################################

TEMPLATE = 'small'

##########################################################################################

LOCAL_DICT = dict()

ACTION = ""

##########################################################################################
RPLIST = list()
RP_INDEX = 0
##########################################################################################
'''
import re
s = "ahhhh_fdlsfj and ffslfsf or jflsdfjl"

pattern =re.compile(r"(?:(?<!and)(?<!or).(?!and)(?!or))+")

print pattern.findall(s)

'''

#x = list(set(a[i]+a[j]))
#y = len(a[j])+len(a[i])
'''
a= ['INT', 'INT', ('m', 2), 'INT', ('f', 1), ('num', 1), ('g', 1), 'INT', ('m', 2), 'INT', ('num', 1)]
b= ['num']
print len(list(set(a+b)))
print len(set(a)),len(set(b))
[['num', 'num'],  
[  ['INT', 'INT', ('m', 2), 'INT', ('f', 1), ('num', 1), ('g', 1), 'INT', ('m', 2), 'INT', ('num', 1)]]

[  [('m', 2), ('f', 1), 'INT', ('g', 1), 'num', ('num', 1)]]

'''



#apply(hello,[('Init', '', ' numStone >0  '), ('Init', '', ' turn(p1) and !turn(p2)    ')])


#hello()