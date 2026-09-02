// probe 38 -- unary <T>x
function op_38(a) {
    return <T>x a;
}

%PrepareFunctionForOptimization(op_38);
op_38(true);
op_38(true);
%OptimizeFunctionOnNextCall(op_38);
op_38(true);
