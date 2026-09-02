// probe 151 -- binary /
function op_151(a, b) {
    return a / b;
}

%PrepareFunctionForOptimization(op_151);
op_151(1.0, 2.0);
op_151(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_151);
op_151(1.0, 2.0);
