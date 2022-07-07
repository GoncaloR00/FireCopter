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
# Hardware
# Organização
# Computador de voo
Para ligar ao pycharm é necessário dar permissões de leitura e de escrita à pasta usada na raspberry

    sudo chmod 777 FireCopter
Para configurar o pycharm seguir este [Tuturial](https://www.youtube.com/watch?v=kuowBMqM1Ow)

O objetivo desta metodologia é ter uma sicronização automática entre os ficheiros locais e a raspberry e uma sicronização manual entre os ficheiros locais e o github.
Desta forma é possivel estar a testar o código recorrentemente e se algo correr mal temos o backup no github.


Para comunicar com a placa por ssh e ter acesso às aplicações gráficas (mudar para o ip correto):

    sudo ssh -X firecopter@192.168.1.213

# Controlador de voo
# Computador local
# Melhorias