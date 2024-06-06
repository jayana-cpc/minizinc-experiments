int: d; 
int: n;
int: N = pow(2, n) - 1;
int: k_max = ceil(log2((pow(2, n) - 1) * d));

var 0..k_max: k;

% Relaxed Constraint
constraint forall(x in 1..N) (
    let {
        var int: a = ceil(pow(2,k) div d);
        var int: sign = (a * d) - pow(2, k);
    } in
    if sign < 0 then
        d * (floor(pow(2, n) div d)) - d + 1 < pow(2, k) div ((pow(2, k)) mod d)
    else
        (d * (floor(pow(2, n) div d)) - d + 1) < (pow(2, k) div (0 - (pow(2, k)) mod d)) 
    endif
);
solve minimize k;
output ["\(k)"];