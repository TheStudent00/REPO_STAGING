// probe 146 -- binary *
function op_146(a, b) {
    return a * b;
}

%PrepareFunctionForOptimization(op_146);
op_146(true, false);
op_146(true, false);
%OptimizeFunctionOnNextCall(op_146);
op_146(true, false);
