# Dispositivo_Microcontrolado_Detec-o_Facial
DISPOSITIVO MICROCONTROLADO DE DIREÇÃO ASSISTIDA EMBARCADO PARA AUXILIAR A REDUÇÃO DE ACIDENTES DE TRÂNSITO 

O desenvolvimento e a utilização de um dispositivo de monitoramento de fadiga e sonolência de motoristas é essencial tendo em vista a alta incidência de acidentes causados por estas condições.Estudos indicam que falhas humanas são responsáveis por 90% dos acidentes fatais nas estradas, como sonolência distrações e fadiga contribuem significativamente para estes números. Estima-se que 1,4% e 9,5% dos acidentes nos EUA envolvem motoristas sonolentos. Segundo a National Highway Traffic Safety Administration (NHTSA) 2,2% dos acidentes fatais em 2021 foram atribuídos a sonolência ou fadiga de motoristas.Logo estes índices refletem a situações de condução prolongada, no qual a atenção diminui gradualmente, devido a fadiga ou sonolência, levando a um aumento de tempo de reação, e eventualmente a perda do controle do veículo. Diante destas informações o desenvolvimento de um sistema embarcado microcontrolado para direção assistida utilizando de visão computacional podendo detectar e alertar o motorista de situações críticas permite uma intervenção precoce e potencialmente salvando vidas. 

Utilizando de técnicas de visão computacional, OpenCV, Média PiPe e ou Dlib que utilizam bibliotecas pré-treinadas como Face Recognition, e sensores embarcados projeto, de uma Raspberry-PI4 e câmeras para monitorar em tempo real o estado do motorista no qual a detecção de fadiga é baseada em métricas como o Eye Aspect Ratio (EAR) e o Mouth Aspect Ratio (MAR) que monitoram características faciais indicativas de sonolência, como o fechamento dos olhos ou bocejos frequentes. Logo quando o sistema detectar esses padrões de risco um alarme sonoro é ativado para alertar o motorista. 

Tendo em vista a simplicidade, baixo custo e a confiabilidade deste sistema, tende a ser uma solução acessível e eficiente aumentando a segurança nas estradas, especialmente em cenários onde a fadiga e distrações do motorista é uma preocupação significa.


Este sistema de monitoramento de fadiga e distração do motorista que utiliza OpenCV e MediaPipe para análise de vídeo em tempo real. O sistema detecta sinais de cansaço, como olhos fechados e bocejos, e também identifica distrações, como uso de celular e alimentação. Baseado na detecção desses sinais, o código aciona alarmes sonoros específicos usando a biblioteca Pygame, e exibe mensagens de alerta na tela. O sistema também inclui lógica para parar os alarmes quando o comportamento normal é retomado e para mostrar uma mensagem após o alarme ser desativado.


Fluxograma de Prototipação e Testes

![Fluxograma de desenvolvimento do Projeto](https://github.com/user-attachments/assets/abfc2a5d-7ad7-4815-b079-3e0f498033c3)


Para o protótipo, após a definição da malha facial de um quadro (imagem capturada pela câmera da face do motorista, é possível monitorar por programação os tempos de movimentos dos olhos e lábios. Os pontos que definem as distâncias horizontais e verticais das pálpebras e dos lábios, permitem verificar se uma pessoa está sonolenta: ou com seus olhos fechados por certo tempo, ou bocejando (considerou-se limite dos lábios na vertical em distância máxima por mais de 2 segundos (HAMDI et al., 2021). A Figura 2 ilustra o que ocorre com uma imagem capturada, após ser submetida ao Face Mesh. Um conjunto de pontos na forma de um vetor em Python é retornado, viabilizando os cálculos EAR e MAR. 

![FeceMash 468 Pontos](https://github.com/user-attachments/assets/547bc5a1-ee1c-4b9f-b72a-53dd0e118e38)

Fonte: Shadmand, Sean: A Simple and efficient Face direction detection in React (MEDIUM, 2024)


Confira o vídeo demonstrativo do projeto:

[![Assista ao vídeo](https://img.youtube.com/vi/F8UC4He-9OY/hqdefault.jpg)](https://youtu.be/F8UC4He-9OY)

Fonte: Autor disponivel em:  (Youtube)

