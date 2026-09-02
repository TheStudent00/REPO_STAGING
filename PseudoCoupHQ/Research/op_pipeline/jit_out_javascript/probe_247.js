// probe 247 -- binary ??
function op_247(a, b) {
    return a ?? b;
}

%PrepareFunctionForOptimization(op_247);
op_247(1.0, 2.0);
op_247(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_247);
op_247(1.0, 2.0);
