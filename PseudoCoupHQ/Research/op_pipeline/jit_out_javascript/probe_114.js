// probe 114 -- binary |
function op_114(a, b) {
    return a | b;
}

%PrepareFunctionForOptimization(op_114);
op_114(1.0, 2.0);
op_114(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_114);
op_114(1.0, 2.0);
