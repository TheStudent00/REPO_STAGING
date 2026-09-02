// probe 91 -- binary <<
function op_91(a, b) {
    return a << b;
}

%PrepareFunctionForOptimization(op_91);
op_91(true, 2.0);
op_91(true, 2.0);
%OptimizeFunctionOnNextCall(op_91);
op_91(true, 2.0);
