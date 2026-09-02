// probe 62 -- binary ||
function op_62(a, b) {
    return a || b;
}

%PrepareFunctionForOptimization(op_62);
op_62(1.0, false);
op_62(1.0, false);
%OptimizeFunctionOnNextCall(op_62);
op_62(1.0, false);
