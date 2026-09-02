// probe 186 -- binary <=
function op_186(a, b) {
    return a <= b;
}

%PrepareFunctionForOptimization(op_186);
op_186(1.0, 2.0);
op_186(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_186);
op_186(1.0, 2.0);
