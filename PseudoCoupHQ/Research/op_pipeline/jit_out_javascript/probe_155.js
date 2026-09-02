// probe 155 -- binary /
function op_155(a, b) {
    return a / b;
}

%PrepareFunctionForOptimization(op_155);
op_155(true, false);
op_155(true, false);
%OptimizeFunctionOnNextCall(op_155);
op_155(true, false);
