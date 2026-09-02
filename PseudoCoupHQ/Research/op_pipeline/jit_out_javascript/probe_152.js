// probe 152 -- binary /
function op_152(a, b) {
    return a / b;
}

%PrepareFunctionForOptimization(op_152);
op_152(1.0, false);
op_152(1.0, false);
%OptimizeFunctionOnNextCall(op_152);
op_152(1.0, false);
