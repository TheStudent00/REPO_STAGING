// probe 20 -- unary delete
function op_20(a) {
    return delete a;
}

%PrepareFunctionForOptimization(op_20);
op_20(true);
op_20(true);
%OptimizeFunctionOnNextCall(op_20);
op_20(true);
