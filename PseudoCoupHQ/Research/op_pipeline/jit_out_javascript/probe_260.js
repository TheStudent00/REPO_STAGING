// probe 260 -- binary instanceof
function op_260(a, b) {
    return a instanceof b;
}

%PrepareFunctionForOptimization(op_260);
op_260(1.0, false);
op_260(1.0, false);
%OptimizeFunctionOnNextCall(op_260);
op_260(1.0, false);
