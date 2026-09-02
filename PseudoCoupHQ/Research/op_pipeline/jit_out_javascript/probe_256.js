// probe 256 -- binary instanceof
function op_256(a, b) {
    return a instanceof b;
}

%PrepareFunctionForOptimization(op_256);
op_256(1.0, 2.0);
op_256(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_256);
op_256(1.0, 2.0);
