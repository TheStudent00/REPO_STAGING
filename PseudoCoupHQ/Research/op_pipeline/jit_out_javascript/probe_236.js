// probe 236 -- binary >=
function op_236(a, b) {
    return a >= b;
}

%PrepareFunctionForOptimization(op_236);
op_236(true, false);
op_236(true, false);
%OptimizeFunctionOnNextCall(op_236);
op_236(true, false);
