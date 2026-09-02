// probe 194 -- binary ==
function op_194(a, b) {
    return a == b;
}

%PrepareFunctionForOptimization(op_194);
op_194(1.0, false);
op_194(1.0, false);
%OptimizeFunctionOnNextCall(op_194);
op_194(1.0, false);
