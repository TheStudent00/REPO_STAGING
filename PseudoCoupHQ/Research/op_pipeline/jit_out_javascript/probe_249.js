// probe 249 -- binary ??
function op_249(a, b) {
    return a ?? b;
}

%PrepareFunctionForOptimization(op_249);
op_249(1.0, 2.0);
op_249(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_249);
op_249(1.0, 2.0);
