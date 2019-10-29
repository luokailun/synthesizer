



#f1 = "(( chip1()=1&chip2()=1 ) => ( chip1()=1&chip2()=1&!turn(p1) ))&!(chip1() = 1&! chip2() = 2)&!(chip2() = 0)&!(chip1() = 0)&!(exists(G0:Int)[G0>=0&chip1() > G0&! chip2() >= G0])"


from parser import BATparser
BATparser.parser('empty.sc')
from regression import program_regress
from algorithm import algorithm3
from basic import context_operator


def get_end():
	End = context_operator.get_axioms()['end']['']
	return End

f1 = "(!chip1()%2=1 | !chip2()%2=1) & turn(p1)"
f2 = " chip1()%2=1 & chip2()%2=1"


regress_formula1 = program_regress.A_regress(f1, algorithm3.__generate_pi_action('p2'))
regress_formula2 = "!(%s)=>(%s)"%(get_end(), program_regress.E_regress(f2, algorithm3.__generate_pi_action('p1')))


print algorithm3.__check_convergence(f1, regress_formula2)
print algorithm3.__check_convergence(f2, regress_formula1)




#print regress_formula1