// probe 164 -- binary %
function op_164(a, b) {
    return a % b;
}

%PrepareFunctionForOptimization(op_164);
op_164(true, false);
op_164(true, false);
%OptimizeFunctionOnNextCall(op_164);
op_164(true, false);
