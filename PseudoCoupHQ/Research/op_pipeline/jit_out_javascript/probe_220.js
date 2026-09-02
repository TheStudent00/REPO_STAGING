// probe 220 -- binary !==
function op_220(a, b) {
    return a !== b;
}

%PrepareFunctionForOptimization(op_220);
op_220(1.0, 2.0);
op_220(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_220);
op_220(1.0, 2.0);
