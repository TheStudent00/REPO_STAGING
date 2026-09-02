// probe 158 -- binary %
function op_158(a, b) {
    return a % b;
}

%PrepareFunctionForOptimization(op_158);
op_158(1.0, false);
op_158(1.0, false);
%OptimizeFunctionOnNextCall(op_158);
op_158(1.0, false);
