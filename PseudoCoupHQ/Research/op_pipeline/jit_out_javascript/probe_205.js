// probe 205 -- binary ===
function op_205(a, b) {
    return a === b;
}

%PrepareFunctionForOptimization(op_205);
op_205(1.0, 2.0);
op_205(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_205);
op_205(1.0, 2.0);
