// probe 190 -- binary <=
function op_190(a, b) {
    return a <= b;
}

%PrepareFunctionForOptimization(op_190);
op_190(true, 2.0);
op_190(true, 2.0);
%OptimizeFunctionOnNextCall(op_190);
op_190(true, 2.0);
