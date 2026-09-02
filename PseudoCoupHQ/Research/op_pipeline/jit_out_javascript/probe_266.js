// probe 266 -- binary in
function op_266(a, b) {
    return a in b;
}

%PrepareFunctionForOptimization(op_266);
op_266(1.0, false);
op_266(1.0, false);
%OptimizeFunctionOnNextCall(op_266);
op_266(1.0, false);
