// probe 137 -- binary -
function op_137(a, b) {
    return a - b;
}

%PrepareFunctionForOptimization(op_137);
op_137(true, false);
op_137(true, false);
%OptimizeFunctionOnNextCall(op_137);
op_137(true, false);
