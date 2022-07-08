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

<h3>Introdução</h3>
Nas considerações iniciais e após pesquisa foi decidido que o protótipo iria ser um quadcopter. Isto porque tentamos encontrar o equilíbrio entre a estabilidade e facilidade de operar com a complexidade tando de hardware como software. Onde um drone com mais meios de propulsão se torna mais fácil de pilotar, no entanto muito mais complicado de programar pois há mais variáveis que o computador de bordo tem de calcular e ajustar. O design do chassi foi das primeiras decisões a ser tomada, no entanto o seu dimensionamento só foi realizado mais tarde após a conclusão da escolha dos componentes principais. De seguida foram escolhidos os motores sobredimensionados, tendo em atenção que o peso médio, de um drone de 50cm de diagonal, é de 1350 gramas. Escolhidos os motores escolhemos os Esc’s e seguidamente os sensores. Sabendo que teriamos de usar um raspberry e um arduino escolhemos uma bateria que fosse capaz de suprir as necessidades energéticas. Por fim escolhemos um conversor DC/DC para que fosse possível alimentar o raspberry. 

No final obtivemos um quadcopter de 49 cm de diagonal e 1283 gramas, onde o arduino opera como o controlador de voo e o raspberry como computador de voo. Isto deveu-se ao facto de os controladores de voo disponíveis no mercado estarem com valores extremamente elevados.

<h3>Chassi</h3>

O chassi foi a primeira escolha de hardware. Foi inspirado no DJI F350, por ser um chassi de design já testado, compacto, mas resistente. A técnica de construção adotada foi impressão 3D, isto porque desta forma poderíamos ir fazendo alterações ao longo do tempo e a adaptação do resto dos componentes ficava facilitada. Foi impresso com o filamento PETG por ser dos filamentos mais “elásticos” e assim ser mais resistente a eventuais impactos.

<h3>Motores</h3>
Os motores utilizados foram 4 Racestar Racing Edition 2205 2300KV. A decisão teve em conta as suas características sendo que este é um motor sem escovas, que comparativamente com os motores com escovas apenas pecam no seu custo inicial, no entanto tendem a ter uma vida mais longa e são mais fiáveis. As hélices escolhidas foram umas 5045 que em conjunto com o motor são capazes de levantar 950 gramas perfazendo um total de 3.8 quilogramas.

<h3>Bateria</h3>
Tendo em atenção a potência dos motores e a energia consumida pelos demais componentes a bateria escolhida foi uma LiPo HRB 4S, ou seja, de 4 células de 5000mAh e 14.8V. A decisão de avançar para uma LiPo foi devido ao facto de que estas são capazes de armazenar muito mais energia, mais seguras de usar e os ciclos de vida também são superiores quando comparado com outros tipos de baterias.  No entanto devido a um erro de encomenda ficamos com uma outra bateria que apenas diferia na amperagem sendo esta de 6000mAh. Na imagem está representado a distribuição de energia.

<h3>Arduino</h3>
O software e hardware de um arduino é bastante versátil, podendo interagir com diversos equipamentos e por isso pode funcionar como o “cérebro” do mais variado número de projetos. No caso deste projeto o arduino funciona como o controlador de voo, ou seja, tem as funções de precessão, comunicação e controle. Os sensores aplicados estão ligados a este controlador transmitindo-lhe a informação. Usando os dados recolhidos o arduino vai calcular a velocidade desejada para cada motor e enviá-la para os Esc’s. Os cálculos de todos os dados recolhidos e necessários ao voo são realizados por um algoritomo denominado PID. O controlador de voo tem, uma última função que é a comunicação, no caso, comunica com o raspberry por comunicação serial. Para além da transmissão de informação ao operador de dados como a altura, velocidade, pitch, roll e yaw, no caso de um voo autónomo o controlador de voo tem de ser capaz de comunicar com outros equipamentos para saber o destino e trajeto de voo.

<h3>Raspberry Pi 3</h3>

O Raspberry Pi é não mais do que um computador, no entanto, de dimensões muito inferiores. As suas capacidades, que vão desde comunicar com o exterior, processar imagem, programar, a correr programas de diferentes linguagens, tornam este pequeno equipamento bastante versátil e por isso decidimos usá-lo, entre outros fatores, para trabalhar como o nosso computador de voo. Neste equipamento é onde se encontram os programas e onde se processa a informação recebida pelos sensores presentes assim como as ordens dadas pelo operador. 

<h3>Esc’s</h3>

