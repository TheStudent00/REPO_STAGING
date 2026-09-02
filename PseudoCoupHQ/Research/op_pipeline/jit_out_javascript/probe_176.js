// probe 176 -- binary <
function op_176(a, b) {
    return a < b;
}

%PrepareFunctionForOptimization(op_176);
op_176(1.0, false);
op_176(1.0, false);
%OptimizeFunctionOnNextCall(op_176);
op_176(1.0, false);
