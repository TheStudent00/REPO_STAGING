// probe 168 -- binary **
function op_168(a, b) {
    return a ** b;
}

%PrepareFunctionForOptimization(op_168);
op_168(1.0, 2.0);
op_168(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_168);
op_168(1.0, 2.0);
