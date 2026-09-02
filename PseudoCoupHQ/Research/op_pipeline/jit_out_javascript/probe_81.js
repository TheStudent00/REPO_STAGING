// probe 81 -- binary >>>
function op_81(a, b) {
    return a >>> b;
}

%PrepareFunctionForOptimization(op_81);
op_81(true, 2.0);
op_81(true, 2.0);
%OptimizeFunctionOnNextCall(op_81);
op_81(true, 2.0);
