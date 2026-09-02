// probe 227 -- binary !==
function op_227(a, b) {
    return a !== b;
}

%PrepareFunctionForOptimization(op_227);
op_227(true, false);
op_227(true, false);
%OptimizeFunctionOnNextCall(op_227);
op_227(true, false);
