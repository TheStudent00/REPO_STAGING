// probe 113 -- binary |
function op_113(a, b) {
    return a | b;
}

%PrepareFunctionForOptimization(op_113);
op_113(1.0, false);
op_113(1.0, false);
%OptimizeFunctionOnNextCall(op_113);
op_113(1.0, false);
