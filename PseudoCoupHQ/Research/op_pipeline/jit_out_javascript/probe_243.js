// probe 243 -- binary >
function op_243(a, b) {
    return a > b;
}

%PrepareFunctionForOptimization(op_243);
op_243(true, 2.0);
op_243(true, 2.0);
%OptimizeFunctionOnNextCall(op_243);
op_243(true, 2.0);
