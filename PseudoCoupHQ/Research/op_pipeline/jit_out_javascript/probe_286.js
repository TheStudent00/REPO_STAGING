// probe 286 -- binary satisfies
function op_286(a, b) {
    return a satisfies b;
}

%PrepareFunctionForOptimization(op_286);
op_286(1.0, 2.0);
op_286(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_286);
op_286(1.0, 2.0);
