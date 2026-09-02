// probe 283 -- binary satisfies
function op_283(a, b) {
    return a satisfies b;
}

%PrepareFunctionForOptimization(op_283);
op_283(1.0, 2.0);
op_283(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_283);
op_283(1.0, 2.0);
