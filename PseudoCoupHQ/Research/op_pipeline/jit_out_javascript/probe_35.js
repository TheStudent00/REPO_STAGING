// probe 35 -- unary ...
function op_35(a) {
    return ...a;
}

%PrepareFunctionForOptimization(op_35);
op_35(true);
op_35(true);
%OptimizeFunctionOnNextCall(op_35);
op_35(true);
