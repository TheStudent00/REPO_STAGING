// probe 214 -- binary !=
function op_214(a, b) {
    return a != b;
}

%PrepareFunctionForOptimization(op_214);
op_214(1.0, 2.0);
op_214(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_214);
op_214(1.0, 2.0);
