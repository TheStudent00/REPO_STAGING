// probe 49 -- binary &&
function op_49(a, b) {
    return a && b;
}

%PrepareFunctionForOptimization(op_49);
op_49(1.0, 2.0);
op_49(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_49);
op_49(1.0, 2.0);
