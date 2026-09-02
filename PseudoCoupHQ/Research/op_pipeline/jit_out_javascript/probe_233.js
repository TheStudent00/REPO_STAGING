// probe 233 -- binary >=
function op_233(a, b) {
    return a >= b;
}

%PrepareFunctionForOptimization(op_233);
op_233(1.0, false);
op_233(1.0, false);
%OptimizeFunctionOnNextCall(op_233);
op_233(1.0, false);
