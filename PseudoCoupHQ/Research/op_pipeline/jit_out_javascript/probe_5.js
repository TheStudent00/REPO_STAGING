// probe 5 -- unary ~
function op_5(a) {
    return ~a;
}

%PrepareFunctionForOptimization(op_5);
op_5(true);
op_5(true);
%OptimizeFunctionOnNextCall(op_5);
op_5(true);
