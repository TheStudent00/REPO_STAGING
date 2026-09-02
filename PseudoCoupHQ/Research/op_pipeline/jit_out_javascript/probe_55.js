// probe 55 -- binary &&
function op_55(a, b) {
    return a && b;
}

%PrepareFunctionForOptimization(op_55);
op_55(true, 2.0);
op_55(true, 2.0);
%OptimizeFunctionOnNextCall(op_55);
op_55(true, 2.0);
