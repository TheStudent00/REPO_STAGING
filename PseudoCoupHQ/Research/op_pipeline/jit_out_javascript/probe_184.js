// probe 184 -- binary <=
function op_184(a, b) {
    return a <= b;
}

%PrepareFunctionForOptimization(op_184);
op_184(1.0, 2.0);
op_184(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_184);
op_184(1.0, 2.0);
