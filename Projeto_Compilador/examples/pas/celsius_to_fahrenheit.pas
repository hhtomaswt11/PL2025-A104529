program CelsiusParaFahrenheit;
var
  celsius: integer;
  fahrenheit: integer;  {TENTAR INCLUIR COM REAL}
begin
  writeln('Introduza a temperatura em Celsius:');
  readln(celsius);
  fahrenheit := (celsius * 9 div 5) + 32;   { TENTAR INCLUIR COM / }  { O OUTPUT ESTA A SAIR NAO INTEIRO PORQUE?}
  writeln('Temperatura em Fahrenheit: ', fahrenheit); {INCLUIR FORMATACAO DE VALORES?}
end.

