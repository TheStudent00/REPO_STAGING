// probe 217 -- binary !=
function op_217(a, b) {
    return a != b;
}

%PrepareFunctionForOptimization(op_217);
op_217(true, 2.0);
op_217(true, 2.0);
%OptimizeFunctionOnNextCall(op_217);
op_217(true, 2.0);
