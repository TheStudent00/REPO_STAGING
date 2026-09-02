// probe 71 -- binary >>
function op_71(a, b) {
    return a >> b;
}

%PrepareFunctionForOptimization(op_71);
op_71(1.0, false);
op_71(1.0, false);
%OptimizeFunctionOnNextCall(op_71);
op_71(1.0, false);
