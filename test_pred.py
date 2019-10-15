


from parser import BATparser
#BATparser.parser('new_chompNN.sc')
#BATparser.parser('new_chomp2N.sc')

'''
BATparser.parser('chompNN.sc')
from formula import Predicate
math_preds, fluent_preds = Predicate.generate_preds('chompNN.sc')

from model import model_interpretor
from basic import Util
from model import util_z3_model
from basic import context_operator

'''


pos_model_list = [
 ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'True', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'True', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'True', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,2)': 'False', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'turn(p1)': 'False', 'Ch(2,4)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(1,3)': 'False', 'Ch(0,3)': 'True', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'})
]

neg_model_list = [({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'True', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'})]


'''
from formula import Xconjunct

pred_list = math_preds + fluent_preds
basic_conjunct_list = [(v_list, s_list, [pred]) for v_list, s_list, pred in pred_list]

#print basic_conjunct_list
#exit(0)
#basic_conjunct_list = [([], [], ['Ch(1,1)'])]
basic_conjunct_list = Xconjunct.unify_conjuncts(basic_conjunct_list)

#print basic_conjunct_list
#exit(0)
empty_conjunct = ([],[],[])
print Xconjunct.generate_conjunct(empty_conjunct, pos_model_list, neg_model_list, basic_conjunct_list, 3)
'''






