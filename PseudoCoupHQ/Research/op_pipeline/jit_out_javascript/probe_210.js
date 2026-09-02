// probe 210 -- binary !=
function op_210(a, b) {
    return a != b;
}

%PrepareFunctionForOptimization(op_210);
op_210(1.0, 2.0);
op_210(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_210);
op_210(1.0, 2.0);
