import numpy as np
import matplotlib.pyplot as plt

N = 4500
Cwv = np.empty(N)
Cww = np.empty(N)
Cwb = np.empty(N)
Cvv = np.empty(N)
Cvb = np.empty(N)
Cvw = np.empty(N)
Wind = np.empty(N)

with open("Aero.txt", "r") as Aero:
    for i in range(N):

        Cwv[i] = float(Aero.readline())
        Cww[i] = float(Aero.readline())
        Cwb[i] = float(Aero.readline())
        Cvv[i] = float(Aero.readline())
        Cvb[i] = float(Aero.readline())
        Cvw[i] = float(Aero.readline())
        Wind[i] = float(Aero.readline())

h = 0.05
uc = 0
duc = 0
dduc = 0
v = 0
y = 0
dv = 0
w = 0
dw = 0
ddw = 0
t = 140.25
t1 = 0.38
t2 = 0.04

X = []
Y = []
Z = []
K = []
A = []
B = []
V = []
W = []

zerX = []
zerY = []

a0 = 1.2
a1 = 2
a2 = 0.0004
a3 = 10*a2

c = 0

for i in range(N):
    dv =  Cvv[i] * Wind[i] - Cvw[i] * w - Cvv[i] * v + Cvb[i] * uc
    ddw = Cwv[i] * Wind[i] - Cww[i] * w - Cwv[i] * v - Cwb[i] * uc

    dduc = (-t1*duc - uc + a0*w + a1*dw + a2*y * a3*v)/t2
    #dduc = signal(dw, Kpw, Kiw, Kdw)

    v += h * dv
    y += h * v

    dw += h * ddw
    w += h * dw
    t += h
    duc += h*dduc
    uc += h*duc

    if uc > 7/57.3:
        uc = 7/57.3

    if uc < -7/57.3:
        uc = -7/57.3

    #if duc > 1/57.3:
    #    duc = 1/57.3

    #if duc < -1/57.3:
    #    duc = -1/57.3

    if t>325:
        Y.append(float(v))
        X.append(float(t))

        Z.append(float(t))
        K.append(float(w*57.3))

        A.append(float(t))
        B.append(float(y))

        zerY.append(float(0))
        zerX.append(float(t))

        V.append(float(uc*57.3))
        W.append(float(t))

    if c==0:
        if (t >= 365.2):
            print(Cwb[i])
            print(Cwv[i])
            print(Cvb[i])
            print(Cvv[i])
            print(Cvw[i])
            print(Cww[i])
            c+=1
    #print(dduc*57.3, "____ dduc|duc ____", duc*57.3)

plt.subplot(4, 1, 1)
plt.plot(X, Y)
plt.ylabel('Скорость(t), м/c',color='gray')
plt.plot(zerX, zerY)
plt.grid(True)

plt.subplot(4, 1, 2)
plt.plot(Z, K)
plt.ylabel('Угол (t), град',color='gray')
plt.plot(zerX, zerY)
plt.grid(True)

plt.subplot(4, 1, 3)
plt.plot(A, B)
plt.ylabel('Перемещение(t), м',color='gray')
plt.plot(zerX, zerY)
plt.grid(True)

plt.subplot(4, 1, 4)
plt.plot(W, V)
plt.ylabel('Поворот ОУ(t), град',color='gray')
plt.plot(zerX, zerY)
plt.grid(True)

plt.show()