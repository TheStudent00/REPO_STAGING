// probe 21 -- unary ++
function op_21(a) {
    return ++a;
}

%PrepareFunctionForOptimization(op_21);
op_21(1.0);
op_21(1.0);
%OptimizeFunctionOnNextCall(op_21);
op_21(1.0);
