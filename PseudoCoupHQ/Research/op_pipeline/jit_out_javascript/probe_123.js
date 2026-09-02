// probe 123 -- binary +
function op_123(a, b) {
    return a + b;
}

%PrepareFunctionForOptimization(op_123);
op_123(1.0, 2.0);
op_123(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_123);
op_123(1.0, 2.0);
