// probe 59 -- binary ||
function op_59(a, b) {
    return a || b;
}

%PrepareFunctionForOptimization(op_59);
op_59(1.0, false);
op_59(1.0, false);
%OptimizeFunctionOnNextCall(op_59);
op_59(1.0, false);
