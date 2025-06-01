program Fatorial;
var
    n, i, fat: integer;
begin
    writeln('Introduza um número inteiro positivo:');
    readln(n);
    fat := 1;
    i := 1;
    while i <= n do
    begin
        fat := fat * i;
        i := i + 1;
    end;
    writeln('Fatorial de ', n, ': ', fat);
end.
