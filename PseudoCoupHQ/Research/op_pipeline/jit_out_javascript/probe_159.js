// probe 159 -- binary %
function op_159(a, b) {
    return a % b;
}

%PrepareFunctionForOptimization(op_159);
op_159(1.0, 2.0);
op_159(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_159);
op_159(1.0, 2.0);
