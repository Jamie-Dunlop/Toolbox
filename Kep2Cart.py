#Anna Middleton 26/10/2016
#Converting Keplerian to cartesian coordinates
#Solving Kepler's equation for eccentric anomaly
#in order to forecast position and velocity vectors


#def kepler(ecc, M):
import math
import numpy as np
def rad(X):
    return ((X * math.pi) / 180)

def deg(X):
    return ((X / math.pi) * 180)

#Test values
a = 26559000 #m
e = 0.704482
i = rad(63.1706)
omega = rad(281.646)
RAAN = rad(206.346)
mu=3.985992e14

#Error tolerance
etol = 1e-8
#period
T = math.pi * 2 * math.sqrt(a**3/mu)
print ("period", T, "secs")
t = 0
step = 1
try:
    while t <= T:


        #Mean anomaly
        M = math.sqrt(mu/a**3) * t

        #Initial guess for Eccentric anomaly
        if M < math.pi:
            E = M - e/2
        else:
            E = M + e/2

        #Iterates Kepler's equation until error is less than tolerance
        error = 1
        try:
            while abs(error) > etol:
                error = (M - E + e * math.sin(E))/ (1 - e*math.cos(E))
                E = E + error
        except KeyboardInterrupt:
            print('interrupted!')

        print ("Error" ,error)
        print ("Eccentric anomaly", deg(E)) #2.71

        #true anomaly
        V = 2 * math.atan(math.sqrt((1+e) / (1-e) ) * math.tan(E/2))
        print ("True anomaly" , deg(V))

        # rotation matrix
        u = omega + V

        R1 = math.cos(u) * math.cos(RAAN) - math.sin(u) * math.cos(i) * math.sin (RAAN)
        R2 = math.cos(u) * math.sin(RAAN) + math.sin(u) * math.cos(i) * math.cos(RAAN)
        R3 = math.sin(u) * math.sin(i)
        R = np.matrix([[R1], [R2], [R3]])

        print ("Rotation Matrix", R)

        #radius
        r=(a*(1 - e**2))/(1 + (e * math.cos(V)))
        r_comp = r * R
        print ("r", r_comp/1000, "km")

        #velocity
        #v = math.sqrt(mu * ((2/r) - (1/a)))
        #v_comp = v * R
        #print ("v", v_comp)

        v_x = math.sqrt(mu/(a * (1-e**2))) * math.sin(V)
        v_y = math.sqrt(mu/(a * (1-e**2))) * (e + math.cos(V))
        v_mag = math.sqrt(v_x**2 + v_y**2)
        print ("v", (v_mag * R)/1000)
        t = t + step
        print(t)
except KeyboardInterrupt:
    print('interrupted!')
