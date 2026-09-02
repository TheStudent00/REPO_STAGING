// probe 46 -- unary !
function op_46(a) {
    return a!;
}

%PrepareFunctionForOptimization(op_46);
op_46(1.0);
op_46(1.0);
%OptimizeFunctionOnNextCall(op_46);
op_46(1.0);
