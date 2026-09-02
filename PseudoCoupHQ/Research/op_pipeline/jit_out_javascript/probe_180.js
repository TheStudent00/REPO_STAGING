// probe 180 -- binary <
function op_180(a, b) {
    return a < b;
}

%PrepareFunctionForOptimization(op_180);
op_180(true, 2.0);
op_180(true, 2.0);
%OptimizeFunctionOnNextCall(op_180);
op_180(true, 2.0);
