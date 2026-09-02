// probe 209 -- binary ===
function op_209(a, b) {
    return a === b;
}

%PrepareFunctionForOptimization(op_209);
op_209(true, false);
op_209(true, false);
%OptimizeFunctionOnNextCall(op_209);
op_209(true, false);
