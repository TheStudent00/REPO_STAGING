// probe 63 -- binary ||
function op_63(a, b) {
    return a || b;
}

%PrepareFunctionForOptimization(op_63);
op_63(true, 2.0);
op_63(true, 2.0);
%OptimizeFunctionOnNextCall(op_63);
op_63(true, 2.0);
