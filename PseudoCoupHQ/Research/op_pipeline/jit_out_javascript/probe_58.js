// probe 58 -- binary ||
function op_58(a, b) {
    return a || b;
}

%PrepareFunctionForOptimization(op_58);
op_58(1.0, 2.0);
op_58(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_58);
op_58(1.0, 2.0);
