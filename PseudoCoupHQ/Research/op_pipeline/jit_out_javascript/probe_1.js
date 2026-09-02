// probe 1 -- unary !
function op_1(a) {
    return !a;
}

%PrepareFunctionForOptimization(op_1);
op_1(1.0);
op_1(1.0);
%OptimizeFunctionOnNextCall(op_1);
op_1(1.0);
