// probe 40 -- unary ++
function op_40(a) {
    return a++;
}

%PrepareFunctionForOptimization(op_40);
op_40(1.0);
op_40(1.0);
%OptimizeFunctionOnNextCall(op_40);
op_40(1.0);
