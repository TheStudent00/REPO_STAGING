// probe 76 -- binary >>>
function op_76(a, b) {
    return a >>> b;
}

%PrepareFunctionForOptimization(op_76);
op_76(1.0, 2.0);
op_76(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_76);
op_76(1.0, 2.0);
