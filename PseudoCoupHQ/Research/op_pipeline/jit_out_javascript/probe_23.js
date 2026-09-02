// probe 23 -- unary ++
function op_23(a) {
    return ++a;
}

%PrepareFunctionForOptimization(op_23);
op_23(true);
op_23(true);
%OptimizeFunctionOnNextCall(op_23);
op_23(true);
