// probe 75 -- binary >>>
function op_75(a, b) {
    return a >>> b;
}

%PrepareFunctionForOptimization(op_75);
op_75(1.0, 2.0);
op_75(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_75);
op_75(1.0, 2.0);
