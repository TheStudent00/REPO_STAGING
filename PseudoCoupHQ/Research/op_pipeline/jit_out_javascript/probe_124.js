// probe 124 -- binary +
function op_124(a, b) {
    return a + b;
}

%PrepareFunctionForOptimization(op_124);
op_124(1.0, 2.0);
op_124(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_124);
op_124(1.0, 2.0);
