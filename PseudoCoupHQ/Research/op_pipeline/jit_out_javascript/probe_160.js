// probe 160 -- binary %
function op_160(a, b) {
    return a % b;
}

%PrepareFunctionForOptimization(op_160);
op_160(1.0, 2.0);
op_160(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_160);
op_160(1.0, 2.0);
