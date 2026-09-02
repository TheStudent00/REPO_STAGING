// probe 135 -- binary -
function op_135(a, b) {
    return a - b;
}

%PrepareFunctionForOptimization(op_135);
op_135(true, 2.0);
op_135(true, 2.0);
%OptimizeFunctionOnNextCall(op_135);
op_135(true, 2.0);
