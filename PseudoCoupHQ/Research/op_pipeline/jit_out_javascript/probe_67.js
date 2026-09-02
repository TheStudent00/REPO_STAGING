// probe 67 -- binary >>
function op_67(a, b) {
    return a >> b;
}

%PrepareFunctionForOptimization(op_67);
op_67(1.0, 2.0);
op_67(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_67);
op_67(1.0, 2.0);
