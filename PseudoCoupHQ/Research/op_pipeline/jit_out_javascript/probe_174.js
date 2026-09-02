// probe 174 -- binary <
function op_174(a, b) {
    return a < b;
}

%PrepareFunctionForOptimization(op_174);
op_174(1.0, 2.0);
op_174(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_174);
op_174(1.0, 2.0);
