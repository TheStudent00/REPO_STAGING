// probe 103 -- binary ^
function op_103(a, b) {
    return a ^ b;
}

%PrepareFunctionForOptimization(op_103);
op_103(1.0, 2.0);
op_103(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_103);
op_103(1.0, 2.0);
