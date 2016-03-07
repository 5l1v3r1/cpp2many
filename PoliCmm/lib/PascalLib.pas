(* PoliCmm library starts *)
unit PascalLib;



interface

type 
    vectorint(n1 : INTEGER) = ARRAY [0 .. n1] OF INTEGER;
    vectorintPtr = ^vectorint;

function suma_chars (var x,y: char): char;
function readbool (var x: boolean): boolean;
function readint (var x: integer): boolean;
function readreal (var x: real): boolean;
function readsingle (var x: single): boolean;
function readdouble (var x: double): boolean;
function readchar (var x: char): boolean;
function readstring (var x: string): boolean;


procedure preadbool (var x: boolean);
procedure preadint (var x: integer);
procedure preadreal (var x: real);
procedure preadsingle (var x: single);
procedure preaddouble (var x: double);
procedure preadchar (var x: char);
procedure preadstring (var x: string);

function castint2real(x : integer) : real;
function castreal2int(x : real) : integer;
function castint2single(x : integer) : single;
function castsingle2int(x : single) : integer;
function castint2double(x : integer) : double;
function castdouble2int(x : double) : integer;


procedure writereal(x: real);
procedure writesingle(x: single);
procedure writedouble(x: double);
procedure writeboolean(x: boolean);
VAR  precision : INTEGER = -1;

function preIncrement(var x:integer):integer;
function postIncrement(var x:integer):integer;
procedure ppreIncrement(var x:integer);
procedure ppostIncrement(var x:integer);
function preIncrementBoolean(var x:integer):boolean;
function postIncrementBoolean(var x:integer):boolean;
function preDecrement(var x:integer):integer;
function postDecrement(var x:integer):integer;
procedure ppreDecrement(var x:integer);
procedure ppostDecrement(var x:integer);
function preDecrementBoolean(var x:integer):boolean;
function postDecrementBoolean(var x:integer):boolean;

const M_PI : real = 3.14159265358979323846264338327950288419716939937510;



procedure qsortvectorint(var v : vectorintPtr; 
                left : Integer; right : Integer);
procedure sortvectorint(var v : vectorintPtr);


implementation

function preIncrement(var x:integer):integer;
begin
    x := x + 1;
    preIncrement := x;
end;
function postIncrement(var x:integer):integer;
begin
    postIncrement := x;
    x := x + 1;
end;
procedure ppreIncrement(var x:integer);
begin
    x := x + 1;
end;
procedure ppostIncrement(var x:integer);
begin
    x := x + 1;
end;
function preIncrementBoolean(var x:integer):boolean;
begin
    x := x + 1;
    preIncrementBoolean := x <> 0;
end;
function postIncrementBoolean(var x:integer):boolean;
begin
    postIncrementBoolean := x <> 0;
    x := x + 1;
end;

function preDecrement(var x:integer):integer;
begin
    x := x - 1;
    preDecrement := x;
end;
function postDecrement(var x:integer):integer;
begin
    postDecrement := x;
    x := x - 1;
end;

procedure ppreDecrement(var x:integer);
begin
    x := x - 1;
end;
procedure ppostDecrement(var x:integer);
begin
    x := x - 1;
end;
function preDecrementBoolean(var x:integer):boolean;
begin
    x := x - 1;
    preDecrementBoolean := x <> 0;
end;
function postDecrementBoolean(var x:integer):boolean;
begin
    postDecrementBoolean := x <> 0;
    x := x - 1;
end;


procedure sortvectorint(var v : vectorintPtr);
begin
    qsortvectorint(v, 0, High(v^) - 1);
end;


procedure qsortvectorint(var v : vectorintPtr; 
                left : Integer; right : Integer);
Var pivot, l_ptr, r_ptr : Integer;


begin
    l_ptr := left;
    r_ptr := right;
    pivot := v^[left];
    while (left < right) do
    begin
        while ((v^[right] >= pivot) AND (left < right)) do
            right := right - 1;
        if (left <> right) then
        begin
            v^[left] := v^[right];
            left := left + 1;
        end;
        while ((v^[left] <= pivot) AND (left < right)) do
            left := left + 1;
        if (left <> right) then
        begin
            v^[right] := v^[left];
            right := right - 1;
        end;
    end;
    v^[left] := pivot;
    pivot := left;
    left := l_ptr;
    right := r_ptr;
    if (left < pivot) then
        qsortvectorint(v, left, pivot-1);
    if (right > pivot) then
        qsortvectorint(v, pivot+1, right);
