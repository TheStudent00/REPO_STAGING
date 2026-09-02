// probe 118 -- binary |
function op_118(a, b) {
    return a | b;
}

%PrepareFunctionForOptimization(op_118);
op_118(true, 2.0);
op_118(true, 2.0);
%OptimizeFunctionOnNextCall(op_118);
op_118(true, 2.0);
