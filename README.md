# 🔦 SafeMotion - Sistema de Alerta por Gestos em Ambientes Sem Iluminação

## 🧠 Descrição do Problema

Em situações de queda de energia, a visibilidade é drasticamente reduzida, dificultando a comunicação e a mobilidade, especialmente em locais críticos como hospitais, centros de controle e residências com pessoas vulneráveis. A ausência de iluminação pode impedir pedidos de ajuda em situações de emergência, colocando vidas em risco.

## 💡 Visão Geral da Solução

**SafeMotion** é uma solução desenvolvida com **Python** e **MediaPipe** que detecta **gestos manuais específicos** mesmo em ambientes com pouca ou nenhuma luz. Ao identificar um gesto de emergência (quatro dedos levantados), o sistema:

- Emite um **alerta sonoro**.
- Exibe uma **tela branca** para chamar atenção.
- **Captura uma imagem** do momento do gesto.
- Envia automaticamente:
  - Uma **mensagem de alerta** para o Telegram.
  - A **imagem capturada**.
  - A **localização estimada** da câmera.

Tudo isso ocorre utilizando apenas a webcam do computador e software Python.

## 🎯 Objetivo

Oferecer um sistema simples, acessível e eficaz que possa ser usado por:

- Pessoas em casa durante apagões.
- Profissionais em ambientes críticos.
- Pessoas com deficiência visual.
- Serviços essenciais que operam em situações emergenciais.

## ⚙️ Como Funciona

1. O programa utiliza a **webcam** para capturar o vídeo em tempo real.  
2. A biblioteca **MediaPipe Hands** detecta a posição dos dedos.  
3. Se o gesto de **4 dedos levantados** for mantido por 3 segundos:  
   - O alarme sonoro toca.  
   - Uma tela branca é exibida.  
   - O sistema captura uma imagem com data/hora.  
   - Essa imagem, a localização e uma mensagem são enviadas via Telegram.  
4. O alerta permanece visível por 5 segundos antes de retornar à visualização normal.

### 📦 Requisitos

- Python 3.x  
- OpenCV  
- MediaPipe  
- NumPy  
- Requests  
- Windows (para `winsound`)

### 📥 Instalação

> Execute o comando:  
> pip install opencv-python mediapipe numpy requests

### ▶️ Execução

> Execute o comando:  
> python gs.py

1. Conecte uma webcam funcional.  
2. Execute o script Python.  
3. Realize o gesto de 4 dedos levantados na frente da câmera por pelo menos 3 segundos.  
4. O alerta será disparado automaticamente.

> Obs.: Caso sua webcam não seja o dispositivo 2, altere `cap = cv2.VideoCapture(2)` para o índice correto.

## 📡 Integração com Telegram

A notificação via Telegram é enviada para um bot configurado previamente. No código estão definidos:

- O `token` do bot.  
- O `chat_id` do destinatário.

> ✅ O link do mapa com localização é incluso na mensagem de alerta.

## 📹 Demonstração em Vídeo

📺 [Clique aqui para assistir ao vídeo demonstrativo](https://youtu.be/N1pf-9vtTmw)

## 👥 Integrantes

| Nome                            | RM      |
|---------------------------------|---------|
| Guilherme Doretto Sobreiro      | 99674   |
| Guilherme Fazito Ziolli Sordili | 550539  |
| Raí Gumieri dos Santos          | 98287   |

## 🛠️ Estrutura de Pastas

SafeMotion/  
│  
├── gs.py # Código principal do projeto  
├── alerta.png # Imagem gerada durante o alerta  
├── README.md # Documento explicativo do projeto  

## 🔐 Observações


---

## 🤖 Como criar seu Bot no Telegram

Para que a aplicação envie mensagens ou alertas via Telegram, é necessário criar um bot. Siga os passos abaixo:

1. Abra o Telegram e procure por `@BotFather` (bot oficial do Telegram para criar bots).

2. Inicie uma conversa com o BotFather e envie o comando:  
   `/start`

3. Envie o comando:  
   `/newbot`

4. Informe um nome para o bot (exemplo: `SafeMotionBot`).

5. Escolha um nome de usuário único para o bot, que termine com `bot` (exemplo: `safemotion_helper_bot`).

6. O BotFather fornecerá um **Token de autenticação**, parecido com:  
   `123456789:ABCdefGhIjkLMnopQrsTUVwxyZ`  
   Copie esse token para usar no código.

7. Para obter seu `chat_id`:  
   - Envie uma mensagem para o bot no Telegram.  
   - Acesse no navegador a URL:  
     `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates`  
   - Procure pelo campo `"chat": { "id": ... }` na resposta JSON. Esse número é o seu `chat_id`.
