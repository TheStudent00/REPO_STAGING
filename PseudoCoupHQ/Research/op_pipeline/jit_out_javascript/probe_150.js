// probe 150 -- binary /
function op_150(a, b) {
    return a / b;
}

%PrepareFunctionForOptimization(op_150);
op_150(1.0, 2.0);
op_150(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_150);
op_150(1.0, 2.0);
