// probe 248 -- binary ??
function op_248(a, b) {
    return a ?? b;
}

%PrepareFunctionForOptimization(op_248);
op_248(1.0, false);
op_248(1.0, false);
%OptimizeFunctionOnNextCall(op_248);
op_248(1.0, false);
