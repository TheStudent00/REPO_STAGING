// probe 56 -- binary &&
function op_56(a, b) {
    return a && b;
}

%PrepareFunctionForOptimization(op_56);
op_56(true, false);
op_56(true, false);
%OptimizeFunctionOnNextCall(op_56);
op_56(true, false);
