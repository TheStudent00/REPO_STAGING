// probe 129 -- binary -
function op_129(a, b) {
    return a - b;
}

%PrepareFunctionForOptimization(op_129);
op_129(1.0, 2.0);
op_129(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_129);
op_129(1.0, 2.0);
