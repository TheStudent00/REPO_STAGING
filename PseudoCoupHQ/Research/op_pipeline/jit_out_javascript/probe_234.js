// probe 234 -- binary >=
function op_234(a, b) {
    return a >= b;
}

%PrepareFunctionForOptimization(op_234);
op_234(true, 2.0);
op_234(true, 2.0);
%OptimizeFunctionOnNextCall(op_234);
op_234(true, 2.0);
