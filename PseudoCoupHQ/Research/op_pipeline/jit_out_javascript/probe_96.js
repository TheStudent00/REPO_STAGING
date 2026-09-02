// probe 96 -- binary &
function op_96(a, b) {
    return a & b;
}

%PrepareFunctionForOptimization(op_96);
op_96(1.0, 2.0);
op_96(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_96);
op_96(1.0, 2.0);
