// probe 187 -- binary <=
function op_187(a, b) {
    return a <= b;
}

%PrepareFunctionForOptimization(op_187);
op_187(1.0, 2.0);
op_187(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_187);
op_187(1.0, 2.0);
