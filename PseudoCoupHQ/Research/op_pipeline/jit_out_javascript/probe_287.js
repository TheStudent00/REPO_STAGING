// probe 287 -- binary satisfies
function op_287(a, b) {
    return a satisfies b;
}

%PrepareFunctionForOptimization(op_287);
op_287(1.0, false);
op_287(1.0, false);
%OptimizeFunctionOnNextCall(op_287);
op_287(1.0, false);
