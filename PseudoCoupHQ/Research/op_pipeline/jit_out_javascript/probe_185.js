// probe 185 -- binary <=
function op_185(a, b) {
    return a <= b;
}

%PrepareFunctionForOptimization(op_185);
op_185(1.0, false);
op_185(1.0, false);
%OptimizeFunctionOnNextCall(op_185);
op_185(1.0, false);
