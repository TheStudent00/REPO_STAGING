// probe 181 -- binary <
function op_181(a, b) {
    return a < b;
}

%PrepareFunctionForOptimization(op_181);
op_181(true, 2.0);
op_181(true, 2.0);
%OptimizeFunctionOnNextCall(op_181);
op_181(true, 2.0);
