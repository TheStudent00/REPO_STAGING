// probe 246 -- binary ??
function op_246(a, b) {
    return a ?? b;
}

%PrepareFunctionForOptimization(op_246);
op_246(1.0, 2.0);
op_246(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_246);
op_246(1.0, 2.0);
