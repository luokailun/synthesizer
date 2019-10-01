


from parser import BATparser
from formula import predicate_filter
BATparser.parser('takeaway.sc')
#BATparser.parser('new_chomp2N.sc')


from formula import Predicate

Predicate.generate_preds('takeaway.sc')


exit(0)

#print '\n'.join([str(e) for e in p1+p2])