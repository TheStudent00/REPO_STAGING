// probe 143 -- binary *
function op_143(a, b) {
    return a * b;
}

%PrepareFunctionForOptimization(op_143);
op_143(1.0, false);
op_143(1.0, false);
%OptimizeFunctionOnNextCall(op_143);
op_143(1.0, false);
