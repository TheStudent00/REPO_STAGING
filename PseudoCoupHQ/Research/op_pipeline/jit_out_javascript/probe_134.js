// probe 134 -- binary -
function op_134(a, b) {
    return a - b;
}

%PrepareFunctionForOptimization(op_134);
op_134(1.0, false);
op_134(1.0, false);
%OptimizeFunctionOnNextCall(op_134);
op_134(1.0, false);
