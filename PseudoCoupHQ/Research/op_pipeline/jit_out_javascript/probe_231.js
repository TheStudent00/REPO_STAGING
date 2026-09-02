// probe 231 -- binary >=
function op_231(a, b) {
    return a >= b;
}

%PrepareFunctionForOptimization(op_231);
op_231(1.0, 2.0);
op_231(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_231);
op_231(1.0, 2.0);
