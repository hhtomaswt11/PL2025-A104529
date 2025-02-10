<!-- 

O manifesto deverá ter a seguinte estrutura: título, data, autor (nome, número e foto), resumo (lista de parágrafos descrevendo sucintamente em que consistiu o trabalho), lista de resultados (lista com apontadores para os ficheiros resultantes);

-->


# Somador ON/OFF
- **Data:** 10 de fevereiro de 2025
- **Autor:** Tomás Henrique Alves Melo - A104529 

<img src="../assets/perfil.jpg" alt="A104529 - Tomás Melo" width="150">


## Resumo

Decidi desenvolver para este trabalho prático duas versões do exercício 'Somador ON/OFF' proposto. A principal diferença entre as duas abordagens está no uso de regex (expressões regulares). 

Na primeira versão, após rever conceitos de linguagem Python, apliquei-os, de modo a conseguir desenvolver uma versão simples e funcional do exercício que consiste na iteração de toda a mensagem, com recurso a uma variável de controlo de estado do somador, váriavel 'ligado', que indica se o somador está ligado ou não, acumulação dos números numa variável temporária (filtragem dos números feita pelo método isdigit()) que irá permitir a soma dos números obtidos até ao momento e posterior reset, de modo a poder acumular novos números sempre que a soma dos já acumulados é feita, procura pelas strings 'on' e 'off' para verificar as mudanças de estado do somador e procura pelo caracetere '=' para, assim, retornar a soma acumulada até ao momento. 

Na segunda versão decidi antecipar o estudo de regex e comecei a ver métodos para expressões regulares da biblioteca re como search(), findall(), split(), entre outros. Assim, recorri ao método findall() para filtrar por padrões (números inteiros, 'on', 'off' e '=') e, com base no padrão, operações são realizadas. Para 'on' alterámos o estado do somador para ligado com recurso à variável de controlo 'ligado', analogamente para o caso em que o padrão atual é 'off'. Se o estado for 'on' e o token atual for um número inteiro, adicionamos esse número à variável soma (somando) e, por fim, quando o caractere/token atual é '=' retornamos a soma acumulada até ao momento. 

Todo o código (das duas versões) encontra-se adequadamente documentado para fácil entendimento daquilo que foi feito neste trabalho prático. 


## Resultados
Ficheiros elaborados:

- [somadoronoff.py](./somadoronoff.py)
- [somadoronoffNOREGEX.py](./somadoronoffNOREGEX.py)


