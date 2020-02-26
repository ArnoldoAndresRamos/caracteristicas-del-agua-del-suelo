from math import exp

S     =0.75
C     =0.137
MO    =1.6


" Moisture Regressions"
 
q1500t= -0.024*S+0.487*C+0.006*MO+0.005*(S*MO)-0.013*(C*MO)+0.068*(S*C)+0.031
q1500 = q1500t+(0.14*q1500t-0.02) 

Q33t	= -0.251*S+0.195*C+0.011*MO+0.006*(S*MO)-0.027*(C*MO)+0.452*(S*C)+0.299
Q33  = Q33t+((1.283*(Q33t*Q33t))-0.374*(Q33t)-0.015)

Qs_33t =0.278*S+0.034*C+0.022*MO-0.018*(S*MO)-0.027*(C*MO)-0.584*(S*C)+0.078
Qs_33  =Qs_33t+(0.636*Qs_33t-0.107) 

Yet = -21.67*S-27.93*C-81.97*Qs_33 +71.12*(S*Qs_33)+8.29*(C*Qs_33)+14.05*(S*C)+27.16
Ye = Yet+(0.02*(Yet*Yet)-0.113*Yet-0.70)

Qs =Q33+Qs_33-0.097*S+0.043
Pn =(1-Qs)*2.65


" Density Effects"
DF = 1                    # 0.9-1.3 factor de ajuste de densidad"
Pdf = Pn*DF                 #  Densidad ajustada en g.cm3 
Qs_df = 1-(Pdf/2.65)        # humedad saturada, densidad ajustada,% v
Q33_df =Q33-0.2*(Qs-Qs_df)
Qs33_df =Qs_df-Q33_df


" Moiseture-Tension "
B       = (log(1500)-log(33))/(log(Q33)-log(q1500)) 
A       = exp(log(33)+B*log(Q33))
Q       = Qs
Y1500_33 = A*pow(Q,-B)   
Y33_Ye = 33.0-((Q-Q33)*(33.0-Ye)/(Qs-Q33))


"  Moisture–Conductivity"
v   =1/B
Ks  =1930*pow((Qs-Q33),(3-v))
Ko  =Ks*pow((Q/Qs),(3+(2/v)))


"  Gravel Effects "
a   =1
Rw  =0.3
PAW=Q33-q1500
Rv = (a*Rw)/(1-Rw*(1-a))
Pb = Pn*(1-Rv)+(Rv*2.65)
PAWb = PAW*(1-Rv) 
Kb_Ks=1-Rw/(1-Rw*(1-3*a/2))

print( q1500*100, Q33*100,abs(q1500-Q33))
print("Ye",Ye)
print(Qs*100,Pn)
print((Qs33_df)*100)
print(Y1500_33,Y33_Ye)
print(Ko,Ks)
print(PAWb,Kb_Ks,.125-.079)