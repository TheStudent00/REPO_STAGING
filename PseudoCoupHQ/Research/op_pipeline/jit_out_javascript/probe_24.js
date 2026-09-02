// probe 24 -- unary --
function op_24(a) {
    return --a;
}

%PrepareFunctionForOptimization(op_24);
op_24(1.0);
op_24(1.0);
%OptimizeFunctionOnNextCall(op_24);
op_24(1.0);
