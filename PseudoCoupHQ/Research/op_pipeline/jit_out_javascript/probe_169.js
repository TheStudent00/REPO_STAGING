// probe 169 -- binary **
function op_169(a, b) {
    return a ** b;
}

%PrepareFunctionForOptimization(op_169);
op_169(1.0, 2.0);
op_169(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_169);
op_169(1.0, 2.0);
