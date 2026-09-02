// probe 14 -- unary typeof
function op_14(a) {
    return typeof a;
}

%PrepareFunctionForOptimization(op_14);
op_14(true);
op_14(true);
%OptimizeFunctionOnNextCall(op_14);
op_14(true);
