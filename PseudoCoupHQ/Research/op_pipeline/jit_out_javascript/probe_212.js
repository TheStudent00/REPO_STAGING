// probe 212 -- binary !=
function op_212(a, b) {
    return a != b;
}

%PrepareFunctionForOptimization(op_212);
op_212(1.0, false);
op_212(1.0, false);
%OptimizeFunctionOnNextCall(op_212);
op_212(1.0, false);
