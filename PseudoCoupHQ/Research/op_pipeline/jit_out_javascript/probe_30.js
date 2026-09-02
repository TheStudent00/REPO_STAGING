// probe 30 -- unary new
function op_30(a) {
    return new a;
}

%PrepareFunctionForOptimization(op_30);
op_30(1.0);
op_30(1.0);
%OptimizeFunctionOnNextCall(op_30);
op_30(1.0);
