// probe 262 -- binary instanceof
function op_262(a, b) {
    return a instanceof b;
}

%PrepareFunctionForOptimization(op_262);
op_262(true, 2.0);
op_262(true, 2.0);
%OptimizeFunctionOnNextCall(op_262);
op_262(true, 2.0);