Para controlar o potencial fornecido aos motores é necessário recorrer a Esc’s (Electronic speed Controllers). Os Esc’s são os dispositivos que vão receber o sinal vindo do controlador de voo e modelá-lo para enviar aos motores. Sendo que os Esc’s disponíveis no mercado normalmente apenas dão para um tipo de motor, com ou sem escovas, teve de se ter em atenção este pormenor e optou-se por adquirir 4 Racestar RS30A. 
 
<h3>Sensores</h3>

Sensores são partes essenciais num drone, isto porque são eles que vão informar o controlador de voo do que se está a passar, desde dados de voo, a distâncias a objetos até à posição do mesmo. Desta forma utilizamos dois tipos de sensores, um IMU, que possui 3 eixos de giroscópio, 3 eixos de acelerómetro, 3 eixos de campo magnético e pressão de ar. É a partir dos dados retirados deste sensor que somos capazes de saber o pitch, roll e yaw, orientação e velocidade do drone, é também, com este sensor saber a altitude. No entanto neste caso, para saber as distâncias ao solo, laterais, frontais e traseiras foram comprados 5 sensores de ultrassom, um para a parte inferior e um para cada face. Estes sensores funcionam emitido ondas sonoras, com uma frequência mais elevada do que o ser humano consegue ouvir, e ao bater num objeto elas retornam ao sensor. Com o cálculo do tempo desde que o sensor emite as ondas até que elas retornem é possível calcular a distância. Optamos por estes uma vez que a zona prevista para o voo seria entre dois edifícios e então este tipo de sensores servia. 

<h3>Conversor DC-DC</h3>

Ubec (7.4V para 5V) converte tensões de baterias de 2S a 6S 

A bateria adotada para construir este drone tem uma tensão nominal de 14.8V, no entanto o Raspberry a ser implementado apenas funciona com uma tensão de 5V. Desta forma foi necessário implementar um conversor DC/DC, denominado de UBEC, que a sua função não é mais do que converter a tensão de 14.8V que a bateria debita para 5V para que o Raspberry possa funcionar. 

<h3>Comando</h3>

Para operação do drone foi usado um comando XBox que transmite os comandos para um computador e seguidamente para o computador de bordo. Abaixo está representado a operação que cada botão do comando realiza. É necessário ter em atenção o joystick esquerdo, o do acelerador. Sendo um comando de uma consola os joysticks têm uma mola interior que faz com que estes tendam sempre a centrar. Por este motivo nesta posição normal (centro), a informação que está a ser transmitida é que os motores devem estar a 50%. Assim ao ligar o drone é necessário levar este joystick para a posição mais inferior para que os motores estejam na sua rotação mínima. Este problema poderia não existir caso se tivesse dito que o acelerador era 0% com o joystick na posição central, mas de forma a se ter mais precisão e o acelerador ser mais gradual para evitar acelerações bruscas optou-se por manter este problema de forma a evitar outros futuramente. 

<h3>Pi Camera</h3>

A camara usada para a parte de visão do drone foi uma Pi camara. Esta camara é especifica para trabalhar com o raspberry e pela facilidade de comunicação entre os dois e o facto de ser uma camara pequena, leve e compacta era a escolha mais acertada. 

<h3>Carregador de Bateria </h3>

Naturalmente, é necessário um equipamento para se carregar a bateria, desta forma foi escolhido um iMAX B6 de 80W e &Amp. Foi escolhido este equipamento pela sua versatilidade podendo carregar baterias do tipo Li-ion, LiPo e LiFe com diferentes números de células assim como diferentes diferenças de potêncial. 

---

# Organização

