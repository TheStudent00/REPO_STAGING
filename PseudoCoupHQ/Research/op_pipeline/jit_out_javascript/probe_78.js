// probe 78 -- binary >>>
function op_78(a, b) {
    return a >>> b;
}

%PrepareFunctionForOptimization(op_78);
op_78(1.0, 2.0);
op_78(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_78);
op_78(1.0, 2.0);
