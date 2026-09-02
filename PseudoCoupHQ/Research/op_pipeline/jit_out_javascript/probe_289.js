// probe 289 -- binary satisfies
function op_289(a, b) {
    return a satisfies b;
}

%PrepareFunctionForOptimization(op_289);
op_289(true, 2.0);
op_289(true, 2.0);
%OptimizeFunctionOnNextCall(op_289);
op_289(true, 2.0);
