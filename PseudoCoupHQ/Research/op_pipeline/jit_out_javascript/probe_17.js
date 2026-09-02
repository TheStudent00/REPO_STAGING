// probe 17 -- unary void
function op_17(a) {
    return void a;
}

%PrepareFunctionForOptimization(op_17);
op_17(true);
op_17(true);
%OptimizeFunctionOnNextCall(op_17);
op_17(true);
