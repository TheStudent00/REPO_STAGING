// probe 80 -- binary >>>
function op_80(a, b) {
    return a >>> b;
}

%PrepareFunctionForOptimization(op_80);
op_80(1.0, false);
op_80(1.0, false);
%OptimizeFunctionOnNextCall(op_80);
op_80(1.0, false);
