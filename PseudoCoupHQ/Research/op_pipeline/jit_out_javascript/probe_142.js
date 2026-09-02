// probe 142 -- binary *
function op_142(a, b) {
    return a * b;
}

%PrepareFunctionForOptimization(op_142);
op_142(1.0, 2.0);
op_142(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_142);
op_142(1.0, 2.0);
