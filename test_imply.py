


from parser import BATparser
BATparser.parser('takeaway.sc')
from prover import z3prover
from model import model_checker
from model import model_interpretor


#f1 = "forall(K12:Int)[ (numStone()>=K12&(K12=1|K12=2|K12=3)&turn(p2) => (( (numStone()=0+K12) ) => ( (numStone()=0+K12)&!((!turn(p1))) ))) ]"
#f2 = 'false'

goal = "numStone()=0 => turn(p2)"

M1 = (None, {'turn(p1)': True, 'numStone()': 0, 'turn(p2)': False})
f1 = model_checker.to_formula(M1)
print f1 
#exit(0)

#f2 = "exists(K13:Int)[ (numStone()=K13+1)&( K13 %4=0&(!turn(p1)))]"
f2 = "forall(K12:Int)[ numStone()>=K12&(K12=1|K12=2|K12=3)&turn(p2)=>(exists(K13:Int)[ (numStone()=K13+K12)&( ! K13 %4=0&(!turn(p1)))]) ]"
print z3prover.imply(f1, f2)
print model_interpretor.interpret_model(z3prover.imply(f1, f2))
print z3prover.imply(f1, goal)





#f3 = "forall(K12:Int)[ 0>=K12&(K12=1|K12=2|K12=3)&turn(p2)=>(exists(K13:Int)[ (numStone()=K13+K12)&( K13 %4=0&(!turn(p1)))]) ]"
