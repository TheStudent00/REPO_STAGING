// probe 147 -- binary /
function op_147(a, b) {
    return a / b;
}

%PrepareFunctionForOptimization(op_147);
op_147(1.0, 2.0);
op_147(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_147);
op_147(1.0, 2.0);
