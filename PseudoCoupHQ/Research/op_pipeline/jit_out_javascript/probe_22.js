// probe 22 -- unary ++
function op_22(a) {
    return ++a;
}

%PrepareFunctionForOptimization(op_22);
op_22(1.0);
op_22(1.0);
%OptimizeFunctionOnNextCall(op_22);
op_22(1.0);
