import cv2
import glob

def create_video(image_folder, output_file):
    # Obtener todas las imágenes en el directorio, ordenadas por nombre
    images = sorted(glob.glob(f"{image_folder}/frame_*.png"))
    
    # Leer la primera imagen para obtener las dimensiones del video
    frame = cv2.imread(images[0])
    height, width, layers = frame.shape

    # Inicializar el VideoWriter
    video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'DIVX'), 1, (width, height))

    # Añadir cada imagen al video
    for image in images:
        video.write(cv2.imread(image))

    # Liberar el VideoWriter
    video.release()

# Crear el video a partir de las imágenes en la carpeta 'frames'
create_video('frames', 'solar_system_video.avi')
