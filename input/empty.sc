

Poss(empty1(P,X)) <=> chip2 >X and X>0 and turn(P)
Poss(empty2(P,X)) <=> chip1 >X and X>0 and turn(P)


SSA(chip1 =Y, empty1(P,X)) <=> Y=X
SSA(chip1 =Y, empty2(P,X)) <=> chip1 = Y+X
SSA(chip2 =Y, empty1(P,X)) <=> chip2 = Y+X
SSA(chip2 =Y, empty2(P,X)) <=> Y=X
			
SSA(turn(P), pi(A)) <=> ! turn(P)


Init() <=>  (! chip1 % 2 = 1 or ! chip2 % 2 = 1) and chip1>0 and chip2>0
End() <=> chip1 = 1 and chip2 = 1

Win(pi(P)) <=> chip1 = 1 and chip2 = 1 and !turn(P) 

