// probe 0 -- unary !
function op_0(a) {
    return !a;
}

%PrepareFunctionForOptimization(op_0);
op_0(1.0);
op_0(1.0);
%OptimizeFunctionOnNextCall(op_0);
op_0(1.0);
