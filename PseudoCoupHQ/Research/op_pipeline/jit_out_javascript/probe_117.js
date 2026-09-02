// probe 117 -- binary |
function op_117(a, b) {
    return a | b;
}

%PrepareFunctionForOptimization(op_117);
op_117(true, 2.0);
op_117(true, 2.0);
%OptimizeFunctionOnNextCall(op_117);
op_117(true, 2.0);
