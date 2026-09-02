// probe 31 -- unary new
function op_31(a) {
    return new a;
}

%PrepareFunctionForOptimization(op_31);
op_31(1.0);
op_31(1.0);
%OptimizeFunctionOnNextCall(op_31);
op_31(1.0);
