


from parser import BATparser
BATparser.parser('new_chompNN.sc')
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


F1 = "(( !Ch(0,0) ) => ( !Ch(0,0)&turn(p1) ))&!(exists(G0:Int)[G0>=0&ylen() > G0&! Ch(0,G0)])"
F2 = "forall(K100:Int,K101:Int)[ Ch(K100,K101)&turn(p2)&K100>=0&K100<xlen()&K101>=0&K101<ylen()=>((( !(Ch(0,0)&(K100>0|K101>0)) ) => ( !(Ch(0,0)&(K100>0|K101>0))&(!turn(p1)) ))&!(exists(G0:Int)[ exists(K102:Int)[ (xlen()=K102)&(G0>=0& K102 > G0&! (Ch(G0,G0)&(K100>G0|K101>G0)))] ])) ]"



result = z3prover.imply(F1, F2)
#print model_interpretor.interpret_model(result)

from algorithm import algorithm2
print algorithm2.__generate_small_model(F1, F2, result,  MAX_VALUE=2)







