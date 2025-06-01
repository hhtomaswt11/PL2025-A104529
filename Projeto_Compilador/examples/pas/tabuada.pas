program Tabuada;
var
  i, num: integer;
begin
  writeln('Introduza um número para ver a tabuada:');
  readln(num);
  for i := 1 to 10 do
    writeln(num, 'x', i, '=', num * i);
end.
