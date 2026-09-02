// probe 130 -- binary -
function op_130(a, b) {
    return a - b;
}

%PrepareFunctionForOptimization(op_130);
op_130(1.0, 2.0);
op_130(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_130);
op_130(1.0, 2.0);
