program NumeroPrimo;
var
    num, i: integer;
    primo: boolean;
begin
    writeln('Introduza um número inteiro positivo:');
    readln(num);
    
    if num < 0 then
    	begin
    	writeln('Não existem números primos negativos.');
    	halt;
    	end;

    if num < 2 then
        primo := false
    else
    begin
        primo := true;
        i := 2;
        while (i <= (num div 2)) and primo do
        begin
            if num mod i = 0 then
                primo := false;
            i := i + 1;
        end;
    end;
    

    if primo then
        writeln(num, ' é um número primo')
    else
        writeln(num, ' não é um número primo');
end.
