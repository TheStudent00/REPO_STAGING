// probe 126 -- binary +
function op_126(a, b) {
    return a + b;
}

%PrepareFunctionForOptimization(op_126);
op_126(true, 2.0);
op_126(true, 2.0);
%OptimizeFunctionOnNextCall(op_126);
op_126(true, 2.0);
