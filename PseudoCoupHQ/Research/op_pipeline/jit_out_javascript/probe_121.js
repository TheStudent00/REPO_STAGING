// probe 121 -- binary +
function op_121(a, b) {
    return a + b;
}

%PrepareFunctionForOptimization(op_121);
op_121(1.0, 2.0);
op_121(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_121);
op_121(1.0, 2.0);
