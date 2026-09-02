// probe 255 -- binary instanceof
function op_255(a, b) {
    return a instanceof b;
}

%PrepareFunctionForOptimization(op_255);
op_255(1.0, 2.0);
op_255(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_255);
op_255(1.0, 2.0);
