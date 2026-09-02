// probe 6 -- unary -
function op_6(a) {
    return -a;
}

%PrepareFunctionForOptimization(op_6);
op_6(1.0);
op_6(1.0);
%OptimizeFunctionOnNextCall(op_6);
op_6(1.0);
