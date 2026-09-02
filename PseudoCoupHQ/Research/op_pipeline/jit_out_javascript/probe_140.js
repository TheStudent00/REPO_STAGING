// probe 140 -- binary *
function op_140(a, b) {
    return a * b;
}

%PrepareFunctionForOptimization(op_140);
op_140(1.0, false);
op_140(1.0, false);
%OptimizeFunctionOnNextCall(op_140);
op_140(1.0, false);
