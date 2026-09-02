// probe 252 -- binary ??
function op_252(a, b) {
    return a ?? b;
}

%PrepareFunctionForOptimization(op_252);
op_252(true, 2.0);
op_252(true, 2.0);
%OptimizeFunctionOnNextCall(op_252);
op_252(true, 2.0);
