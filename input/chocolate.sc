

Poss(takeF(P,X)) <=> fpile >X and X>0 and fpile -X >= spile and turn(P)
Poss(takeS(P,X)) <=> spile >X and X>0 and turn(P)


SSA(fpile =Y, takeF(P,X)) <=> fpile = Y+X
SSA(fpile =Y, takeS(P,X)) <=> fpile = Y
SSA(spile =Y, takeS(P,X)) <=> spile = Y+X
SSA(spile =Y, takeF(P,X)) <=> spile = Y
			
SSA(turn(P), pi(A)) <=> ! turn(P)


Init() <=>  !fpile=spile and fpile>=1 and spile>=1
End() <=> fpile = 1 and spile = 1

Win(pi(P)) <=> fpile = 1 and spile = 1 and !turn(P) 

