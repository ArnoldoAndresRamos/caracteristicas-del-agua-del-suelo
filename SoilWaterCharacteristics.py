import math

def watersoil(Arcilla = 0, Arena = 0, MateriaOrganica = 0, Salinidad=0, Compactacion = 0, Grava = 0):
    
    C = Arcilla             # % 
    S = Arena               # %
    MO = MateriaOrganica    # %
    DF = Compactacion       # Factor de Densidad ajustada entre 0.9 - 1.3
    Rw = Grava              # % Volumen
      
        
    """ Q1500  humedad a 1500 kPa """
    def humedad_1500KPa():
        Q1500t = -(0.024*S) + (0.487*C) + (0.006*MO) + (0.005*(S*MO)) - (0.013*(C*MO)) + (0.068*(S*C)) + 0.031
        return Q1500t + (0.14 * Q1500t -0.02)
    Q1500 = humedad_1500KPa()
    print(Q1500)
    
    
    """ Q33t = humedad a 33 kPa  """
    def humedad_33KPa():
        Q33t = -0.251*S+0.195*C+0.011*MO+0.006*(S*MO)-0.027*(C*MO)+0.452*(S*C)+0.299
        return Q33t+(1.283*(Q33t*Q33t)-0.374*(Q33t)-0.015)
       
    Q33 = humedad_33KPa()
    print(Q33)
    
        
    """  Qs_33 = Humedad de saturación 0kPa - humedad a 33 kPa, densidad normal  """
    def humedad_saturacion_de_0KPa_a_33KPa():
        Qs_33t = 0.278*S+0.034*C+0.022*MO-0.018*(S*MO)-0.027*(C*MO)-0.584*(S*C)+0.078
        return Qs_33t + (0.636*Qs_33t-0.107)
    
    Qs_33 = humedad_saturacion_de_0KPa_a_33KPa()
    print(Qs_33)
    
    
    """Humedad saturada (0 kPa), densidad normal,% v"""
    def humedad_saturada_0KPa():
        return Q33 + Qs_33 - 0.097 * S + 0.043
            
    Qs = humedad_saturada_0KPa()
    print("Qs",Qs)
        
    
    """  Densidad normal, g/cm3 """
    Pn = (1-Qs)*2.65
    print("Pn ",Pn)   
    
    
    """  efecto de la densidad """
    Pdf = Pn * DF 
    print("Pdf ",Pdf)
    
    """  humedad de Saturacio   Saturated moisture (0 kPa), adjusted density, """
    Qs_DF = 1-(Pdf/2.65)
    print(Qs_DF)
    
    
    
    """  humedad a 33 kPa ajustada a la densidad normal  """
    Q33_DF = Q33 - 0.2 * (Qs-Qs_DF)
    print("Q33_DF",Q33_DF)
    
    
    """  humedad a 33 kPa ajustada a la densidad """
    QsDF_Q33DF = Qs_DF - Q33_DF
    print(QsDF_Q33DF)
    
    
    B = (math.log(Q33_DF)-math.log(Q1500))/(math.log(1500)-math.log(33))
    print("B",B)
    delta = 1/B 
    
    
    Ks = 1930 * (math.pow((QsDF_Q33DF),3-B))
    print(Ks) 
    
    
    """ Gravel Red. Of  Sat Cond."""
    u = (1-Rw)/(1-Rw*(1-1.5*(Pdf/2.65)))
    print(u)
    
    
    """ efecto de la graba en la Ks """
    Ks = Ks*u
    print("Ks DF",Ks)

    
    A = math.exp(math.log(33)+(delta * math.log(Q33_DF)))
    print(A)
    print(delta)
    
    
    """Humedad saturada (0 kPa), densidad ajustada,% v"""
    
    Q1 = Q33_DF +QsDF_Q33DF - 0.097 * S + 0.043
    print("Qs2",Q1)
    
    
    """ Tension en la entrada de aire primera solucion en KPa """
    def tension_entrada_de_aire():
        Yet = -21.67*S-27.94*C - 81.79*Qs_33+71.12*(S*Qs_33)+8.29*(C*Qs_33)+14.05*(S*C)+27.16
        return  Yet+(0.02*(Yet*Yet)-0.113*Yet-0.70)
    
    Ye  = tension_entrada_de_aire()
    print(Ye)        
   
        
    ### tension de humeda
    B = (math.log(1500)-math.log(33))/(math.log(Q33_DF)-math.log(Q1500))
    print(B)
    A = math.exp( math.log(33) +    B * math.log(Q33) )
    A2= math.exp( (math.log(10)*33) + (B*math.log(10)*Q33) )
    
    
    Q = Qs
    Y0 = A*pow(Q,-B)
    print("Y0",Y0)
    Y33_ye=  33 - ((Q-Q33)*(33-Ye)/ (Qs-Q33))
    print("Y33_ye:",Y33_ye)
        
    
    """ Conductividad Saturada """
    delta = 1/B 
    Q = Qs
    
    Ks = 1930 * (math.pow(Q - Q33,3-delta))
    
    
    
    
    Q_Div_Qs = Ks*(math.pow(Q/Qs, (3+(2/delta))))
    print("Q_Div_Qs",Q_Div_Qs)
    
    
    """ Efecto de la Graba """
    Rw = Rw
    p = 1                               # matriz de desidad del suelo 
    a = 2.65/2.65                       # matriz de desidad del suelo / densidad de la grava(2.65) = p/2.65
    
    Rv = ( a * Rw ) / ( 1-Rw * (1-a) ) # Volumen de la fraccon de grava 
    print("Rv",Rv)
    PB = Pn * ( 1-Rv ) + ( Rv*2.65 )    # densidad aparente del suelo
    PB2= Pdf*( 1-Rv ) + ( Rv*2.65 )
    print("PB",PB)
    PAW = Q33_DF - Q1500                # Humedad disponible para la planta
    PAWB = PAW * (1-Rv)                 # humedad disponible para la planta(
    Kb_Ks = (1-Rw)/(1-Rw*(1-3*a/2))     # 
    
    

    Punto_Marchitez_Permanente = round(Q1500*100,1) # % Volumen
    Capacidad_Campo = round(Q33_DF*100,1)           # % Volumen
    Saturacion =  round(Qs_DF*100,1)                # % Volumen
    Agua_Disponible = round(PAWB,2)                 # cm/cm
    densidad_aparente =   round(Pdf,2)              # gr/cm3
    Conductividad_Hidraulica = Ks                   # primera solucion

    print(" Ks:",Ks," Qs:",Qs, " Q:",Q," Q1:",Q1,Y33_ye)
   
    
    
    return Punto_Marchitez_Permanente, Capacidad_Campo,  Saturacion,Agua_Disponible, densidad_aparente



Arcilla = 0.0430151515151515; Arena =0.846272727272727; MateriaOrganica=2.08  ; Salinidad=0; Compactacion=1.0; Grava=0.1

P1 = watersoil( Arcilla, Arena, MateriaOrganica, Salinidad, Compactacion, Grava )
print(Arcilla, Arena, MateriaOrganica, Salinidad, Compactacion, Grava)
print(P1)