// probe 257 -- binary instanceof
function op_257(a, b) {
    return a instanceof b;
}

%PrepareFunctionForOptimization(op_257);
op_257(1.0, false);
op_257(1.0, false);
%OptimizeFunctionOnNextCall(op_257);
op_257(1.0, false);
