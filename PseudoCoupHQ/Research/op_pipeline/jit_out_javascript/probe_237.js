// probe 237 -- binary >
function op_237(a, b) {
    return a > b;
}

%PrepareFunctionForOptimization(op_237);
op_237(1.0, 2.0);
op_237(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_237);
op_237(1.0, 2.0);
