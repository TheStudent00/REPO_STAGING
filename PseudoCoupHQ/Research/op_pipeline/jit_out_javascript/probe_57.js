// probe 57 -- binary ||
function op_57(a, b) {
    return a || b;
}

%PrepareFunctionForOptimization(op_57);
op_57(1.0, 2.0);
op_57(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_57);
op_57(1.0, 2.0);
