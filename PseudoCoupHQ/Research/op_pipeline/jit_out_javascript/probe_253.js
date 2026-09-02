// probe 253 -- binary ??
function op_253(a, b) {
    return a ?? b;
}

%PrepareFunctionForOptimization(op_253);
op_253(true, 2.0);
op_253(true, 2.0);
%OptimizeFunctionOnNextCall(op_253);
op_253(true, 2.0);
