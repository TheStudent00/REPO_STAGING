// probe 202 -- binary ===
function op_202(a, b) {
    return a === b;
}

%PrepareFunctionForOptimization(op_202);
op_202(1.0, 2.0);
op_202(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_202);
op_202(1.0, 2.0);
