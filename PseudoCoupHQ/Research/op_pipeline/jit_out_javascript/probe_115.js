// probe 115 -- binary |
function op_115(a, b) {
    return a | b;
}

%PrepareFunctionForOptimization(op_115);
op_115(1.0, 2.0);
op_115(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_115);
op_115(1.0, 2.0);
