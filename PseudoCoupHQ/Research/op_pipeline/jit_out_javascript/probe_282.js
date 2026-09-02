// probe 282 -- binary satisfies
function op_282(a, b) {
    return a satisfies b;
}

%PrepareFunctionForOptimization(op_282);
op_282(1.0, 2.0);
op_282(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_282);
op_282(1.0, 2.0);
