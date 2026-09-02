// probe 144 -- binary *
function op_144(a, b) {
    return a * b;
}

%PrepareFunctionForOptimization(op_144);
op_144(true, 2.0);
op_144(true, 2.0);
%OptimizeFunctionOnNextCall(op_144);
op_144(true, 2.0);
