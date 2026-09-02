// probe 183 -- binary <=
function op_183(a, b) {
    return a <= b;
}

%PrepareFunctionForOptimization(op_183);
op_183(1.0, 2.0);
op_183(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_183);
op_183(1.0, 2.0);
