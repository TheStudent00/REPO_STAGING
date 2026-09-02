// probe 29 -- unary await
function op_29(a) {
    return await a;
}

%PrepareFunctionForOptimization(op_29);
op_29(true);
op_29(true);
%OptimizeFunctionOnNextCall(op_29);
op_29(true);
