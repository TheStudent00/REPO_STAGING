// probe 149 -- binary /
function op_149(a, b) {
    return a / b;
}

%PrepareFunctionForOptimization(op_149);
op_149(1.0, false);
op_149(1.0, false);
%OptimizeFunctionOnNextCall(op_149);
op_149(1.0, false);
