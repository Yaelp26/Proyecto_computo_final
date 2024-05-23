import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import os
import shutil

# Ruta a las imágenes de los planetas y el sol
planet_images = {
    "Sol": "imagenesPlanetas/sol.png",
    "Mercurio": "imagenesPlanetas/mercurio.png",
    "Venus": "imagenesPlanetas/venus.png",
    "Tierra": "imagenesPlanetas/tierra.png",
    "Marte": "imagenesPlanetas/marte.png",
    "Jupiter": "imagenesPlanetas/jupiter.png",
    "Saturno": "imagenesPlanetas/saturno.png",
    "Urano": "imagenesPlanetas/urano.png",
    "Neptuno": "imagenesPlanetas/neptuno.png"
}

# Tamaño reducido de las imágenes
image_size = (30, 30)

# Cargar y reducir el tamaño de las imágenes
loaded_images = {}
for planet, image_path in planet_images.items():
    img = Image.open(image_path)
    img = img.resize(image_size, Image.Resampling.LANCZOS)  # Cambiado a Image.Resampling.LANCZOS
    loaded_images[planet] = img

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
    client_socket.connect(('192.168.100.42', 12345))

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor('black')  # Fondo negro
    ax.set_xlabel('Distancia (UA)', color='white')
    ax.set_ylabel('Distancia (UA)', color='white')
    ax.set_title('Simulación del Sistema Solar', color='white')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.tick_params(colors='white')  #Cambiar color de las etiquetas de los ejes

    #crear directorio de imagenes
    os.makedirs('frames', exist_ok=True)
    
    # Inicializar el diccionario para las imágenes en el gráfico
    image_artists = {}

    def update_plot(i):
        client_socket.send('SOLICITAR_POSICIONES'.encode())
        data = client_socket.recv(1024).decode()
        positions = deserialize_positions(data)

        # Eliminar imágenes anteriores del eje
        for artist in ax.get_images():
            artist.remove()

        # Dibujar nuevas imágenes
        for planeta, (x, y) in positions.items():
            img = loaded_images[planeta]
            image = ax.imshow(img, extent=(x-0.05, x+0.05, y-0.05, y+0.05), zorder=1)
            image_artists[planeta] = image

        # Añadir la imagen del Sol en el centro
        img_sol = loaded_images["Sol"]
        ax.imshow(img_sol, extent=(-0.05, 0.05, -0.05, 0.05), zorder=2)

        if i % 10 == 0:
            plt.savefig(f'frames/frame_{i:03d}.png')

        return image_artists.values()

    ani = animation.FuncAnimation(
        fig, update_plot, frames=range(450), interval=1000, blit=True)
    ax.legend()
    plt.show()

    # Comprimir la carpeta 'frames' en un archivo ZIP
    shutil.make_archive('frames', 'zip', 'frames')

    # Enviar el archivo ZIP al servidor
    with open('frames.zip', 'rb') as f:
        client_socket.sendall(f.read())

    client_socket.close()

if __name__ == "__main__":
    main()