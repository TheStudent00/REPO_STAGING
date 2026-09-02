// probe 251 -- binary ??
function op_251(a, b) {
    return a ?? b;
}

%PrepareFunctionForOptimization(op_251);
op_251(1.0, false);
op_251(1.0, false);
%OptimizeFunctionOnNextCall(op_251);
op_251(1.0, false);
