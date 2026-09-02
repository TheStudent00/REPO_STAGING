// probe 61 -- binary ||
function op_61(a, b) {
    return a || b;
}

%PrepareFunctionForOptimization(op_61);
op_61(1.0, 2.0);
op_61(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_61);
op_61(1.0, 2.0);
