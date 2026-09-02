// probe 42 -- unary --
function op_42(a) {
    return a--;
}

%PrepareFunctionForOptimization(op_42);
op_42(1.0);
op_42(1.0);
%OptimizeFunctionOnNextCall(op_42);
op_42(1.0);
