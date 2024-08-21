import cv2
import mediapipe as mp
import time
import math
import pygame

# Inicializa o VideoCapture para capturar vídeo da webcam
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
mpFaceMesh = mp.solutions.face_mesh
mpHands = mp.solutions.hands

faceMesh = mpFaceMesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5,
                               min_tracking_confidence=0.5)
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

# Inicializa o mixer do Pygame para os alertas sonoros
pygame.mixer.init()

# Carrega os arquivos de áudio
alarme_dormindo = pygame.mixer.Sound("C:/Users/Denis/PycharmProjects/Projeto detector de fadiga/sons/alarm.wav")
alarme_bocejo = pygame.mixer.Sound(
    "C:/Users/Denis/PycharmProjects/Projeto detector de fadiga/sons/emergency-alarm-with-reverb-29431.mp3")
alarme_cabeca_baixa = pygame.mixer.Sound(
    "C:/Users/Denis/PycharmProjects/Projeto detector de fadiga/sons/alarm-26718.mp3")
alarme_desatencao = pygame.mixer.Sound(
    "C:/Users/Denis/PycharmProjects/Projeto detector de fadiga/sons/rooster-crowing-in-turkey-142039.mp3")
alarme_celular = pygame.mixer.Sound(
    "C:/Users/Denis/PycharmProjects/Projeto detector de fadiga/sons/biohazard-alarm-143105.mp3")
alarme_alimentacao = pygame.mixer.Sound(
    "C:/Users/Denis/PycharmProjects/Projeto detector de fadiga/sons/siren-alert-96052.mp3")

# Variáveis de tempo para controle de estados
inicio_olhos = 0
inicio_bocejo = 0
inicio_cabeca_baixa = 0
inicio_desatencao = 0
inicio_celular = 0
inicio_alimentacao = 0

alarme_ativo = False
tipo_alarme_ativo = None
inicio_alarme = 0
mensagem_apresentada = False
inicio_mensagem = 0


def parar_todos_alarmes():
    """Função para parar todos os alarmes."""
    alarme_dormindo.stop()
    alarme_bocejo.stop()
    alarme_cabeca_baixa.stop()
    alarme_desatencao.stop()
    alarme_celular.stop()
    alarme_alimentacao.stop()


