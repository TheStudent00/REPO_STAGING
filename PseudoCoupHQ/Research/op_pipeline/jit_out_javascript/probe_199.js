// probe 199 -- binary ==
function op_199(a, b) {
    return a == b;
}

%PrepareFunctionForOptimization(op_199);
op_199(true, 2.0);
op_199(true, 2.0);
%OptimizeFunctionOnNextCall(op_199);
op_199(true, 2.0);
