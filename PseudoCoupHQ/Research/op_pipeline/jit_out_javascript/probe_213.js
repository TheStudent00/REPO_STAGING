// probe 213 -- binary !=
function op_213(a, b) {
    return a != b;
}

%PrepareFunctionForOptimization(op_213);
op_213(1.0, 2.0);
op_213(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_213);
op_213(1.0, 2.0);
