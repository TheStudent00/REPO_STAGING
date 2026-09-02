// probe 193 -- binary ==
function op_193(a, b) {
    return a == b;
}

%PrepareFunctionForOptimization(op_193);
op_193(1.0, 2.0);
op_193(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_193);
op_193(1.0, 2.0);
