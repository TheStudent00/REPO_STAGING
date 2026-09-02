// probe 290 -- binary satisfies
function op_290(a, b) {
    return a satisfies b;
}

%PrepareFunctionForOptimization(op_290);
op_290(true, false);
op_290(true, false);
%OptimizeFunctionOnNextCall(op_290);
op_290(true, false);
