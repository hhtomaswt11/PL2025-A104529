program VerificarNumero;
var
  num: real; {integer}
begin
  writeln('Introduza um número:');
  readln(num);
  if num > 0.0 then {0}
    writeln('Número positivo')
  else if num < 0.0 then {0}
    writeln('Número negativo')
  else
    writeln('Zero');
end.
