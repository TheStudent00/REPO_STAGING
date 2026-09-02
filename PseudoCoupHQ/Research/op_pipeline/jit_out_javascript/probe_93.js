// probe 93 -- binary &
function op_93(a, b) {
    return a & b;
}

%PrepareFunctionForOptimization(op_93);
op_93(1.0, 2.0);
op_93(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_93);
op_93(1.0, 2.0);
