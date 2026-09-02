// probe 284 -- binary satisfies
function op_284(a, b) {
    return a satisfies b;
}

%PrepareFunctionForOptimization(op_284);
op_284(1.0, false);
op_284(1.0, false);
%OptimizeFunctionOnNextCall(op_284);
op_284(1.0, false);
