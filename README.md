<h1 align="center">FireCopter</h1>
<h2>Índice</h2>

* [Descrição do Projeto](#Descrição do Projeto)
* [Hardware](#Hardware)
* [Organização dos ficheiros de Software](#Organização)
* [Computador de Voo](#Computador de voo)
* [Controlador de Voo](#Controlador de voo)
* [Computador local](#Computador local)
* [Melhorias necessárias](#Melhorias)

# Descrição do Projeto
O projeto consiste no Drone autónomo que deteta incêndios

[//]: # (TODO: Colocar foto do drone)
# Hardware

# Organização
[//]: # (TODO: imagens)
# Computador de voo

No computador de voo, foi utilizado o sistema operativo Ubuntu 20.04.4 Server (Para poupar o processamento com GUI) com a [Plataforma ROS](http://wiki.ros.org/ROS/Installation)

A versão do ROS utilizada foi a Noetic e optou-se pelo ROS-Base por não incluir as ferramentas GUI.

Para programar a raspberry utilizou-se o PyCharm num computador a comunicar via SSH com a Raspberry. Para ligar ao pycharm é necessário dar permissões de leitura e de escrita à pasta usada na raspberry

    sudo chmod 777 FireCopter
Para configurar o pycharm seguir este [Tuturial](https://www.youtube.com/watch?v=kuowBMqM1Ow) e este [Tuturial](https://www.youtube.com/watch?v=lTew9mbXrAs)

O objetivo desta metodologia é ter uma sicronização automática entre os ficheiros locais e a raspberry e uma sicronização manual entre os ficheiros locais e o github.
Desta forma é possivel estar a testar o código recorrentemente e se algo correr mal existe o backup no github.

Para comunicar com a placa por ssh e ter acesso às aplicações gráficas (mudar para o ip correto):

    sudo ssh -X firecopter@[IP da Raspberry]

Como se pode ver no esquema, existem três grandes grupos: o computador local, o computador e o controlador de voo. Assim como neste documento, também no GitHub os programas estão divididos em pastas seguindo o mesmo raciocínio. 

 O computador local (que corresponde à pasta local_computer) é responsável por receber os dados do comando e enviá-los via WiFi, utilizando os protocolos TCP e IP para o computador de voo (GamePad_Sender.py) e por apresentar a interface gráfica do drone através de um browser. 

O computador de voo (que corresponde à pasta flight_computer) é responsável pelo processamento de imagens, pelas comunicações sem fios e pelo controlo autónomo. Aqui só devem ser executados os programas que não necessitam de um processamento constante e de muito alta velocidade. 

Neste componente do drone existem quatro nós de aquisição de dados: Aquisição de vídeo, que obtém as imagens da camera, que serão posteriormente utilizadas nos nós de processamento de imagem e de interface gráfica; Sensores Sonar, que obtém os dados dos sensores de ultrassons, que serão utilizados na deteção de obstáculos e no auxiliarão a aterragem autónoma; Comunicação TCP que obtém os dados do comando, que serão essenciais para dar as ordens ao drone; Comunicação serial, que recebe os dados dos sensores ligados ao Arduíno. 

Em termos de processamento de imagem apenas existem dois nós: o Deteção de Incêndios e o Optical Flow: O primeiro é responsável por detetar incêndios, que será útil tanto para o modo autónomo, como para alertar a ocorrência de um incêndio; já o segundo determina a velocidade e a orientação do movimento do drone e comunica essas informações para o controlo. 

No que toca à componente autónoma do drone existem também dois nós: o Piloto automático que faz a decisão de trajetórias e o Controlo x,y,z que transforma coordenadas cartesianas em percentagens de throttle, pitch, roll e yaw. A escolha entre comandos do modo automático e manual é acionada pelo botão dedicado no comando (mencionado no hardware) e é feita pelo nó Envio de comandos. 

Por fim, temos dois nós de envio de dados para o exterior, sendo eles Comunicação serial que envia os dados de throttle, pitch, roll, yaw e arranque e paragem de motores para o controlador de voo e Interface web que cria uma interface gráfica, que poderá ser aberta a partir de um browser num computador ligado na mesma rede. 

O controlador de voo (que corresponde à pasta flight_controller) é, ao contrário do computador de voo, utilizado com vista em dar prioridade a um processamento estável e veloz, uma vez que é aqui que são executadas as tarefas de controlo do drone. Este lê os dados dos sensores que estão ligados via I2C e converte essa informação em ângulos. Esses ângulos entram numa malha de controlo fechada, que têm em vista corrigir em tempo real a velocidade de cada motor, de forma que os comandos de throttle, roll yaw e pitch, recebidos via serial, sejam executados corretamente. Os comandos de velocidade são enviados com recurso a sinais PWM para os ESCs, que por sua vez enviam energia para os motores, mediante o sinal recebido.

No decorrer do projeto, este esquema teve de sofrer alterações devido à falta de tempo, no entanto a estrutura inicial foi mantida de forma a puder ser continuado futuramente. O esquema atual está de acordo com a figura seguinte:

[//]: # (TODO: Adicionar imagem)

# Controlador de voo
O controlador de voo, o arduino, 
# Computador local
# Melhorias