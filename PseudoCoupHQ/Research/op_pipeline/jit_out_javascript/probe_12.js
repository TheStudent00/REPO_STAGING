// probe 12 -- unary typeof
function op_12(a) {
    return typeof a;
}

%PrepareFunctionForOptimization(op_12);
op_12(1.0);
op_12(1.0);
%OptimizeFunctionOnNextCall(op_12);
op_12(1.0);
