// probe 245 -- binary >
function op_245(a, b) {
    return a > b;
}

%PrepareFunctionForOptimization(op_245);
op_245(true, false);
op_245(true, false);
%OptimizeFunctionOnNextCall(op_245);
op_245(true, false);
