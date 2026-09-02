// probe 198 -- binary ==
function op_198(a, b) {
    return a == b;
}

%PrepareFunctionForOptimization(op_198);
op_198(true, 2.0);
op_198(true, 2.0);
%OptimizeFunctionOnNextCall(op_198);
op_198(true, 2.0);
