// probe 274 -- binary as
function op_274(a, b) {
    return a as b;
}

%PrepareFunctionForOptimization(op_274);
op_274(1.0, 2.0);
op_274(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_274);
op_274(1.0, 2.0);
