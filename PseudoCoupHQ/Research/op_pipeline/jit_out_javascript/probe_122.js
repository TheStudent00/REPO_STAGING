// probe 122 -- binary +
function op_122(a, b) {
    return a + b;
}

%PrepareFunctionForOptimization(op_122);
op_122(1.0, false);
op_122(1.0, false);
%OptimizeFunctionOnNextCall(op_122);
op_122(1.0, false);
