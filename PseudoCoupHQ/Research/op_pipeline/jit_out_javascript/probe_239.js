// probe 239 -- binary >
function op_239(a, b) {
    return a > b;
}

%PrepareFunctionForOptimization(op_239);
op_239(1.0, false);
op_239(1.0, false);
%OptimizeFunctionOnNextCall(op_239);
op_239(1.0, false);
