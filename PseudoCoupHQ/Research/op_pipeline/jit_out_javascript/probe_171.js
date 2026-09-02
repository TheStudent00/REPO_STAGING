// probe 171 -- binary **
function op_171(a, b) {
    return a ** b;
}

%PrepareFunctionForOptimization(op_171);
op_171(true, 2.0);
op_171(true, 2.0);
%OptimizeFunctionOnNextCall(op_171);
op_171(true, 2.0);
