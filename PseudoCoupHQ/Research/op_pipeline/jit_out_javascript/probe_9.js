// probe 9 -- unary +
function op_9(a) {
    return +a;
}

%PrepareFunctionForOptimization(op_9);
op_9(1.0);
op_9(1.0);
%OptimizeFunctionOnNextCall(op_9);
op_9(1.0);
