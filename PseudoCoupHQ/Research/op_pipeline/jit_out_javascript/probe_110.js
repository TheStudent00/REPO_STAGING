// probe 110 -- binary ^
function op_110(a, b) {
    return a ^ b;
}

%PrepareFunctionForOptimization(op_110);
op_110(true, false);
op_110(true, false);
%OptimizeFunctionOnNextCall(op_110);
op_110(true, false);
