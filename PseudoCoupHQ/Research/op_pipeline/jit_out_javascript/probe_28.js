// probe 28 -- unary await
function op_28(a) {
    return await a;
}

%PrepareFunctionForOptimization(op_28);
op_28(1.0);
op_28(1.0);
%OptimizeFunctionOnNextCall(op_28);
op_28(1.0);
