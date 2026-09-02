// probe 230 -- binary >=
function op_230(a, b) {
    return a >= b;
}

%PrepareFunctionForOptimization(op_230);
op_230(1.0, false);
op_230(1.0, false);
%OptimizeFunctionOnNextCall(op_230);
op_230(1.0, false);