end;



procedure writeboolean(x: boolean);
begin
    if x = True then write(1) else write (0);
end;

function castint2real(x : integer) : real;
begin
    castint2real := x;
end;

function castreal2int(x : real) : integer;
begin
    castreal2int := trunc(x);
end;


function castint2single(x : integer) : single;
begin
    castint2single := x;
end;

function castsingle2int(x : single) : integer;
begin
    castsingle2int := trunc(x);
end;


function castint2double(x : integer) : double;
begin
    castint2double := x;
end;

function castdouble2int(x : double) : integer;
begin
    castdouble2int := trunc(x);
end;


procedure writereal(x: real);
begin
    write(x:0:precision);
end;

procedure writesingle(x: single);
begin
    write(x:0:precision);
end;

procedure writedouble(x: double);
begin
    if precision <> -1 then write(x:0:precision)
    else write(x);
//     else begin 
//         var rest : double;
//         var th : double = 0.0000005;
//         var st, i, t: integer;
//         t := trunc(x);
//         write(t);
//         rest := x - t;
//         st := -1;
//         if (t> 0) then st := 0;
//         if (rest < th) and (t > 0) then return;
//         write('.');
//         i := 1;
//         while ((i <= st + 6) or (st = -1) ) and (rest > th) do
//         begin
//             rest := rest * 10;
//             t := trunc(rest + 10 * th);
//             write(t);
//             rest := rest - t;
//             if (t > 0) and (st = -1) then begin
//                 st := i - 1;
//             end;
//             if (st >= 0) then th := th * 10;
//             i := i + 1;
//         end;
//     end;
end;

function suma_chars (var x,y: char): char;
begin
    suma_chars := chr(ord(x) + ord(y))
end;


function readbool (var x: boolean): boolean;
begin
    var y : integer;
    if SeekEof then begin
        readbool := False;
    end else begin
        read(y);
        if y = 0 then
            x := False
        else
            x := True;
        readbool := True;
    end;
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

function readsingle (var x: single): boolean;
begin
    if SeekEof then begin
        readsingle := false;
    end else begin
        readsingle := true;
        Read(x);
   end;
end;

function readdouble (var x: double): boolean;
begin
    if SeekEof then begin
        readdouble := false;
    end else begin
        readdouble := true;
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


function readstring (var x: string): boolean;
var
   c: char;
begin
    if SeekEof then begin
        readstring := false;
    end else begin
        while SeekEoln do ReadLn;
        x := '';
        readstring := true;
        while not Eof and not Eoln do begin
            Read(c);
            if c = ' ' then break;
            x := x + c;
         end;
    end;
end;


procedure preadint (var x: integer);
begin
    if SeekEof then begin
    end else begin
        read(x);
    end;
end;

procedure preadbool (var x: boolean);
begin
    var y : integer;
    if SeekEof then begin
    end else begin
        read(y);
        if y = 0 then
            x := False
        else
            x := True;
    end;
end;


procedure preadreal (var x: real);
begin
    if SeekEof then begin
    end else begin
        Read(x);
   end;
end;

procedure preadsingle (var x: single);
begin
    if SeekEof then begin
    end else begin
        Read(x);
   end;
end;

procedure preaddouble (var x: double);
begin
    if SeekEof then begin
    end else begin
        Read(x);
   end;
end;


procedure preadchar (var x: char);
begin
    if SeekEof then begin
    end else begin
        Read(x);
   end;
end;


procedure preadstring (var x: string);
var
   c: char;
begin
    if SeekEof then begin
    end else begin
        while SeekEoln do ReadLn;
        x := '';
        while not Eof and not Eoln do begin
            Read(c);
            if c = ' ' then break;
            x := x + c;
         end;
    end;
end;
  
end.
(* PoliCmm library ends *)
