// probe 119 -- binary |
function op_119(a, b) {
    return a | b;
}

%PrepareFunctionForOptimization(op_119);
op_119(true, false);
op_119(true, false);
%OptimizeFunctionOnNextCall(op_119);
op_119(true, false);
