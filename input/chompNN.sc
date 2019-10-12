
Poss(eat(P,X,Y)) <=> Ch(X,Y) and turn(P) and X>=0 and X<xlen and Y>=0 and Y<ylen

SSA(Ch(X,Y), eat(P,I,J)) <=>  Ch(X,Y) and (I>X or J>Y)

SSA(xlen = Y, pi(A)) <=> xlen =Y
SSA(ylen = Y, pi(A)) <=> ylen =Y

Init() <=> forall(X,Y)[ X>=0 and X<xlen and Y>=0 and Y<ylen =>Ch(X,Y)] and xlen>1 and ylen=xlen
End() <=> !Ch(0,0)
Win(pi(P)) <=> !Ch(0,0) and turn(P)
  




