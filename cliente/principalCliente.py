#Codigo del cliente
import socket
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def deserialize_positions(data):
    positions = {}
    items = data.split(';')
    for item in items:
        planet, pos = item.split(':')
        x, y = map(float, pos.split(','))
        positions[planet] = (x, y)
    return positions


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.100.42', 12345))

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlabel('Distancia (UA)')
ax.set_ylabel('Distancia (UA)')
ax.set_title('Simulación del Sistema Solar')
ax.scatter(0, 0, color='yellow', s=100, marker='o', label='Sol')
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

points = {}
for planeta in ["Mercurio", "Venus", "Tierra", "Marte", "Jupiter", "Saturno", "Urano", "Neptuno"]:
    point, = ax.plot([], [], 'o', markersize=5, label=planeta)
    points[planeta] = point


def update_plot(i):
    client_socket.send('SOLICITAR_POSICIONES'.encode())
    data = client_socket.recv(1024).decode()
    positions = deserialize_positions(data)

    for planeta, point in points.items():
        if planeta in positions:
            x, y = positions[planeta]
            point.set_data(x, y)

    return points.values()


ani = animation.FuncAnimation(
    fig, update_plot, frames=range(100), interval=1000, blit=True)
ax.legend()
plt.show()

client_socket.close()
