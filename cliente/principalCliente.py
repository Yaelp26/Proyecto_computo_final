#Codigo del cliente
import socket
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image, ImageDraw

# Ruta a las imágenes de los planetas
planet_images = {
    "Mercurio": "imagenesPlanetas/mercurio.png",
    "Venus": "imagenesPlanetas/venus.png",
    "Tierra": "imagenesPlanetas/tierra.png",
    "Marte": "imagenesPlanetas/marte.png",
    "Jupiter": "imagenesPlanetas/jupiter.png",
    "Saturno": "imagenesPlanetas/saturno.png",
    "Urano": "imagenesPlanetas/urano.png",
    "Neptuno": "imagenesPlanetas/neptuno.png"
}

def deserialize_positions(data):
    positions = {}
    items = data.split(';')
    for item in items:
        planet, pos = item.split(':')
        x, y = map(float, pos.split(','))
        positions[planet] = (x, y)
    return positions

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.100.15', 12345))

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlabel('Distancia (UA)')
    ax.set_ylabel('Distancia (UA)')
    ax.set_title('Simulación del Sistema Solar')
    ax.scatter(0, 0, color='yellow', s=100, marker='o', label='Sol')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    points = {}
    for planeta in planet_images.keys():
        point, = ax.plot([], [], 'o', markersize=0)  # No dibujamos puntos, solo usaremos las imágenes
        points[planeta] = point

    def update_plot(i):
        client_socket.send('SOLICITAR_POSICIONES'.encode())
        data = client_socket.recv(1024).decode()
        positions = deserialize_positions(data)

        for planeta, point in points.items():
            if planeta in positions:
                x, y = positions[planeta]
                point.set_data(x, y)
                # Añadir imagen del planeta en la posición
                planet_image = Image.open(planet_images[planeta])
                plt.imshow(planet_image, extent=(x-0.05, x+0.05, y-0.05, y+0.05))

        return points.values()

    ani = animation.FuncAnimation(
        fig, update_plot, frames=range(100), interval=1000, blit=True)
    ax.legend()
    plt.show()

    client_socket.close()

if __name__ == "__main__":
    main()
