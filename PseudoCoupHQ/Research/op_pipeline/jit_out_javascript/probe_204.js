// probe 204 -- binary ===
function op_204(a, b) {
    return a === b;
}

%PrepareFunctionForOptimization(op_204);
op_204(1.0, 2.0);
op_204(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_204);
op_204(1.0, 2.0);
