int: d; 
int: n;
int: N = pow(2, n) - 1;
int: k_max = ceil(log2((pow(2, n) - 1) * d));
var 0..k_max: k;

var 0..(pow(2, k_max) - 1): a;  
var 0..(pow(2, k_max) - 1): b;  

constraint forall(x in 1..N)(floor(x div d) == floor((((a * x) + b) div (pow(2, k)))));
solve minimize k;
output["\(a) \(b) \(k)"]


%
