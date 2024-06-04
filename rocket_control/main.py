import numpy as np
import matplotlib.pyplot as plt

def signal(input, Kp, Ki, Kd):
    global Err, Summ_Err, prev_Err
    global Goal, h

    Err = input - Goal
    Summ_Err += Err * h
    dErr = (Err - prev_Err) / h
    prev_Err = Err
    P = Err * Kp
    I = Summ_Err * Ki
    D = dErr * Kd

    return P + I + D

N = 1406
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

h = 0.1
uc = 0
duc = 0
dduc = 0
v = 0
dv = 0
w = 0
dw = 0
ddw = 0
t = 0
eps = 0.7
w_autos = 0.023
t1 = 0.21
t2 = 0.02

X = []
Y = []
Z = []
K = []
A = []
B = []

Goal = 0.0

Kpw = 0.02
Kiw = 0.005
Kdw = 1

Kpv = 0.0
Kiv = 0.0
Kdv = 0.0

Err = 0.0
Summ_Err = 0.0
prev_Err = 0.0

for i in range(N):
    dv = Cvv[i] * Wind[i] - Cvw[i] * w - Cvv[i] * v + Cvb[i] * uc
    ddw = Cwv[i] * Wind[i] - Cww[i] * w - Cwv[i] * v - Cwb[i] * uc

    dduc = signal(dw, Kpw, Kiw, Kdw)


    v += h * dv
    dw += h * ddw
    w += h * dw
    t += h
    duc += h*dduc
    uc += h*duc

    if uc > 5/57.3:
        uc = 5/57.3

    if uc < -5/57.3:
        uc = -5/57.3

    if duc > 1/57.3:
        duc = 1/57.3

    if duc < -1/57.3:
        duc = -1/57.3

    X.append(float(t))
    Y.append(float(v))

    Z.append(float(t))
    K.append(float(w*57.3))

    A.append(float(t))
    B.append(float(uc*57.3))

    print(dduc*57.3, "____ dduc|duc ____", duc*57.3)

plt.subplot(1, 3, 1)
plt.plot(X, Y)
plt.title("V")

plt.subplot(1, 3, 2)
plt.plot(Z, K)
plt.title("W")

plt.subplot(1, 3, 3)
plt.plot(A, B)
plt.title("b")

plt.show()
