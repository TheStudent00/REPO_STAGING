// probe 222 -- binary !==
function op_222(a, b) {
    return a !== b;
}

%PrepareFunctionForOptimization(op_222);
op_222(1.0, 2.0);
op_222(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_222);
op_222(1.0, 2.0);
