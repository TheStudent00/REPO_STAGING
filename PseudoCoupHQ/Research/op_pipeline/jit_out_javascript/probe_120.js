// probe 120 -- binary +
function op_120(a, b) {
    return a + b;
}

%PrepareFunctionForOptimization(op_120);
op_120(1.0, 2.0);
op_120(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_120);
op_120(1.0, 2.0);
