// probe 215 -- binary !=
function op_215(a, b) {
    return a != b;
}

%PrepareFunctionForOptimization(op_215);
op_215(1.0, false);
op_215(1.0, false);
%OptimizeFunctionOnNextCall(op_215);
op_215(1.0, false);
