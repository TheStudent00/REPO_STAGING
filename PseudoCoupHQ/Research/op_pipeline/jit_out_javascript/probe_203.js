// probe 203 -- binary ===
function op_203(a, b) {
    return a === b;
}

%PrepareFunctionForOptimization(op_203);
op_203(1.0, false);
op_203(1.0, false);
%OptimizeFunctionOnNextCall(op_203);
op_203(1.0, false);
