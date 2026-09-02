// probe 64 -- binary ||
function op_64(a, b) {
    return a || b;
}

%PrepareFunctionForOptimization(op_64);
op_64(true, 2.0);
op_64(true, 2.0);
%OptimizeFunctionOnNextCall(op_64);
op_64(true, 2.0);
