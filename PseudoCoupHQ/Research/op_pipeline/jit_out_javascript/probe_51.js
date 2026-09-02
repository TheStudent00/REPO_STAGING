// probe 51 -- binary &&
function op_51(a, b) {
    return a && b;
}

%PrepareFunctionForOptimization(op_51);
op_51(1.0, 2.0);
op_51(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_51);
op_51(1.0, 2.0);
