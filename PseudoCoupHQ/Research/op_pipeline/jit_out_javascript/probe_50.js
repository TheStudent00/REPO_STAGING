// probe 50 -- binary &&
function op_50(a, b) {
    return a && b;
}

%PrepareFunctionForOptimization(op_50);
op_50(1.0, false);
op_50(1.0, false);
%OptimizeFunctionOnNextCall(op_50);
op_50(1.0, false);
