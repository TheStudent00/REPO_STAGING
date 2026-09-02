// probe 125 -- binary +
function op_125(a, b) {
    return a + b;
}

%PrepareFunctionForOptimization(op_125);
op_125(1.0, false);
op_125(1.0, false);
%OptimizeFunctionOnNextCall(op_125);
op_125(1.0, false);
