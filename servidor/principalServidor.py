#Codigo del servidor
import socket
import random
import math
import threading


def serialize_positions(positions):
    items = []
    for planet, (x, y) in positions.items():
        items.append(f'{planet}:{x},{y}')
    return ';'.join(items)


# Distancias de los planetas al sol en Unidades Astronómicas (UA), escaladas por la distancia de Neptuno al Sol
distances = {
    "Mercurio": 0.39 / 30.07,
    "Venus": 0.72 / 30.07,
    "Tierra": 1.0 / 30.07,
    "Marte": 1.52 / 30.07,
    "Jupiter": 5.20 / 30.07,
    "Saturno": 9.58 / 30.07,
    "Urano": 19.18 / 30.07,
    "Neptuno": 30.07 / 30.07
}

# Velocidades angulares de los planetas (grados por día)
speeds = {
    "Mercurio": 4.092,
    "Venus": 1.602,
    "Tierra": 0.985,
    "Marte": 0.524,
    "Jupiter": 0.083,
    "Saturno": 0.033,
    "Urano": 0.011,
    "Neptuno": 0.006
}

# Ángulos iniciales de los planetas
angles = {planet: random.uniform(0, 360) for planet in distances.keys()}

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            if data.decode() == 'SOLICITAR_POSICIONES':
                positions = {}
                for planet in distances.keys():
                    r = distances[planet]
                    theta = math.radians(angles[planet])
                    x = r * math.cos(theta)
                    y = r * math.sin(theta)
                    positions[planet] = (x, y)
                    angles[planet] += speeds[planet]  # Incrementar el ángulo

                client_socket.send(serialize_positions(positions).encode())
    except Exception as e:
        print(f"Error durante la comunicación con el cliente: {e}")
    finally:
        client_socket.close()

def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 12345))
        server_socket.listen(5)
        print("Servidor iniciado en el puerto 12345")
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
        return

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Aceptada conexión desde {client_address}')
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()