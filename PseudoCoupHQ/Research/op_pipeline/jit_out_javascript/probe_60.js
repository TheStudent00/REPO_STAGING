// probe 60 -- binary ||
function op_60(a, b) {
    return a || b;
}

%PrepareFunctionForOptimization(op_60);
op_60(1.0, 2.0);
op_60(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_60);
op_60(1.0, 2.0);
