


from parser import BATparser
BATparser.parser('takeaway.sc')
from prover import z3prover
from model import model_checker
from model import model_interpretor



f2 = "(( numStone()=0 ) => ( numStone()=0&!(turn(p1)) ))&!exists(X1:Int)[numStone() > X1]"
print z3prover.imply(f2, 'false')
print z3prover.imply('false', f2)


