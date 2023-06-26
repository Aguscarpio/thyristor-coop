import numpy as np
import matplotlib.pyplot as plt
import time
from poincare import period, period_temporal
from numba import njit, jit

Cs = 0.1

@njit()
def modelo_thyristor(It, Vt, Vs, Rs, Iin, Cm):
    #  It_dot = It*(Vt - 13.2) + 8.44*It**2 - 2.025*It**3 + 0.1
    It_dot = It*(Vt - 10) + 5*It**2 - It**3 + 0.1
    Vt_dot = Iin/Cm - It*(1/Cm + 1/Cs) + Vs/(Rs*Cs)
    Vs_dot = (1/Cs)*(It - Vs/Rs)

    return [It_dot, Vt_dot, Vs_dot]


@njit()
def rk4_numba(It0, Vt0, Vs0, N_steps, dt, Rs, Iin, Cm):
    It_OT = np.zeros(N_steps)
    Vt_OT = np.zeros(N_steps)
    Vs_OT = np.zeros(N_steps)
    It_OT[0] = It0
    Vt_OT[0] = Vt0
    Vs_OT[0] = Vs0

    for i in range(1, N_steps):
        k1a, k1b, k1c = np.asarray(modelo_thyristor(It_OT[i-1], Vt_OT[i-1], Vs_OT[i-1], Rs, Iin, Cm))*dt
        k2a, k2b, k2c = np.asarray(modelo_thyristor(It_OT[i-1] + k1a*0.5, Vt_OT[i-1] + k1b*0.5, Vs_OT[i-1] + k1c*0.5, Rs, Iin, Cm))*dt
        k3a, k3b, k3c = np.asarray(modelo_thyristor(It_OT[i-1] + k2a*0.5, Vt_OT[i-1] + k2b*0.5, Vs_OT[i-1] + k2c*0.5, Rs, Iin, Cm))*dt
        k4a, k4b, k4c = np.asarray(modelo_thyristor(It_OT[i-1] + k3a, Vt_OT[i-1] + k3b, Vs_OT[i-1] + k3c, Rs, Iin, Cm))*dt

        It_OT[i] = It_OT[i-1] + (k1a + 2*k2a + 2*k3a + k4a)/6
        Vt_OT[i] = Vt_OT[i-1] + (k1b + 2*k2b + 2*k3b + k4b)/6
        Vs_OT[i] = Vs_OT[i-1] + (k1c + 2*k2c + 2*k3c + k4c)/6

    return It_OT, Vt_OT, Vs_OT

if __name__ == "__main__":
    total_time = 1600
    dt = 0.001
    N_steps = int(total_time/dt)
    #  Iin0 = 1.313
    #  Rs0 = 2.3
    #  Iin0 = 0.8223
    #  Rs0 = 3.086
    #  Iin0 = 1.351466
    #  Rs0 = 2.22524
    #  Iin0 = 0.726
    #  Rs0 = 3.176
    Iin0 = 1
    Rs0 = 3.5
    #  Iin0 = 0.43
    #  Rs0 = 3.000


    #  Iin0 = 1.618169636457
    #  eps =  0.000000000001
    #  Iin0 = 1.61816963
    #  eps =  0.00000001
    #  Rs0 = 1.705
    Cm = 10

    It0 = Vt0 = Vs0 = 0.1
    #  It0 = 1
    #  Vt0 = 5.91
    #  Vs0 = 100/29
    #  It0 = 1.5772688376501063
    #  Vt0 = 4.505056178608963
    #  Vs0 = 2.704358084805494
    #  It0 = 1.3330207099756717
    #  Vt0 = 4.997315571210392
    #  Vs0 = 2.2881011819475576

    It_OT, Vt_OT, Vs_OT = rk4_numba(It0, Vt0, Vs0, N_steps, dt, Rs0, Iin0, Cm)
    #  It_OT = It_OT
    #  Vt_OT = Vt_OT
    times = np.arange(0, N_steps*dt, dt)
    #  fig, ax = plt.subplots(1,1, figsize=(16,9))
    fig, [ax1, ax2, ax3] = plt.subplots(3,1, sharex=True, figsize=(16,9))
    #  ax.plot(It_OT[-150000:], Vt_OT[-150000:])
    ax1.plot(times, It_OT)
    ax2.plot(times, Vt_OT)
    ax3.plot(times, Vs_OT)
    #  It_OT, Vt_OT, Vs_OT = rk4_numba(It0, Vt0, Vs0, N_steps, dt, Rs0, Iin0+eps, Cm)
    #  ax1.plot(times, It_OT)
    #  ax2.plot(times, Vt_OT)
    #  ax3.plot(times, Vs_OT)
    plt.show()

    with open("p1_blue.npy", "wb") as f:
        np.save(f, Vs_OT[int(1200/dt):int(1250/dt)])


    #  t0 = time.time()

    print(f"Solución de período {period_temporal(Vs_OT[int(800/dt):], dt)}")
    print(f"Last state:\nIt0 = {It_OT[-1]}\nVt0 = {Vt_OT[-1]}\nVs0 = {Vs_OT[-1]}")

    #  plt.plot(Vt_OT[int(800/dt):], np.gradient(Vt_OT)[int(800/dt):])
    plt.show()
    #  tf = time.time()
    #  print(f"tardó {tf-t0} en hacer {N_steps}")
    #  plt.show()
