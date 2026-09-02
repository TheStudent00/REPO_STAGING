// probe 8 -- unary -
function op_8(a) {
    return -a;
}

%PrepareFunctionForOptimization(op_8);
op_8(true);
op_8(true);
%OptimizeFunctionOnNextCall(op_8);
op_8(true);
