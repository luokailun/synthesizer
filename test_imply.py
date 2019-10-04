


from parser import BATparser
BATparser.parser('takeaway.sc')
from prover import z3prover
from model import model_checker
from model import model_interpretor
from model import util_model


'''
#Goal:( numStone()=0 ) => ( numStone()=0&!(turn(p1)) )
#(+)model:
  ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': 'True', 'numStone()': '1', 'turn(p2)': 'False'})
  ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': 'True', 'numStone()': '3', 'turn(p2)': 'False'})
  ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '5', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': 'True', 'numStone()': '5', 'turn(p2)': 'False'})
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'], 'Bool': ['True', 'False']}, {'turn(p1)': 'True', 'numStone()': '11', 'turn(p2)': 'False'})
#conjuncts:
(0):(['G0'], ['_S1'], ['turn(G0)', 'turn(p2)'])
  ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': 'False', 'numStone()': '1', 'turn(p2)': 'True'})
(1):(['G0'], ['Int'], ['G0 > 4', 'G0 % 3 = 1', 'numStone() = G0'])
  ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '5', '4', '7', '6', '8'], 'Bool': ['True', 'False']}, {'turn(p1)': 'True', 'numStone()': '7', 'turn(p2)': 'False'})
(2):(['G0'], ['Int'], ['G0 = 4', 'numStone() = G0'])
  ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '5', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': 'True', 'numStone()': '4', 'turn(p2)': 'False'})
'''

X1 = " (( numStone()=0 ) => ( numStone()=0&!(turn(p1)) ))&!(exists(G0:_S1)[turn(G0)&turn(p2)])&!(exists(G0:Int)[G0>=0&G0 > 4&G0 % 3 = 1&numStone() = G0])&!(exists(G0:Int)[G0>=0&G0 = 4&numStone() = G0])"
#RM1 = ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '5', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': 'False', 'numStone()': '4', 'turn(p2)': 'True'})
M1 =  ({'_S1': ['p2', 'p1'], 'Bool': ['True', 'False']}, {'turn(p1)': 'True', 'numStone()': '7', 'turn(p2)': 'False'})
FM1 = util_model.to_formula(M1)
print FM1
#print z3prover.imply(FM1, X1)
print z3prover.imply(FM1, X1)


