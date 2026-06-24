import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

nx, ny = 1000, 500
Ez = np.zeros((nx, ny))
Hx = np.zeros((nx, ny))
Hy = np.zeros((nx, ny))

c = 997
dt = 0.5
dx = 1.0

source_x, source_y = 499, 1
bulb_x, bulb_y = 499, 498
corner_x, corner_y = 1, 1

t = 0

def step(Ez, Hx, Hy, t):
    Hx[:, :-1] -= (Ez[:, 1:] - Ez[:, :-1])*(dt/dx)
    Hy[:-1, :] += (Ez[1:, :] - Ez[:-1, :])*(dt/dx)

    Ez[1:, 1:] += dt/dx * ((Hy[1:, 1:] - Hy[:-1, 1:]) - (Hx[1:, 1:] - Hx[1:, :-1]))
    Ez[source_x, source_y] += np.exp(-0.5 * ((t - 30) / 10) ** 2) * 200
    Ez[:, 0] = 0
    Ez[:, -1] = 0
    Ez[0, :] = 0
    Ez[-1, :] = 0
    return Ez, Hx, Hy

fig, ax = plt.subplots(figsize=(6, 6))
img = ax.imshow(Ez.T, cmap='RdBu', vmin=-2, vmax=2, animated=True)
ax.set_title('EM Field Propagation')

bulb_signal = []
corner_signal = []
time_steps = []
step_count = 0

def animate(frame):
    global Ez, Hx, Hy, t, step_count
    for _ in range(5):
        Ez, Hx, Hy = step(Ez, Hx, Hy, t)
        t += 1
    bulb_signal.append(Ez[bulb_x, bulb_y])
    corner_signal.append(Ez[corner_x, corner_y])
    time_steps.append(step_count)
    step_count += 5
    img.set_array(Ez.T)
    return img,

ani = animation.FuncAnimation(fig, animate, interval=20, blit=True)
plt.show()

plt.figure(figsize=(10, 4))
plt.plot(time_steps, bulb_signal, color='yellow', label='Bulb (499 cells through space)')
plt.plot(time_steps, corner_signal, color='cyan', label='Corner (499 cells through wire)')
plt.axhline(0, color='white', lw=0.5)
plt.facecolor = 'black'
plt.legend()
plt.xlabel('Timestep')
plt.ylabel('Ez field strength')
plt.title('When does the field arrive?')
plt.savefig('signal.png')
plt.show()
