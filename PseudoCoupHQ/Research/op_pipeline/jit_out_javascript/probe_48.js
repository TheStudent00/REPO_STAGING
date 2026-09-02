// probe 48 -- binary &&
function op_48(a, b) {
    return a && b;
}

%PrepareFunctionForOptimization(op_48);
op_48(1.0, 2.0);
op_48(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_48);
op_48(1.0, 2.0);
