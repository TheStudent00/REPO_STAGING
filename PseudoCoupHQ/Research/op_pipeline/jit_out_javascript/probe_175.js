// probe 175 -- binary <
function op_175(a, b) {
    return a < b;
}

%PrepareFunctionForOptimization(op_175);
op_175(1.0, 2.0);
op_175(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_175);
op_175(1.0, 2.0);
