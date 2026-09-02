// probe 82 -- binary >>>
function op_82(a, b) {
    return a >>> b;
}

%PrepareFunctionForOptimization(op_82);
op_82(true, 2.0);
op_82(true, 2.0);
%OptimizeFunctionOnNextCall(op_82);
op_82(true, 2.0);
