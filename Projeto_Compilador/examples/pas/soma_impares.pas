program SomaIndicesImpares;
var
  v: array[1..6] of integer;
  i, soma: integer;
begin
  soma := 0;
  writeln('Introduza 6 números:');
  for i := 1 to 6 do
    readln(v[i]);

  for i := 1 to 6 do
    if i mod 2 = 1 then
      soma := soma + v[i];

  writeln('Soma dos índices ímpares: ', soma);
end.
