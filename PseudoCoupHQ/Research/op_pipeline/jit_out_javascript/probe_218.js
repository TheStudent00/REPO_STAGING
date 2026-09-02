// probe 218 -- binary !=
function op_218(a, b) {
    return a != b;
}

%PrepareFunctionForOptimization(op_218);
op_218(true, false);
op_218(true, false);
%OptimizeFunctionOnNextCall(op_218);
op_218(true, false);
