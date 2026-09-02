// probe 250 -- binary ??
function op_250(a, b) {
    return a ?? b;
}

%PrepareFunctionForOptimization(op_250);
op_250(1.0, 2.0);
op_250(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_250);
op_250(1.0, 2.0);
