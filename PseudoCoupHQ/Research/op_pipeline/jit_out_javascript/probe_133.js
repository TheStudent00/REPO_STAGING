// probe 133 -- binary -
function op_133(a, b) {
    return a - b;
}

%PrepareFunctionForOptimization(op_133);
op_133(1.0, 2.0);
op_133(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_133);
op_133(1.0, 2.0);
