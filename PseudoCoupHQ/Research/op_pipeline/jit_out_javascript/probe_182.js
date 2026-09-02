// probe 182 -- binary <
function op_182(a, b) {
    return a < b;
}

%PrepareFunctionForOptimization(op_182);
op_182(true, false);
op_182(true, false);
%OptimizeFunctionOnNextCall(op_182);
op_182(true, false);
