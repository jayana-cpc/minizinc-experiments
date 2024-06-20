/* Model Leveraging Expression Reuse
*  Optimization Goal: 
*   - Reduce Operation Count
*   - Maximize Expression Reuse
*/

int: C;
int: N = ceil(log2(C));
array[0..N] of var -1..1: L;
array[0..N] of var {0, 1, 3, 5, 9, 17, 33, 65, 129, 257, 513, 1025, 2049, 4097, 8193}: R;

function var int: optimize(array[int] of var int: L, array[int] of var int: R) =
   sum(k in 0..N - 1)(abs(L[k])) - 1 + (uniqueExpressions(R));
         
function var int: uniqueExpressions(array[int] of var int: R) =
    let {
        set of int: values = {3, 5, 9, 17, 33, 65, 129, 257, 513, 1025, 2049, 4097, 8193},
        array[1..card(values)] of var int: count_values = [sum(k in 0..N where R[k] == v)(1) | v in values]
    } in
        sum(i in 1..card(values) where count_values[i] > 0)(1);
            
function string: multiplication(array[int] of var int: L, array[int] of var int: R) =
    concat(
        [ if fix(L[k]) == 1 /\ fix(R[k]) != 0 then "+" ++ show(fix(2^k)) ++ "(" ++ show((R[k])) ++ "x" ++ ")" 
          elseif fix(L[k]) == -1 /\ fix(R[k]) != 0 then "-" ++ show(fix(2^k)) ++ "(" ++ show((R[k])) ++ "x" ++ ")"
          else "" endif
        | k in reverse(0..N - 1)
        ]
    );

constraint (C == sum(k in 0..N - 1)(L[k] * R[k] * (2^k)));

solve minimize optimize(L, R);

output [
    show(optimize(L, R)), " ", multiplication(L, R)
];

