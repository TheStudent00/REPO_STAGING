// probe 128 -- binary +
function op_128(a, b) {
    return a + b;
}

%PrepareFunctionForOptimization(op_128);
op_128(true, false);
op_128(true, false);
%OptimizeFunctionOnNextCall(op_128);
op_128(true, false);
