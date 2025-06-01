program ParOuImpar;
var
  num: integer;
begin
  writeln('Introduza um número:');
  readln(num);
  if num mod 2 = 0 then
    writeln(num, ' é par')
  else
    writeln(num, ' é ímpar');
end.
