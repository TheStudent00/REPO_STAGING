// probe 139 -- binary *
function op_139(a, b) {
    return a * b;
}

%PrepareFunctionForOptimization(op_139);
op_139(1.0, 2.0);
op_139(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_139);
op_139(1.0, 2.0);
