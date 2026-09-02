// probe 196 -- binary ==
function op_196(a, b) {
    return a == b;
}

%PrepareFunctionForOptimization(op_196);
op_196(1.0, 2.0);
op_196(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_196);
op_196(1.0, 2.0);
