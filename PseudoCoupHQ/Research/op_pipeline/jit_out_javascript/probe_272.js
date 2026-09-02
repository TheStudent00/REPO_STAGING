// probe 272 -- binary in
function op_272(a, b) {
    return a in b;
}

%PrepareFunctionForOptimization(op_272);
op_272(true, false);
op_272(true, false);
%OptimizeFunctionOnNextCall(op_272);
op_272(true, false);
