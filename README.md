# FireCopter
## Como escrever e testar o código - Raspberry
Para enviar o código para o github convém que este tenha sido testado. Como não há placas para todos trabalharem é necessário recorrer a um emulador. Sugetão: [Tuturial com QEMU](https://azeria-labs.com/emulate-raspberry-pi-with-qemu/).

Para programar a raspberry tenho usado o protocolo ssh: Permite programar remotamente e testar na placa ou num simulador

 

Para ligar ao pycharm é necessário dar permissões de leitura e de escrita à pasta usada na raspberry

    sudo chmod 777 FireCopter
Para configurar o pycharm seguir este [Tuturial](https://www.youtube.com/watch?v=kuowBMqM1Ow)

O objetivo desta metodologia é ter uma sicronização automática entre os ficheiros locais e a raspberry e uma sicronização manual entre os ficheiros locais e o github.
Desta forma é possivel estar a testar o código recorrentemente e se algo correr mal temos o backup no github.


Para comunicar com a placa por ssh e ter acesso às aplicações gráficas (mudar para o ip correto):

    sudo ssh -X firecopter@192.168.1.213