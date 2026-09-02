// probe 104 -- binary ^
function op_104(a, b) {
    return a ^ b;
}

%PrepareFunctionForOptimization(op_104);
op_104(1.0, false);
op_104(1.0, false);
%OptimizeFunctionOnNextCall(op_104);
op_104(1.0, false);
