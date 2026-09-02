// probe 107 -- binary ^
function op_107(a, b) {
    return a ^ b;
}

%PrepareFunctionForOptimization(op_107);
op_107(1.0, false);
op_107(1.0, false);
%OptimizeFunctionOnNextCall(op_107);
op_107(1.0, false);
