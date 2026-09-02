// probe 170 -- binary **
function op_170(a, b) {
    return a ** b;
}

%PrepareFunctionForOptimization(op_170);
op_170(1.0, false);
op_170(1.0, false);
%OptimizeFunctionOnNextCall(op_170);
op_170(1.0, false);
