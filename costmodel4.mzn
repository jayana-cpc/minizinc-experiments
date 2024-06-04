int: C;
int: N2 = ceil(log2(C)); 
int: N3 = ceil(log(3, C));  

set of int: X = -2*C..2*C; 
array[0..N2+N3] of var -1..1: L;

function var float: optimize(array[int] of var int: L) =
    sum(k in 0..N2)(abs(L[k])) + 
    sum(k in N2+1..N2+N3)(abs(L[k]) * 3);


function string: multiplication(array[int] of var int: L) =
    concat(
        [ if k <= N2 then
            if fix(L[k]) == 1 then "+" ++ show(2^k) ++ "x"
            elseif fix(L[k]) == -1 then "-" ++ show(2^k) ++ "x"
            else "" endif
          elseif k > N2 then
            if fix(L[k]) == 1 then "+" ++ show(3^(k-N2-1)) ++ "x"
            elseif fix(L[k]) == -1 then "-" ++ show(3^(k-N2-1)) ++ "x"
            else "" endif
          else "" endif
        | k in reverse(0..N2+N3)
        ]
    );

constraint forall(x in X)(
    C * x == sum(k in 0..N2)(L[k] * (2^k) * x) + 
    sum(k in N2+1..N2+N3)(L[k] * (3^(k-N2-1)) * x)
);

solve minimize optimize(L);

output [
    show(optimize(L)), " ", multiplication(L)
];
