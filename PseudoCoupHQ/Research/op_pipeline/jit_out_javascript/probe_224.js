// probe 224 -- binary !==
function op_224(a, b) {
    return a !== b;
}

%PrepareFunctionForOptimization(op_224);
op_224(1.0, false);
op_224(1.0, false);
%OptimizeFunctionOnNextCall(op_224);
op_224(1.0, false);
