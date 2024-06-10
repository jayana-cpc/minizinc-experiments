int: C;
int: N = ceil(log2(C));
set of int: X = -2*C..2*C; 
array[0..N] of var -1..1: L;
array[0..N] of var {0, 1, 3, 17, 257}: R;

function var int: optimize(array[int] of var int: L) =
    sum(k in 0..N)(abs(L[k]));

function string: multiplication(array[int] of var int: L, array[int] of var int: R) =
    concat(
        [ if fix(L[k]) == 1 then "+" ++ show(fix(R[k]) * (2^k)) ++ "x"
          elseif fix(L[k]) == -1 then "-" ++ show(fix(R[k]) * (2^k)) ++ "x"
          else "" endif
        | k in reverse(0..N)
        ]
    );

constraint forall(x in X)(C * x == sum(k in 0..N)(L[k] * R[k] * (2^k) * x));

solve minimize optimize(L);
%, " L: ", show(L), " R: ", show(R)
output [
    show(optimize(L)), " ", multiplication(L, R)
];
