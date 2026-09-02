// probe 235 -- binary >=
function op_235(a, b) {
    return a >= b;
}

%PrepareFunctionForOptimization(op_235);
op_235(true, 2.0);
op_235(true, 2.0);
%OptimizeFunctionOnNextCall(op_235);
op_235(true, 2.0);
