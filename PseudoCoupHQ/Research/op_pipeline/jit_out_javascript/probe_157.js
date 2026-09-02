// probe 157 -- binary %
function op_157(a, b) {
    return a % b;
}

%PrepareFunctionForOptimization(op_157);
op_157(1.0, 2.0);
op_157(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_157);
op_157(1.0, 2.0);
