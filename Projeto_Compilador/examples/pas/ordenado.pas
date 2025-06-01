program VerificarOrdem;

var
  i, n, atual, anterior: integer;
  ordenado: boolean;

begin
  writeln('Quantos números vais inserir?');
  readln(n);

  if n <= 1 then
  begin
    writeln('Sequência está ordenada por definição.');
    halt;
  end;

  ordenado := true;

  writeln('Número 1:');
  readln(anterior);

  for i := 2 to n do
  begin
    writeln('Número ', i, ':');
    readln(atual);
    if atual < anterior then
      ordenado := false;
    anterior := atual;
  end;

  if ordenado then
    writeln('A sequência está ordenada!')
  else
    writeln('A sequência não está ordenada.');
end.
