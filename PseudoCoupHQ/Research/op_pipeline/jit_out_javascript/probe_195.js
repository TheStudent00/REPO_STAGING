// probe 195 -- binary ==
function op_195(a, b) {
    return a == b;
}

%PrepareFunctionForOptimization(op_195);
op_195(1.0, 2.0);
op_195(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_195);
op_195(1.0, 2.0);
