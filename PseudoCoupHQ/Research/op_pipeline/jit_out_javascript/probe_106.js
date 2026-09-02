// probe 106 -- binary ^
function op_106(a, b) {
    return a ^ b;
}

%PrepareFunctionForOptimization(op_106);
op_106(1.0, 2.0);
op_106(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_106);
op_106(1.0, 2.0);
