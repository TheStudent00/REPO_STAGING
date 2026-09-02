// probe 265 -- binary in
function op_265(a, b) {
    return a in b;
}

%PrepareFunctionForOptimization(op_265);
op_265(1.0, 2.0);
op_265(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_265);
op_265(1.0, 2.0);
