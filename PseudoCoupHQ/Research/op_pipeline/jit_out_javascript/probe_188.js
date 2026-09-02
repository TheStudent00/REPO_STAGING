// probe 188 -- binary <=
function op_188(a, b) {
    return a <= b;
}

%PrepareFunctionForOptimization(op_188);
op_188(1.0, false);
op_188(1.0, false);
%OptimizeFunctionOnNextCall(op_188);
op_188(1.0, false);
