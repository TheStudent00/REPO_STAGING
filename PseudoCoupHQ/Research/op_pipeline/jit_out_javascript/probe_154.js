// probe 154 -- binary /
function op_154(a, b) {
    return a / b;
}

%PrepareFunctionForOptimization(op_154);
op_154(true, 2.0);
op_154(true, 2.0);
%OptimizeFunctionOnNextCall(op_154);
op_154(true, 2.0);
