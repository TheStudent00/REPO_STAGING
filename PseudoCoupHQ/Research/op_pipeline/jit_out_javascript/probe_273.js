// probe 273 -- binary as
function op_273(a, b) {
    return a as b;
}

%PrepareFunctionForOptimization(op_273);
op_273(1.0, 2.0);
op_273(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_273);
op_273(1.0, 2.0);
