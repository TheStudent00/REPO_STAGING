// probe 53 -- binary &&
function op_53(a, b) {
    return a && b;
}

%PrepareFunctionForOptimization(op_53);
op_53(1.0, false);
op_53(1.0, false);
%OptimizeFunctionOnNextCall(op_53);
op_53(1.0, false);
