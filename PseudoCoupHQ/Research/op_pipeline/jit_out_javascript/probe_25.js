// probe 25 -- unary --
function op_25(a) {
    return --a;
}

%PrepareFunctionForOptimization(op_25);
op_25(1.0);
op_25(1.0);
%OptimizeFunctionOnNextCall(op_25);
op_25(1.0);
