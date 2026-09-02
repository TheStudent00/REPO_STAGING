// probe 19 -- unary delete
function op_19(a) {
    return delete a;
}

%PrepareFunctionForOptimization(op_19);
op_19(1.0);
op_19(1.0);
%OptimizeFunctionOnNextCall(op_19);
op_19(1.0);
