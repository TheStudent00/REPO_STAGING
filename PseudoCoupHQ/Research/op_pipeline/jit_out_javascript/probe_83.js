// probe 83 -- binary >>>
function op_83(a, b) {
    return a >>> b;
}

%PrepareFunctionForOptimization(op_83);
op_83(true, false);
op_83(true, false);
%OptimizeFunctionOnNextCall(op_83);
op_83(true, false);
