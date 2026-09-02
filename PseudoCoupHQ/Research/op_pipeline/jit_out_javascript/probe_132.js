// probe 132 -- binary -
function op_132(a, b) {
    return a - b;
}

%PrepareFunctionForOptimization(op_132);
op_132(1.0, 2.0);
op_132(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_132);
op_132(1.0, 2.0);
