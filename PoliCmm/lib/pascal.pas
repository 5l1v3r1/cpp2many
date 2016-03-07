(* PoliCmm library starts *)

function suma_chars (var x,y: char): char;
begin
    suma_chars := chr(ord(x) + ord(y))
end;




function readint (var x: integer): boolean;
begin
    if SeekEof then begin
        readint := false;
    end else begin
        readint := true;
        read(x);
    end;
end;


function readreal (var x: real): boolean;
begin
    if SeekEof then begin
        readreal := false;
    end else begin
        readreal := true;
        Read(x);
   end;
end;


function readchar (var x: char): boolean;
begin
    if SeekEof then begin
        readchar := false;
    end else begin
        readchar := true;
        Read(x);
   end;
end;


function readword (var x: string): boolean;
var
   c: char;
begin
    if SeekEof then begin
        readword := false;
    end else begin
        while SeekEoln do ReadLn;
        x := '';
        readword := true;
        while not Eof and not Eoln do begin
            Read(c);
            if c = ' ' then break;
            x := x + c;
         end;
    end;
end;
  
(* PoliCmm library ends *)
