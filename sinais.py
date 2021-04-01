import cv2
from datetime import datetime
import numpy as np
from pydub import AudioSegment
from pydub.playback import play


sons = {'luz_1': 'sounds/nota1.mp3',
        'luz_2': 'sounds/nota2.mp3',
        'luz_3': 'sounds/nota3.mp3',
        'luz_4': 'sounds/nota4.mp3'}

status_anterior = {'luz_1': 'desligado',
                   'luz_2': 'desligado',
                   'luz_3': 'desligado',
                   'luz_4': 'desligado'}

counter = 0

X, Y = 547, 205
x1_1, y1_1 = X - 185, Y - 12 # Coordenadas x e y
x1_2, y1_2 = x1_1 + 10, y1_1 + 10
x2_1, y2_1 = X, Y # Coordenadas x e y
x2_2, y2_2 = X + 10, Y + 10
x3_1, y3_1 = X + 138, Y + 10 # Coordenadas x e y
x3_2, y3_2 = x3_1 + 10, y3_1 + 10
x4_1, y4_1 = X + 280, Y + 20 # Coordenadas x e y
x4_2, y4_2 = x4_1 + 10, y4_1 + 10


def match_template(frame, template_file):
    template = cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)
    frame_pb = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]
    method = cv2.TM_SQDIFF
    res = cv2.matchTemplate(frame_pb, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(frame, top_left, bottom_right, 255, 2)
    return top_left, bottom_right


def status_luz(luz):
    mediana_luz = luz.mean() # Valor para mediana da primeira luz
    if mediana_luz > 120:
        status_luz = 'ligado'
    else:
        status_luz = 'desligado'
    return status_luz


def toca_som(status_luz, status_anterior, som):
    global counter
    if status_luz == status_anterior:
        pass
    else:
        if status_luz == 'ligado':
            if counter == 0:
                pass
            else:
                play(AudioSegment.from_file(som, format='mp3'))


# play(AudioSegment.from_file('sounds/ambiente.mp3', format='mp3'))
# toca o som ambiente

cap = cv2.VideoCapture("http://177.72.3.203:8001/mjpg/video.mjpg?timestamp=1616807959425")
# Define a origem do vídeo que será capturado.

while True:

    ret, frame = cap.read()
    # Lê a captura de vídeo.

    # Pesquisa o padrão na imagem.
    if counter < 10:
        coordenadas = match_template(frame, './templates/template.png')
        print(coordenadas)
        X, Y = coordenadas[0]
        X, Y = X - 5, Y - 9

    # Primeira luz
    luz_1 = frame[y1_1:y1_2, x1_1:x1_2]
    # Delimita uma ROI em torno da primeira luz
    status_luz_1 = status_luz(luz_1)
    # Define status da primeira luz
    toca_som(status_luz_1, status_anterior['luz_1'], sons['luz_1'])
    # Toca o som da primeira luz de acordo com seu status
    status_anterior['luz_1'] = status_luz_1 # atualiza o status anterior
    cv2.rectangle(frame, (x1_1 + 10, y1_1 + 10), (x1_2 + 10, y1_2 + 10), (0, 255, 0), 1)
        # Desenha um retângulo em torno da primeira luz

    # Segunda luz
    luz_2 = frame[y2_1:y2_2, x2_1:x2_2]
    # Delimita uma ROI em torno da segunda luz
    status_luz_2 = status_luz(luz_2)
    # Define status da segunda luz
    # toca_som(status_luz_2, status_anterior['luz_2'], sons['luz_2'])
    # Toca o som da segunda luz de acordo com seu status
    status_anterior['luz_2'] = status_luz_2 # atualiza o status anterior
    cv2.rectangle(frame, (x2_1 + 10, y2_1 + 10), (x2_2 + 10, y2_2 + 10), (0, 255, 0), 1)
        # Desenha um retângulo em torno da segunda luz

    # Terceira luz
    luz_3 = frame[y3_1:y3_2, x3_1:x3_2]
    # Delimita uma ROI em torno da terceira luz
    status_luz_3 = status_luz(luz_3)
    # Define status da terceira luz
    toca_som(status_luz_3, status_anterior['luz_3'], sons['luz_3'])
    # Toca o som da terceira luz de acordo com seu status
    status_anterior['luz_3'] = status_luz_3 # atualiza o status anterior
    cv2.rectangle(frame, (x3_1 + 10, y3_1 + 10), (x3_2 + 10, y3_2 + 10), (0, 255, 0), 1)
        # Desenha um retângulo em torno da terceira luz

    # Quarta luz
    luz_4 = frame[y4_1:y4_2, x4_1:x4_2]
    # Delimita uma ROI em torno da quarta luz
    status_luz_4 = status_luz(luz_4)
    # Define status da quarta luz
    toca_som(status_luz_4, status_anterior['luz_4'], sons['luz_4'])
    # Toca o som da quarta luz de acordo com seu status
    status_anterior['luz_4'] = status_luz_4 # atualiza o status anterior
    cv2.rectangle(frame, (x4_1 + 10, y4_1 + 10), (x4_2 + 10, y4_2 + 10), (0, 255, 0), 1)
        # Desenha um retângulo em torno da quarta luz

    data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    gc = data_hora + ' - SINAIS - Recife-PE - A. Bomfim'
    fonte = cv2.FONT_HERSHEY_PLAIN
    cv2.putText(frame, gc, (15, 700), fonte, 1, (255, 255, 255))

    cv2.imshow("Sinais (Recife-PE)",frame)
    # Exibe frame do vídeo.

    counter += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
    # Define tecla 'Q' para interromper a execução do vídeo.
        break

cap.release()
cv2.destroyAllWindows()
