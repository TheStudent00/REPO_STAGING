// probe 280 -- binary as
function op_280(a, b) {
    return a as b;
}

%PrepareFunctionForOptimization(op_280);
op_280(true, 2.0);
op_280(true, 2.0);
%OptimizeFunctionOnNextCall(op_280);
op_280(true, 2.0);
