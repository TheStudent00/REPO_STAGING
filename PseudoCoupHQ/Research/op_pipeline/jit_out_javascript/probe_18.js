// probe 18 -- unary delete
function op_18(a) {
    return delete a;
}

%PrepareFunctionForOptimization(op_18);
op_18(1.0);
op_18(1.0);
%OptimizeFunctionOnNextCall(op_18);
op_18(1.0);
