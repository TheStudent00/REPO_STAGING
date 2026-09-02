// probe 33 -- unary ...
function op_33(a) {
    return ...a;
}

%PrepareFunctionForOptimization(op_33);
op_33(1.0);
op_33(1.0);
%OptimizeFunctionOnNextCall(op_33);
op_33(1.0);
