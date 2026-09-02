// probe 3 -- unary ~
function op_3(a) {
    return ~a;
}

%PrepareFunctionForOptimization(op_3);
op_3(1.0);
op_3(1.0);
%OptimizeFunctionOnNextCall(op_3);
op_3(1.0);
