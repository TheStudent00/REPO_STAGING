// probe 37 -- unary <T>x
function op_37(a) {
    return <T>x a;
}

%PrepareFunctionForOptimization(op_37);
op_37(1.0);
op_37(1.0);
%OptimizeFunctionOnNextCall(op_37);
op_37(1.0);
