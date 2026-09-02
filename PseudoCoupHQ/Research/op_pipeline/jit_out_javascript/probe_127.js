// probe 127 -- binary +
function op_127(a, b) {
    return a + b;
}

%PrepareFunctionForOptimization(op_127);
op_127(true, 2.0);
op_127(true, 2.0);
%OptimizeFunctionOnNextCall(op_127);
op_127(true, 2.0);
