// probe 102 -- binary ^
function op_102(a, b) {
    return a ^ b;
}

%PrepareFunctionForOptimization(op_102);
op_102(1.0, 2.0);
op_102(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_102);
op_102(1.0, 2.0);
