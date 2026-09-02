// probe 16 -- unary void
function op_16(a) {
    return void a;
}

%PrepareFunctionForOptimization(op_16);
op_16(1.0);
op_16(1.0);
%OptimizeFunctionOnNextCall(op_16);
op_16(1.0);
