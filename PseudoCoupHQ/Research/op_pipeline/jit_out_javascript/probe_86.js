// probe 86 -- binary <<
function op_86(a, b) {
    return a << b;
}

%PrepareFunctionForOptimization(op_86);
op_86(1.0, false);
op_86(1.0, false);
%OptimizeFunctionOnNextCall(op_86);
op_86(1.0, false);
