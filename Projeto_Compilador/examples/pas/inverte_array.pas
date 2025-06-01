program InverterArray;
var
  a: array[1..5] of integer;
  i: integer;
begin
  writeln('Introduza 5 números:');
  for i := 1 to 5 do
    readln(a[i]);

  writeln('Em ordem inversa:');
  for i := 5 downto 1 do
    writeln(a[i]);
end.
