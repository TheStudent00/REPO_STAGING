// probe 27 -- unary await
function op_27(a) {
    return await a;
}

%PrepareFunctionForOptimization(op_27);
op_27(1.0);
op_27(1.0);
%OptimizeFunctionOnNextCall(op_27);
op_27(1.0);
