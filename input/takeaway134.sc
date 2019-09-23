

Poss(take(P,X)) <=> numStone>=X and (X=1 or X=3 or X=4) and turn(P)

SSA(numStone=Y, take(P,X)) <=>
			numStone = Y+X

SSA(turn(P), pi(A)) <=> ! turn(P)

Init() <=>  numStone>0 and !numStone%7=0 and !(numStone-2)%7=0 
End() <=> numStone = 0

Win(pi(P)) <=> numStone = 0 and !(turn(P)) 

