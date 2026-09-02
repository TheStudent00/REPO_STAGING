// probe 192 -- binary ==
function op_192(a, b) {
    return a == b;
}

%PrepareFunctionForOptimization(op_192);
op_192(1.0, 2.0);
op_192(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_192);
op_192(1.0, 2.0);
