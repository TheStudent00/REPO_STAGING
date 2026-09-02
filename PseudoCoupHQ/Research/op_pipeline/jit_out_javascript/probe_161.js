// probe 161 -- binary %
function op_161(a, b) {
    return a % b;
}

%PrepareFunctionForOptimization(op_161);
op_161(1.0, false);
op_161(1.0, false);
%OptimizeFunctionOnNextCall(op_161);
op_161(1.0, false);
