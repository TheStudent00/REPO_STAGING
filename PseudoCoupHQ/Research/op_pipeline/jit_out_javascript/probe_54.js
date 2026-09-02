// probe 54 -- binary &&
function op_54(a, b) {
    return a && b;
}

%PrepareFunctionForOptimization(op_54);
op_54(true, 2.0);
op_54(true, 2.0);
%OptimizeFunctionOnNextCall(op_54);
op_54(true, 2.0);
