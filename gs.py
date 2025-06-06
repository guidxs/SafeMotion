import cv2
import mediapipe as mp
import time
import threading
import winsound
import numpy as np
import requests

#função de envio de notificação para o telegram
def enviar_alerta_telegram(data_hora):
    token = '7896404908:AAFKQ-f7Cd2k-Nh4GFMWI_z2abVaKt1jT4I'
    chat_id = '1890284199'

    #coordenadas da camera
    latitude = -23.56417 
    longitude = -46.6525

    #mensagem formatada com data/hora e link do mapa
    mensagem = (
        "📢 *ALERTA DE EMERGÊNCIA*\n"
        f"🕒 *Horário:* {data_hora}\n"
        f"📍 *Localização estimada:* [Ver no mapa](https://www.google.com/maps/search/?api=1&query={latitude},{longitude})\n"
        "📸 *Imagem capturada no momento do alerta.*\n"
        "⚠️ *Situação detectada automaticamente por gesto.*"
    )

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id, 'text': mensagem, 'parse_mode': 'Markdown'}

    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"Erro ao enviar: {response.text}")
    except Exception as e:
        print(f"Erro: {e}")
        
def enviar_localizacao_telegram():
    token = '7896404908:AAFKQ-f7Cd2k-Nh4GFMWI_z2abVaKt1jT4I'
    chat_id = '1890284199'

    #coordenadas da camera
    latitude = -23.56417 
    longitude = -46.6525

    url = f'https://api.telegram.org/bot{token}/sendLocation'
    data = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude}

    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"Erro ao enviar localização: {response.text}")
    except Exception as e:
        print(f"Erro ao enviar localização: {e}")
        
def enviar_imagem_telegram(caminho_imagem):
    token = '7896404908:AAFKQ-f7Cd2k-Nh4GFMWI_z2abVaKt1jT4I'
    chat_id = '1890284199'
    url = f'https://api.telegram.org/bot{token}/sendPhoto'

    try:
        with open(caminho_imagem, 'rb') as foto:
            files = {'photo': foto}
            data = {'chat_id': chat_id}
            response = requests.post(url, files=files, data=data)
            if response.status_code != 200:
                print(f"Erro ao enviar imagem: {response.text}")
    except Exception as e:
        print(f"Erro ao enviar imagem: {e}")


# === MediaPipe e variáveis ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

gesto_inicio = 0
gesto_detectado = False
alerta_ativo = False
alerta_ativado_em = 0
TEMPO_GESTO = 3        #tempo necessário com gesto ativo
TEMPO_ALERTA = 5       #tempo que o alerta fica ativo (inclui tela branca)

def tocar_alarme():
    for _ in range(3):
        winsound.Beep(1000, 500)
        time.sleep(0.5)

#webcam
cap = cv2.VideoCapture(2)

while cap.isOpened():
    sucesso, frame = cap.read()
    if not sucesso:
        break

    frame = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(img_rgb)

    if resultado.multi_hand_landmarks:
        for mao in resultado.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, mao, mp_hands.HAND_CONNECTIONS)

            dedos = [8, 12, 16, 20]
            levantados = 0
            for d in dedos:
                if mao.landmark[d].y < mao.landmark[d - 2].y:
                    levantados += 1

            if levantados == 4:
                if not gesto_detectado:
                    gesto_inicio = time.time()
                    gesto_detectado = True
                elif time.time() - gesto_inicio >= TEMPO_GESTO and not alerta_ativo:
                    alerta_ativo = True
                    alerta_ativado_em = time.time()
                    threading.Thread(target=tocar_alarme).start()
                    
                    #obter data e hora atual 
                    agora = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                    #adicionar o texto na imagem (amarelo)
                    cv2.putText(frame, f"Alerta em: {agora}", (10, frame.shape[0] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                    
                    #salva a imagem com data/hora
                    cv2.imwrite("alerta.png", frame)
                    
                    #envia alerta com mensagem
                    threading.Thread(target=enviar_alerta_telegram, args=(agora,)).start()  
                    threading.Thread(target=enviar_localizacao_telegram).start()
                    threading.Thread(target=enviar_imagem_telegram, args=("alerta.png",)).start()
            else:
                gesto_detectado = False
    else:
        gesto_detectado = False

    #tela branca e mensagem
    if alerta_ativo:
        tempo_passado = time.time() - alerta_ativado_em
        if tempo_passado < TEMPO_ALERTA:
            frame = 255 * np.ones_like(frame)  # tela branca
            cv2.putText(frame, 'ALERTA DE SOCORRO ATIVADO', (50, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        else:
            alerta_ativo = False  #encerra o alerta

    cv2.imshow("SafeMotion", frame)
    if cv2.waitKey(1) & 0xFF == 27:  #ESC
        break

cap.release()
cv2.destroyAllWindows()