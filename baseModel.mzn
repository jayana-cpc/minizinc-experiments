/* Base Model
*  Optimization Goal: Reduce operation count.
*/

int: C;
int: N = ceil(log2(C));
array[0..N] of var -1..1: L;

function var int: optimize(array[int] of var int: L) =
    sum(k in 0..N)(abs(L[k])) - 1;

function string: multiplication(array[int] of var int: L) =
    concat(
        [ if fix(L[k]) == 1 then "+" ++ show(2^k) ++ "x"
          elseif fix(L[k]) == -1 then "-" ++ show(2^k) ++ "x"
          else "" endif
        | k in reverse(0..N)
        ]
    );

constraint (C == sum(k in 0..N)(L[k] * (2^k)));

solve minimize optimize(L);

output [
    show(optimize(L)), " ", multiplication(L)
];
