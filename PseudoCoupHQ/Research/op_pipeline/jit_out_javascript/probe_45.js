// probe 45 -- unary !
function op_45(a) {
    return a!;
}

%PrepareFunctionForOptimization(op_45);
op_45(1.0);
op_45(1.0);
%OptimizeFunctionOnNextCall(op_45);
op_45(1.0);
