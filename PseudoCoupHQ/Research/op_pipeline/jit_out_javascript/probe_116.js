// probe 116 -- binary |
function op_116(a, b) {
    return a | b;
}

%PrepareFunctionForOptimization(op_116);
op_116(1.0, false);
op_116(1.0, false);
%OptimizeFunctionOnNextCall(op_116);
op_116(1.0, false);
