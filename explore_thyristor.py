import numpy as np
import matplotlib.pyplot as plt
import time
from period_funcs import period
from numba import njit, jit

Cs = 0.1
a = 10
b = 5
c = 1
d = 0.1

@njit()
def modelo_thyristor(It, Vt, Vs, Rs, Iin, Cm, Cs, a, b, c, d):
    It_dot = It*(Vt - a) + 0.2*It*Vt*Vs + b*It**2 - c*It**3 + d
    Vt_dot = Iin/Cm - It*(1/Cm + 1/Cs) + Vs/(Rs*Cs)
    Vs_dot = (1/Cs)*(It - Vs/Rs)

    return [It_dot, Vt_dot, Vs_dot]


@njit()
def rk4_numba(It0, Vt0, Vs0, N_steps, dt, Rs, Iin, Cm, Cs, a, b, c, d):
    It_OT = np.zeros(N_steps)
    Vt_OT = np.zeros(N_steps)
    Vs_OT = np.zeros(N_steps)
    It_OT[0] = It0
    Vt_OT[0] = Vt0
    Vs_OT[0] = Vs0

    for i in range(1, N_steps):
        k1a, k1b, k1c = np.asarray(modelo_thyristor(It_OT[i-1], Vt_OT[i-1], Vs_OT[i-1], Rs, Iin, Cm, Cs, a, b, c, d))*dt
        k2a, k2b, k2c = np.asarray(modelo_thyristor(It_OT[i-1] + k1a*0.5, Vt_OT[i-1] + k1b*0.5, Vs_OT[i-1] + k1c*0.5, Rs, Iin, Cm, Cs, a, b, c, d))*dt
        k3a, k3b, k3c = np.asarray(modelo_thyristor(It_OT[i-1] + k2a*0.5, Vt_OT[i-1] + k2b*0.5, Vs_OT[i-1] + k2c*0.5, Rs, Iin, Cm, Cs, a, b, c, d))*dt
        k4a, k4b, k4c = np.asarray(modelo_thyristor(It_OT[i-1] + k3a, Vt_OT[i-1] + k3b, Vs_OT[i-1] + k3c, Rs, Iin, Cm, Cs, a, b, c, d))*dt

        It_OT[i] = It_OT[i-1] + (k1a + 2*k2a + 2*k3a + k4a)/6
        Vt_OT[i] = Vt_OT[i-1] + (k1b + 2*k2b + 2*k3b + k4b)/6
        Vs_OT[i] = Vs_OT[i-1] + (k1c + 2*k2c + 2*k3c + k4c)/6

    return It_OT, Vt_OT, Vs_OT

if __name__ == "__main__":
    from matplotlib.widgets import Slider
    total_time = 1300
    dt = 0.01
    N_steps = int(total_time/dt)
    Iin0 = 1
    Rs0 = 1
    Cm = 10

    It0 = Vt0 = Vs0 = 0.1
    #  It0 = 1
    #  Vt0 = 5.91
    #  Vs0 = 100/29


    It_OT, Vt_OT, Vs_OT = rk4_numba(It0, Vt0, Vs0, N_steps, dt, Rs0, Iin0, Cm, Cs, a, b, c, d)
    It_OT = It_OT
    Vt_OT = Vt_OT
    times = np.arange(0, N_steps*dt, dt)
    #  fig, ax = plt.subplots(1,1, figsize=(16,9))
    fig, [ax1, ax2, ax3] = plt.subplots(3,1, sharex=True, figsize=(16,9))
    fig2 = plt.figure()
    fig3, [ax1_3, ax2_3, ax3_3] = plt.subplots(1,3, figsize=(16,6))
    fig4 = plt.figure()
    ax3d = fig4.add_subplot(111, projection='3d')

    # Grafica la curva en 3D
    plot_3d, = ax3d.plot(It_OT, Vt_OT, Vs_OT, color='red', linewidth=0.1)

    # Etiquetas de los ejes
    ax3d.set_xlabel('It')
    ax3d.set_ylabel('Vt')
    ax3d.set_zlabel('Vs')

    IinAx = fig2.add_axes([0.15, 0.85, 0.75, 0.03])
    sIin = Slider(IinAx, 'Iin', 0, 3, valinit=1)
    RsAx = fig2.add_axes([0.15, 0.75, 0.75, 0.03])
    sRs = Slider(RsAx, 'Rs', 0, 8, valinit=1)
    CsAx = fig2.add_axes([0.15, 0.65, 0.75, 0.03])
    sCs = Slider(CsAx, 'Cs', 0.001, 2, valinit=0.1)
    CmAx = fig2.add_axes([0.15, 0.55, 0.75, 0.03])
    sCm = Slider(CmAx, 'Cm', 0, 20, valinit=8.47)
    aAx = fig2.add_axes([0.15, 0.45, 0.75, 0.03])
    sa = Slider(aAx, 'a', 0, 20 , valinit=16.3)
    bAx = fig2.add_axes([0.15, 0.35, 0.75, 0.03])
    sb = Slider(bAx, 'b', 0, 10 , valinit=5)
    cAx = fig2.add_axes([0.15, 0.25, 0.75, 0.03])
    sc = Slider(cAx, 'c', 0, 3, valinit=1)
    dAx = fig2.add_axes([0.15, 0.15, 0.75, 0.03])
    sd = Slider(dAx, 'd', -1, 1 , valinit=0.1)

    It_plot, = ax1.plot(times, It_OT)
    Vt_plot, = ax2.plot(times, Vt_OT)
    Vs_plot, = ax3.plot(times, Vs_OT)

    ItVt_plot, = ax1_3.plot(Vt_OT, It_OT)
    ItVs_plot, = ax2_3.plot(Vs_OT, It_OT)
    VtVs_plot, = ax3_3.plot(Vt_OT, Vs_OT)
    ax1_3.set_title("It contra Vt")
    ax2_3.set_title("It contra Vs")
    ax3_3.set_title("Vs contra Vt")

    def update(val):
        Rs = sRs.val
        Iin = sIin.val
        Cs = sCs.val
        Cm = sCm.val
        a = sa.val
        b = sb.val
        c = sc.val
        d = sd.val
        It_OT, Vt_OT, Vs_OT = rk4_numba(It0, Vt0, Vs0, N_steps, dt, Rs, Iin, Cm, Cs, a, b, c, d)
        It_plot.set_ydata(It_OT)
        Vt_plot.set_ydata(Vt_OT)
        Vs_plot.set_ydata(Vs_OT)
        ItVt_plot.set_data(Vt_OT, It_OT)
        ItVs_plot.set_data(Vs_OT, It_OT)
        VtVs_plot.set_data(Vt_OT, Vs_OT)
        ax3d.clear()
        plot_3d, = ax3d.plot(It_OT, Vt_OT, Vs_OT, color='red', linewidth=0.1)
        for ax in [ax1, ax2, ax3, ax1_3, ax2_3, ax3_3]:
            ax.relim()
            ax.autoscale_view()

        fig.canvas.draw_idle()
        fig3.canvas.draw_idle()
        fig4.canvas.draw_idle()

    sIin.on_changed(update)
    sRs.on_changed(update)
    sCs.on_changed(update)
    sCm.on_changed(update)
    sa.on_changed(update)
    sb.on_changed(update)
    sc.on_changed(update)
    sd.on_changed(update)
    #  ax.plot(It_OT[-150000:], Vt_OT[-150000:])
    plt.show()
