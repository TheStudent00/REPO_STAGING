// probe 148 -- binary /
function op_148(a, b) {
    return a / b;
}

%PrepareFunctionForOptimization(op_148);
op_148(1.0, 2.0);
op_148(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_148);
op_148(1.0, 2.0);