[//]: # (TODO: Adicionar imagem)
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

---

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

Como se viu no tópico da organização, o software foi organizado segundo uma esquematização.
Para a parte do computador de voo, as comunicações entre programas foram feitas com recurso ao ROS.


# Controlador de voo

O controlador de voo tem como função receber os comandos, ler os dados sensoriais, realizar o controlo e enviar os sinais resultantes para os ESCs.
<h3>Troca de dados com o computador de voo</h3>
A receção de comandos e o envio dos ângulos do drone são feitos via serial.

Para evitar que a sequência de inicialização dos motores seja feita sem o computador de voo estar completamente inicializado, adicionou-se uma etapa de espera enquanto não houverem comunicações. Neste ponto poderia existir algum dispostitivo de corte de corrente aos motores, em que estes só seriam alimentados após o início das comunicações.

<h3>Leitura de dados dos sensores</h3>
Para comunicar com a IMU (Inertial measurement unit) por I2C foi utilizada a biblioteca wire . De seguida, foi definido o endereço slave 0x68, pois este é o valor predefinido no manual da IMU, e é enviado um 0 para registo 6B para fazer reset da IMU. Os endereços para os dados de cada sensor estão tabelados no folha de dados da IMU. Como as mensagens enviadas pelos sensores têm 16bits, são divididas em duas partes de 8bits, daí haver dois endereços para cada eixo. Para cada um dos sensores tem de ser selecionada uma escala de funcionamento, para isso é visto o sensitivity scale factor correspondente na folha de dados da IMU e divididas as leituras dos sensores por este para ter na saída valores com as unidades pretendidas. 

Para estimar o angulo de inclinação através dos três dados do acelerómetro foram utilizadas as fórmula do ângulo de Euler.  

[//]: # (TODO: Adicionar imagem)

Para combinar estes dados fez-se uma fusão de sensores.

Para perceber o intuito da fusão de sensores, comece-se por analisar o exemplo da medida do roll. Este não é medido diretamente, mas sim estimado através do giroscópio e do acelerómetro.  

O giroscópio mede a taxa de variação do ângulo em º/s em cada instante. Considerando que a horizontal é o ângulo 0º, no primeiro instante é estimado o ângulo do drone através de 0+Δt.taxa de variação do ângulo, no segundo instante é somando ao valor anterior Δt.taxa de variação do ângulo e sucessivamente, basicamente integrando a taxa de variação. Esta abordagem é chamada dead reckoning e é bastante eficaz a registar movimento em curtos períodos de tempo.  Este período de tempo é definido pelo erro e ruído intrínsecos do giroscópio. Estas variações, assim como ruído de alta frequência aleatório vão sendo incluídos em cada parcela, acumulando-se ao longo do tempo. Como não há uma referência fixa, o valor estimado vai se desviando do valor real do ângulo. 

Já no acelerómetro, quando o drone está estacionário a aceleração gravítica é a única detetada, apontando para baixo. Com um vetor de referência que aponta para baixo é possível calcular o ângulo entre este e o drone num dado momento. No entanto, o acelerómetro contém bastante ruído e as acelerações derivadas do movimento do drone também são incluídas, deixando a medição de apontar para baixo. Assim, o acelerómetro não é ideal para medidas em curtos intervalos de tempo, mas tem uma referência estável a longo prazo dado que a aceleração gravítica mantém-se constante. 

Tendo isto em conta, o ideal é combinar a capacidade do giroscópio de medir variações bruscas de ângulo com a estabilidade da referência do acelerómetro, para isso é utilizada a fusão de sensores. Uma das formas mais comuns e mais simples de fazer isto é utilizar um filtro complementar. Este filtro funciona de forma semelhante a uma média ponderada, sendo possível variar o peso da medida do giroscópio (98% neste caso) e do acelerómetro (2%) na estimativa final do ângulo.  Com esta combinação é possível manter a sensibilidade a variações súbitas do giroscópio preservando a exatidão ao longo do tempo do acelerómetro.  

Além destes sensores, idealmente, seria também incluído um magnetómetro para aumentar a fiabilidade das estimativas dos valores do pitch e do roll. Dado que o valor de referência do acelerómetro, a aceleração gravitacional, está alinhado com o eixo z não é apropriado para a determinação do yaw. Para isso, um magnetómetro é uma opção melhor dado que o seu valor de referência é um vetor que aponta diretamente para norte, algo que é necessário ter em consideração nos cálculos dado que a posição geográfica tem uma influência substancial na direção deste.

# Computador local


# Melhorias
No Hardware deveria ser adicionado um corte de corrente aos ESCs.

No computador de voo, o que é detectado são manchas dentro de uma gama de cores especificada e não incendios,a componente autónoma está a zeros e a interface gráfica está pouco desenvolvida
O programa de comunicação TCP também tem defeitos, fazendo com que apenas seja possível parar o programa com ctrl + \.
Por causa deste problema também não foi finalizado o launch file para automatizar a inicialização dos nós.

No controlador de voo o controlo é apenas feito no pitch e no roll. Para controlar o Yaw é necessário utilizar também o magnetómetro e para controlar o throttle é necessário o barómetro

No computador local a aplicação utilizada para receber os comandos apenas é compativel com linux. Esta poderia ser implementada na interface WEB