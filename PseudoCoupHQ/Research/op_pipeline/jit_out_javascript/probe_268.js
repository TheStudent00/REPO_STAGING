// probe 268 -- binary in
function op_268(a, b) {
    return a in b;
}

%PrepareFunctionForOptimization(op_268);
op_268(1.0, 2.0);
op_268(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_268);
op_268(1.0, 2.0);
