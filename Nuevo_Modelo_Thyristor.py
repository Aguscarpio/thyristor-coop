import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time as timee
#%%
def rk4(dxdt, x, t, dt, *args, **kwargs):
    x = np.asarray(x)

    k1 = np.asarray(dxdt(x, t, *args, **kwargs))*dt
    k2 = np.asarray(dxdt(x + k1*0.5, t, *args, **kwargs))*dt
    k3 = np.asarray(dxdt(x + k2*0.5, t, *args, **kwargs))*dt
    k4 = np.asarray(dxdt(x + k3, t, *args, **kwargs))*dt

    return x + (k1 + 2*k2 + 2*k3 + k4)/6

def modelo_thyristor(x, t, Iin, Cm, Cs, Rs):
    It, Vt, Vs = x

    It_dot = It*(Vt - 10) + 5*It**2 - It**3 + 0.1
    Vt_dot = Iin/Cm - It*(1/Cm + 1/Cs) + Vs/(Rs*Cs)
    Vs_dot = (1/Cs)*(It - Vs/Rs)

    return [It_dot, Vt_dot, Vs_dot]

# Condiciones iniciales
It0 = 0.1
Vt0 = 0.1
Vs0 = 0.1

# Parámetros

Iin = 0.8
Cm = 10
Cs = 0.1
Rs = 3.1

# Paso temporal y número de iteraciones
dt = 0.0001
t_final = 400
num_iterations = int(t_final / dt)

# Array de tiempo
time = np.arange(0, t_final, dt)

It = np.zeros(num_iterations)
Vt = np.zeros(num_iterations)
Vs = np.zeros(num_iterations)

It[0] = It0
Vt[0] = Vt0
Vs[0] = Vs0

# Resolver el sistema utilizando RK4
last_progress = -1  # Variable para almacenar el último progreso impreso

t0 = timee.time()
for i, tt in enumerate(time[:-1]):
    t = tt
    x = [It[i], Vt[i], Vs[i]]
    x_new = rk4(modelo_thyristor, x, t, dt, Iin, Cm, Cs, Rs)
    It[i+1] = x_new[0]
    Vt[i+1] = x_new[1]
    Vs[i+1] = x_new[2]


    progress = int((i + 1) / num_iterations * 100)  # Progreso actual como número entero

    if progress > last_progress:  # Imprimir solo cuando el progreso cambia
        print(f"Progreso: {progress}%")
        last_progress = progress

tf = timee.time()
print(f"Finalizado en {tf-t0} segundos")

# Crea el plot
fig = plt.figure(figsize=(12, 9), dpi=150)

# Define los límites iniciales
x_inicial = 200
x_final = t_final

# Crea los subplots de la izquierda
ax1 = fig.add_subplot(3, 2, 1)
ax2 = fig.add_subplot(3, 2, 3)
ax3 = fig.add_subplot(3, 2, 5)

# Filtrar los valores de time, It, Vt y Vs en el rango especificado
time_filt = time[(time >= x_inicial) & (time <= x_final)]
It_filt = It[(time >= x_inicial) & (time <= x_final)]
Vt_filt = Vt[(time >= x_inicial) & (time <= x_final)]
Vs_filt = Vs[(time >= x_inicial) & (time <= x_final)]

# Plot de It en función de time (Top Left)
ax1.plot(time_filt, It_filt, label='It')
ax1.set_ylabel('It', fontsize=15)
ax1.legend()

# Plot de Vt en función de time (Middle Left)
ax2.plot(time_filt, Vt_filt, label='Vt')
ax2.set_ylabel('Vt', fontsize=15)
ax2.legend()

# Plot de Vs en función de time (Bottom Left)
ax3.plot(time_filt, Vs_filt, label='Vs')
ax3.set_xlabel('Tiempo', fontsize=15)
ax3.set_ylabel('Vs', fontsize=15)
ax3.legend()

# Crea el subplot de la derecha
ax4 = fig.add_subplot(1, 2, 2)

# Plot de It en función de Vt (Right)
ax4.plot(Vt_filt, It_filt, color='red', label='It vs Vt')
ax4.set_xlabel('Vt', fontsize=15)
ax4.set_ylabel('It', fontsize=15)
ax4.legend()

# Ajustar el espacio entre los subplots
fig.tight_layout()

# Ajustar el tamaño del plot y el dpi
fig.set_size_inches(12, 9)
plt.savefig('resultados.png', dpi=300)

# Mostrar el plot
plt.show()
#%%
# Crea una figura y un eje 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Grafica la curva en 3D
ax.plot(It_filt, Vt_filt, Vs_filt, color='red', linewidth=0.1)

# Etiquetas de los ejes
ax.set_xlabel('It')
ax.set_ylabel('Vt')
ax.set_zlabel('Vs')

# Muestra el gráfico
plt.show()
