// probe 221 -- binary !==
function op_221(a, b) {
    return a !== b;
}

%PrepareFunctionForOptimization(op_221);
op_221(1.0, false);
op_221(1.0, false);
%OptimizeFunctionOnNextCall(op_221);
op_221(1.0, false);
