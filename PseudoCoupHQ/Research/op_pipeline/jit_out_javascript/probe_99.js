// probe 99 -- binary &
function op_99(a, b) {
    return a & b;
}

%PrepareFunctionForOptimization(op_99);
op_99(true, 2.0);
op_99(true, 2.0);
%OptimizeFunctionOnNextCall(op_99);
op_99(true, 2.0);
