// probe 208 -- binary ===
function op_208(a, b) {
    return a === b;
}

%PrepareFunctionForOptimization(op_208);
op_208(true, 2.0);
op_208(true, 2.0);
%OptimizeFunctionOnNextCall(op_208);
op_208(true, 2.0);
