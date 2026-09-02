// probe 179 -- binary <
function op_179(a, b) {
    return a < b;
}

%PrepareFunctionForOptimization(op_179);
op_179(1.0, false);
op_179(1.0, false);
%OptimizeFunctionOnNextCall(op_179);
op_179(1.0, false);
