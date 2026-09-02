// probe 240 -- binary >
function op_240(a, b) {
    return a > b;
}

%PrepareFunctionForOptimization(op_240);
op_240(1.0, 2.0);
op_240(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_240);
op_240(1.0, 2.0);
