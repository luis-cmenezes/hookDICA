## Descrição

Desenvolvido para o evento Brincando e Aprendendo do Museu DICA - UFU, este projeto tem como objetivo implementar um controlador para um braço robótico com 6 GDL. Este controlador trata-se da disponibilização de 14 comandos utilizados para:

 - Reiniciar o braço para a posição inicial;
 - Ativar/Desativar modo de precisão;
 - Rotacionar individualmente os motores do braço para cada direção.

## Como é feito

Através da biblioteca dynamixel_sdk (os motores utilizados são AX-12) e pynput, tem-se uma função callback ativada por qualquer tecla pressionada. Nessa função callback, à depender de uma interpretalção do input, há chamadas de funções de comunicação com os motores (torque, led, posição e velocidade).
