// probe 232 -- binary >=
function op_232(a, b) {
    return a >= b;
}

%PrepareFunctionForOptimization(op_232);
op_232(1.0, 2.0);
op_232(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_232);
op_232(1.0, 2.0);
