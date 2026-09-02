// probe 11 -- unary +
function op_11(a) {
    return +a;
}

%PrepareFunctionForOptimization(op_11);
op_11(true);
op_11(true);
%OptimizeFunctionOnNextCall(op_11);
op_11(true);
