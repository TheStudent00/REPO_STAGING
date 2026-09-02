// probe 178 -- binary <
function op_178(a, b) {
    return a < b;
}

%PrepareFunctionForOptimization(op_178);
op_178(1.0, 2.0);
op_178(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_178);
op_178(1.0, 2.0);
