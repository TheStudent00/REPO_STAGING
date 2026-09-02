// probe 173 -- binary **
function op_173(a, b) {
    return a ** b;
}

%PrepareFunctionForOptimization(op_173);
op_173(true, false);
op_173(true, false);
%OptimizeFunctionOnNextCall(op_173);
op_173(true, false);
