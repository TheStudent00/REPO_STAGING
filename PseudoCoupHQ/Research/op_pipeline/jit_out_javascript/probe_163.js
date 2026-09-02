// probe 163 -- binary %
function op_163(a, b) {
    return a % b;
}

%PrepareFunctionForOptimization(op_163);
op_163(true, 2.0);
op_163(true, 2.0);
%OptimizeFunctionOnNextCall(op_163);
op_163(true, 2.0);
