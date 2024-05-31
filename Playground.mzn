int: C;
int: N = ceil(log2(C));
set of int: X = -2*C..2*C; 
array[0..N] of var -1..1: L;
% All values of X, C times X equals the sum
% existential quantifier in minizinc
function var int: optimize(array[int] of var int: L) =
    sum(k in 0..N)(abs(L[k]) * (k + 1));
    
function string: multiplcation(array[int] of var int: L) =
    concat(
        [ if fix(L[k]) == 1 then "+" ++ show(2^k) ++ "x"
          elseif fix(L[k]) == -1 then "-" ++ show(2^k) ++ "x"
          else "" endif
        | k in reverse(0..N)
        ]
    );       
constraint forall(x in X)(C * x == sum(k in 0..N)(L[k] * (2^k) * x));

solve minimize optimize(L);
output [ "L:", show(L),"\n cost:", show(optimize(L)), "\n multiplication: ", multiplcation(L)];

% Print function to format L, Goal: Print out the full operation 
% ex: c = 7: print 8x - x
% Run on more interesting examples
% C = 21474836, 52711, 648391, 9737333

% Change cost function to compare results (Weight cost function)
