// probe 141 -- binary *
function op_141(a, b) {
    return a * b;
}

%PrepareFunctionForOptimization(op_141);
op_141(1.0, 2.0);
op_141(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_141);
op_141(1.0, 2.0);
