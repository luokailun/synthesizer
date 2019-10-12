


from parser import BATparser
BATparser.parser('chompNN.sc')
from prover import z3prover
from model import model_checker
from model import model_interpretor
from model import util_model
from basic import format_output


'''
X1 = "(( numStone()=0 ) => ( numStone()=0&!(turn(p1)) ))&!(exists(G0:Int)[G0>=0&numStone() > G0&! turn(p1)])&!(exists(G0:Int)[G0>=0 &  numStone() = G0 & G0 % 4 = 0 ])"
X2 = "exists(K100:Int)[ (numStone()>=K100&(K100=1|K100=2|K100=3)&turn(p1))&((( (numStone()=0+K100) ) => ( (numStone()=0+K100)&!((!turn(p1))) ))&!(exists(G0:Int)[G0>=0&G0 % 2 = 1&(numStone()=G0+K100)])&!(exists(G0:Int)[G0>=0&G0 % 4 = 2&(numStone()=G0+K100)])) ]"


Y1 = "(( numStone()=0 ) => ( numStone()=0&!(turn(p1)) ))&!(exists(G0:Int)[G0>=0&numStone() > G0&! turn(p1)])&!(exists(G0:Int)[G0>=0&numStone() = G0&G0 % 4 = 0])"
Y2 = "exists(K103:Int)[ (numStone()>=K103&(K103=1|K103=2|K103=3)&turn(p1))&((( (numStone()=0+K103) ) => ( (numStone()=0+K103)&!((!turn(p1))) ))&!(exists(G0:Int)[G0>=0&G0 % 2 = 1&(numStone()=G0+K103)])&!(exists(G0:Int)[G0>=0&G0 % 4 = 2&(numStone()=G0+K103)])) ]"

print z3prover.imply(X1, 'false')
print z3prover.imply(Y1, 'false')
print
print z3prover.imply(X1, Y1)
print z3prover.imply(Y1, X1)

print z3prover.imply(X2, Y2)
print z3prover.imply(Y2, X2)

print z3prover.imply(Y1, Y2)
print z3prover.imply(X1, X2)
#print z3prover.imply(Y1, X2)
'''



'''
M1 = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'fpile()': '1', 'turn(p1)': 'False', 'spile()': '1', 'turn(p2)': 'True'}, {})

from model import util_model
from model import model_interpretor
M1 = util_model.to_formula(M1)
#print M1

G1 ="(( fpile()=0&spile()=0 ) => ( fpile()=0&spile()=0&!turn(p1) ))&!(exists(G0:_S1)[turn(G0)&turn(p2)])"
G2 = "(( fpile()=0&spile()=0 ) => ( fpile()=0&spile()=0&!turn(p1) ))&!(exists(G0:Int)[G0>=0&fpile() = G0&spile() > G0])"


M2 = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'fpile()': '1', 'turn(p1)': 'True', 'spile()': '2', 'turn(p2)': 'False'}, {})
M2 = util_model.to_formula(M2)

from regression import program_regress
from algorithm import algorithm2
RG2 = program_regress.E_regress(G2, "pi(K23:Int)[takeF(p1,K23)]")
#print model_interpretor.interpret_model(z3prover.imply(G1, RG2))

print
print z3prover.imply(M2, G1)
print z3prover.imply(M2, RG2)



print 

RM1 = program_regress.E_regress(M1, algorithm2.__generate_pi_action('p1'))
print z3prover.imply(M2, RM1)

print 
print z3prover.imply(M1, G2)
print 
print z3prover.imply(RM1, RG2)

print '````````````'
print M1
print RM1
print 
print G2
print RG2
'''

from model import model_interpretor
from basic import context_operator


F1 = " (( !Ch(0,0) ) => ( !Ch(0,0)&turn(p1) ))&!(exists(G0:Int)[G0>=0&G0 = 0&Ch(0,G0)])"
F2 = "(( !Ch(0,0) ) => ( !Ch(0,0)&turn(p1) ))&!(exists(X1:Int)[X1>=0&Ch(1,X1)])&!(exists(X1:Int)[X1>=0&Ch(0,X1)])"
DS0 = context_operator.get_axioms()['init']['']

M = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'False', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'})
FM = util_model.to_formula(M)
print format_output.format_output(M, 'CH')

