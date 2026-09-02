// probe 225 -- binary !==
function op_225(a, b) {
    return a !== b;
}

%PrepareFunctionForOptimization(op_225);
op_225(true, 2.0);
op_225(true, 2.0);
%OptimizeFunctionOnNextCall(op_225);
op_225(true, 2.0);
