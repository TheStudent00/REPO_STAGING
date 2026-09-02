// probe 189 -- binary <=
function op_189(a, b) {
    return a <= b;
}

%PrepareFunctionForOptimization(op_189);
op_189(true, 2.0);
op_189(true, 2.0);
%OptimizeFunctionOnNextCall(op_189);
op_189(true, 2.0);
