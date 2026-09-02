// probe 79 -- binary >>>
function op_79(a, b) {
    return a >>> b;
}

%PrepareFunctionForOptimization(op_79);
op_79(1.0, 2.0);
op_79(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_79);
op_79(1.0, 2.0);
