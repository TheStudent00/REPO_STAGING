// probe 219 -- binary !==
function op_219(a, b) {
    return a !== b;
}

%PrepareFunctionForOptimization(op_219);
op_219(1.0, 2.0);
op_219(1.0, 2.0);
%OptimizeFunctionOnNextCall(op_219);
op_219(1.0, 2.0);
