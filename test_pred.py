


from parser import BATparser
#BATparser.parser('new_chompNN.sc')
#BATparser.parser('new_chomp2N.sc')
BATparser.parser('takeaway134.sc')


from model import model_interpretor
from basic import Util
from model import util_z3_model

M =['sat\n', '(model \n', '  ;; universe for _S1:\n', '  ;;   _S1!val!1 _S1!val!0 \n', '  ;; -----------\n', '  ;; definitions for universe elements:\n', '  (declare-fun _S1!val!1 () _S1)\n', '  (declare-fun _S1!val!0 () _S1)\n', '  ;; cardinality constraint:\n', '  (forall ((x _S1)) (or (= x _S1!val!1) (= x _S1!val!0)))\n', '  ;; -----------\n', '  (define-fun numStone () Int\n', '    9)\n', '  (define-fun p1 () _S1\n', '    _S1!val!0)\n', '  (define-fun p2 () _S1\n', '    _S1!val!1)\n', '  (define-fun True () Bool\n', '    false)\n', '  (define-fun False () Bool\n', '    false)\n', '  (define-fun turn ((x!0 _S1)) Bool\n', '    (= (ite (= x!0 _S1!val!0) _S1!val!0 _S1!val!1) _S1!val!0))\n', ')\n']
#print util_z3_model.get_fun(M)
print model_interpretor.interpret_model(M)


