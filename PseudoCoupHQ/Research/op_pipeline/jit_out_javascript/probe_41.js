// probe 41 -- unary ++
function op_41(a) {
    return a++;
}

%PrepareFunctionForOptimization(op_41);
op_41(true);
op_41(true);
%OptimizeFunctionOnNextCall(op_41);
op_41(true);
