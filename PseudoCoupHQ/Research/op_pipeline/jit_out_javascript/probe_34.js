// probe 34 -- unary ...
function op_34(a) {
    return ...a;
}

%PrepareFunctionForOptimization(op_34);
op_34(1.0);
op_34(1.0);
%OptimizeFunctionOnNextCall(op_34);
op_34(1.0);
