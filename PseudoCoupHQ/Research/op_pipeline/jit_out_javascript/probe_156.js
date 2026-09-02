// probe 156 -- binary %
function op_156(a, b) {
    return a % b;
}

%PrepareFunctionForOptimization(op_156);
op_156(1.0, 2.0);
op_156(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_156);
op_156(1.0, 2.0);
