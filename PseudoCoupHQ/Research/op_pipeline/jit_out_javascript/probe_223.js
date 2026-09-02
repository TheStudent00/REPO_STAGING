// probe 223 -- binary !==
function op_223(a, b) {
    return a !== b;
}

%PrepareFunctionForOptimization(op_223);
op_223(1.0, 2.0);
op_223(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_223);
op_223(1.0, 2.0);
