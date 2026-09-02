// probe 36 -- unary <T>x
function op_36(a) {
    return <T>x a;
}

%PrepareFunctionForOptimization(op_36);
op_36(1.0);
op_36(1.0);
%OptimizeFunctionOnNextCall(op_36);
op_36(1.0);
