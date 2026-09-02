// probe 85 -- binary <<
function op_85(a, b) {
    return a << b;
}

%PrepareFunctionForOptimization(op_85);
op_85(1.0, 2.0);
op_85(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_85);
op_85(1.0, 2.0);
