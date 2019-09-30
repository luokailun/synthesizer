


from model import model_checker


#!exists(X1:Int)[numStone() > X1]


M = ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': 'False', 'numStone()': '0', 'turn(p2)': 'True'})

C = (['X1'],['Int'],["numStone()> X1"])


M =({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], 'Bool': ['True', 'False']}, {'turn(p1)': 'False', 'numStone()': '4', 'turn(p2)': 'True'})
M = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], 'Bool': ['True', 'False']}, {'turn(p1)': 'False', 'numStone()': '0', 'turn(p2)': 'True'})
C = (['X1'], ['Int'], ['! numStone() = 4', 'numStone()> X1', 'X1 >=0'])

print model_checker.unsat_conjunct_math([M],C)


from model import model_checker
from model import model_interpretor
from prover import z3prover
from formula import Conjunct

from parser import BATparser
BATparser.parser('takeaway.sc')

C = (['X1'], ['Int'], ['! numStone() = 4', 'numStone()> X1'])
C = (['X1'],['Int'],["numStone()> X1", "X1>=0"])

print '!(%s)'%(Conjunct.to_formula(C))

print z3prover.check_unsat('!(%s)'%(Conjunct.to_formula(C)))