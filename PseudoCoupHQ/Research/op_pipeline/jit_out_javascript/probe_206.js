// probe 206 -- binary ===
function op_206(a, b) {
    return a === b;
}

%PrepareFunctionForOptimization(op_206);
op_206(1.0, false);
op_206(1.0, false);
%OptimizeFunctionOnNextCall(op_206);
op_206(1.0, false);
