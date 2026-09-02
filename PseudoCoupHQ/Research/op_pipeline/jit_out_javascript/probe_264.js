// probe 264 -- binary in
function op_264(a, b) {
    return a in b;
}

%PrepareFunctionForOptimization(op_264);
op_264(1.0, 2.0);
op_264(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_264);
op_264(1.0, 2.0);
