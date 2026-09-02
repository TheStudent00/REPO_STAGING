// probe 32 -- unary new
function op_32(a) {
    return new a;
}

%PrepareFunctionForOptimization(op_32);
op_32(true);
op_32(true);
%OptimizeFunctionOnNextCall(op_32);
op_32(true);