while True:
    check, img = video.read()

    if not check or img is None:
        continue

    img = cv2.resize(img, (1000, 720))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results_face = faceMesh.process(imgRGB)
    results_hands = hands.process(imgRGB)

    olhos_fechados = False
    rosto_presente = results_face.multi_face_landmarks is not None

    if rosto_presente:
        for face_landmarks in results_face.multi_face_landmarks:
            mp_drawing.draw_landmarks(img, face_landmarks, mpFaceMesh.FACEMESH_CONTOURS)

            olho_esq_top = face_landmarks.landmark[159]
            olho_esq_bottom = face_landmarks.landmark[145]
            olho_dir_top = face_landmarks.landmark[386]
            olho_dir_bottom = face_landmarks.landmark[374]

            dist_olho_esq = math.hypot(olho_esq_top.x - olho_esq_bottom.x, olho_esq_top.y - olho_esq_bottom.y)
            dist_olho_dir = math.hypot(olho_dir_top.x - olho_dir_bottom.x, olho_dir_top.y - olho_dir_bottom.y)

            olhos_fechados = dist_olho_esq < 0.02 and dist_olho_dir < 0.02

            if olhos_fechados:
                if inicio_olhos == 0:
                    inicio_olhos = time.time()
                else:
                    tempo_olhos_fechados = int(time.time() - inicio_olhos)
                    if tempo_olhos_fechados >= 4:
                        cv2.putText(img, "DORMINDO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        if not alarme_ativo and tempo_olhos_fechados >= 6:
                            parar_todos_alarmes()
                            alarme_dormindo.play()
                            alarme_ativo = True
                            tipo_alarme_ativo = 'dormindo'
                            inicio_alarme = time.time()
                    else:
                        cv2.putText(img, f"OLHOS FECHADOS: {tempo_olhos_fechados} s", (50, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(img, "OLHOS ABERTOS", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                inicio_olhos = 0
                if alarme_ativo and tipo_alarme_ativo == 'dormindo':
                    parar_todos_alarmes()
                    alarme_ativo = False
                    tipo_alarme_ativo = None

            boca_cima = face_landmarks.landmark[13]
            boca_baixo = face_landmarks.landmark[14]
            distancia_boca = math.hypot(boca_cima.x - boca_baixo.x, boca_cima.y - boca_baixo.y) * img.shape[1]

            if distancia_boca > 30:
                if inicio_bocejo == 0:
                    inicio_bocejo = time.time()
                elif time.time() - inicio_bocejo >= 3:
                    cv2.putText(img, "BOCEJANDO", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    if not alarme_ativo:
                        parar_todos_alarmes()
                        alarme_bocejo.play()
                        alarme_ativo = True
                        tipo_alarme_ativo = 'bocejo'
                        inicio_alarme = time.time()
            else:
                inicio_bocejo = 0
                if alarme_ativo and tipo_alarme_ativo == 'bocejo':
                    parar_todos_alarmes()
                    alarme_ativo = False
                    tipo_alarme_ativo = None

            olho_esq = face_landmarks.landmark[33]
            olho_dir = face_landmarks.landmark[263]
            nariz_top = face_landmarks.landmark[1]
            nariz_baixo = face_landmarks.landmark[2]
            queixo = face_landmarks.landmark[152]

            ponto_orelha_esq = face_landmarks.landmark[234]
            ponto_orelha_dir = face_landmarks.landmark[454]
            dist_nariz_testa = abs(nariz_top.y - ponto_orelha_esq.y)
            dist_nariz_orelhas = math.hypot(ponto_orelha_esq.x - ponto_orelha_dir.x,
                                            ponto_orelha_esq.y - ponto_orelha_dir.y)
            dist_nariz_queixo = math.hypot(nariz_top.x - queixo.x, nariz_top.y - queixo.y)

            if dist_nariz_testa > 0.1 or dist_nariz_orelhas > 0.15 or dist_nariz_queixo > 0.2:
                if inicio_desatencao == 0:
                    inicio_desatencao = time.time()
                else:
                    tempo_desatencao = int(time.time() - inicio_desatencao)
                    if tempo_desatencao >= 8:
                        cv2.putText(img, "MOTORISTA DESATENTO", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        if not alarme_ativo:
                            parar_todos_alarmes()
                            alarme_desatencao.play()
                            alarme_ativo = True
                            tipo_alarme_ativo = 'desatencao'
                            inicio_alarme = time.time()
                    else:
                        cv2.putText(img, f"MOTORISTA DESATENTO: {tempo_desatencao} s", (50, 150),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                inicio_desatencao = 0
                if alarme_ativo and tipo_alarme_ativo == 'desatencao':
                    parar_todos_alarmes()
                    alarme_ativo = False
                    tipo_alarme_ativo = None

    else:
        cv2.putText(img, "MOTORISTA DESATENTO ou FORA DE VISAO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if inicio_desatencao == 0:
            inicio_desatencao = time.time()
        else:
            tempo_desatencao = int(time.time() - inicio_desatencao)
            if tempo_desatencao >= 20:
                if not alarme_ativo:
                    parar_todos_alarmes()
                    alarme_desatencao.play()
                    alarme_ativo = True
                    tipo_alarme_ativo = 'desatencao'
                    inicio_alarme = time.time()

    # Detecção de uso de celular e alimentação
    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)

            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Detecção de uso de celular (mão na frente do rosto)
                if cx > img.shape[1] / 2 - 100 and cx < img.shape[1] / 2 + 100 and cy > img.shape[0] / 2 - 100 and cy < \
                        img.shape[0] / 2 + 100:
                    if inicio_celular == 0:
                        inicio_celular = time.time()
                    else:
                        tempo_celular = int(time.time() - inicio_celular)
                        if tempo_celular >= 5:
                            cv2.putText(img, "USO DE CELULAR", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            if not alarme_ativo:
                                parar_todos_alarmes()
                                alarme_celular.play()
                                alarme_ativo = True
                                tipo_alarme_ativo = 'celular'
                                inicio_alarme = time.time()
                else:
                    inicio_celular = 0
                    if alarme_ativo and tipo_alarme_ativo == 'celular':
                        parar_todos_alarmes()
                        alarme_ativo = False
                        tipo_alarme_ativo = None

                # Detecção de alimentação (mão na boca repetidas vezes)
                if cx > img.shape[1] / 2 - 50 and cx < img.shape[1] / 2 + 50 and cy > img.shape[0] - 100:
                    if inicio_alimentacao == 0:
                        inicio_alimentacao = time.time()
                    else:
                        tempo_alimentacao = int(time.time() - inicio_alimentacao)
                        if tempo_alimentacao >= 3:
                            cv2.putText(img, "ALIMENTANDO/ BEBENDO", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (0, 0, 255), 2)
                            if not alarme_ativo:
                                parar_todos_alarmes()
                                alarme_alimentacao.play()
                                alarme_ativo = True
                                tipo_alarme_ativo = 'alimentacao'
                                inicio_alarme = time.time()
                else:
                    inicio_alimentacao = 0
                    if alarme_ativo and tipo_alarme_ativo == 'alimentacao':
                        parar_todos_alarmes()
                        alarme_ativo = False
                        tipo_alarme_ativo = None

    # Verifica se os olhos estão abertos por 30 segundos para desativar o alarme
    if not olhos_fechados and alarme_ativo:
        tempo_olhos_abertos = int(time.time() - inicio_alarme)
        if tempo_olhos_abertos >= 30:
            parar_todos_alarmes()
            alarme_ativo = False
            tipo_alarme_ativo = None

    # Mostra a mensagem após o alarme ser desativado por 10 segundos
    if time.time() - inicio_alarme < 10 and inicio_alarme > 0:
        cv2.putText(img, "Motorista apresenta sinais de fadiga ou nao esta na direcao", (50, img.shape[0] - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('IMG', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()