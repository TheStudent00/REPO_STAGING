// probe 162 -- binary %
function op_162(a, b) {
    return a % b;
}

%PrepareFunctionForOptimization(op_162);
op_162(true, 2.0);
op_162(true, 2.0);
%OptimizeFunctionOnNextCall(op_162);
op_162(true, 2.0);
