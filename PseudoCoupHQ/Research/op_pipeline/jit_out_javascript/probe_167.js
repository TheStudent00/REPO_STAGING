// probe 167 -- binary **
function op_167(a, b) {
    return a ** b;
}

%PrepareFunctionForOptimization(op_167);
op_167(1.0, false);
op_167(1.0, false);
%OptimizeFunctionOnNextCall(op_167);
op_167(1.0, false);
