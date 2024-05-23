import socket
import threading
import math
import random

# Constantes
G = 4 * math.pi ** 2  # Constante gravitacional en UA^3/(ano^2 * M_sol)
M_sol = 1  # Masa del sol en masas solares

# Distancias iniciales de los planetas al sol en Unidades Astronómicas (UA)
initial_positions = {
    "Mercurio": (0.39, 0),
    "Venus": (0.72, 0),
    "Tierra": (1.0, 0),
    "Marte": (1.52, 0),
    "Jupiter": (5.20, 0),
    "Saturno": (9.58, 0),
    "Urano": (19.18, 0),
    "Neptuno": (30.07, 0)
}

# Velocidades iniciales de los planetas (UA/año)
initial_velocities = {
    "Mercurio": (0, 9.99),
    "Venus": (0, 7.35),
    "Tierra": (0, 6.28),
    "Marte": (0, 5.07),
    "Jupiter": (0, 2.75),
    "Saturno": (0, 2.03),
    "Urano": (0, 1.43),
    "Neptuno": (0, 1.14)
}

# Inicializar posiciones y velocidades
positions = {planet: list(pos) for planet, pos in initial_positions.items()}
velocities = {planet: list(vel) for planet, vel in initial_velocities.items()}

def serialize_positions(positions):
    items = []
    for planet, (x, y) in positions.items():
        items.append(f'{planet}:{x},{y}')
    return ';'.join(items)

def acceleration(x, y):
    r = math.sqrt(x**2 + y**2)
    a = -G * M_sol / r**3
    return a * x, a * y

def runge_kutta_step(h):
    global positions, velocities
    new_positions = {}
    new_velocities = {}

    for planet in positions.keys():
        x, y = positions[planet]
        vx, vy = velocities[planet]

        ax1, ay1 = acceleration(x, y)
        kx1 = h * vx
        ky1 = h * vy
        kvx1 = h * ax1
        kvy1 = h * ay1

        ax2, ay2 = acceleration(x + kx1 / 2, y + ky1 / 2)
        kx2 = h * (vx + kvx1 / 2)
        ky2 = h * (vy + kvy1 / 2)
        kvx2 = h * ax2
        kvy2 = h * ay2

        ax3, ay3 = acceleration(x + kx2 / 2, y + ky2 / 2)
        kx3 = h * (vx + kvx2 / 2)
        ky3 = h * (vy + kvy2 / 2)
        kvx3 = h * ax3
        kvy3 = h * ay3

        ax4, ay4 = acceleration(x + kx3, y + ky3)
        kx4 = h * (vx + kvx3)
        ky4 = h * (vy + kvy3)
        kvx4 = h * ax4
        kvy4 = h * ay4

        new_x = x + (kx1 + 2 * kx2 + 2 * kx3 + kx4) / 6
        new_y = y + (ky1 + 2 * ky2 + 2 * ky3 + ky4) / 6
        new_vx = vx + (kvx1 + 2 * kvx2 + 2 * kvx3 + kvx4) / 6
        new_vy = vy + (kvy1 + 2 * kvy2 + 2 * kvy3 + kvy4) / 6

        new_positions[planet] = (new_x, new_y)
        new_velocities[planet] = (new_vx, new_vy)

    positions = new_positions
    velocities = new_velocities

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            if data.decode() == 'SOLICITAR_POSICIONES':
                # Actualizar posiciones usando Runge-Kutta
                runge_kutta_step(0.01)  # Paso de tiempo arbitrario

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
