// probe 131 -- binary -
function op_131(a, b) {
    return a - b;
}

%PrepareFunctionForOptimization(op_131);
op_131(1.0, false);
op_131(1.0, false);
%OptimizeFunctionOnNextCall(op_131);
op_131(1.0, false);
