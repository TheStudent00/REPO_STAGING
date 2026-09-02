// probe 74 -- binary >>
function op_74(a, b) {
    return a >> b;
}

%PrepareFunctionForOptimization(op_74);
op_74(true, false);
op_74(true, false);
%OptimizeFunctionOnNextCall(op_74);
op_74(true, false);
