// probe 172 -- binary **
function op_172(a, b) {
    return a ** b;
}

%PrepareFunctionForOptimization(op_172);
op_172(true, 2.0);
op_172(true, 2.0);
%OptimizeFunctionOnNextCall(op_172);
op_172(true, 2.0);
