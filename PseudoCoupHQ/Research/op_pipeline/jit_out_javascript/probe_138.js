// probe 138 -- binary *
function op_138(a, b) {
    return a * b;
}

%PrepareFunctionForOptimization(op_138);
op_138(1.0, 2.0);
op_138(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_138);
op_138(1.0, 2.0);
