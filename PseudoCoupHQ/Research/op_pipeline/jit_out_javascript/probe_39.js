// probe 39 -- unary ++
function op_39(a) {
    return a++;
}

%PrepareFunctionForOptimization(op_39);
op_39(1.0);
op_39(1.0);
%OptimizeFunctionOnNextCall(op_39);
op_39(1.0);
