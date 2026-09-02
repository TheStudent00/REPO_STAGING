// probe 145 -- binary *
function op_145(a, b) {
    return a * b;
}

%PrepareFunctionForOptimization(op_145);
op_145(true, 2.0);
op_145(true, 2.0);
%OptimizeFunctionOnNextCall(op_145);
op_145(true, 2.0);
