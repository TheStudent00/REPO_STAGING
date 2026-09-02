// probe 207 -- binary ===
function op_207(a, b) {
    return a === b;
}

%PrepareFunctionForOptimization(op_207);
op_207(true, 2.0);
op_207(true, 2.0);
%OptimizeFunctionOnNextCall(op_207);
op_207(true, 2.0);
