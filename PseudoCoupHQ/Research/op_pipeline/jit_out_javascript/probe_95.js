// probe 95 -- binary &
function op_95(a, b) {
    return a & b;
}

%PrepareFunctionForOptimization(op_95);
op_95(1.0, false);
op_95(1.0, false);
%OptimizeFunctionOnNextCall(op_95);
op_95(1.0, false);
