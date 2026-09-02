// probe 197 -- binary ==
function op_197(a, b) {
    return a == b;
}

%PrepareFunctionForOptimization(op_197);
op_197(1.0, false);
op_197(1.0, false);
%OptimizeFunctionOnNextCall(op_197);
op_197(1.0, false);
