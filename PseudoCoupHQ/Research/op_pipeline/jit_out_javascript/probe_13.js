// probe 13 -- unary typeof
function op_13(a) {
    return typeof a;
}

%PrepareFunctionForOptimization(op_13);
op_13(1.0);
op_13(1.0);
%OptimizeFunctionOnNextCall(op_13);
op_13(1.0);
