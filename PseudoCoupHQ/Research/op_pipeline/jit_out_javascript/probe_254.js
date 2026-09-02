// probe 254 -- binary ??
function op_254(a, b) {
    return a ?? b;
}

%PrepareFunctionForOptimization(op_254);
op_254(true, false);
op_254(true, false);
%OptimizeFunctionOnNextCall(op_254);
op_254(true, false);
