// probe 15 -- unary void
function op_15(a) {
    return void a;
}

%PrepareFunctionForOptimization(op_15);
op_15(1.0);
op_15(1.0);
%OptimizeFunctionOnNextCall(op_15);
op_15(1.0);
