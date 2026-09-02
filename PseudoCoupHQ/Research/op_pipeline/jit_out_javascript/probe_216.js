// probe 216 -- binary !=
function op_216(a, b) {
    return a != b;
}

%PrepareFunctionForOptimization(op_216);
op_216(true, 2.0);
op_216(true, 2.0);
%OptimizeFunctionOnNextCall(op_216);
op_216(true, 2.0);
