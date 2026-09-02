// probe 136 -- binary -
function op_136(a, b) {
    return a - b;
}

%PrepareFunctionForOptimization(op_136);
op_136(true, 2.0);
op_136(true, 2.0);
%OptimizeFunctionOnNextCall(op_136);
op_136(true, 2.0);
