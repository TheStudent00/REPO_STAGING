// probe 108 -- binary ^
function op_108(a, b) {
    return a ^ b;
}

%PrepareFunctionForOptimization(op_108);
op_108(true, 2.0);
op_108(true, 2.0);
%OptimizeFunctionOnNextCall(op_108);
op_108(true, 2.0);
