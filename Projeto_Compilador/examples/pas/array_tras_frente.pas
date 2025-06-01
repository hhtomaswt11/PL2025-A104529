program InverterArray;
var
  numeros: array[1..4] of integer;
  i: integer;
begin
  writeln('Introduza 4 números:');
  for i := 1 to 4 do
    readln(numeros[i]);

  writeln('Em ordem inversa:');
  for i := 4 downto 1 do
    writeln(numeros[i]);
end.
