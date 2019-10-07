


from parser import BATparser
BATparser.parser('takeaway.sc')
from prover import z3prover
from model import model_checker
from model import model_interpretor
from model import util_model


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







