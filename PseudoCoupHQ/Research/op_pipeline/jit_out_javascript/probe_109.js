// probe 109 -- binary ^
function op_109(a, b) {
    return a ^ b;
}

%PrepareFunctionForOptimization(op_109);
op_109(true, 2.0);
op_109(true, 2.0);
%OptimizeFunctionOnNextCall(op_109);
op_109(true, 2.0);
