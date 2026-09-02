// probe 228 -- binary >=
function op_228(a, b) {
    return a >= b;
}

%PrepareFunctionForOptimization(op_228);
op_228(1.0, 2.0);
op_228(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_228);
op_228(1.0, 2.0);
