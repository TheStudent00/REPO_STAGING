// probe 10 -- unary +
function op_10(a) {
    return +a;
}

%PrepareFunctionForOptimization(op_10);
op_10(1.0);
op_10(1.0);
%OptimizeFunctionOnNextCall(op_10);
op_10(1.0);
