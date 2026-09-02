// probe 7 -- unary -
function op_7(a) {
    return -a;
}

%PrepareFunctionForOptimization(op_7);
op_7(1.0);
op_7(1.0);
%OptimizeFunctionOnNextCall(op_7);
op_7(1.0);
