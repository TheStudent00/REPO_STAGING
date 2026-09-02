// probe 4 -- unary ~
function op_4(a) {
    return ~a;
}

%PrepareFunctionForOptimization(op_4);
op_4(1.0);
op_4(1.0);
%OptimizeFunctionOnNextCall(op_4);
op_4(1.0);
