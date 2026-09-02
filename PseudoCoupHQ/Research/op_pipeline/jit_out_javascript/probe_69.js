// probe 69 -- binary >>
function op_69(a, b) {
    return a >> b;
}

%PrepareFunctionForOptimization(op_69);
op_69(1.0, 2.0);
op_69(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_69);
op_69(1.0, 2.0);
