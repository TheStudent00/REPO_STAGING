// probe 226 -- binary !==
function op_226(a, b) {
    return a !== b;
}

%PrepareFunctionForOptimization(op_226);
op_226(true, 2.0);
op_226(true, 2.0);
%OptimizeFunctionOnNextCall(op_226);
op_226(true, 2.0);
