// probe 77 -- binary >>>
function op_77(a, b) {
    return a >>> b;
}

%PrepareFunctionForOptimization(op_77);
op_77(1.0, false);
op_77(1.0, false);
%OptimizeFunctionOnNextCall(op_77);
op_77(1.0, false);
