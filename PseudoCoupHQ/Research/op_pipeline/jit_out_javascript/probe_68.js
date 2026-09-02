// probe 68 -- binary >>
function op_68(a, b) {
    return a >> b;
}

%PrepareFunctionForOptimization(op_68);
op_68(1.0, false);
op_68(1.0, false);
%OptimizeFunctionOnNextCall(op_68);
op_68(1.0, false);
