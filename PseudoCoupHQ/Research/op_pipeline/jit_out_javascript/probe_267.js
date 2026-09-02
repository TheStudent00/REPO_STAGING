// probe 267 -- binary in
function op_267(a, b) {
    return a in b;
}

%PrepareFunctionForOptimization(op_267);
op_267(1.0, 2.0);
op_267(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_267);
op_267(1.0, 2.0);
