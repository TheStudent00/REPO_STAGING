// probe 111 -- binary |
function op_111(a, b) {
    return a | b;
}

%PrepareFunctionForOptimization(op_111);
op_111(1.0, 2.0);
op_111(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_111);
op_111(1.0, 2.0);
