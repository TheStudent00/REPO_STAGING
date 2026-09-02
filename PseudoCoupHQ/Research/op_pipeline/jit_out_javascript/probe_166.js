// probe 166 -- binary **
function op_166(a, b) {
    return a ** b;
}

%PrepareFunctionForOptimization(op_166);
op_166(1.0, 2.0);
op_166(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_166);
op_166(1.0, 2.0);
