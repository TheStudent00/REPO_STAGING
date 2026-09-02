// probe 270 -- binary in
function op_270(a, b) {
    return a in b;
}

%PrepareFunctionForOptimization(op_270);
op_270(true, 2.0);
op_270(true, 2.0);
%OptimizeFunctionOnNextCall(op_270);
op_270(true, 2.0);
