// probe 285 -- binary satisfies
function op_285(a, b) {
    return a satisfies b;
}

%PrepareFunctionForOptimization(op_285);
op_285(1.0, 2.0);
op_285(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_285);
op_285(1.0, 2.0);
