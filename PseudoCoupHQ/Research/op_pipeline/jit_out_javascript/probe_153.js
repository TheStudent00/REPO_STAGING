// probe 153 -- binary /
function op_153(a, b) {
    return a / b;
}

%PrepareFunctionForOptimization(op_153);
op_153(true, 2.0);
op_153(true, 2.0);
%OptimizeFunctionOnNextCall(op_153);
op_153(true, 2.0);
