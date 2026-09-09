# operator_variants_by_search

| compiler | sites (lowered operators) | sites fully resolved | sites partly resolved (one side) | unresolved | distinct variants resolved | of which both types in the language's core type inventory |
|---|---|---|---|---|---|---|
| clang/llvm (c, cpp) | 39451 | 6894 | 11036 | 21521 | 937 | 29 |
| go (cmd/compile) | 103475 | 22810 | 22605 | 58060 | 1050 | 248 |
| go (standard library, rest of checkout) | 346057 | 68351 | 103471 | 174235 | 4299 | 161 |
| rustc | 9182 | 528 | 651 | 8003 | 187 | 21 |
| swiftc (compiler) | 138142 | 15541 | 35247 | 87354 | 2363 | 73 |
| swift (standard library) | 12257 | 1068 | 2855 | 8334 | 243 | 26 |

## clang/llvm (c, cpp)

**unresolved histogram**

| reason | sites | share |
|---|---|---|
| call result | 13925 | 0.428 |
| other (binary_expression) | 7949 | 0.244 |
| declared in another file or not found | 7727 | 0.237 |
| member access | 1160 | 0.036 |
| inferred binding | 689 | 0.021 |
| nested operator, mixed operand types | 519 | 0.016 |
| index expression | 372 | 0.011 |
| macro | 81 | 0.002 |
| other (null) | 43 | 0.001 |
| other (assignment_expression) | 23 | 0.001 |
| other (type_descriptor) | 20 | 0.001 |
| other (conditional_expression) | 11 | 0.0 |
| other (concatenated_string) | 10 | 0.0 |
| other (sizeof_expression) | 10 | 0.0 |
| other (template_function) | 9 | 0.0 |
| other (alignof_expression) | 5 | 0.0 |
| other (new_expression) | 3 | 0.0 |
| other (ERROR) | 1 | 0.0 |

**resolved variants** (full table; log_210 carries the first 20)

| operator | lhs type | rhs type | sites |
|---|---|---|---|
| ++ | unsigned | None | 679 |
| ! | bool | None | 339 |
| != | unsigned | unsigned | 325 |
| < | unsigned | unsigned | 241 |
| - | unsigned | integer literal | 220 |
| == | unsigned | integer literal | 177 |
| - | unsigned | unsigned | 155 |
| << | integer literal | integer literal | 150 |
| && | bool | bool | 118 |
| + | unsigned | integer literal | 98 |
| * | unsigned | unsigned | 96 |
| != | unsigned | integer literal | 90 |
| / | unsigned | integer literal | 89 |
| == | SDValue | SDValue | 78 |
| + | unsigned | unsigned | 77 |
| && | bool | string literal | 73 |
| || | bool | bool | 68 |
| / | unsigned | unsigned | 66 |
| > | unsigned | integer literal | 66 |
| ! | APInt | None | 61 |
| % | unsigned | unsigned | 60 |
| > | unsigned | unsigned | 55 |
| ++ | int | None | 55 |
| ++ | size_t | None | 55 |
| ! | ConstantSDNode | None | 54 |
| ! | SDValue | None | 53 |
| -- | unsigned | None | 52 |
| < | int | integer literal | 49 |
| == | unsigned | unsigned | 47 |
| ! | Register | None | 44 |
| * | std::optional<unsigned> | None | 43 |
| == | EVT | EVT | 42 |
| ! | unsigned | None | 39 |
| + | integer literal | unsigned | 39 |
| != | int | int | 35 |
| * | unsigned | integer literal | 34 |
| < | unsigned | integer literal | 33 |
| <= | unsigned | unsigned | 32 |
| != | SDValue | SDValue | 32 |
| * | MachineFunction | None | 32 |
| < | int | int | 31 |
| & | unsigned | integer literal | 31 |
| != | EVT | EVT | 30 |
| <= | unsigned | integer literal | 30 |
| % | unsigned | integer literal | 29 |
| * | integer literal | unsigned | 29 |
| ~ | APInt | None | 28 |
| == | int | integer literal | 28 |
| ~ | integer literal (suffix u) | None | 28 |
| << | integer literal (suffix u) | integer literal | 27 |
| >= | unsigned | integer literal | 26 |
| * | MaybeAlign | None | 26 |
| & | unsigned | None | 25 |
| * | MachineInstr | None | 25 |
| > | int | integer literal | 22 |
| >= | int | integer literal | 21 |
| + | int | int | 21 |
| >= | unsigned | unsigned | 20 |
| + | APInt | APInt | 20 |
| ~ | integer literal (suffix U) | None | 20 |
| & | APInt | APInt | 19 |
| ! | cl::opt<bool> | None | 19 |
| ! | SDNode | None | 19 |
| == | APInt | integer literal | 17 |
| & | bool | None | 17 |
| * | int | int | 16 |
| << | raw_ostream | string literal | 16 |
| - | int | integer literal | 15 |
| + | InstructionCost | InstructionCost | 15 |
| ! | MaybeAlign | None | 14 |
| || | SDValue | SDValue | 13 |
| != | int | integer literal | 13 |
| * | std::optional<bool> | None | 13 |
| == | APInt | APInt | 13 |
| + | APInt | integer literal | 13 |
| != | bool | bool | 13 |
| + | uint64_t | unsigned | 12 |
| == | uint64_t | integer literal | 12 |
| - | int | int | 12 |
| << | integer literal (suffix ULL) | integer literal | 12 |
| -- | int | None | 12 |
| + | int | integer literal | 12 |
| * | std::optional<EVT> | None | 12 |
| ! | SUnit | None | 12 |
| - | int | unsigned | 11 |
| - | unsigned | uint64_t | 11 |
| ~ | unsigned | None | 11 |
| + | int | unsigned | 11 |
| * | std::optional<APInt> | None | 11 |
| & | TargetMachine | None | 11 |
| == | int | int | 10 |
| - | APInt | None | 10 |
| / | int | int | 10 |
| << | integer literal | unsigned | 10 |
| ++ | uint64_t | None | 10 |
| - | int | None | 9 |
| << | integer literal (suffix ULL) | unsigned | 9 |
| << | uint64_t | unsigned | 9 |
| ~ | FPClassTest | None | 9 |
| % | uint64_t | unsigned | 9 |
| && | MachineOperand | string literal | 9 |
| == | ISD::CondCode | ISD::CondCode | 9 |
| && | ConstantSDNode | ConstantSDNode | 9 |
| * | SDDbgInfo::DbgIterator | None | 9 |
| && | MachineInstr | string literal | 9 |
| * | APInt | APInt | 8 |
| - | APInt | APInt | 8 |
| && | unsigned | string literal | 8 |
| % | int | unsigned | 8 |
| - | uint64_t | unsigned | 8 |
| ~ | integer literal | None | 8 |
| % | int | int | 8 |
| != | SDNode::use_iterator | SDNode::use_iterator | 8 |
| ! | PointerSumType<ExtraInfoInlineKinds,
                 PointerSumTypeMember<EIIK_MMO, MachineMemOperand *>,
                 PointerSumTypeMember<EIIK_PreInstrSymbol, MCSymbol *>,
                 PointerSumTypeMember<EIIK_PostInstrSymbol, MCSymbol *>,
                 PointerSumTypeMember<EIIK_OutOfLine, ExtraInfo *>> | None | 8 |
| & | unsigned | unsigned | 8 |
| * | Use | None | 8 |
| >= | int | int | 7 |
| - | APInt | integer literal | 7 |
| & | Function | None | 7 |
| ! | MachineInstr | None | 7 |
| && | SDValue | string literal | 7 |
| + | uint64_t | integer literal | 7 |
| || | ConstantSDNode | ConstantSDNode | 7 |
| / | int | integer literal | 7 |
| + | size_t | integer literal | 7 |
| <= | uint64_t | uint64_t | 7 |
| & | SDNode | None | 7 |
| & | uint8_t | integer literal | 7 |
| << | integer literal (suffix U) | integer literal | 7 |
| ! | std::optional<unsigned> | None | 6 |
| ++ | MachineBasicBlock::iterator | None | 6 |
| << | OptimizationRemarkMissed | string literal | 6 |
| - | size_t | integer literal | 6 |
| / | int | unsigned | 6 |
| ! | uint64_t | None | 6 |
| < | uint64_t | unsigned | 6 |
| && | TargetRegisterClass | string literal | 6 |
| * | APInt | None | 6 |
| - | unsigned | int | 6 |
| * | std::optional<int> | None | 6 |
| == | int64_t | integer literal | 6 |
| ! | std::optional<EVT> | None | 6 |
| * | std::vector<SUnit *>::iterator | None | 6 |
| * | const_succ_iterator | None | 6 |
| + | bool | bool | 6 |
| >> | unsigned | integer literal | 6 |
| & | RegisterId | RegisterId | 6 |
| * | std::optional<StringRef> | None | 6 |
| == | DIExpression::expr_op_iterator | DIExpression::expr_op_iterator | 6 |
| - | integer literal | int | 5 |
| | | APInt | APInt | 5 |
| && | SDValue | SDValue | 5 |
| && | SDValue | bool | 5 |
| & | unsigned | integer literal (suffix U) | 5 |
| && | cl::opt<bool> | bool | 5 |
| != | uint64_t | integer literal | 5 |
| & | uint64_t | integer literal | 5 |
| == | SDNode | SDNode | 5 |
| * | MDNode | None | 5 |
| - | unsigned | None | 5 |
| ! | std::optional<MachineOperand> | None | 5 |
| * | TargetRegisterClass | None | 5 |
| ! | TargetRegisterClass | None | 5 |
| * | StaticAllocaInfo | None | 5 |
| * | MachineBasicBlock::iterator | None | 5 |
| / | BranchProbability | integer literal | 5 |
| * | int | unsigned | 5 |
| + | integer literal | SDValue | 5 |
| / | uint64_t | unsigned | 5 |
| != | TargetRegisterClass | TargetRegisterClass | 5 |
| == | bool | bool | 5 |
| == | unsigned | SDValue | 5 |
| >= | int64_t | integer literal | 5 |
| * | int64_t | integer literal | 5 |
| * | SUnit | None | 5 |
| & | APInt | None | 5 |
| ++ | SDNode::use_iterator | None | 5 |
| & | MachineBasicBlock::const_iterator | None | 5 |
| * | MachineBasicBlock::const_iterator | None | 5 |
| ! | MachineOperand | None | 5 |
| * | MachinePassRegistryNode<PassCtorTy> | None | 5 |
| * | unsigned | InstructionCost | 5 |
| * | integer literal | InstructionCost | 5 |
| * | Metadata | None | 5 |
| != | APInt | APInt | 4 |
| <= | integer literal | int | 4 |
| > | int | int | 4 |
| == | FPClassTest | FPClassTest | 4 |
| + | string literal | StringRef | 4 |
| > | int64_t | integer literal | 4 |
| * | char | None | 4 |
| * | MachineBasicBlock | None | 4 |
| * | BasicBlock::const_iterator | None | 4 |
| * | Instruction | None | 4 |
| != | SDNode | SDNode | 4 |
| == | MVT | MVT | 4 |
| && | Value | string literal | 4 |
| != | APInt | integer literal | 4 |
| * | std::optional<RoundingMode> | None | 4 |
| * | fltSemantics | None | 4 |
| & | TargetRegisterInfo | None | 4 |
| != | size_t | size_t | 4 |
| == | integer literal | unsigned | 4 |
| * | integer literal | APFloat::ExponentType | 4 |
| == | uint64_t | unsigned | 4 |
| - | int64_t | None | 4 |
| != | int | unsigned | 4 |
| ! | StoreSDNode | None | 4 |
| - | int64_t | int64_t | 4 |
| == | TypeSize | TypeSize | 4 |
| * | uint64_t | unsigned | 4 |
| + | uint64_t | uint64_t | 4 |
| ! | std::optional<APInt> | None | 4 |
| != | SDDbgInfo::DbgIterator | SDDbgInfo::DbgIterator | 4 |
| * | int | None | 4 |
| & | BitVector | None | 4 |
| ! | SDVTListNode | None | 4 |
| * | SDNode::use_iterator | None | 4 |
| & | SDUse | None | 4 |
| << | uint16_t | unsigned | 4 |
| < | PBQPNum | PBQPNum | 4 |
| == | MachineBasicBlock::instr_iterator | MachineBasicBlock::instr_iterator | 4 |
| * | DIE | None | 4 |
| * | Matrix | None | 4 |
| & | Value | None | 4 |
| ! | GlobalValueSummary | None | 4 |
| & | Use | None | 4 |
| && | std::optional<StringRef> | string literal | 4 |
| & | IRUnitT | None | 4 |
| == | Value | Value | 4 |
| > | unsigned | uint64_t | 3 |
| < | unsigned | uint64_t | 3 |
| ! | Value | None | 3 |
| <= | NegatibleCost | NegatibleCost | 3 |
| << | integer literal (suffix u) | unsigned | 3 |
| << | integer literal (suffix U) | unsigned | 3 |
| ~ | SDValue | None | 3 |
| ++ | SelectionDAG::allnodes_iterator | None | 3 |
| > | cl::opt<int> | integer literal | 3 |
| != | BasicBlock::const_iterator | BasicBlock::const_iterator | 3 |
| + | size_t | unsigned | 3 |
| - | ElementCount | ElementCount | 3 |
| || | MDNode | MDNode | 3 |
| && | MachineBasicBlock | string literal | 3 |
| & | SmallVector<EVT, 4> | None | 3 |
| & | SmallVector<uint64_t, 4> | None | 3 |
| & | SmallMapVector<const Instruction *, bool, 8> | None | 3 |
| == | SDValue | integer literal | 3 |
| * | LLVMContext | None | 3 |
| & | SmallVector<TypeSize, 4> | None | 3 |
| + | unsigned | int | 3 |
| * | std::optional<MachineOperand> | None | 3 |
| + | Register | unsigned | 3 |
| ++ | Register | None | 3 |
| > | Align | Align | 3 |
| + | APFloat::ExponentType | int | 3 |
| < | unsigned | unsigned int | 3 |
| & | MCInstrDesc | None | 3 |
| < | int64_t | int64_t | 3 |
| < | int64_t | integer literal | 3 |
| && | ConstantSDNode | string literal | 3 |
| << | APInt | APInt | 3 |
| ! | std::optional<int> | None | 3 |
| && | SelectionDAG | string literal | 3 |
| ! | LoadSDNode | None | 3 |
| / | uint64_t | uint64_t | 3 |
| - | std::optional<unsigned> | integer literal | 3 |
| * | ShuffleVectorSDNode | None | 3 |
| * | ElementCount | unsigned | 3 |
| != | int64_t | int64_t | 3 |
| && | SUnit | string literal | 3 |
| ++ | SDDbgInfo::DbgIterator | None | 3 |
| * | SDDbgInfo::DbgLabelIterator | None | 3 |
| & | TargetSubtargetInfo | None | 3 |
| ! | uint32_t | None | 3 |
| * | SDNode::op_iterator | None | 3 |
| & | FPClassTest | FPClassTest | 3 |
| && | APInt | APInt | 3 |
| < | size_t | size_t | 3 |
| - | TypeSize | TypeSize | 3 |
| & | uint64_t | None | 3 |
| & | CallBase | None | 3 |
| << | llvm::raw_ostream | string literal | 3 |
| != | const_succ_iterator | const_succ_iterator | 3 |
| * | std::optional<int64_t> | None | 3 |
| ~ | uint32_t | None | 3 |
| << | bool | integer literal | 3 |
| != | unsigned | integer literal (suffix u) | 3 |
| * | NodeSet::iterator | None | 3 |
| * | std::optional<uint64_t> | None | 3 |
| & | FeatureBitset | FeatureBitset | 3 |
| && | int | string literal | 3 |
| * | std::optional<Intrinsic::ID> | None | 3 |
| & | ValTy | None | 3 |
| ~ | integer literal (suffix ULL) | None | 3 |
| == | LLT | LLT | 3 |
| && | Type | string literal | 3 |
| ++ | const_op_iterator | None | 3 |
| & | AnalysisManagerT | None | 3 |
| * | DIExpression::expr_op_iterator | None | 3 |
| - | unsigned | SDValue | 2 |
| << | APInt | unsigned | 2 |
| != | char | char literal | 2 |
| * | ConstantFP | None | 2 |
| & | ConstantRange | None | 2 |
| & | int | integer literal | 2 |
| & | SelectionDAG::allnodes_iterator | None | 2 |
| * | SelectionDAG::allnodes_iterator | None | 2 |
| != | MachineSDNode::mmo_iterator | MachineSDNode::mmo_iterator | 2 |
| ++ | MachineSDNode::mmo_iterator | None | 2 |
| * | MachineSDNode::mmo_iterator | None | 2 |
| -- | BasicBlock::iterator | None | 2 |
| * | BasicBlock::iterator | None | 2 |
| & | BasicBlock::const_iterator | None | 2 |
| ! | FastISel | None | 2 |
| && | FastISel | bool | 2 |
| -- | BasicBlock::const_iterator | None | 2 |
| != | MachineBasicBlock::iterator | MachineBasicBlock::iterator | 2 |
| -- | uint64_t | None | 2 |
| & | int64_t | integer literal | 2 |
| * | SDNode | None | 2 |
| == | size_t | integer literal | 2 |
| * | int64_t | None | 2 |
| & | DbgVariableRecord | None | 2 |
| * | Value | None | 2 |
| * | ConstantInt | None | 2 |
| && | BasicBlock | string literal | 2 |
| && | Function | string literal | 2 |
| != | gep_type_iterator | gep_type_iterator | 2 |
| ++ | gep_type_iterator | None | 2 |
| ~ | uint64_t | None | 2 |
| >= | unsigned | uint64_t | 2 |
| ! | fltSemantics | None | 2 |
| * | Function | None | 2 |
| & | SDValue | None | 2 |
| && | bool literal | string literal | 2 |
| & | MachineBasicBlock::iterator | None | 2 |
| ++ | MachineFunction::iterator | None | 2 |
| ^ | APInt | APInt | 2 |
| ++ | CaseClusterIt | None | 2 |
| > | cl::opt<unsigned> | integer literal | 2 |
| * | integer literal | int | 2 |
| > | unsigned int | integer literal | 2 |
| <= | uint64_t | unsigned | 2 |
| == | TargetRegisterClass | TargetRegisterClass | 2 |
| && | TargetRegisterClass | bool | 2 |
| == | Register | integer literal | 2 |
| * | MachineInstrBuilder | None | 2 |
| != | ISD::CondCode | ISD::CondCode | 2 |
| <= | unsigned | uint64_t | 2 |
| > | uint64_t | uint64_t | 2 |
| < | int | unsigned | 2 |
| ! | std::optional<BaseIndexOffset> | None | 2 |
| || | bool | unsigned | 2 |
| ~ | std::optional<APInt> | None | 2 |
| ! | ConstantFPSDNode | None | 2 |
| && | SDNode | string literal | 2 |
| * | LoadedSlice | None | 2 |
| != | Value | Value | 2 |
| * | std::optional<MachineMemOperand::Flags> | None | 2 |
| == | int64_t | int64_t | 2 |
| % | uint64_t | uint64_t | 2 |
| * | uint64_t | integer literal | 2 |
| == | integer literal | int | 2 |
| ! | ShuffleVectorSDNode | None | 2 |
| <= | int | int | 2 |
| != | unsigned | int | 2 |
| - | integer literal | unsigned | 2 |
| + | int64_t | int64_t | 2 |
| & | Function::const_arg_iterator | None | 2 |
| * | Function::const_arg_iterator | None | 2 |
| >= | uint64_t | uint64_t | 2 |
| != | unsigned | SDNode::user_iterator | 2 |
| ! | MCRegister | None | 2 |
| & | MachineInstr | None | 2 |
| && | TargetRegisterClass | SUnit | 2 |
| * | std::vector<SUnit *>::const_iterator | None | 2 |
| < | bool | bool | 2 |
| || | unsigned | unsigned | 2 |
| << | unsigned | integer literal | 2 |
| != | SDNode::op_iterator | SDNode::op_iterator | 2 |
| ++ | SDNode::op_iterator | None | 2 |
| * | int | integer literal | 2 |
| ++ | op_iterator | None | 2 |
| ++ | allnodes_iterator | None | 2 |
| <= | int | integer literal | 2 |
| <= | Align | Align | 2 |
| && | Register | string literal | 2 |
| ! | LiveOutInfo | None | 2 |
| - | uint64_t | uint64_t | 2 |
| != | SUnit | SUnit | 2 |
| & | SUnit | None | 2 |
| + | long | integer literal (suffix L) | 2 |
| - | long | long | 2 |
| + | long | long | 2 |
| * | livein_iterator | None | 2 |
| + | MachineOperand | uint32_t | 2 |
| * | MCContext | None | 2 |
| * | MachineRegisterInfo | None | 2 |
| * | TargetRegisterInfo | None | 2 |
| >> | uint32_t | uint32_t | 2 |
| & | IndexList::iterator | None | 2 |
| * | IndexList::iterator | None | 2 |
| == | MachineBasicBlock::const_iterator | MachineBasicBlock::const_iterator | 2 |
| ++ | MachineBasicBlock::const_iterator | None | 2 |
| * | uint16_t | None | 2 |
| ++ | uint16_t | None | 2 |
| * | uint32_t | None | 2 |
| * | LiveRange | None | 2 |
| << | uint32_t | uint32_t | 2 |
| - | uint16_t | integer literal | 2 |
| == | const_iterator | const_iterator | 2 |
| * | T | None | 2 |
| * | SDUse | None | 2 |
| && | SDUse | string literal | 2 |
| & | APInt | integer literal | 2 |
| >> | int | integer literal | 2 |
| == | MachineInstr::mop_iterator | MachineInstr::mop_iterator | 2 |
| * | MachineInstr::mop_iterator | None | 2 |
| && | TargetRegisterInfo | string literal | 2 |
| && | bool | MachineBasicBlock | 2 |
| && | MachineBasicBlock | MachineBasicBlock | 2 |
| ! | MachineBasicBlock | None | 2 |
| ~ | FeatureBitset | None | 2 |
| & | FunctionAnalysisManager | None | 2 |
| * | FunctionAnalysisManager | None | 2 |
| ! | Node | None | 2 |
| == | Node | Node | 2 |
| == | uint8_t | unsigned | 2 |
| == | uint16_t | unsigned | 2 |
| == | uint32_t | unsigned | 2 |
| || | MachineOperand | MachineOperand | 2 |
| * | std::unique_ptr<PhysicalRegisterUsageInfo> | None | 2 |
| ! | std::optional<uint64_t> | None | 2 |
| ~ | RegisterId | None | 2 |
| != | RegisterId | integer literal | 2 |
| ! | RegisterId | None | 2 |
| * | typename EntrySetT::iterator | None | 2 |
| * | typename GraphT::AdjEdgeItr | None | 2 |
| && | SolverT | string literal | 2 |
| != | unsigned | uint16_t | 2 |
| && | ValueInfo | string literal | 2 |
| * | std::unique_ptr<ParamAccessesTy> | None | 2 |
| * | std::unique_ptr<CallsitesTy> | None | 2 |
| * | std::unique_ptr<AllocsTy> | None | 2 |
| + | Use | integer literal | 2 |
| * | std::unique_ptr<ToolOutputFile> | None | 2 |
| & | DebugValueUser | None | 2 |
| ++ | MDNode::op_iterator | None | 2 |
| ! | Metadata | None | 2 |
| && | Metadata | string literal | 2 |
| ! | std::optional<APFloat> | None | 2 |
| * | std::optional<APFloat> | None | 2 |
| ! | std::optional<MDMapT> | None | 2 |
| * | typename Config::mutex_type | None | 2 |
| & | TrackingMDRef | None | 2 |
| * | ItTy | None | 2 |
| * | CmpPredicate | None | 2 |
| != | const_op_iterator | const_op_iterator | 2 |
| * | AnalysisManagerT | None | 2 |
| ! | CycleRef | None | 2 |
| >> | unsigned | unsigned | 2 |
| && | UseT | string literal | 2 |
| * | use_iterator_impl<Use> | None | 2 |
| ! | Use | None | 2 |
| && | Target | string literal | 2 |
| ! | MCSymbol | None | 2 |
| == | Type | integer literal | 2 |
| ~ | Type | None | 2 |
| - | integer literal | integer literal | 2 |
| * | integer literal | integer literal | 2 |
| + | InstrStage | unsigned | 2 |
| + | std::optional<unsigned> | integer literal | 2 |
| - | uint32_t | uint32_t | 2 |
| || | APInt | APInt | 1 |
| + | SDValue | unsigned | 1 |
| == | std::optional<unsigned> | unsigned | 1 |
| >= | std::optional<unsigned> | unsigned | 1 |
| ! | BuildVectorSDNode | None | 1 |
| + | uint64_t | int64_t | 1 |
| && | llvm::Type | string literal | 1 |
| * | InlineAsm::ConstraintCodeVector | None | 1 |
| > | ConstraintWeight | ConstraintWeight | 1 |
| * | integer literal | APInt | 1 |
| << | integer literal (suffix ull) | unsigned | 1 |
| - | uint64_t | integer literal | 1 |
| | | SDValue | APInt | 1 |
| && | GlobalVariable | string literal | 1 |
| && | TableId | string literal | 1 |
| != | TableId | TableId | 1 |
| + | unsigned | bool | 1 |
| - | unsigned | bool | 1 |
| ! | ModuleLibcallLoweringInfo | None | 1 |
| ++ | BasicBlock::iterator | None | 1 |
| & | BasicBlock::iterator | None | 1 |
| ++ | BasicBlock::const_iterator | None | 1 |
| -- | SelectionDAG::allnodes_iterator | None | 1 |
| && | MCRegister | string literal | 1 |
| ! | llvm::WinEHFuncInfo | None | 1 |
| != | Instruction | BasicBlock::const_iterator | 1 |
| != | Instruction | Instruction | 1 |
| ! | OptimizationRemarkMissed | None | 1 |
| * | std::optional<SDValue> | None | 1 |
| + | uint16_t | integer literal | 1 |
| == | unsigned | uint16_t | 1 |
| & | size_t | integer literal | 1 |
| * | SDValue | None | 1 |
| >= | int32_t | integer literal | 1 |
| ! | Instruction | None | 1 |
| * | CallInst | None | 1 |
| * | std::optional<ElementCount> | None | 1 |
| ! | FunctionLoweringInfo::LiveOutInfo | None | 1 |
| * | DILocalVariable | None | 1 |
| * | ConstantExpr | None | 1 |
| && | BranchProbabilityInfo | BasicBlock | 1 |
| ! | BranchProbabilityInfo | None | 1 |
| <= | InstructionCost | integer literal | 1 |
| > | InstructionCost | InstructionCost | 1 |
| < | SDValue | integer literal | 1 |
| != | MVT | MVT | 1 |
| <= | MaybeAlign | Align | 1 |
| ! | GetElementPtrInst | None | 1 |
| != | TypeSize | integer literal | 1 |
| && | cl::opt<bool> | MaybeAlign | 1 |
| ! | Argument | None | 1 |
| ! | Function | None | 1 |
| ! | AllocaInst | None | 1 |
| + | SDValue | integer literal | 1 |
| & | TargetLowering::PtrAuthInfo | None | 1 |
| ++ | TargetRegisterClass::iterator | None | 1 |
| * | TargetRegisterClass::iterator | None | 1 |
| ! | std::optional<ConstantRange> | None | 1 |
| != | size_t | unsigned | 1 |
| < | size_t | unsigned | 1 |
| & | BasicBlock | None | 1 |
| ! | StaticAllocaInfo | None | 1 |
| ! | std::optional<TypeSize> | None | 1 |
| * | std::optional<TypeSize> | None | 1 |
| * | AllocaInst | None | 1 |
| ! | Type | None | 1 |
| & | MachineFunction::iterator | None | 1 |
| * | MachineFunction::iterator | None | 1 |
| -- | CaseClusterIt | None | 1 |
| * | CaseClusterIt | None | 1 |
| <= | CaseClusterIt | CaseClusterIt | 1 |
| != | MachineBasicBlock::succ_iterator | MachineBasicBlock::succ_iterator | 1 |
| ++ | MachineBasicBlock::succ_iterator | None | 1 |
| * | MachineBasicBlock::succ_iterator | None | 1 |
| * | SwitchCG::JumpTable | None | 1 |
| * | JumpTableHeader | None | 1 |
| * | BitTestBlock | None | 1 |
| == | MachineBasicBlock | MachineBasicBlock | 1 |
| != | TypeSize | TypeSize | 1 |
| && | TargetRegisterClass | TargetRegisterClass | 1 |
| ! | RegisterSDNode | None | 1 |
| & | MachineInstrBuilder | None | 1 |
| == | Register | Register | 1 |
| ^ | unsigned | integer literal | 1 |
| >= | uint64_t | unsigned | 1 |
| * | APInt | SDValue | 1 |
| || | unsigned | bool | 1 |
| % | uint64_t | integer literal | 1 |
| / | uint64_t | integer literal | 1 |
| >= | int64_t | unsigned | 1 |
| && | StoreSDNode | string literal | 1 |
| && | std::optional<BaseIndexOffset> | string literal | 1 |
| ! | std::optional<bool> | None | 1 |
| && | std::optional<SDByteProvider> | string literal | 1 |
| * | std::optional<SDByteProvider> | None | 1 |
| != | bool | std::optional<bool> | 1 |
| + | APInt | unsigned | 1 |
| >= | APInt | uint64_t | 1 |
| < | APInt | uint64_t | 1 |
| - | unsigned | APInt | 1 |
| || | bool | std::optional<APInt> | 1 |
| ! | MaskedLoadSDNode | None | 1 |
| == | std::optional<int> | int | 1 |
| && | ConstantFPSDNode | bool | 1 |
| / | float literal (suffix f) | float literal (suffix f) | 1 |
| / | float literal | float literal | 1 |
| - | int | bool | 1 |
| / | int64_t | integer literal | 1 |
| != | int64_t | integer literal | 1 |
| && | LoadSDNode | string literal | 1 |
| || | LoadSDNode | SDNode | 1 |
| ! | SelectionDAG | None | 1 |
| && | SDNode | LoadSDNode | 1 |
| ! | TargetRegisterInfo | None | 1 |
| ! | LoadedSlice | None | 1 |
| >> | uint64_t | unsigned | 1 |
| && | Value | bool | 1 |
| ! | std::optional<MachineMemOperand::Flags> | None | 1 |
| * | StoreSDNode | None | 1 |
| * | int64_t | unsigned | 1 |
| * | unsigned | int64_t | 1 |
| * | LoadSDNode | None | 1 |
| & | uint64_t | float literal (suffix FFFFFFFF) | 1 |
| >> | uint64_t | integer literal | 1 |
| % | int | integer literal | 1 |
| || | SDValue | bool | 1 |
| > | SDValue | int | 1 |
| % | SDValue | unsigned | 1 |
| / | SDValue | unsigned | 1 |
| * | unsigned | uint64_t | 1 |
| == | uint64_t | uint64_t | 1 |
| > | uint64_t | integer literal | 1 |
| - | SDValue | integer literal | 1 |
| + | int64_t | unsigned | 1 |
| & | SmallVector<SDValue, 4> | None | 1 |
| < | std::optional<unsigned> | unsigned | 1 |
| % | unsigned | int | 1 |
| * | unsigned | int | 1 |
| == | std::optional<APInt> | integer literal | 1 |
| == | Align | Align | 1 |
| == | LocationSize | LocationSize | 1 |
| != | Function::const_arg_iterator | Function::const_arg_iterator | 1 |
| ++ | Function::const_arg_iterator | None | 1 |
| ! | ExtractValueInst | None | 1 |
| * | unsigned | None | 1 |
| - | SDNode::user_iterator | integer literal | 1 |
| || | MCRegister | bool | 1 |
| > | std::optional<unsigned> | integer literal (suffix U) | 1 |
| == | MachineBasicBlock::iterator | MachineBasicBlock::iterator | 1 |
| != | SDDbgInfo::DbgLabelIterator | SDDbgInfo::DbgLabelIterator | 1 |
| ++ | SDDbgInfo::DbgLabelIterator | None | 1 |
| == | SDDbgInfo::DbgLabelIterator | SDDbgInfo::DbgLabelIterator | 1 |
| == | MachineInstr | MachineBasicBlock::iterator | 1 |
| && | bool | SUnit | 1 |
| || | cl::opt<bool> | bool | 1 |
| || | SDNode | bool | 1 |
| < | cl::opt<unsigned> | integer literal | 1 |
| ++ | std::vector<SUnit *>::const_iterator | None | 1 |
| || | cl::opt<bool> | cl::opt<bool> | 1 |
| * | ElementCount | integer literal | 1 |
| + | SDDbgOperand | size_t | 1 |
| && | std::optional<int> | bool | 1 |
| != | std::optional<int> | std::optional<int> | 1 |
| + | integer literal | int64_t | 1 |
| * | FrameIndexSDNode | None | 1 |
| || | bool | cl::opt<bool> | 1 |
| & | uint64_t | uint64_t | 1 |
| != | SDNodeIterator | SDNodeIterator | 1 |
| ++ | SDNodeIterator | None | 1 |
| * | SDNodeIterator | None | 1 |
| && | bool | int | 1 |
| < | Align | Align | 1 |
| && | bool | ConstantSDNode | 1 |
| + | unsigned | std::optional<unsigned> | 1 |
| | | KnownFPClass | KnownFPClass | 1 |
| && | std::optional<bool> | std::optional<bool> | 1 |
| && | std::optional<APInt> | string literal | 1 |
| && | ConstantFPSDNode | ConstantFPSDNode | 1 |
| ! | GlobalAddressSDNode | None | 1 |
| == | cl::opt<int> | integer literal | 1 |
| & | EVT | None | 1 |
| * | size_t | None | 1 |
| != | op_iterator | op_iterator | 1 |
| * | op_iterator | None | 1 |
| && | SDNode | SDNode | 1 |
| * | DIExpression | None | 1 |
| < | intptr_t | intptr_t | 1 |
| != | allnodes_iterator | allnodes_iterator | 1 |
| - | unsigned int | integer literal | 1 |
| * | APInt | int | 1 |
| * | APInt | unsigned | 1 |
| * | LiveOutInfo | None | 1 |
| != | TargetLowering::BooleanContent | TargetLowering::BooleanContent | 1 |
| + | ElementCount | ElementCount | 1 |
| < | uint64_t | uint64_t | 1 |
| == | ElementCount | ElementCount | 1 |
| * | integer literal | int64_t | 1 |
| && | SUnit | bool | 1 |
| & | RegisterBank | None | 1 |
| + | PartialMapping | unsigned | 1 |
| && | PartialMapping | unsigned | 1 |
| || | bool | BasicBlock | 1 |
| & | Instructions | None | 1 |
| ++ | livein_iterator | None | 1 |
| & | livein_iterator | None | 1 |
| ++ | const_succ_iterator | None | 1 |
| == | const_succ_iterator | const_succ_iterator | 1 |
| & | Pass | None | 1 |
| & | MachineFunctionAnalysisManager | None | 1 |
| & | char | None | 1 |
| & | uint32_t | unsigned | 1 |
| * | MCInstrDesc | None | 1 |
| + | size_t | size_t | 1 |
| ! | InstrStage::FuncUnits | None | 1 |
| && | MachineFunction | string literal | 1 |
| & | uint32_t | float literal (suffix FFFFFF) | 1 |
| << | uint32_t | integer literal | 1 |
| << | float literal (suffix F) | integer literal | 1 |
| << | integer literal | uint32_t | 1 |
| - | NodeId | integer literal | 1 |
| & | uint32_t | uint32_t | 1 |
| + | Slot | integer literal | 1 |
| - | Slot | integer literal | 1 |
| != | IndexList::iterator | IndexList::iterator | 1 |
| ++ | IndexList::iterator | None | 1 |
| -- | MachineBasicBlock::const_iterator | None | 1 |
| * | IndexListEntry | None | 1 |
| & | Module | None | 1 |
| ! | std::optional<ISelOp> | None | 1 |
| && | MaybeAlign | string literal | 1 |
| * | std::unique_ptr<MachineFunction> | None | 1 |
| * | vt_iterator | None | 1 |
| ++ | vt_iterator | None | 1 |
| ++ | uint32_t | None | 1 |
| | | unsigned | unsigned | 1 |
| & | RTLIB::RuntimeLibcallsInfo | None | 1 |
| * | RTLIB::RuntimeLibcallsInfo | None | 1 |
| * | MachineDominatorTree | None | 1 |
| ! | LiveRange | None | 1 |
| & | uint32_t | float literal (suffix F) | 1 |
| < | unsigned | float literal (suffix f) | 1 |
| == | unsigned | integer literal (suffix u) | 1 |
| * | GraphMetadata::AllowedRegVecRef | None | 1 |
| == | PBQPNum | PBQPNum | 1 |
| > | uint16_t | integer literal | 1 |
| & | TargetRegisterClass | None | 1 |
| == | VNInfo | VNInfo | 1 |
| * | VNInfo | None | 1 |
| & | const_iterator | None | 1 |
| * | const_iterator | None | 1 |
| & | iterator | None | 1 |
| * | iterator | None | 1 |
| ++ | const_iterator | None | 1 |
| < | SlotIndex | SlotIndex | 1 |
| < | int32_t | integer literal | 1 |
| ~ | int32_t | None | 1 |
| ++ | use_iterator | None | 1 |
| * | use_iterator | None | 1 |
| < | unsigned | unsigned short | 1 |
| + | SDUse | unsigned short | 1 |
| + | EVT | unsigned short | 1 |
| & | uint16_t | None | 1 |
| * | std::optional<ISD::CondCode> | None | 1 |
| * | ISD::CondCode | None | 1 |
| == | size_t | size_t | 1 |
| ++ | def_iterator | None | 1 |
| & | def_iterator | None | 1 |
| * | def_iterator | None | 1 |
| == | MachineOperand | MachineOperand | 1 |
| * | MachineOperand | None | 1 |
| & | MachinePassRegistryNode | None | 1 |
| && | PassCtorTy | string literal | 1 |
| & | MachinePassRegistryNode<PassCtorTy> | None | 1 |
| ++ | MachineBasicBlock::instr_iterator | None | 1 |
| != | MachineInstr::mop_iterator | MachineInstr::mop_iterator | 1 |
| ++ | MachineInstr::mop_iterator | None | 1 |
| & | MachineInstr::mop_iterator | None | 1 |
| != | std::vector<MachineBasicBlock::RegisterMaskPair> | std::vector<MachineBasicBlock::RegisterMaskPair> | 1 |
| * | std::unique_ptr<AsmPrinter> | None | 1 |
| << | uintptr_t | integer literal | 1 |
| - | integer literal | None | 1 |
| != | FeatureBitset | FeatureBitset | 1 |
| == | FeatureBitset | FeatureBitset | 1 |
| * | InstructionCost | None | 1 |
| ! | FixedVectorType | None | 1 |
| * | InstructionCost | integer literal | 1 |
| != | MachineBasicBlock | MachineBasicBlock | 1 |
| & | LiveRange | None | 1 |
| > | unsigned long long | integer literal | 1 |
| & | MCSchedModel | None | 1 |
| & | InstrItineraryData | None | 1 |
| == | int8_t | int64_t | 1 |
| == | int16_t | int64_t | 1 |
| == | int32_t | int64_t | 1 |
| & | DIEValue | None | 1 |
| != | T | T | 1 |
| * | instr_iterator | None | 1 |
| sizeof | union ContentsUnion {
    ContentsUnion() {}
    MachineBasicBlock *MBB;  // For MO_MachineBasicBlock.
    const ConstantFP *CFP;   // For MO_FPImmediate.
    const ConstantInt *CI;   // For MO_CImmediate. Integers > 64bit.
    int64_t ImmVal;          // For MO_Immediate.
    const uint32_t *RegMask; // For MO_RegisterMask and MO_RegisterLiveOut.
    const MDNode *MD;        // For MO_Metadata.
    MCSymbol *Sym;           // For MO_MCSymbol.
    unsigned CFIIndex;       // For MO_CFI.
    Intrinsic::ID IntrinsicID; // For MO_IntrinsicID.
    unsigned Pred;           // For MO_Predicate
    ArrayRef<int> ShuffleMask; // For MO_ShuffleMask
    LaneBitmask LaneMask;      // For MO_LaneMask

    struct {                  // For MO_Register.
      // Register number is in SmallContents.RegNo.
      MachineOperand *Prev;   // Access list for register. See MRI.
      MachineOperand *Next;
    } Reg;

    struct { // For MO_DbgInstrRef.
      unsigned InstrIdx;
      unsigned OpIdx;
    } InstrRef;

    /// OffsetedInfo - This struct contains the offset and an object identifier.
    /// this represent the object as with an optional offset from it.
    struct {
      union {
        int Index;                // For MO_*Index - The index itself.
        const char *SymbolName;   // For MO_ExternalSymbol.
        const GlobalValue *GV;    // For MO_GlobalAddress.
        const BlockAddress *BA;   // For MO_BlockAddress.
      } Val;
      // Low bits of offset are in SmallContents.OffsetLo.
      int OffsetHi;               // An offset from the object, high 32 bits.
    } OffsetedInfo;
  } | None | 1 |
| * | AliasAnalysis | None | 1 |
| == | RegisterId | integer literal | 1 |
| ++ | MapType::iterator | None | 1 |
| - | uint64_t | None | 1 |
| == | MachineInstr | MachineInstr | 1 |
| ++ | typename GraphT::AdjEdgeItr | None | 1 |
| ++ | NodeId | None | 1 |
| ++ | EdgeId | None | 1 |
| ! | SolverT | None | 1 |
| * | VectorPtr | None | 1 |
| * | MatrixPtr | None | 1 |
| != | AdjEdgeItr | AdjEdgeItr | 1 |
| * | AdjEdgeItr | None | 1 |
| ++ | AdjEdgeItr | None | 1 |
| << | OStream | string literal | 1 |
| != | uint64_t | integer literal (suffix u) | 1 |
| < | unsigned | uint16_t | 1 |
| <= | uint16_t | unsigned | 1 |
| - | unsigned | uint16_t | 1 |
| < | int64_t | uint16_t | 1 |
| <= | uint16_t | int64_t | 1 |
| - | int64_t | uint16_t | 1 |
| != | unsigned | uint64_t | 1 |
| * | ComplexRendererFns | None | 1 |
| & | Ty | None | 1 |
| sizeof | Ty | None | 1 |
| >= | uint64_t | integer literal | 1 |
| * | TargetInstrInfo | None | 1 |
| * | RegisterBankInfo | None | 1 |
| ! | std::optional<DefinitionAndSourceRegister> | None | 1 |
| && | unsigned | bool | 1 |
| != | LLT | LLT | 1 |
| << | raw_ostream | ListSeparator | 1 |
| && | GlobalValueSummary | string literal | 1 |
| * | GlobalValueSummary | None | 1 |
| ! | std::unique_ptr<TypeIdInfo> | None | 1 |
| ! | std::unique_ptr<CallsitesTy> | None | 1 |
| ! | std::unique_ptr<AllocsTy> | None | 1 |
| ! | std::unique_ptr<VTableFuncList> | None | 1 |
| * | std::unique_ptr<VTableFuncList> | None | 1 |
| - | integer literal (suffix L) | integer literal | 1 |
| ~ | integer literal (suffix L) | None | 1 |
| + | ptrdiff_t | integer literal | 1 |
| + | integer literal | int | 1 |
| & | std::unique_ptr<ToolOutputFile> | None | 1 |
| || | bool | MDNode | 1 |
| & | Metadata | None | 1 |
| * | size_t | size_t | 1 |
| ! | size_t | None | 1 |
| * | MDNode::op_iterator | None | 1 |
| * | integer literal | TypeSize | 1 |
| * | std::optional<MDMapT> | None | 1 |
| ++ | BaseT | None | 1 |
| & | AnalysisSetKey | None | 1 |
| ! | ConstantInt | None | 1 |
| ! | MDNode | None | 1 |
| ! | DILocation | None | 1 |
| * | BI_t | None | 1 |
| ++ | BI_t | None | 1 |
| -- | BB_i_t | None | 1 |
| -- | BI_t | None | 1 |
| ++ | BB_i_t | None | 1 |
| * | USE_iterator | None | 1 |
| ++ | USE_iterator | None | 1 |
| * | PHINodeT | None | 1 |
| && | PHINodeT | string literal | 1 |
| | | integer literal | integer literal | 1 |
| & | ItTy | None | 1 |
| ++ | ItTy | None | 1 |
| && | integer literal | string literal | 1 |
| >> | uint8_t | integer literal | 1 |
| & | uint8_t | float literal (suffix f) | 1 |
| ! | Constant | None | 1 |
| * | Constant | None | 1 |
| & | ValueSymbolTable | None | 1 |
| ! | ResultConceptT | None | 1 |
| ! | AnalysisManagerT | None | 1 |
| ! | PassInstrumentationCallbacks | None | 1 |
| != | Type | Type | 1 |
| & | ValueHandleBase | None | 1 |
| * | UseT | None | 1 |
| ++ | use_iterator_impl<Use> | None | 1 |
| && | Use | string literal | 1 |
| + | LLVMValueRef | unsigned | 1 |
| != | LLVMValueRef | LLVMValueRef | 1 |
| ++ | LLVMValueRef | None | 1 |
| * | LLVMValueRef | None | 1 |
| ! | MDTuple | None | 1 |
| ! | DISubprogram | None | 1 |
| * | uint64_t | None | 1 |
| & | ExprOperand | None | 1 |
| ++ | DIExpression::expr_op_iterator | None | 1 |
| != | DIExpression::expr_op_iterator | DIExpression::expr_op_iterator | 1 |
| * | std::optional<FragmentInfo> | None | 1 |
| - | unsigned short | integer literal | 1 |
| != | uint16_t | unsigned short | 1 |
| == | uint16_t | unsigned short | 1 |
| * | MCExtraProcessorInfo | None | 1 |
| * | StringTable | None | 1 |
| ! | MCSchedClassDesc | None | 1 |
| * | MCSchedClassDesc | None | 1 |
| == | uint32_t | uint32_t | 1 |
| * | std::unique_ptr<MCAsmBackend> | None | 1 |
| * | std::unique_ptr<MCCodeEmitter> | None | 1 |
| * | std::unique_ptr<MCObjectWriter> | None | 1 |
| == | unsigned | integer literal (suffix U) | 1 |
| ! | std::optional<wasm::WasmSymbolType> | None | 1 |
| * | std::optional<wasm::WasmGlobalType> | None | 1 |
| * | std::optional<wasm::WasmTableType> | None | 1 |
| - | NameEntryStorageTy | integer literal | 1 |
| ! | MCAsmInfoCtorFnTy | None | 1 |
| ! | MCObjectFileInfoCtorFnTy | None | 1 |
| ! | MCInstrInfoCtorFnTy | None | 1 |
| ! | MCInstrAnalysisCtorFnTy | None | 1 |
| ! | MCRegInfoCtorFnTy | None | 1 |
| ! | MCSubtargetInfoCtorFnTy | None | 1 |
| ! | TargetMachineCtorTy | None | 1 |
| ! | MCAsmBackendCtorTy | None | 1 |
| ! | MCAsmParserCtorTy | None | 1 |
| ! | AsmPrinterCtorTy | None | 1 |
| ! | MCDisassemblerCtorTy | None | 1 |
| ! | MCInstPrinterCtorTy | None | 1 |
| ! | MCCodeEmitterCtorTy | None | 1 |
| * | MCStreamer | None | 1 |
| * | Target | None | 1 |
| != | int16_t | integer literal | 1 |
| * | unsigned | int16_t | 1 |
| - | MCInstrDesc | unsigned | 1 |
| & | dxbc::PSV::v3::RuntimeInfo | None | 1 |
| & | int | float literal (suffix f) | 1 |
| != | unsigned | integer literal (suffix U) | 1 |
| && | MCSymbol | MCSymbol | 1 |
| >= | unsigned | uint16_t | 1 |
| * | int16_t | None | 1 |
| ++ | int16_t | None | 1 |
| ! | int16_t | None | 1 |
| * | MCSubRegIterator | None | 1 |
| ++ | MCSubRegIterator | None | 1 |
| * | MCRegUnitIterator | None | 1 |
| * | LaneBitmask | None | 1 |
| ++ | LaneBitmask | None | 1 |
| ++ | MCRegUnitIterator | None | 1 |
| -- | MCPhysReg | None | 1 |
| != | MCPhysReg | MCPhysReg | 1 |
| * | MCPhysReg | None | 1 |
| ++ | MCPhysReg | None | 1 |
| != | Type | integer literal | 1 |
| * | MCSymbol | None | 1 |
| != | MCReadAdvanceEntry | MCReadAdvanceEntry | 1 |
| ++ | MCReadAdvanceEntry | None | 1 |
| * | std::unique_ptr<MCAssembler> | None | 1 |
| && | std::optional<XCOFF::StorageClass> | string literal | 1 |
| * | std::optional<XCOFF::StorageClass> | None | 1 |
| * | std::optional<CodeModel> | None | 1 |
| | | uint8_t | integer literal | 1 |
| != | InstrStage | InstrStage | 1 |
| ++ | InstrStage | None | 1 |
| || | std::optional<unsigned> | std::optional<unsigned> | 1 |
| - | std::optional<unsigned> | std::optional<unsigned> | 1 |
| > | std::optional<unsigned> | integer literal (suffix u) | 1 |
| & | MCSubtargetInfo | None | 1 |
| + | uint32_t | uint32_t | 1 |
| & | MCExpr | None | 1 |
| * | MCExpr | None | 1 |
| * | MCFragment | None | 1 |

**excerpts, resolved**
- `/sources/llvm-project/llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp:95` operator `!=` operand types ['unsigned', 'unsigned'] resolved against ['/sources/llvm-project/llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp:95', '/sources/llvm-project/llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp:95']
- `/sources/llvm-project/llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp:95` operator `++` operand types ['unsigned'] resolved against ['/sources/llvm-project/llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp:95']
- `/sources/llvm-project/llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp:169` operator `++` operand types ['unsigned'] resolved against ['/sources/llvm-project/llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp:169']

**excerpts, unresolved**
- `/sources/llvm-project/llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp:83` operator `||` reason: call result
- `/sources/llvm-project/llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp:97` operator `!` reason: call result
- `/sources/llvm-project/llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp:107` operator `==` reason: call result
- `/sources/llvm-project/llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp:137` operator `&&` reason: other (binary_expression)
- `/sources/llvm-project/llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp:137` operator `<=` reason: other (binary_expression)
- `/sources/llvm-project/llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp:137` operator `+` reason: other (binary_expression)

## go (cmd/compile)

**unresolved histogram**

| reason | sites | share |
|---|---|---|
| member access | 24894 | 0.309 |
| inferred binding | 19054 | 0.236 |
| other (binary_expression) | 16826 | 0.209 |
| call result | 15711 | 0.195 |
| declared in another file or not found | 2067 | 0.026 |
| other (nil) | 826 | 0.01 |
| index expression | 763 | 0.009 |
| nested operator, mixed operand types | 478 | 0.006 |
| other (iota) | 44 | 0.001 |
| other (type_instantiation_expression) | 2 | 0.0 |

**resolved variants** (full table; log_210 carries the first 20)

| operator | lhs type | rhs type | sites |
|---|---|---|---|
| - | integer literal | None | 7225 |
| ! | bool | None | 1436 |
| != | int64 | integer literal | 677 |
| != | int16 | integer literal | 432 |
| != | int8 | integer literal | 420 |
| << | integer literal | integer literal | 386 |
| != | int32 | integer literal | 349 |
| && | bool | bool | 303 |
| || | bool | bool | 292 |
| != | uint64 | integer literal | 210 |
| == | T | T | 192 |
| <= | T | T | 192 |
| < | T | T | 192 |
| != | T | T | 192 |
| >= | T | T | 192 |
| > | T | T | 192 |
| != | uint32 | integer literal | 139 |
| != | uint16 | integer literal | 130 |
| != | uint8 | integer literal | 124 |
| & | operand | None | 110 |
| & | bytes.Buffer | None | 109 |
| + | string literal | string literal | 109 |
| + | int64 | int64 | 102 |
| - | int64 | int64 | 97 |
| >= | int64 | int64 | 89 |
| > | int64 | int64 | 87 |
| * | int64 | int64 | 86 |
| - | integer literal | integer literal | 85 |
| < | int64 | int64 | 85 |
| != | int64 | int64 | 84 |
| < | int64 | integer literal | 83 |
| == | int64 | int64 | 82 |
| <= | int64 | int64 | 81 |
| + | integer literal | integer literal | 76 |
| / | int64 | int64 | 75 |
| % | int64 | int64 | 75 |
| + | int32 | int32 | 69 |
| == | int64 | integer literal | 68 |
| >= | int64 | integer literal | 67 |
| == | string | string literal | 63 |
| - | int64 | integer literal | 62 |
| + | int64 | integer literal | 59 |
| & | strings.Builder | None | 57 |
| * | int8 | int8 | 56 |
| - | int16 | int16 | 55 |
| - | int8 | int8 | 55 |
| + | string literal | string | 54 |
| + | int | integer literal | 53 |
| + | int16 | int16 | 52 |
| + | int8 | int8 | 52 |
| <= | int64 | integer literal | 50 |
| + | string | string literal | 50 |
| * | int16 | int16 | 50 |
| != | int16 | int16 | 50 |
| > | int16 | int16 | 50 |
| == | int16 | int16 | 49 |
| < | int16 | int16 | 49 |
| <= | int16 | int16 | 49 |
| >= | int16 | int16 | 49 |
| == | int8 | int8 | 49 |
| != | int8 | int8 | 49 |
| < | int8 | int8 | 49 |
| > | int8 | int8 | 49 |
| <= | int8 | int8 | 49 |
| >= | int8 | int8 | 49 |
| - | uint64 | integer literal | 47 |
| - | int32 | int32 | 46 |
| > | int64 | integer literal | 45 |
| != | string | string literal | 44 |
| / | int16 | int16 | 43 |
| % | int16 | int16 | 43 |
| / | int8 | int8 | 43 |
| % | int8 | int8 | 43 |
| == | int | integer literal | 42 |
| < | int | integer literal | 40 |
| % | int64 | integer literal | 38 |
| << | int64 | uint64 | 38 |
| >> | int64 | uint64 | 38 |
| == | uint64 | integer literal | 37 |
| < | int32 | integer literal | 37 |
| * | int32 | int32 | 37 |
| != | int32 | int32 | 37 |
| * | int64 | integer literal | 36 |
| == | int32 | int32 | 36 |
| < | int32 | int32 | 36 |
| > | int32 | int32 | 36 |
| <= | int32 | int32 | 36 |
| >= | int32 | int32 | 36 |
| / | uint64 | integer literal | 33 |
| * | integer literal | integer literal | 33 |
| % | uint64 | integer literal | 33 |
| + | uint64 | uint64 | 32 |
| * | integer literal | int64 | 32 |
| / | int32 | int32 | 31 |
| % | int32 | int32 | 31 |
| >= | int32 | integer literal | 31 |
| != | int | integer literal | 30 |
| << | int64 | uint16 | 30 |
| >> | int64 | uint16 | 30 |
| << | int64 | uint8 | 30 |
| >> | int64 | uint8 | 30 |
| << | int16 | uint64 | 30 |
| >> | int16 | uint64 | 30 |
| << | int8 | uint64 | 30 |
| >> | int8 | uint64 | 30 |
| >= | uint64 | integer literal | 30 |
| < | uint64 | integer literal | 29 |
| << | int64 | uint32 | 29 |
| >> | int64 | uint32 | 29 |
| >> | int32 | uint8 | 29 |
| <= | uint64 | integer literal | 28 |
| > | uint64 | integer literal | 28 |
| == | int32 | integer literal | 28 |
| * | int | integer literal | 27 |
| & | Info | None | 26 |
| != | float32 | float32 | 26 |
| * | int32 | integer literal | 26 |
| << | int32 | uint64 | 26 |
| >> | int32 | uint64 | 26 |
| & | V | None | 26 |
| * | integer literal | int32 | 25 |
| <= | int32 | integer literal | 25 |
| > | int32 | integer literal | 25 |
| + | integer literal | float literal (suffix i) | 24 |
| << | int16 | uint16 | 24 |
| >> | int16 | uint16 | 24 |
| << | int16 | uint8 | 24 |
| >> | int16 | uint8 | 24 |
| << | int8 | uint16 | 24 |
| >> | int8 | uint16 | 24 |
| << | int8 | uint8 | 24 |
| >> | int8 | uint8 | 24 |
| - | uint64 | uint64 | 23 |
| - | float literal | None | 23 |
| == | rune | char literal | 23 |
| << | int16 | uint32 | 23 |
| >> | int16 | uint32 | 23 |
| << | int8 | uint32 | 23 |
| >> | int8 | uint32 | 23 |
| ^ | integer literal | None | 22 |
| * | integer literal | uint64 | 22 |
| == | uint32 | integer literal | 22 |
| * | *string | None | 22 |
| + | uint16 | uint16 | 22 |
| + | uint8 | uint8 | 22 |
| * | uint64 | integer literal | 22 |
| % | int16 | integer literal | 22 |
| < | uint32 | integer literal | 21 |
| > | uint32 | integer literal | 21 |
| << | int32 | uint32 | 21 |
| >> | int32 | uint32 | 21 |
| << | int32 | uint16 | 21 |
| >> | int32 | uint16 | 21 |
| << | int32 | uint8 | 21 |
| << | uint64 | uint64 | 20 |
| >> | uint64 | uint64 | 20 |
| != | float64 | float64 | 20 |
| <= | uint32 | integer literal | 20 |
| >= | uint32 | integer literal | 20 |
| - | int | integer literal | 19 |
| & | int64 | integer literal | 19 |
| < | float64 | float64 | 19 |
| < | float32 | float32 | 19 |
| * | uint64 | uint64 | 19 |
| >> | uint32 | uint8 | 19 |
| < | uint64 | uint64 | 19 |
| >> | uint32 | integer literal | 19 |
| * | uint32 | integer literal | 19 |
| * | integer literal | uint32 | 19 |
| + | integer literal | None | 18 |
| <= | float64 | float64 | 18 |
| == | float64 | float64 | 18 |
| >= | float64 | float64 | 18 |
| > | float64 | float64 | 18 |
| <= | float32 | float32 | 18 |
| == | float32 | float32 | 18 |
| >= | float32 | float32 | 18 |
| > | float32 | float32 | 18 |
| >> | uint | integer literal | 18 |
| & | types.Sym | None | 17 |
| < | int | int | 17 |
| > | int | integer literal | 17 |
| - | integer literal | int64 | 17 |
| & | ir.Nodes | None | 17 |
| >> | uint64 | integer literal | 17 |
| << | uint32 | uint8 | 17 |
| != | uint64 | uint64 | 17 |
| & | int16 | integer literal | 16 |
| == | uint64 | uint64 | 16 |
| > | uint64 | uint64 | 16 |
| <= | uint64 | uint64 | 16 |
| >= | uint64 | uint64 | 16 |
| << | uint32 | integer literal | 16 |
| < | int16 | integer literal | 16 |
| <= | int16 | integer literal | 16 |
| > | int16 | integer literal | 16 |
| >= | int16 | integer literal | 16 |
| == | int16 | integer literal | 16 |
| / | uint64 | uint64 | 15 |
| % | uint64 | uint64 | 15 |
| * | *ir.Node | None | 14 |
| >> | uint64 | uint32 | 14 |
| >> | uint64 | uint16 | 14 |
| >> | uint64 | uint8 | 14 |
| >> | uint32 | uint64 | 14 |
| >> | uint16 | uint64 | 14 |
| >> | uint8 | uint64 | 14 |
| % | int8 | integer literal | 14 |
| & | int | None | 13 |
| & | Bar | None | 13 |
| + | integer literal | int64 | 13 |
| >> | uint32 | uint32 | 13 |
| - | float64 | float64 | 13 |
| < | uint16 | integer literal | 13 |
| <= | uint16 | integer literal | 13 |
| > | uint16 | integer literal | 13 |
| >= | uint16 | integer literal | 13 |
| == | uint16 | integer literal | 13 |
| & | syntax.BlockStmt | None | 12 |
| * | **types.Field | None | 12 |
| * | *int | None | 12 |
| & | int64 | int64 | 12 |
| ^ | int32 | None | 12 |
| << | uint64 | uint32 | 12 |
| << | uint64 | uint16 | 12 |
| << | uint64 | uint8 | 12 |
| << | uint32 | uint64 | 12 |
| << | uint16 | uint64 | 12 |
| << | uint8 | uint64 | 12 |
| << | uint64 | integer literal | 12 |
| - | integer literal | uint | 12 |
| / | integer literal | integer literal | 12 |
| * | *uint32 | None | 11 |
| & | uint64 | integer literal | 11 |
| + | int | int | 11 |
| * | uint32 | uint32 | 11 |
| > | uint32 | uint32 | 11 |
| - | uint32 | uint32 | 11 |
| | | int64 | int64 | 11 |
| | | int64 | integer literal | 11 |
| ^ | int64 | integer literal | 11 |
| >> | uint32 | uint16 | 11 |
| >> | uint16 | uint32 | 11 |
| >> | uint16 | uint16 | 11 |
| >> | uint16 | uint8 | 11 |
| >> | uint8 | uint32 | 11 |
| >> | uint8 | uint16 | 11 |
| >> | uint8 | uint8 | 11 |
| == | uint32 | uint32 | 11 |
| >> | int32 | integer literal | 11 |
| ^ | integer literal | int64 | 11 |
| - | uint | integer literal | 11 |
| & | obj.LSym | None | 10 |
| & | syntax.ReturnStmt | None | 10 |
| & | Config | None | 10 |
| & | int8 | None | 10 |
| ^ | int64 | int64 | 10 |
| | | int32 | int32 | 10 |
| & | int32 | int32 | 10 |
| | | int16 | int16 | 10 |
| & | int16 | int16 | 10 |
| | | int8 | int8 | 10 |
| & | int8 | int8 | 10 |
| + | uint32 | uint32 | 10 |
| - | uint16 | uint16 | 10 |
| * | uint16 | uint16 | 10 |
| - | uint8 | uint8 | 10 |
| * | uint8 | uint8 | 10 |
| << | uint32 | uint32 | 10 |
| != | uint32 | uint32 | 10 |
| < | uint32 | uint32 | 10 |
| != | uint16 | uint16 | 10 |
| + | float literal | float literal (suffix i) | 10 |
| % | int32 | integer literal | 10 |
| & | registerCursor | None | 10 |
| << | uint8 | integer literal | 9 |
| - | int | int | 9 |
| & | syntax.CallExpr | None | 9 |
| != | rune | char literal | 9 |
| >= | *obj.Prog | integer literal | 9 |
| / | int64 | integer literal | 9 |
| & | pairWant | None | 9 |
| ^ | int32 | int32 | 9 |
| | | int16 | integer literal | 9 |
| ^ | int16 | int16 | 9 |
| ^ | int16 | integer literal | 9 |
| | | int8 | integer literal | 9 |
| & | int8 | integer literal | 9 |
| ^ | int8 | int8 | 9 |
| ^ | int8 | integer literal | 9 |
| + | int8 | integer literal | 9 |
| << | uint32 | uint16 | 9 |
| << | uint16 | uint32 | 9 |
| << | uint16 | uint16 | 9 |
| << | uint16 | uint8 | 9 |
| << | uint8 | uint32 | 9 |
| << | uint8 | uint16 | 9 |
| << | uint8 | uint8 | 9 |
| <= | uint32 | uint32 | 9 |
| >= | uint32 | uint32 | 9 |
| == | uint16 | uint16 | 9 |
| < | uint16 | uint16 | 9 |
| > | uint16 | uint16 | 9 |
| <= | uint16 | uint16 | 9 |
| >= | uint16 | uint16 | 9 |
| == | uint8 | uint8 | 9 |
| != | uint8 | uint8 | 9 |
| < | uint8 | uint8 | 9 |
| > | uint8 | uint8 | 9 |
| <= | uint8 | uint8 | 9 |
| >= | uint8 | uint8 | 9 |
| >> | uint16 | integer literal | 9 |
| / | integer literal | int64 | 9 |
| % | integer literal | int64 | 9 |
| & | integer literal | int64 | 9 |
| | | integer literal | int64 | 9 |
| * | *LocalSlot | None | 9 |
| <= | int | integer literal | 8 |
| & | syntax.SelectorExpr | None | 8 |
| & | syntax.AssignStmt | None | 8 |
| > | uint8 | integer literal | 8 |
| & | string | None | 8 |
| / | float literal | integer literal | 8 |
| | | int32 | integer literal | 8 |
| & | int32 | integer literal | 8 |
| ^ | int32 | integer literal | 8 |
| + | int32 | integer literal | 8 |
| + | int16 | integer literal | 8 |
| * | int16 | integer literal | 8 |
| * | int8 | integer literal | 8 |
| << | int64 | integer literal | 8 |
| - | int16 | integer literal | 8 |
| - | int8 | integer literal | 8 |
| * | integer literal | int8 | 8 |
| >> | int | integer literal | 8 |
| & | Func | None | 7 |
| - | integer literal | int | 7 |
| <= | integer literal | int64 | 7 |
| / | uint32 | uint32 | 7 |
| % | uint32 | uint32 | 7 |
| / | uint16 | uint16 | 7 |
| % | uint16 | uint16 | 7 |
| / | uint8 | uint8 | 7 |
| % | uint8 | uint8 | 7 |
| >> | int64 | integer literal | 7 |
| >> | uint8 | integer literal | 7 |
| - | integer literal | uint64 | 7 |
| - | int32 | integer literal | 7 |
| + | integer literal | int16 | 7 |
| - | integer literal | int16 | 7 |
| / | integer literal | int16 | 7 |
| * | integer literal | int16 | 7 |
| % | integer literal | int16 | 7 |
| & | integer literal | int16 | 7 |
| | | integer literal | int16 | 7 |
| ^ | integer literal | int16 | 7 |
| + | integer literal | int8 | 7 |
| - | integer literal | int8 | 7 |
| / | integer literal | int8 | 7 |
| % | integer literal | int8 | 7 |
| & | integer literal | int8 | 7 |
| | | integer literal | int8 | 7 |
| ^ | integer literal | int8 | 7 |
| < | uint8 | integer literal | 7 |
| <= | uint8 | integer literal | 7 |
| >= | uint8 | integer literal | 7 |
| == | uint8 | integer literal | 7 |
| < | int8 | integer literal | 7 |
| <= | int8 | integer literal | 7 |
| > | int8 | integer literal | 7 |
| >= | int8 | integer literal | 7 |
| == | int8 | integer literal | 7 |
| + | uint64 | integer literal | 6 |
| & | uint8 | integer literal | 6 |
| * | *ir.Nodes | None | 6 |
| * | *syntax.Expr | None | 6 |
| * | *constant.Value | None | 6 |
| <= | integer literal | constant.Value | 6 |
| & | int64 | None | 6 |
| ^ | int64 | None | 6 |
| & | uint32 | integer literal | 6 |
| + | integer literal | int32 | 6 |
| - | integer literal | int32 | 6 |
| / | integer literal | int32 | 6 |
| % | integer literal | int32 | 6 |
| & | integer literal | int32 | 6 |
| | | integer literal | int32 | 6 |
| ^ | integer literal | int32 | 6 |
| / | int16 | integer literal | 6 |
| / | int8 | integer literal | 6 |
| + | integer literal | int | 6 |
| & | AuxCall | None | 6 |
| == | *Value | *Value | 6 |
| & | Value | None | 6 |
| & | State | None | 5 |
| & | int | integer literal | 5 |
| & | syntax.VarDecl | None | 5 |
| & | syntax.BasicLit | None | 5 |
| & | syntax.ExprStmt | None | 5 |
| & | syntax.IfStmt | None | 5 |
| & | syntax.ListExpr | None | 5 |
| <= | char literal | rune | 5 |
| <= | rune | char literal | 5 |
| & | int32 | None | 5 |
| & | *types.Field | None | 5 |
| & | obj.Prog | None | 5 |
| & | types.Type | None | 5 |
| + | string | string | 5 |
| != | int | int | 5 |
| & | runtime.MemStats | None | 5 |
| << | integer literal | uint32 | 5 |
| & | Slice | None | 5 |
| & | declInfo | None | 5 |
| < | uint | integer literal | 5 |
| % | int | integer literal | 5 |
| << | uint16 | integer literal | 5 |
| + | integer literal | uint64 | 5 |
| / | integer literal | uint64 | 5 |
| << | integer literal | uint64 | 5 |
| >> | integer literal | uint64 | 5 |
| % | integer literal | uint64 | 5 |
| & | integer literal | uint64 | 5 |
| | | uint64 | integer literal | 5 |
| | | integer literal | uint64 | 5 |
| ^ | uint64 | integer literal | 5 |
| ^ | integer literal | uint64 | 5 |
| / | int32 | integer literal | 5 |
| & | B | None | 5 |
| ^ | int | integer literal | 5 |
| & | T | None | 5 |
| * | *int64 | None | 4 |
| != | *ssa.Value | *ssa.Value | 4 |
| > | int | int | 4 |
| & | syntax.DeclStmt | None | 4 |
| / | int | integer literal | 4 |
| & | reader | None | 4 |
| & | types2.Config | None | 4 |
| << | integer literal | uint8 | 4 |
| >= | int | integer literal | 4 |
| & | obj.Link | None | 4 |
| & | obj.LinkArch | None | 4 |
| & | sys.Arch | None | 4 |
| * | integer literal | int | 4 |
| & | Array | None | 4 |
| * | *[]*Type | None | 4 |
| & | IRNode | None | 4 |
| - | int | None | 4 |
| * | int | int | 4 |
| == | uint | integer literal | 4 |
| & | block | None | 4 |
| & | Union | None | 4 |
| == | Type | Type | 4 |
| & | Pointer | None | 4 |
| & | Signature | None | 4 |
| & | _TypeSet | None | 4 |
| & | int16 | None | 4 |
| - | int64 | None | 4 |
| ^ | int8 | None | 4 |
| + | float64 | float literal | 4 |
| * | float64 | float64 | 4 |
| - | integer literal | uint32 | 4 |
| % | uint32 | integer literal | 4 |
| % | uint16 | integer literal | 4 |
| % | uint8 | integer literal | 4 |
| * | *[2]byte | None | 4 |
| * | *[3]byte | None | 4 |
| * | *[4]byte | None | 4 |
| * | *[5]byte | None | 4 |
| * | *[6]byte | None | 4 |
| * | *[7]byte | None | 4 |
| & | integer literal | integer literal | 4 |
| * | *uint16 | None | 4 |
| & | MyInt | None | 4 |
| & | regInfo | None | 4 |
| == | *Block | *Block | 4 |
| << | integer literal | int64 | 4 |
| < | register | integer literal | 4 |
| - | register | integer literal | 4 |
| * | **Value | None | 4 |
| - | int8 | None | 3 |
| & | intrinsicBuildConfig | None | 3 |
| * | *types2.Type | None | 3 |
| + | float literal | None | 3 |
| & | Name | None | 3 |
| == | *Func | *Func | 3 |
| & | ir.ReassignOracle | None | 3 |
| == | *types.Type | *types.Type | 3 |
| * | **types.Type | None | 3 |
| / | integer literal | int | 3 |
| & | dwarf.Var | None | 3 |
| == | int | int | 3 |
| + | uint | integer literal | 3 |
| & | ifacePair | None | 3 |
| & | Interface | None | 3 |
| & | TypeParamList | None | 3 |
| == | byte | char literal | 3 |
| * | *operand | None | 3 |
| == | any | any | 3 |
| ^ | int16 | None | 3 |
| & | uint64 | None | 3 |
| << | int32 | integer literal | 3 |
| << | int16 | integer literal | 3 |
| >> | int16 | integer literal | 3 |
| << | int8 | integer literal | 3 |
| >> | int8 | integer literal | 3 |
| * | float32 | float32 | 3 |
| != | complex128 | complex128 | 3 |
| + | uint32 | integer literal | 3 |
| + | integer literal | uint32 | 3 |
| - | uint32 | integer literal | 3 |
| / | integer literal | uint32 | 3 |
| >> | integer literal | uint32 | 3 |
| % | integer literal | uint32 | 3 |
| & | integer literal | uint32 | 3 |
| | | uint32 | integer literal | 3 |
| | | integer literal | uint32 | 3 |
| ^ | uint32 | integer literal | 3 |
| ^ | integer literal | uint32 | 3 |
| + | uint16 | integer literal | 3 |
| + | integer literal | uint16 | 3 |
| - | uint16 | integer literal | 3 |
| - | integer literal | uint16 | 3 |
| / | integer literal | uint16 | 3 |
| * | uint16 | integer literal | 3 |
| * | integer literal | uint16 | 3 |
| << | integer literal | uint16 | 3 |
| >> | integer literal | uint16 | 3 |
| % | integer literal | uint16 | 3 |
| & | uint16 | integer literal | 3 |
| & | integer literal | uint16 | 3 |
| | | uint16 | integer literal | 3 |
| | | integer literal | uint16 | 3 |
| ^ | uint16 | integer literal | 3 |
| ^ | integer literal | uint16 | 3 |
| + | uint8 | integer literal | 3 |
| + | integer literal | uint8 | 3 |
| - | uint8 | integer literal | 3 |
| - | integer literal | uint8 | 3 |
| / | integer literal | uint8 | 3 |
| * | uint8 | integer literal | 3 |
| * | integer literal | uint8 | 3 |
| >> | integer literal | uint8 | 3 |
| % | integer literal | uint8 | 3 |
| & | integer literal | uint8 | 3 |
| | | uint8 | integer literal | 3 |
| | | integer literal | uint8 | 3 |
| ^ | uint8 | integer literal | 3 |
| ^ | integer literal | uint8 | 3 |
| * | *[1]byte | None | 3 |
| * | *[8]byte | None | 3 |
| * | *[9]byte | None | 3 |
| * | *[10]byte | None | 3 |
| * | *[15]byte | None | 3 |
| * | *[16]byte | None | 3 |
| * | *[17]byte | None | 3 |
| * | *[23]byte | None | 3 |
| * | *[24]byte | None | 3 |
| * | *[25]byte | None | 3 |
| * | *[31]byte | None | 3 |
| * | *[32]byte | None | 3 |
| * | *[33]byte | None | 3 |
| * | *[63]byte | None | 3 |
| * | *[64]byte | None | 3 |
| * | *[65]byte | None | 3 |
| * | *[1023]byte | None | 3 |
| * | *[1024]byte | None | 3 |
| * | *[1025]byte | None | 3 |
| ^ | integer literal | integer literal | 3 |
| & | uint64 | uint64 | 3 |
| & | tstAux | None | 3 |
| & | AuxNameOffset | None | 3 |
| << | integer literal | uint | 3 |
| != | *Block | *Block | 3 |
| << | integer literal | register | 3 |
| & | Case | None | 3 |
| & | ABIParamResultInfo | None | 2 |
| & | sparseSet | None | 2 |
| == | skipMask | integer literal | 2 |
| & | uint32 | None | 2 |
| & | MergeLocalsState | None | 2 |
| & | syntax.ImportDecl | None | 2 |
| & | syntax.SwitchStmt | None | 2 |
| & | syntax.CaseClause | None | 2 |
| & | syntax.FuncLit | None | 2 |
| & | syntax.Operation | None | 2 |
| & | syntax.InterfaceType | None | 2 |
| & | syntax.FuncType | None | 2 |
| & | syntax.BranchStmt | None | 2 |
| == | Node | Node | 2 |
| == | string | string | 2 |
| & | ast.Ident | None | 2 |
| & | typeSig | None | 2 |
| == | *uint32 | integer literal | 2 |
| >> | *obj.Prog | integer literal | 2 |
| * | *types2.Package | None | 2 |
| != | types2.ImportMode | integer literal | 2 |
| <= | char literal | byte | 2 |
| <= | byte | char literal | 2 |
| & | ir.Inline | None | 2 |
| & | types2.Info | None | 2 |
| & | covcmd.CoverFixupConfig | None | 2 |
| & | Type | None | 2 |
| == | *Pkg | *Pkg | 2 |
| & | Sym | None | 2 |
| & | dwarf.InlCalls | None | 2 |
| & | dwarf.LineEntry | None | 2 |
| & | IREdge | None | 2 |
| & | scoreAdjustTyp | scoreAdjustTyp | 2 |
| & | FuncProps | None | 2 |
| & | inlClosureState | None | 2 |
| * | Expr | None | 2 |
| & | PosBase | None | 2 |
| << | int | integer literal | 2 |
| & | Map[K, V] | None | 2 |
| & | node[K, V] | None | 2 |
| & | Iterator[K, V] | None | 2 |
| & | ArgumentError | None | 2 |
| & | Chan | None | 2 |
| & | Struct | None | 2 |
| & | Map | None | 2 |
| & | Tuple | None | 2 |
| & | typeWriter | None | 2 |
| - | uint | uint | 2 |
| & | StdSizes | None | 2 |
| & | typeError | None | 2 |
| & | Var | None | 2 |
| + | char literal | integer literal | 2 |
| & | Named | None | 2 |
| & | types2.StdSizes | None | 2 |
| * | P | None | 2 |
| >= | float32 | integer literal | 2 |
| * | *T1 | None | 2 |
| * | *T2 | None | 2 |
| * | *A2 | None | 2 |
| * | *A4 | None | 2 |
| * | *A8 | None | 2 |
| & | T1 | None | 2 |
| & | T2 | None | 2 |
| + | float64 | float64 | 2 |
| & | uint | integer literal | 2 |
| != | complex64 | complex64 | 2 |
| - | integer literal | float literal (suffix i) | 2 |
| / | uint32 | integer literal | 2 |
| / | uint16 | integer literal | 2 |
| / | uint8 | integer literal | 2 |
| * | *[1031]byte | None | 2 |
| * | *[1032]byte | None | 2 |
| * | *[1033]byte | None | 2 |
| * | *[1039]byte | None | 2 |
| * | *[1040]byte | None | 2 |
| * | *[1041]byte | None | 2 |
| ^ | uint32 | uint32 | 2 |
| | | integer literal | integer literal | 2 |
| == | int | char literal | 2 |
| * | *V | None | 2 |
| * | *uint64 | None | 2 |
| * | *byte | None | 2 |
| * | *int8 | None | 2 |
| * | *uint8 | None | 2 |
| * | *int16 | None | 2 |
| * | *int32 | None | 2 |
| - | uint64 | None | 2 |
| & | A | None | 2 |
| & | big.Int | None | 2 |
| & | biasedSparseMap | None | 2 |
| << | int64 | int64 | 2 |
| >> | int64 | int64 | 2 |
| == | sliceInfo | sliceInfo | 2 |
| - | integer literal | predIndex | 2 |
| & | liveSlot | None | 2 |
| != | *Value | *Value | 2 |
| * | *Block | None | 2 |
| * | *Value | None | 2 |
| - | T | integer literal | 2 |
| & | nextHist | None | 2 |
| <= | integer literal | int | 2 |
| & | Switch | None | 2 |
| & | RuleRewrite | None | 2 |
| & | object | None | 2 |
| & | Declare | None | 2 |
| & | CondBreak | None | 2 |
| & | ABIConfig | None | 1 |
| & | SymABIs | None | 1 |
| & | nowritebarrierrecChecker | None | 1 |
| & | ssa.FuncDebug | None | 1 |
| & | ssa.AuxNameOffset | None | 1 |
| - | uintptr | integer literal | 1 |
| + | uintptr | uintptr | 1 |
| & | ssa.FuncLines | None | 1 |
| & | backingStoreInfo | None | 1 |
| & | openDeferInfo | None | 1 |
| & | testIntrinsicKey | None | 1 |
| & | Interval | None | 1 |
| == | liveEffect | integer literal | 1 |
| & | Liveness | None | 1 |
| + | string literal | *ssa.Value | 1 |
| & | cstate | None | 1 |
| & | argLiveness | None | 1 |
| & | Analyzer | None | 1 |
| & | Rewriter | None | 1 |
| & | DeepCopier | None | 1 |
| & | syntax.TypeDecl | None | 1 |
| & | syntax.ConstDecl | None | 1 |
| & | syntax.FuncDecl | None | 1 |
| & | syntax.CompositeLit | None | 1 |
| & | syntax.KeyValueExpr | None | 1 |
| & | syntax.ParenExpr | None | 1 |
| & | syntax.IndexExpr | None | 1 |
| & | syntax.SliceExpr | None | 1 |
| & | syntax.AssertExpr | None | 1 |
| & | syntax.TypeSwitchGuard | None | 1 |
| & | syntax.ArrayType | None | 1 |
| & | syntax.SliceType | None | 1 |
| & | syntax.DotsType | None | 1 |
| & | syntax.StructType | None | 1 |
| & | syntax.MapType | None | 1 |
| & | syntax.ChanType | None | 1 |
| & | syntax.BadExpr | None | 1 |
| & | syntax.SendStmt | None | 1 |
| & | syntax.CallStmt | None | 1 |
| & | syntax.ForStmt | None | 1 |
| & | syntax.SelectStmt | None | 1 |
| & | syntax.EmptyStmt | None | 1 |
| & | syntax.LabeledStmt | None | 1 |
| & | syntax.RangeClause | None | 1 |
| & | syntax.CommClause | None | 1 |
| & | syntax.Field | None | 1 |
| & | readerDict | None | 1 |
| * | *[]*types2.TypeParam | None | 1 |
| & | visitor | None | 1 |
| & | AddStringExpr | None | 1 |
| & | AddrExpr | None | 1 |
| & | BasicLit | None | 1 |
| & | BinaryExpr | None | 1 |
| & | CallExpr | None | 1 |
| & | CompLitExpr | None | 1 |
| & | ConvExpr | None | 1 |
| & | IndexExpr | None | 1 |
| & | KeyExpr | None | 1 |
| & | StructKeyExpr | None | 1 |
| & | InlinedCallExpr | None | 1 |
| & | LogicalExpr | None | 1 |
| & | MakeExpr | None | 1 |
| & | NilExpr | None | 1 |
| & | ParenExpr | None | 1 |
| & | ResultExpr | None | 1 |
| & | LinksymOffsetExpr | None | 1 |
| & | SelectorExpr | None | 1 |
| & | SliceExpr | None | 1 |
| & | SliceHeaderExpr | None | 1 |
| & | StringHeaderExpr | None | 1 |
| & | StarExpr | None | 1 |
| & | TypeAssertExpr | None | 1 |
| & | DynamicTypeAssertExpr | None | 1 |
| & | UnaryExpr | None | 1 |
| & | MoveToHeapExpr | None | 1 |
| & | typeNode | None | 1 |
| & | DynamicType | None | 1 |
| & | Decl | None | 1 |
| & | AssignListStmt | None | 1 |
| & | AssignStmt | None | 1 |
| & | AssignOpStmt | None | 1 |
| & | BlockStmt | None | 1 |
| & | BranchStmt | None | 1 |
| & | CaseClause | None | 1 |
| & | CommClause | None | 1 |
| & | ForStmt | None | 1 |
| & | GoDeferStmt | None | 1 |
| & | IfStmt | None | 1 |
| & | JumpTableStmt | None | 1 |
| & | InterfaceSwitchStmt | None | 1 |
| & | InlineMarkStmt | None | 1 |
| & | LabelStmt | None | 1 |
| & | RangeStmt | None | 1 |
| & | ReturnStmt | None | 1 |
| & | SelectStmt | None | 1 |
| & | SendStmt | None | 1 |
| & | SwitchStmt | None | 1 |
| & | TailCallStmt | None | 1 |
| & | TypeSwitchGuard | None | 1 |
| & | BufferedWriterCloser | None | 1 |
| & | ast.ArrayType | None | 1 |
| & | ClosureExpr | None | 1 |
| == | [5]string | [5]string | 1 |
| == | [64]string | [64]string | 1 |
| == | [1024]string | [1024]string | 1 |
| == | [5]float32 | [5]float32 | 1 |
| == | [64]float32 | [64]float32 | 1 |
| == | [1024]float32 | [1024]float32 | 1 |
| & | ir.CaseClause | None | 1 |
| & | ir.Node | None | 1 |
| & | ClosureStructIter | None | 1 |
| & | LoggedOpt | None | 1 |
| == | ir.Node | ir.Node | 1 |
| & | queue | None | 1 |
| & | escape | None | 1 |
| & | note | None | 1 |
| & | location | None | 1 |
| & | WasmImport | None | 1 |
| & | WasmExport | None | 1 |
| & | pkgReader | None | 1 |
| & | ir.WasmImport | None | 1 |
| & | ir.WasmExport | None | 1 |
| & | pkgWriter | None | 1 |
| & | writer | None | 1 |
| & | writerDict | None | 1 |
| != | ir.Op | integer literal | 1 |
| & | declCollector | None | 1 |
| & | fileImports | None | 1 |
| & | profileBuilder | None | 1 |
| & | pgoir.Profile | None | 1 |
| & | pgoir.IRGraph | None | 1 |
| & | pgoir.IRNode | None | 1 |
| & | pgoir.IREdge | None | 1 |
| == | *types.Type | types.Type | 1 |
| != | *types.Type | *types.Type | 1 |
| & | types.Field | None | 1 |
| & | CmdFlags | None | 1 |
| & | event | None | 1 |
| != | time.Duration | integer literal | 1 |
| & | HashDebug | None | 1 |
| & | testTypeName | None | 1 |
| & | Field | None | 1 |
| == | *Sym | *Sym | 1 |
| & | Pkg | None | 1 |
| == | *Type | *Type | 1 |
| & | lexblock | None | 1 |
| & | sliceInfo | None | 1 |
| & | rewriter | None | 1 |
| & | forLoop | None | 1 |
| & | syntax.Name | None | 1 |
| & | Profile | None | 1 |
| & | IRGraph | None | 1 |
| != | scoreAdjustTyp | integer literal | 1 |
| == | scoreAdjustTyp | integer literal | 1 |
| & | dumpReader | None | 1 |
| & | upexState | None | 1 |
| & | resultsAnalyzer | None | 1 |
| & | nameFinder | None | 1 |
| == | *ir.Name | *ir.Name | 1 |
| & | funcFlagsAnalyzer | None | 1 |
| & | exprClassifier | None | 1 |
| & | paramsAnalyzer | None | 1 |
| & | callSiteAnalyzer | None | 1 |
| & | callSiteTableBuilder | None | 1 |
| & | CallSite | None | 1 |
| & | state | None | 1 |
| & | resultUseAnalyzer | None | 1 |
| % | int | int | 1 |
| << | integer literal | int | 1 |
| & | devirtualize.State | None | 1 |
| & | labelScope | None | 1 |
| & | label | None | 1 |
| << | integer literal | token | 1 |
| & | shortBuffer | None | 1 |
| - | token | integer literal | 1 |
| | | char literal | rune | 1 |
| - | char literal | char literal | 1 |
| + | char literal | int | 1 |
| < | *int | integer literal | 1 |
| <= | integer literal | uint32 | 1 |
| == | Form | integer literal | 1 |
| & | printGroup | None | 1 |
| != | token | integer literal | 1 |
| || | y | int | 1 |
| || | int | z | 1 |
| || | bool literal | integer literal | 1 |
| & | Sender[T] | None | 1 |
| & | Receiver[T] | None | 1 |
| - | T | T | 1 |
| & | Term | None | 1 |
| * | **TypeParamList | None | 1 |
| & | unifier | None | 1 |
| != | Type | Type | 1 |
| & | target | None | 1 |
| != | string | string | 1 |
| & | Scope | None | 1 |
| & | lazyObject | None | 1 |
| & | subster | None | 1 |
| * | *Var | None | 1 |
| * | *Func | None | 1 |
| == | Code | integer literal | 1 |
| & | error_ | None | 1 |
| != | Code | integer literal | 1 |
| < | uint | uint | 1 |
| > | uint | uint | 1 |
| * | *term | None | 1 |
| & | TypeParam | None | 1 |
| & | PkgName | None | 1 |
| & | Const | None | 1 |
| & | TypeName | None | 1 |
| & | Label | None | 1 |
| & | Builtin | None | 1 |
| & | TypeList | None | 1 |
| & | Package | None | 1 |
| & | gcimports | None | 1 |
| & | Nil | None | 1 |
| & | instance | None | 1 |
| & | Context | None | 1 |
| & | Initializer | None | 1 |
| & | graphNode | None | 1 |
| & | term | None | 1 |
| & | Selection | None | 1 |
| & | actionDesc | None | 1 |
| & | Checker | None | 1 |
| * | *error | None | 1 |
| > | *operand | integer literal | 1 |
| != | ImportMode | integer literal | 1 |
| & | stdlibChecker | None | 1 |
| & | futurePackage | None | 1 |
| == | *Package | *Package | 1 |
| / | float64 | float literal | 1 |
| > | float64 | integer literal | 1 |
| >= | float64 | integer literal | 1 |
| < | float64 | integer literal | 1 |
| <= | float64 | integer literal | 1 |
| > | float32 | integer literal | 1 |
| < | float32 | integer literal | 1 |
| <= | float32 | integer literal | 1 |
| != | any | any | 1 |
| * | *[16]int | None | 1 |
| - | int32 | None | 1 |
| - | int16 | None | 1 |
| != | *T1 | *T1 | 1 |
| != | *T2 | *T2 | 1 |
| != | *A2 | *A2 | 1 |
| != | *A4 | *A4 | 1 |
| != | *A8 | *A8 | 1 |
| & | A2 | None | 1 |
| & | A4 | None | 1 |
| & | A8 | None | 1 |
| * | *Int | None | 1 |
| << | int64 | int | 1 |
| << | uint64 | int | 1 |
| << | int32 | int | 1 |
| << | uint32 | int | 1 |
| << | int16 | int | 1 |
| << | uint16 | int | 1 |
| << | int8 | int | 1 |
| << | uint8 | int | 1 |
| >> | int64 | int | 1 |
| >> | uint64 | int | 1 |
| >> | int32 | int | 1 |
| >> | uint32 | int | 1 |
| >> | int16 | int | 1 |
| >> | uint16 | int | 1 |
| >> | int8 | int | 1 |
| >> | uint8 | int | 1 |
| / | float64 | float64 | 1 |
| - | float64 | None | 1 |
| * | integer literal | float64 | 1 |
| + | float32 | float32 | 1 |
| - | float32 | float32 | 1 |
| / | float32 | float32 | 1 |
| - | float32 | None | 1 |
| * | integer literal | float32 | 1 |
| + | complex128 | complex128 | 1 |
| - | complex128 | complex128 | 1 |
| * | complex128 | complex128 | 1 |
| / | complex128 | complex128 | 1 |
| - | complex128 | None | 1 |
| + | complex64 | complex64 | 1 |
| - | complex64 | complex64 | 1 |
| * | complex64 | complex64 | 1 |
| / | complex64 | complex64 | 1 |
| - | complex64 | None | 1 |
| == | complex128 | complex128 | 1 |
| == | complex64 | complex64 | 1 |
| / | float literal | float64 | 1 |
| != | bool | bool | 1 |
| & | [2]byte | None | 1 |
| & | [3]byte | None | 1 |
| & | [4]byte | None | 1 |
| & | [5]byte | None | 1 |
| & | [6]byte | None | 1 |
| & | [7]byte | None | 1 |
| & | uint32 | uint32 | 1 |
| | | uint32 | uint32 | 1 |
| | | int | integer literal | 1 |
| & | prefix | None | 1 |
| <= | char literal | int | 1 |
| <= | int | char literal | 1 |
| * | interface{} | None | 1 |
| / | uint | uint | 1 |
| * | *[10]int | None | 1 |
| & | X | None | 1 |
| & | byte | None | 1 |
| & | Add | None | 1 |
| & | Sub | None | 1 |
| & | BS | None | 1 |
| | | uint64 | uint64 | 1 |
| ^ | uint64 | uint64 | 1 |
| * | float64 | integer literal | 1 |
| * | *[]*Value | None | 1 |
| * | *[]limit | None | 1 |
| / | integer literal | float32 | 1 |
| * | *float64 | None | 1 |
| & | sparseMapPos | None | 1 |
| & | pass | None | 1 |
| & | knownBitsState | None | 1 |
| >> | uint64 | uint | 1 |
| & | factsTable | None | 1 |
| & | ordering | None | 1 |
| == | domain | integer literal | 1 |
| & | lcaRange | None | 1 |
| & | slotCanonicalizer | None | 1 |
| & | LocalSlot | None | 1 |
| == | RegisterSet | integer literal | 1 |
| & | lcaEasy | None | 1 |
| & | poset | None | 1 |
| & | Conf | None | 1 |
| & | dotWriter | None | 1 |
| & | use | None | 1 |
| ! | regMask | None | 1 |
| & | desiredState | None | 1 |
| != | T | integer literal | 1 |
| > | T | integer literal | 1 |
| &^ | uint32 | integer literal | 1 |
| &^ | int64 | integer literal | 1 |
| ^ | uint64 | None | 1 |
| == | lattice | lattice | 1 |
| & | expandState | None | 1 |
| - | uint8 | None | 1 |
| ^ | uint8 | None | 1 |
| & | Block | None | 1 |
| & | delveState | None | 1 |
| & | gdbState | None | 1 |
| & | ioState | None | 1 |
| & | xposmap | None | 1 |
| & | genericSparseMap[K, V] | None | 1 |
| & | shadowRanges | None | 1 |
| & | loop | None | 1 |
| & | loopnest | None | 1 |
| & | ExtNode[V] | None | 1 |
| & | thing | None | 1 |
| & | File | None | 1 |
| & | scope | None | 1 |
| & | ast.BinaryExpr | None | 1 |
| & | MultiScanner | None | 1 |
| > | token.Pos | token.Pos | 1 |
| == | token.Pos | token.Pos | 1 |
| + | token.Pos | integer literal | 1 |
| & | struct{ ast.Node } | None | 1 |
| & | application | None | 1 |
| & | ast.ImportSpec | None | 1 |
| & | ast.BasicLit | None | 1 |
| & | ast.GenDecl | None | 1 |
| & | obj.Plist | None | 1 |
| & | sstring | None | 1 |
| & | node32 | None | 1 |

**excerpts, resolved**
- `/sources/golang_src/src/cmd/compile/script_test.go:55` operator `==` operand types ['string', 'string literal'] resolved against ['/sources/golang_src/src/cmd/compile/script_test.go:20']
- `/sources/golang_src/src/cmd/compile/internal/amd64/versions_test.go:353` operator `-` operand types ['integer literal', 'integer literal'] resolved against []
- `/sources/golang_src/src/cmd/compile/internal/amd64/versions_test.go:353` operator `<<` operand types ['integer literal', 'integer literal'] resolved against []

**excerpts, unresolved**
- `/sources/golang_src/src/cmd/compile/internal/amd64/versions_test.go:34` operator `!=` reason: member access
- `/sources/golang_src/src/cmd/compile/internal/amd64/versions_test.go:37` operator `!=` reason: member access
- `/sources/golang_src/src/cmd/compile/internal/amd64/versions_test.go:37` operator `!=` reason: member access
- `/sources/golang_src/src/cmd/compile/main.go:52` operator `!` reason: inferred binding
- `/sources/golang_src/src/cmd/compile/script_test.go:35` operator `==` reason: inferred binding
- `/sources/golang_src/src/cmd/compile/script_test.go:66` operator `*` reason: inferred binding

## go (standard library, rest of checkout)

**unresolved histogram**

| reason | sites | share |
|---|---|---|
| inferred binding | 94454 | 0.34 |
| other (binary_expression) | 48413 | 0.174 |
| call result | 45499 | 0.164 |
| member access | 37817 | 0.136 |
| declared in another file or not found | 33872 | 0.122 |
| index expression | 8984 | 0.032 |
| other (nil) | 4303 | 0.015 |
| nested operator, mixed operand types | 4169 | 0.015 |
| other (iota) | 182 | 0.001 |
| other (comment) | 12 | 0.0 |
| other (func_literal) | 1 | 0.0 |

**resolved variants** (full table; log_210 carries the first 20)

| operator | lhs type | rhs type | sites |
|---|---|---|---|
| - | integer literal | None | 13131 |
| + | string literal | string literal | 6830 |
| << | integer literal | integer literal | 6555 |
| * | integer literal | integer literal | 1479 |
| - | integer literal | integer literal | 1406 |
| == | string | string literal | 1022 |
| & | bytes.Buffer | None | 1008 |
| >> | uint32 | integer literal | 938 |
| | | integer literal | integer literal | 937 |
| & | inst | None | 920 |
| - | float literal | None | 886 |
| == | int | integer literal | 854 |
| ! | bool | None | 738 |
| + | int | integer literal | 629 |
| + | integer literal | integer literal | 566 |
| & | uint32 | integer literal | 530 |
| & | strings.Builder | None | 509 |
| + | string literal | string | 424 |
| - | int | integer literal | 414 |
| != | string | string literal | 402 |
| + | string | string literal | 361 |
| + | integer literal | None | 338 |
| < | int | integer literal | 337 |
| << | uint32 | integer literal | 300 |
| >> | uint64 | integer literal | 287 |
| > | int | integer literal | 283 |
| >> | int64 | integer literal | 267 |
| & | RangeTable | None | 259 |
| & | uint32 | None | 235 |
| & | uint64 | None | 233 |
| & | string | None | 230 |
| / | integer literal | integer literal | 229 |
| & | Int | None | 202 |
| + | float literal | float literal (suffix i) | 184 |
| & | uint8 | integer literal | 179 |
| == | byte | char literal | 170 |
| & | Plain | None | 170 |
| & | argField | None | 167 |
| & | PathError | None | 165 |
| & | uint64 | integer literal | 165 |
| & | int | None | 161 |
| * | *[]byte | None | 141 |
| & | KNOWNFOLDERID | None | 141 |
| < | int64 | integer literal | 137 |
| != | int | integer literal | 136 |
| & | cryptobyte.String | None | 135 |
| & | map[string]interface{} | None | 132 |
| & | OpError | None | 130 |
| * | integer literal | int | 129 |
| << | integer literal | char literal | 119 |
| <= | byte | char literal | 117 |
| << | integer literal | uint | 113 |
| & | operand | None | 112 |
| & | field.Element | None | 112 |
| == | rune | char literal | 108 |
| + | uintptr | uintptr | 108 |
| & | byte | None | 108 |
| + | integer literal | float literal (suffix i) | 106 |
| & | uintptr | None | 106 |
| & | TCPAddr | None | 106 |
| & | Element | None | 106 |
| & | any | None | 104 |
| - | float literal | float literal (suffix i) | 104 |
| & | Header | None | 103 |
| ^ | uint64 | uint64 | 102 |
| <= | char literal | byte | 101 |
| & | UnmarshalTypeError | None | 100 |
| &^ | uint64 | uint64 | 100 |
| << | float literal | uint | 99 |
| * | *int | None | 97 |
| == | int64 | integer literal | 95 |
| & | SyntaxError | None | 93 |
| & | url.URL | None | 92 |
| & | int32 | None | 92 |
| & | RawSockaddrAny | None | 90 |
| & | nestedError | None | 90 |
| <= | int | integer literal | 88 |
| & | int64 | integer literal | 88 |
| - | int | int | 87 |
| & | T | None | 87 |
| == | uint64 | integer literal | 87 |
| & | URL | None | 86 |
| / | int | integer literal | 84 |
| & | Cookie | None | 83 |
| >= | int | integer literal | 79 |
| & | Certificate | None | 78 |
| > | uint32 | integer literal | 77 |
| * | *string | None | 76 |
| + | integer literal | int | 75 |
| + | int | int | 74 |
| & | Config | None | 74 |
| * | *uint64 | None | 73 |
| & | fs.PathError | None | 73 |
| == | uintptr | integer literal | 72 |
| <= | rune | char literal | 70 |
| / | uint | integer literal | 70 |
| - | float64 | None | 68 |
| & | Inst | None | 67 |
| & | analysis.Analyzer | None | 66 |
| & | AddrError | None | 65 |
| == | float64 | integer literal | 64 |
| & | UDPAddr | None | 64 |
| & | Request | None | 64 |
| * | *uint32 | None | 62 |
| & | Error | None | 62 |
| & | P256Point | None | 62 |
| & | ValueError | None | 61 |
| < | float64 | integer literal | 61 |
| == | uint32 | integer literal | 61 |
| >= | int64 | integer literal | 61 |
| & | tls.Config | None | 61 |
| * | *bool | None | 59 |
| <= | char literal | rune | 59 |
| < | int | int | 59 |
| * | int | integer literal | 59 |
| - | char literal | char literal | 57 |
| & | int16 | integer literal | 57 |
| & | DNSError | None | 56 |
| & | Name | None | 56 |
| & | [gcmBlockSize]byte | None | 56 |
| & | FormatError | None | 55 |
| - | integer literal | uint64 | 55 |
| & | bool | None | 54 |
| / | int64 | float literal | 53 |
| & | base.Command | None | 52 |
| & | Scalar | None | 52 |
| + | float literal | None | 51 |
| & | int | integer literal | 51 |
| == | string | string | 50 |
| <= | int64 | integer literal | 50 |
| != | uint32 | integer literal | 49 |
| << | uint64 | integer literal | 49 |
| + | int64 | integer literal | 49 |
| * | *int64 | None | 48 |
| % | int64 | float literal | 48 |
| & | Options | None | 48 |
| % | int | integer literal | 47 |
| & | int64 | None | 47 |
| & | Rat | None | 47 |
| & | runtime.MemStats | None | 46 |
| < | int32 | integer literal | 45 |
| - | uintptr | integer literal | 44 |
| != | int64 | integer literal | 44 |
| & | []byte | None | 44 |
| & | Transport | None | 44 |
| & | syscall.SysProcAttr | None | 43 |
| & | IPAddr | None | 43 |
| && | bool | bool | 42 |
| & | ParseError | None | 41 |
| / | uint32 | integer literal | 41 |
| & | Point | None | 40 |
| / | float literal | integer literal | 40 |
| * | float64 | float64 | 40 |
| & | Buffer | None | 40 |
| & | clientTest | None | 40 |
| != | uint64 | integer literal | 39 |
| > | int64 | integer literal | 39 |
| == | uint8 | integer literal | 39 |
| & | IPNet | None | 39 |
| & | Client | None | 38 |
| % | uint32 | integer literal | 38 |
| & | instruction | None | 38 |
| & | Float | None | 38 |
| & | http.Request | None | 37 |
| & | SemanticError | None | 37 |
| & | PrivateKey | None | 37 |
| & | _Socklen | None | 36 |
| >> | uint16 | integer literal | 36 |
| & | ast.Ident | None | 36 |
| & | Server | None | 36 |
| & | serverTest | None | 36 |
| & | QUICConfig | None | 36 |
| || | bool | bool | 35 |
| * | *baseEvent | None | 35 |
| & | Template | None | 35 |
| - | uint | integer literal | 35 |
| - | int | None | 35 |
| == | uint | integer literal | 34 |
| & | op | None | 34 |
| & | Arch | None | 34 |
| - | uint32 | integer literal | 33 |
| + | float literal | float literal | 33 |
| < | uint32 | integer literal | 32 |
| & | conf | None | 32 |
| != | int32 | integer literal | 32 |
| & | goTest | None | 32 |
| == | integer literal | integer literal | 31 |
| * | *uintptr | None | 31 |
| & | Info | None | 31 |
| % | uintptr | integer literal | 31 |
| << | uint8 | integer literal | 31 |
| & | RevInfo | None | 31 |
| - | int64 | None | 30 |
| & | Profile | None | 30 |
| & | Reader | None | 29 |
| + | string | string | 29 |
| & | _C_int | None | 29 |
| & | http.Client | None | 29 |
| >> | uint8 | integer literal | 29 |
| & | dwarf.DWDie | None | 29 |
| & | jsontext.SyntacticError | None | 29 |
| != | string | string | 28 |
| & | sync.WaitGroup | None | 28 |
| & | oneConnListener | None | 28 |
| <= | integer literal | int16 | 28 |
| <= | int16 | integer literal | 28 |
| & | ast.BadExpr | None | 28 |
| == | int | int | 27 |
| - | integer literal | float literal (suffix i) | 27 |
| <= | uint32 | integer literal | 27 |
| & | dnsConfig | None | 27 |
| & | [32]byte | None | 27 |
| & | obj.Prog | None | 27 |
| & | clientHelloMsg | None | 27 |
| & | FileHeader | None | 26 |
| >= | uint64 | integer literal | 26 |
| & | net.OpError | None | 26 |
| * | *[]string | None | 26 |
| > | int32 | integer literal | 26 |
| & | httptrace.ClientTrace | None | 26 |
| == | int32 | integer literal | 26 |
| & | Args | None | 26 |
| & | ClientHelloInfo | None | 26 |
| & | map[string]any | None | 25 |
| > | uint64 | integer literal | 25 |
| & | Protocols | None | 25 |
| & | mutex | None | 25 |
| + | uint32 | uint32 | 25 |
| & | LinkError | None | 25 |
| & | Qualified | None | 25 |
| & | streamError | None | 25 |
| & | exec.Cmd | None | 24 |
| & | Handler | None | 24 |
| - | uintptr | uintptr | 24 |
| & | ast.BasicLit | None | 24 |
| & | decInstr | None | 24 |
| & | Tree | None | 24 |
| & | Nat | None | 24 |
| == | T | T | 23 |
| != | uint | integer literal | 23 |
| & | Timeval | None | 23 |
| >> | int | integer literal | 23 |
| - | float64 | float64 | 23 |
| + | uint64 | integer literal | 23 |
| == | float literal | float literal | 23 |
| + | uint32 | integer literal | 23 |
| & | sigactiont | None | 23 |
| & | shapes | None | 23 |
| & | PublicKey | None | 23 |
| & | RevocationList | None | 23 |
| << | int | integer literal | 22 |
| == | int | char literal | 22 |
| & | UnixAddr | None | 22 |
| & | sigset | None | 22 |
| + | int32 | integer literal | 22 |
| & | Writer | None | 21 |
| & | sync.Mutex | None | 21 |
| >> | rune | integer literal | 21 |
| - | int64 | integer literal | 21 |
| & | InetAddr | None | 21 |
| ^ | uint32 | None | 21 |
| - | int64 | int64 | 21 |
| != | uintptr | integer literal | 21 |
| * | *byte | None | 21 |
| & | ast.Field | None | 21 |
| & | Special | None | 21 |
| >> | byte | integer literal | 20 |
| & | uintptr | integer literal | 20 |
| > | time.Duration | integer literal | 20 |
| & | parseError | None | 20 |
| * | int | int | 20 |
| & | Builder | None | 20 |
| & | String | None | 20 |
| == | time.Duration | integer literal | 20 |
| < | time.Duration | integer literal | 20 |
| & | exactSig | None | 20 |
| + | int8 | int8 | 20 |
| & | LSym | None | 20 |
| - | int32 | None | 20 |
| & | Action | None | 20 |
| & | dwarf.Entry | None | 20 |
| & | yaml.Node | None | 20 |
| - | float literal | float literal | 20 |
| & | []int | None | 19 |
| & | float64 | None | 19 |
| & | Address | None | 19 |
| & | uint16 | None | 19 |
| - | integer literal | uint8 | 19 |
| + | uint64 | uint64 | 19 |
| <= | uint64 | integer literal | 19 |
| > | float64 | integer literal | 19 |
| <= | integer literal | int | 19 |
| & | persistConn | None | 19 |
| & | http.Response | None | 19 |
| & | ast.FieldList | None | 19 |
| & | PackageError | None | 19 |
| & | Msghdr | None | 18 |
| / | int64 | integer literal | 18 |
| & | syscall.Rlimit | None | 18 |
| & | File | None | 18 |
| << | integer literal | int | 18 |
| & | uint | uint | 18 |
| & | http.Transport | None | 18 |
| * | any | None | 18 |
| & | fileStat | None | 18 |
| & | obj.Addr | None | 18 |
| & | BuiltinType | None | 18 |
| / | integer literal | float64 | 18 |
| & | codeResponse | None | 18 |
| & | jsonwire.ValueFlags | None | 18 |
| & | projP1xP1 | None | 18 |
| >= | byte | char literal | 17 |
| > | int | int | 17 |
| & | HandlerOptions | None | 17 |
| + | char literal | char literal | 17 |
| & | format.Event | None | 17 |
| < | int64 | int64 | 17 |
| & | Resolver | None | 17 |
| & | os.SyscallError | None | 17 |
| & | Response | None | 17 |
| & | writeData | None | 17 |
| & | ReverseProxy | None | 17 |
| * | *sigset | None | 17 |
| & | ast.BlockStmt | None | 17 |
| & | int32 | integer literal | 17 |
| & | ast.StarExpr | None | 17 |
| & | Type | None | 17 |
| >= | float64 | integer literal | 17 |
| & | big.Float | None | 17 |
| * | **node | None | 17 |
| & | x509.Certificate | None | 17 |
| - | byte | char literal | 16 |
| != | uint8 | integer literal | 16 |
| * | *T | None | 16 |
| & | [2]_C_int | None | 16 |
| & | P | None | 16 |
| & | []any | None | 16 |
| != | rune | char literal | 16 |
| - | uint64 | uint64 | 16 |
| + | float64 | float64 | 16 |
| == | gclinkptr | integer literal | 16 |
| % | uint64 | integer literal | 16 |
| + | uint8 | uint8 | 16 |
| + | uint16 | uint16 | 16 |
| & | C.int | None | 16 |
| & | ast.SelectorExpr | None | 16 |
| == | Sym | integer literal | 16 |
| & | ast.CallExpr | None | 16 |
| & | pem.Block | None | 16 |
| & | NumError | None | 16 |
| & | projCached | None | 16 |
| & | affineCached | None | 16 |
| * | *int32 | None | 15 |
| * | *Time_t | None | 15 |
| * | float literal | integer literal | 15 |
| & | wireFormat | None | 15 |
| / | integer literal | float literal | 15 |
| & | uint8 | None | 15 |
| * | integer literal | float literal | 15 |
| + | float64 | integer literal | 15 |
| ^ | integer literal | None | 15 |
| & | stream | None | 15 |
| & | timespec | None | 15 |
| & | os.LinkError | None | 15 |
| << | int64 | integer literal | 15 |
| & | ast.ArrayType | None | 15 |
| & | connectionError | None | 15 |
| & | encInstr | None | 15 |
| & | ir.Instruction | None | 15 |
| & | unsafe.Pointer | None | 14 |
| & | I | None | 14 |
| + | int64 | int64 | 14 |
| & | Iovec | None | 14 |
| * | *Statfs_t | None | 14 |
| & | size | None | 14 |
| * | *error | None | 14 |
| / | float64 | float64 | 14 |
| * | *uint8 | None | 14 |
| << | integer literal | uint8 | 14 |
| % | uint | integer literal | 14 |
| * | *[]uint64 | None | 14 |
| - | rune | char literal | 14 |
| != | byte | char literal | 14 |
| & | http.HTTP2Config | None | 14 |
| & | []string | None | 14 |
| & | Package | None | 14 |
| & | Data | None | 14 |
| & | work.Action | None | 14 |
| & | module.ModuleError | None | 14 |
| & | flag.FlagSet | None | 14 |
| * | float literal | float64 | 14 |
| & | simdType | None | 14 |
| & | InvalidUnmarshalError | None | 14 |
| & | Struct | None | 14 |
| & | ast.BadStmt | None | 14 |
| & | echConfigErr | None | 14 |
| & | syscall.Handle | None | 13 |
| & | IO_STATUS_BLOCK | None | 13 |
| == | float64 | float64 | 13 |
| > | uintptr | integer literal | 13 |
| - | uint64 | integer literal | 13 |
| - | integer literal | int | 13 |
| & | Location | None | 13 |
| <= | rune | integer literal | 13 |
| & | rwTestConn | None | 13 |
| & | serverConn | None | 13 |
| == | byte | integer literal | 13 |
| >= | int32 | integer literal | 13 |
| > | int64 | int64 | 13 |
| & | quick.Config | None | 13 |
| & | T2 | None | 13 |
| & | ast.UnaryExpr | None | 13 |
| & | Block | None | 13 |
| & | module.InvalidVersionError | None | 13 |
| & | RepoRoot | None | 13 |
| & | modinfo.ModulePublic | None | 13 |
| >> | packetNumber | integer literal | 13 |
| & | AResource | None | 13 |
| & | numError | None | 13 |
| != | bool | integer literal | 13 |
| & | byte | integer literal | 12 |
| * | uint32 | integer literal | 12 |
| & | [16]byte | None | 12 |
| & | Loop | None | 12 |
| & | Loopy | None | 12 |
| * | *buffer.Buffer | None | 12 |
| & | FD | None | 12 |
| & | T3 | None | 12 |
| &^ | uint32 | integer literal | 12 |
| * | *[]int64 | None | 12 |
| < | rune | integer literal | 12 |
| <= | integer literal | rune | 12 |
| - | float literal | integer literal | 12 |
| & | dnsmessage.AResource | None | 12 |
| & | _C_struct_addrinfo | None | 12 |
| - | int32 | integer literal | 12 |
| & | maskedSig | None | 12 |
| ^ | uint64 | None | 12 |
| * | *[]arenaIdx | None | 12 |
| & | ast.AssignStmt | None | 12 |
| & | ast.BinaryExpr | None | 12 |
| == | lex.ScanToken | char literal | 12 |
| == | sym.SymKind | integer literal | 12 |
| & | Link | None | 12 |
| & | SegmentHeader | None | 12 |
| + | integer literal | uint32 | 12 |
| & | T1 | None | 12 |
| & | arshaler | None | 12 |
| * | *Mem | None | 12 |
| & | PSSOptions | None | 12 |
| - | byte | integer literal | 11 |
| & | sync.Pool | None | 11 |
| & | abi.RegArgs | None | 11 |
| & | [3]int | None | 11 |
| != | T | T | 11 |
| * | *uint16 | None | 11 |
| & | uint32 | uint32 | 11 |
| >= | rune | integer literal | 11 |
| * | *[][]byte | None | 11 |
| & | uint64 | uint64 | 11 |
| & | Regexp | None | 11 |
| <= | uintptr | integer literal | 11 |
| <= | int64 | int64 | 11 |
| == | P | P | 11 |
| + | uint | uint | 11 |
| != | int | int | 11 |
| & | Conn | None | 11 |
| & | strings.Reader | None | 11 |
| & | nssConf | None | 11 |
| & | io.LimitedReader | None | 11 |
| - | uint32 | uint32 | 11 |
| & | pthreadattr | None | 11 |
| * | int64 | integer literal | 11 |
| & | ast.GenDecl | None | 11 |
| + | char literal | integer literal | 11 |
| & | ast.CompositeLit | None | 11 |
| & | ast.FuncType | None | 11 |
| < | float64 | float literal | 11 |
| & | ast.Comment | None | 11 |
| & | GIF | None | 11 |
| & | S | None | 10 |
| & | V | None | 10 |
| & | slog.HandlerOptions | None | 10 |
| < | T | T | 10 |
| & | [2]int32 | None | 10 |
| & | IPMreqn | None | 10 |
| >= | int | int | 10 |
| - | integer literal | float literal | 10 |
| & | scaler | None | 10 |
| & | slicewriter.WriteSeeker | None | 10 |
| & | ValueType | None | 10 |
| & | F | None | 10 |
| >= | rune | char literal | 10 |
| & | streamListener | None | 10 |
| - | char literal | integer literal | 10 |
| + | int32 | int32 | 10 |
| & | Mutex | None | 10 |
| & | RWMutex | None | 10 |
| >> | int32 | integer literal | 10 |
| & | parseDurationError | None | 10 |
| & | RotateParams | None | 10 |
| != | rune | integer literal | 10 |
| & | Line | None | 10 |
| - | integer literal | float64 | 10 |
| & | entryNotFoundError | None | 10 |
| & | gover.TooNewError | None | 10 |
| & | ImportStack | None | 10 |
| & | DecodingError | None | 10 |
| == | Word | integer literal | 10 |
| & | Embed0a | None | 10 |
| | | byte | byte | 10 |
| + | tab | integer literal | 10 |
| & | errorT | None | 10 |
| & | rsa.PSSOptions | None | 10 |
| & | Digest | None | 10 |
| & | InterfaceMessage | None | 9 |
| & | *uint16 | None | 9 |
| == | uint8 | char literal | 9 |
| & | Stat_t | None | 9 |
| & | Timespec | None | 9 |
| >> | uintptr | integer literal | 9 |
| != | float64 | float64 | 9 |
| > | uint | integer literal | 9 |
| >= | int64 | int64 | 9 |
| * | float literal | float literal | 9 |
| & | [...]int | None | 9 |
| + | byte | char literal | 9 |
| & | sysDialer | None | 9 |
| & | Dialer | None | 9 |
| >= | uint8 | integer literal | 9 |
| / | time.Duration | integer literal | 9 |
| < | byte | integer literal | 9 |
| & | http.Server | None | 9 |
| == | int32 | char literal | 9 |
| & | gList | None | 9 |
| & | *pthreadattr | None | 9 |
| % | int32 | integer literal | 9 |
| < | uint64 | integer literal | 9 |
| & | event | None | 9 |
| > | byte | integer literal | 9 |
| & | ast.ValueSpec | None | 9 |
| == | rune | integer literal | 9 |
| < | uint | integer literal | 9 |
| != | loader.Sym | integer literal | 9 |
| & | C.VkDeviceCreateInfo | None | 9 |
| & | decoder | None | 9 |
| & | encoder | None | 9 |
| & | Origin | None | 9 |
| != | writeCountingDiscard | integer literal | 9 |
| & | LineFile | None | 9 |
| - | float64 | integer literal | 9 |
| != | Reg | Reg | 9 |
| & | MarshalerError | None | 9 |
| & | SHAKE | None | 9 |
| << | byte | integer literal | 8 |
| & | float32 | None | 8 |
| & | [10]int | None | 8 |
| & | B | None | 8 |
| & | replace | None | 8 |
| & | InterfaceAddrMessage | None | 8 |
| * | *WaitStatus | None | 8 |
| & | libcFunc | None | 8 |
| & | IPMreq | None | 8 |
| & | IPv6Mreq | None | 8 |
| & | IPv6MTUInfo | None | 8 |
| & | ICMPv6Filter | None | 8 |
| & | os.ProcAttr | None | 8 |
| > | *uint32 | integer literal | 8 |
| & | win32finddata1 | None | 8 |
| & | stat_t | None | 8 |
| - | uint64 | None | 8 |
| & | syscall.ByHandleFileInformation | None | 8 |
| & | syscall.WSABuf | None | 8 |
| <= | time.Duration | integer literal | 8 |
| * | *orderEventList | None | 8 |
| == | uint16 | integer literal | 8 |
| & | kind | None | 8 |
| & | [128]uint32 | None | 8 |
| | | uint64 | uint64 | 8 |
| & | uint16 | integer literal | 8 |
| + | uint | integer literal | 8 |
| + | T | T | 8 |
| == | float literal (suffix i) | float literal (suffix i) | 8 |
| & | State | None | 8 |
| & | value | None | 8 |
| & | Sample | None | 8 |
| &^ | char literal | char literal | 8 |
| <= | int32 | integer literal | 8 |
| & | sysListener | None | 8 |
| & | dnsmessage.MXResource | None | 8 |
| * | time.Duration | integer literal | 8 |
| & | ClientConn | None | 8 |
| & | unsupportedTEError | None | 8 |
| & | HeadersFrame | None | 8 |
| & | struct{} | None | 8 |
| >= | uint | integer literal | 8 |
| & | libFunc | None | 8 |
| & | libcall | None | 8 |
| & | types.Info | None | 8 |
| / | uintptr | integer literal | 8 |
| & | stackScanState | None | 8 |
| & | Ptr | None | 8 |
| & | User | None | 8 |
| <= | Duration | integer literal | 8 |
| & | tokens | None | 8 |
| * | *[]rune | None | 8 |
| != | int16 | integer literal | 8 |
| & | XcoffSymEnt64 | None | 8 |
| & | List | None | 8 |
| & | Stat_LE_t | None | 8 |
| <= | int | int | 8 |
| & | ast.ParenExpr | None | 8 |
| & | ast.IndexExpr | None | 8 |
| & | Prefix | integer literal | 8 |
| & | MethodWithQualifiers | None | 8 |
| & | modinfo.ModuleError | None | 8 |
| & | LineEntry | None | 8 |
| & | Rela64 | None | 8 |
| >= | float64 | float literal | 8 |
| == | Reg | Reg | 8 |
| < | T | integer literal | 8 |
| ^ | int32 | int32 | 8 |
| & | Value | None | 8 |
| & | Embed0b | None | 8 |
| & | SyntacticError | None | 8 |
| * | *nocaseString | None | 8 |
| * | encoding.TextMarshaler | None | 8 |
| & | Port | None | 8 |
| * | reflect.Value | None | 8 |
| & | Stmt | None | 8 |
| & | Signature | None | 8 |
| & | *C.GO_BIGNUM | None | 8 |
| & | GCM | None | 8 |
| & | [gcmTagSize]byte | None | 8 |
| & | S1 | None | 7 |
| & | S2 | None | 7 |
| / | uint64 | integer literal | 7 |
| * | *Timeval | None | 7 |
| & | ProcAttr | None | 7 |
| & | syscall.Credential | None | 7 |
| * | uint64 | uint64 | 7 |
| < | float64 | float64 | 7 |
| < | string | string | 7 |
| < | uint64 | uint64 | 7 |
| & | Encoder | None | 7 |
| & | myStruct | None | 7 |
| * | P | None | 7 |
| & | Interface | None | 7 |
| * | uint | integer literal | 7 |
| & | coverage.FuncDesc | None | 7 |
| & | MapFile | None | 7 |
| & | syscall.SockaddrInet4 | None | 7 |
| & | timeoutError | None | 7 |
| & | pipe | None | 7 |
| & | ServerInfo | None | 7 |
| * | *Header | None | 7 |
| & | recordingTransport | None | 7 |
| & | ProtocolError | None | 7 |
| & | func() | None | 7 |
| & | fakeFileInfo | None | 7 |
| & | ClientRequest | None | 7 |
| & | PriorityUpdateFrame | None | 7 |
| & | ClientTrace | None | 7 |
| & | *m | None | 7 |
| & | *byte | None | 7 |
| > | float64 | float literal | 7 |
| == | *int | integer literal | 7 |
| & | BytesKey | None | 7 |
| & | ast.EmptyStmt | None | 7 |
| - | integer literal | uint | 7 |
| & | obj.Reloc | None | 7 |
| & | obj.LSym | None | 7 |
| & | dwarf.LineEntry | None | 7 |
| & | IMAGE_EXPORT_DIRECTORY | None | 7 |
| * | *[]stackCheckChain | None | 7 |
| & | Termios | None | 7 |
| & | targets | None | 7 |
| & | InvalidVersionError | None | 7 |
| & | ImportMissingError | None | 7 |
| & | bytesKey | None | 7 |
| & | image.Uniform | None | 7 |
| - | float64 | float literal | 7 |
| & | statsResults | None | 7 |
| & | [8]int16 | None | 7 |
| & | [4]int32 | None | 7 |
| & | [2]int64 | None | 7 |
| & | [4]float32 | None | 7 |
| & | structEmbeddedL2 | None | 7 |
| & | StructEmbed2 | None | 7 |
| & | IfaceAny | None | 7 |
| & | byteSliceReader | None | 7 |
| & | poser | None | 7 |
| & | rsa.PublicKey | None | 7 |
| & | DecapsulationKey768 | None | 7 |
| & | serverHelloMsg | None | 7 |
| & | file | None | 6 |
| == | *abi.Type | *abi.Type | 6 |
| & | Big | None | 6 |
| & | [1]float64 | None | 6 |
| & | [4]byte | None | 6 |
| & | captureHandler | None | 6 |
| & | commonHandler | None | 6 |
| & | RouteMessage | None | 6 |
| & | ProcessEntry32 | None | 6 |
| & | Ucred | None | 6 |
| & | rune | None | 6 |
| & | LinkAddr | None | 6 |
| & | OBJECT_ATTRIBUTES | None | 6 |
| & | syscall.Stat_t | None | 6 |
| & | node | None | 6 |
| & | profile.Function | None | 6 |
| >= | uint32 | integer literal | 6 |
| - | uint32 | None | 6 |
| & | [512]uint8 | None | 6 |
| & | K | None | 6 |
| & | A | None | 6 |
| == | T | integer literal | 6 |
| >> | uint | uint | 6 |
| < | string | integer literal | 6 |
| & | T0 | None | 6 |
| | | uint64 | integer literal | 6 |
| & | uint | integer literal | 6 |
| & | buffer | None | 6 |
| / | int64 | int64 | 6 |
| * | int64 | int64 | 6 |
| & | MX | None | 6 |
| & | *syscall.DNSRecord | None | 6 |
| & | netFD | None | 6 |
| & | ListenConfig | None | 6 |
| >= | uint16 | integer literal | 6 |
| & | handler | None | 6 |
| & | inflow | None | 6 |
| & | http.PushOptions | None | 6 |
| != | time.Duration | integer literal | 6 |
| < | int64 | float literal | 6 |
| > | uint64 | uint64 | 6 |
| + | uintptr | integer literal | 6 |
| & | unwinder | None | 6 |
| & | sigctxt | None | 6 |
| < | uint8 | integer literal | 6 |
| > | float64 | float64 | 6 |
| & | TypeAssertionError | None | 6 |
| & | stackt | None | 6 |
| != | *int | integer literal | 6 |
| == | objptr | integer literal | 6 |
| & | adjustinfo | None | 6 |
| & | sysDir | None | 6 |
| & | Cmd | None | 6 |
| % | int64 | int64 | 6 |
| & | integer literal | integer literal | 6 |
| - | uint8 | integer literal | 6 |
| & | Slice | None | 6 |
| == | loader.Sym | integer literal | 6 |
| & | macho.Segment64 | None | 6 |
| & | XcoffAuxCSect64 | None | 6 |
| & | Winsize | None | 6 |
| & | ast.MapType | None | 6 |
| & | declInfo | None | 6 |
| & | asyncCall | None | 6 |
| * | *[]*Replace | None | 6 |
| & | Qualifier | None | 6 |
| & | TypeWithQualifiers | None | 6 |
| & | ExprList | None | 6 |
| & | *C.char | None | 6 |
| & | Hash | None | 6 |
| & | modfetch.RevInfo | None | 6 |
| & | StringReader | None | 6 |
| & | [16]int8 | None | 6 |
| & | map[textUnmarshalerString]string | None | 6 |
| & | StartElement | None | 6 |
| & | CDataTest | None | 6 |
| & | IndirAny | None | 6 |
| & | driverStmt | None | 6 |
| & | Rows | None | 6 |
| & | afterFuncContext | None | 6 |
| * | *constant.Value | None | 6 |
| <= | integer literal | constant.Value | 6 |
| & | *fs.PathError | None | 6 |
| & | p256AffinePoint | None | 6 |
| & | DecapsulationKey1024 | None | 6 |
| & | CertificateVerificationError | None | 6 |
| & | slowReader | None | 5 |
| == | any | any | 5 |
| >= | uintptr | integer literal | 5 |
| != | *string | string literal | 5 |
| & | Node | None | 5 |
| & | mmapper | None | 5 |
| * | *IPMreqn | None | 5 |
| & | DLLError | None | 5 |
| & | Xs | None | 5 |
| & | Graph | None | 5 |
| & | syscall.Token | None | 5 |
| & | evTable | None | 5 |
| < | uintptr | integer literal | 5 |
| & | Func | None | 5 |
| & | gc.ObjMask | None | 5 |
| | | uintptr | uintptr | 5 |
| & | workerServer | None | 5 |
| >= | uint64 | uint64 | 5 |
| >> | uint64 | uint | 5 |
| / | int | int | 5 |
| + | float64 | float literal | 5 |
| >> | integer literal | float literal | 5 |
| < | rune | char literal | 5 |
| & | decodecounter.FuncPayload | None | 5 |
| & | Index | None | 5 |
| >= | time.Duration | integer literal | 5 |
| & | dnsmessage.TXTResource | None | 5 |
| & | NS | None | 5 |
| & | syscall.SockaddrUnix | None | 5 |
| & | TCPListener | None | 5 |
| == | error | error | 5 |
| & | Message | None | 5 |
| & | addrParser | None | 5 |
| / | uint8 | integer literal | 5 |
| % | uint8 | integer literal | 5 |
| & | routingNode | None | 5 |
| & | writeCountingConn | None | 5 |
| * | *Request | None | 5 |
| & | tls.ConnectionState | None | 5 |
| & | dataBuffer | None | 5 |
| & | moduledata | None | 5 |
| != | unsafe.Pointer | unsafe.Pointer | 5 |
| == | unsafe.Pointer | unsafe.Pointer | 5 |
| % | int64 | integer literal | 5 |
| != | byte | integer literal | 5 |
| & | ast.DeclStmt | None | 5 |
| & | profile.Mapping | None | 5 |
| & | Group | None | 5 |
| & | Time | None | 5 |
| == | int64 | int64 | 5 |
| + | uint16 | integer literal | 5 |
| & | unicode.RangeTable | None | 5 |
| & | token.FileSet | None | 5 |
| > | uint32 | uint32 | 5 |
| & | obj.Link | None | 5 |
| == | int16 | integer literal | 5 |
| * | *obj.Addr | None | 5 |
| - | int32 | int32 | 5 |
| * | *heap | None | 5 |
| & | OutBuf | None | 5 |
| & | htmlBuilder | None | 5 |
| & | Decoder | None | 5 |
| & | ast.ExprStmt | None | 5 |
| & | ast.ChanType | None | 5 |
| & | ast.Ellipsis | None | 5 |
| & | ast.ImportSpec | None | 5 |
| & | types.Config | None | 5 |
| & | LineBlock | None | 5 |
| & | badPathError | None | 5 |
| & | counterStateBits | None | 5 |
| + | integer literal | float64 | 5 |
| * | float64 | float literal | 5 |
| & | ArrayType | None | 5 |
| & | Unary | None | 5 |
| & | Operator | None | 5 |
| & | TypeRepr | None | 5 |
| & | ast.FuncDecl | None | 5 |
| & | Context | None | 5 |
| & | reader | None | 5 |
| & | fileInfo | None | 5 |
| & | PackageNotInModuleError | None | 5 |
| & | ast.CommentGroup | None | 5 |
| & | Ring | None | 5 |
| & | WaitGroup | None | 5 |
| - | T | None | 5 |
| & | RpathCmd | None | 5 |
| & | formatError | None | 5 |
| <= | float64 | float literal | 5 |
| == | float64 | float literal | 5 |
| >> | Word | uint | 5 |
| & | quic.Config | None | 5 |
| & | lifreq | None | 5 |
| & | [4]uint32 | None | 5 |
| & | [4]float64 | None | 5 |
| & | envExpr | None | 5 |
| & | UnsupportedValueError | None | 5 |
| & | jsonflags.Flags | None | 5 |
| * | *seenPointers | None | 5 |
| & | structOmitZeroEmptyAll | None | 5 |
| / | float literal | uint64 | 5 |
| & | Test | None | 5 |
| & | TagPathError | None | 5 |
| & | NestedItems | None | 5 |
| & | Service | None | 5 |
| & | AnyTest | None | 5 |
| & | U | None | 5 |
| & | ByteStruct | None | 5 |
| & | StringStruct | None | 5 |
| & | Bench | None | 5 |
| & | Row | None | 5 |
| & | time.Time | None | 5 |
| & | ctxOnlyConn | None | 5 |
| & | ast.File | None | 5 |
| & | Pointer | None | 5 |
| * | **E | None | 5 |
| & | errorUncomparable | None | 5 |
| & | hash.Hash | None | 5 |
| & | SHA3 | None | 5 |
| & | entropy.ScratchBuffer | None | 5 |
| >> | uint | integer literal | 5 |
| * | *[32]byte | None | 5 |
| & | [CiphertextSize768]byte | None | 5 |
| & | cryptobyte_asn1.Tag | None | 5 |
| & | asn1.BitString | None | 5 |
| & | VerifyOptions | None | 5 |
| & | finishedMsg | None | 5 |
| & | OAEPOptions | None | 5 |
| & | regFileReader | None | 5 |
| & | flagVar | None | 4 |
| & | [4]int | None | 4 |
| & | []unsafe.Pointer | None | 4 |
| & | S3 | None | 4 |
| & | structWithSelfPtr | None | 4 |
| & | [3]any | None | 4 |
| & | fstest.MapFile | None | 4 |
| * | *[]error | None | 4 |
| + | char literal | int | 4 |
| & | LevelVar | None | 4 |
| >> | uintptr | uint | 4 |
| & | InterfaceAnnounceMessage | None | 4 |
| & | InterfaceMulticastAddrMessage | None | 4 |
| & | DLL | None | 4 |
| & | Dirent | None | 4 |
| & | Token | None | 4 |
| >> | *int64 | integer literal | 4 |
| & | Handle | None | 4 |
| * | *PtraceRegs | None | 4 |
| & | os.PathError | None | 4 |
| & | syscall.Utsname | None | 4 |
| & | windows.IO_STATUS_BLOCK | None | 4 |
| & | context | None | 4 |
| & | profile.ValueType | None | 4 |
| & | profile.Location | None | 4 |
| == | bitset | integer literal | 4 |
| * | *unsafe.Pointer | None | 4 |
| & | [128]uint64 | None | 4 |
| & | sharedMem | None | 4 |
| & | Result | None | 4 |
| << | integer literal | float literal | 4 |
| * | T | T | 4 |
| >> | uint64 | int | 4 |
| <= | integer literal | int64 | 4 |
| * | integer literal | uint32 | 4 |
| & | cmerge.Merger | None | 4 |
| & | emitState | None | 4 |
| & | Mapping | None | 4 |
| & | wrapper | None | 4 |
| & | Map | None | 4 |
| * | *Dialer | None | 4 |
| & | SRV | None | 4 |
| & | dnsmessage.AAAAResource | None | 4 |
| & | dnsmessage.NSResource | None | 4 |
| & | timeoutTemporaryError | None | 4 |
| & | body | None | 4 |
| & | url.Error | None | 4 |
| & | net.TCPAddr | None | 4 |
| & | gzipReader | None | 4 |
| & | writeResHeaders | None | 4 |
| <= | integer literal | int32 | 4 |
| / | int32 | int32 | 4 |
| * | *[]int | None | 4 |
| < | uintptr | uintptr | 4 |
| & | note | None | 4 |
| & | cgoSymbolizerArg | None | 4 |
| & | X | None | 4 |
| != | F | F | 4 |
| * | *[4]uint32 | None | 4 |
| & | structWithMethod | None | 4 |
| / | integer literal | int | 4 |
| & | *pthreadcond | None | 4 |
| & | foo | None | 4 |
| & | obj | None | 4 |
| * | *sigactiont | None | 4 |
| & | usigactiont | None | 4 |
| & | mspan | None | 4 |
| & | Module | None | 4 |
| & | syscall.Rusage | None | 4 |
| & | ProcessState | None | 4 |
| & | reparseData | None | 4 |
| != | _C_int | integer literal | 4 |
| * | integer literal | Duration | 4 |
| - | integer literal | uint32 | 4 |
| < | integer literal | int | 4 |
| == | syntax.EmptyOp | integer literal | 4 |
| * | *map[*Regexp]printFlags | None | 4 |
| & | ast.IfStmt | None | 4 |
| & | ast.ReturnStmt | None | 4 |
| == | int32 | int32 | 4 |
| < | uint32 | uint32 | 4 |
| + | int32 | None | 4 |
| << | integer literal | uint32 | 4 |
| & | Entry | None | 4 |
| & | Archive | None | 4 |
| * | *[]*wasmFuncType | None | 4 |
| & | uuidCmd | None | 4 |
| & | Heading | None | 4 |
| & | *SECURITY_DESCRIPTOR | None | 4 |
| & | Linger | None | 4 |
| & | strbuf | None | 4 |
| & | Uvmexp | None | 4 |
| & | state | None | 4 |
| & | argument | None | 4 |
| & | ast.SliceExpr | None | 4 |
| & | zipError | None | 4 |
| & | ErrorList | None | 4 |
| & | Go | None | 4 |
| & | Toolchain | None | 4 |
| & | Godebug | None | 4 |
| * | *ErrorList | None | 4 |
| & | Tag | None | 4 |
| & | nfcTrie | None | 4 |
| & | nfkcTrie | None | 4 |
| & | fileAddr2Line | None | 4 |
| != | float64 | integer literal | 4 |
| & | Binary | None | 4 |
| & | TemplateParam | None | 4 |
| & | apiPackage | None | 4 |
| & | countWriter | None | 4 |
| & | importReader | None | 4 |
| * | ast.Expr | None | 4 |
| * | *Type | None | 4 |
| & | Generator | None | 4 |
| & | load.Package | None | 4 |
| & | build.Package | None | 4 |
| & | Versions | None | 4 |
| & | DownloadDirPartialError | None | 4 |
| & | modload.QueryMatchesMainModulesError | None | 4 |
| & | modFileSummary | None | 4 |
| & | teststringwriter | None | 4 |
| <= | rune | rune | 4 |
| & | UnknownLineError | None | 4 |
| & | Dylib | None | 4 |
| - | uint8 | uint8 | 4 |
| >> | image.Rectangle | integer literal | 4 |
| * | *block | None | 4 |
| * | Word | integer literal | 4 |
| & | Rand | None | 4 |
| & | [8]uint16 | None | 4 |
| + | integer literal | float32 | 4 |
| * | integer literal | uint64 | 4 |
| & | inexactError | None | 4 |
| & | struct {
		X  float64
		Id RawMessage
		Y  float32
	} | None | 4 |
| & | struct {
		X     float64
		Id    RawMessage
		IdPtr *RawMessage
		Y     float32
	} | None | 4 |
| & | UnsupportedTypeError | None | 4 |
| & | struct {
		Bytes []byte
	} | None | 4 |
| & | []Animal | None | 4 |
| & | NoPanicStruct | None | 4 |
| & | SamePointerNoCycle | None | 4 |
| & | struct{ M RawMessage } | None | 4 |
| & | struct{ M *RawMessage } | None | 4 |
| & | Xint | None | 4 |
| & | unexportedFields | None | 4 |
| & | XYZ | None | 4 |
| & | FaultyBuffer | None | 4 |
| & | ioError | None | 4 |
| & | allMethods | None | 4 |
| * | *fmt.Stringer | None | 4 |
| & | IndirComment | None | 4 |
| & | IfaceComment | None | 4 |
| & | IndirChardata | None | 4 |
| & | IfaceChardata | None | 4 |
| & | IndirCDATA | None | 4 |
| & | IfaceCDATA | None | 4 |
| & | IndirInnerXML | None | 4 |
| & | IfaceInnerXML | None | 4 |
| & | DirectInnerXML | None | 4 |
| & | IfaceElement | None | 4 |
| & | IndirOmitEmpty | None | 4 |
| & | IfaceOmitEmpty | None | 4 |
| & | DirectAny | None | 4 |
| > | rune | integer literal | 4 |
| & | gobEncoderType | None | 4 |
| & | fakeConnector | None | 4 |
| & | sql.TxOptions | None | 4 |
| & | NullString | None | 4 |
| * | *func() bool | None | 4 |
| & | RawBytes | None | 4 |
| == | any | int | 4 |
| & | ast.SendStmt | None | 4 |
| & | stringVal | None | 4 |
| & | Union | None | 4 |
| == | Type | Type | 4 |
| & | MethodSet | None | 4 |
| & | _TypeSet | None | 4 |
| & | interface{ Timeout() bool } | None | 4 |
| * | **C.GO_BIGNUM | None | 4 |
| & | edwards25519.Point | None | 4 |
| & | p384NonMontgomeryDomainFieldElement | None | 4 |
| & | p224NonMontgomeryDomainFieldElement | None | 4 |
| & | p256NonMontgomeryDomainFieldElement | None | 4 |
| & | p521NonMontgomeryDomainFieldElement | None | 4 |
| & | [BlockSize]byte | None | 4 |
| & | GCMWithXORCounterNonce | None | 4 |
| - | fieldElement | fieldElement | 4 |
| & | EncapsulationKey1024 | None | 4 |
| & | EncapsulationKey768 | None | 4 |
| & | projP2 | None | 4 |
| & | [SeedSize]byte | None | 4 |
| & | CurveParams | None | 4 |
| & | publicKeyInfo | None | 4 |
| & | CertPool | None | 4 |
| & | ecdsa.PrivateKey | None | 4 |
| & | CertificateRequest | None | 4 |
| & | certificateVerifyMsg | None | 4 |
| & | keyUpdateMsg | None | 4 |
| & | certificateMsgTLS13 | None | 4 |
| & | ecdhKeyExchange | None | 4 |
| & | SessionState | None | 4 |
| & | ClientSessionState | None | 4 |
| & | hybridPublicKey | None | 4 |
| & | dhKEM | None | 4 |
| & | regFileWriter | None | 4 |
| & | Small | None | 3 |
| & | io.Reader | None | 3 |
| & | struct {
		E any
	} | None | 3 |
| & | testTypeWithMethod | None | 3 |
| & | noReadFrom | None | 3 |
| + | char literal | uint64 | 3 |
| & | MultiHandler | None | 3 |
| & | defaultHandler | None | 3 |
| & | TextHandler | None | 3 |
| & | JSONHandler | None | 3 |
| != | Errno | integer literal | 3 |
| & | Proc | None | 3 |
| & | LazyDLL | None | 3 |
| & | command | None | 3 |
| & | SysProcAttr | None | 3 |
| & | WaitStatus | None | 3 |
| & | timestamp | None | 3 |
| * | *Ucred | None | 3 |
| == | uint32 | uint32 | 3 |
| & | TwoLines | None | 3 |
| & | runeScanner | None | 3 |
| & | RecursiveInt | None | 3 |
| & | syscall.WSAProtocolInfo | None | 3 |
| * | *[]syscall.WSABuf | None | 3 |
| & | gState | None | 3 |
| & | trace.ClockSnapshot | None | 3 |
| & | rawEvent | None | 3 |
| & | profile.Sample | None | 3 |
| & | nobitsSectionReader | None | 3 |
| & | map[int]int | None | 3 |
| & | linux.EpollEvent | None | 3 |
| & | opHeap | None | 3 |
| == | *uint64 | uint64 | 3 |
| & | mutator | None | 3 |
| <= | float64 | float64 | 3 |
| - | uint | uint | 3 |
| < | P | P | 3 |
| < | F | F | 3 |
| + | int | float literal | 3 |
| < | *int | integer literal | 3 |
| % | int | int | 3 |
| - | float literal (suffix i) | None | 3 |
| << | float literal | integer literal | 3 |
| << | int | uint | 3 |
| + | string literal | integer literal | 3 |
| % | integer literal | integer literal | 3 |
| == | *int | *int | 3 |
| & | [32]uint64 | None | 3 |
| > | rune | char literal | 3 |
| + | uint64 | char literal | 3 |
| & | Function | None | 3 |
| * | integer literal | int64 | 3 |
| & | common | None | 3 |
| & | smallByteReader | None | 3 |
| & | mapFileInfo | None | 3 |
| & | testCase | None | 3 |
| & | temporaryError | None | 3 |
| & | TCPConn | None | 3 |
| & | dnsmessage.PTRResource | None | 3 |
| & | dnsmessage.SRVResource | None | 3 |
| * | *UDPAddr | None | 3 |
| & | packetListener | None | 3 |
| & | testInterface | None | 3 |
| & | Addr | None | 3 |
| != | Addr | Addr | 3 |
| & | HTTP2Config | None | 3 |
| & | transportRequest | None | 3 |
| & | delegateReader | None | 3 |
| & | dumpConn | None | 3 |
| & | ctHeader | None | 3 |
| & | repeatReader | None | 3 |
| & | response | None | 3 |
| & | PriorityFrame | None | 3 |
| & | ContinuationFrame | None | 3 |
| & | http.Cookie | None | 3 |
| & | eofReader | None | 3 |
| & | http.ProtocolError | None | 3 |
| & | ArithAddResp | None | 3 |
| + | integer literal | uint64 | 3 |
| >= | uintptr | uintptr | 3 |
| | | uint32 | uint32 | 3 |
| & | cgothreadstart | None | 3 |
| & | godebugInc | None | 3 |
| << | uintptr | integer literal | 3 |
| > | int64 | float literal | 3 |
| & | windows.SystemInfo | None | 3 |
| & | windows.MemoryBasicInformation | None | 3 |
| & | *dloggerImpl | None | 3 |
| & | funcDescriptor | None | 3 |
| * | **arenaHint | None | 3 |
| == | complex128 | integer literal | 3 |
| & | func(S) | None | 3 |
| & | *pthreadmutex | None | 3 |
| != | int64 | int64 | 3 |
| != | any | any | 3 |
| <= | uint64 | uint64 | 3 |
| & | objWith[*obj] | None | 3 |
| & | InterImpl | None | 3 |
| & | windows.PROCESS_MEMORY_COUNTERS | None | 3 |
| != | C.int | integer literal | 3 |
| > | uint8 | uint8 | 3 |
| & | windows.ModuleEntry32 | None | 3 |
| * | float64 | integer literal | 3 |
| & | comment.Printer | None | 3 |
| & | FileMode | integer literal | 3 |
| & | Root | None | 3 |
| & | root | None | 3 |
| & | syscall.Win32FileAttributeData | None | 3 |
| & | Process | None | 3 |
| <= | char literal | uint8 | 3 |
| <= | uint8 | char literal | 3 |
| & | syscall.Win32finddata | None | 3 |
| + | integer literal | float literal | 3 |
| >> | int16 | integer literal | 3 |
| == | Element | Element | 3 |
| < | uint16 | integer literal | 3 |
| & | failWriter | None | 3 |
| & | limitedWriter | None | 3 |
| * | *ast.Expr | None | 3 |
| & | pvacfgnode | None | 3 |
| & | script.Engine | None | 3 |
| & | excludedReader | None | 3 |
| << | integer literal | ABI | 3 |
| & | regVar | None | 3 |
| % | int32 | int32 | 3 |
| &^ | uint8 | integer literal | 3 |
| ^ | int64 | None | 3 |
| & | Optab | None | 3 |
| == | int16 | int16 | 3 |
| << | int16 | integer literal | 3 |
| < | int16 | integer literal | 3 |
| == | int8 | integer literal | 3 |
| & | Pos | None | 3 |
| & | ArHdr | None | 3 |
| * | **dwarf.DWDie | None | 3 |
| & | dwarfSecInfo | None | 3 |
| & | pe.OptionalHeader64 | None | 3 |
| & | pe.OptionalHeader32 | None | 3 |
| * | **Elflib | None | 3 |
| & | Loader | None | 3 |
| & | ptrStringer | None | 3 |
| & | embeddedStringer | None | 3 |
| & | errorer | None | 3 |
| & | Item | None | 3 |
| & | HTMLTag | None | 3 |
| == | *byte | integer literal | 3 |
| & | Coord | None | 3 |
| & | DevInfoData | None | 3 |
| * | *CPUSet | None | 3 |
| * | *Bpxystat_t | None | 3 |
| * | *Bpxyatt_t | None | 3 |
| & | TCPInfo | None | 3 |
| * | *Timespec | None | 3 |
| & | Itimerval | None | 3 |
| & | md.Plain | None | 3 |
| & | ast.FuncLit | None | 3 |
| & | ast.KeyValueExpr | None | 3 |
| & | ast.IndexListExpr | None | 3 |
| & | newLike | None | 3 |
| & | constraint.AndExpr | None | 3 |
| & | goFixInlineAliasFact | None | 3 |
| & | goFixInlineConstFact | None | 3 |
| & | ModuleError | None | 3 |
| & | InvalidPathError | None | 3 |
| * | *[]*Exclude | None | 3 |
| * | *[]*Tool | None | 3 |
| * | *[]*Ignore | None | 3 |
| & | Counter | None | 3 |
| & | telemetry.UploadConfig | None | 3 |
| & | telemetry.Report | None | 3 |
| == | Prefix | integer literal | 3 |
| < | uint8 | uint8 | 3 |
| <= | uint8 | integer literal | 3 |
| & | transport | None | 3 |
| - | uint64 | *uint64 | 3 |
| & | fileNM | None | 3 |
| & | ReferenceType | None | 3 |
| & | SuffixType | None | 3 |
| & | Destructor | None | 3 |
| & | GlobalCDtor | None | 3 |
| & | PackExpansion | None | 3 |
| & | Fold | None | 3 |
| & | Closure | None | 3 |
| & | LambdaAuto | None | 3 |
| & | FunctionParam | None | 3 |
| & | ast.StructType | None | 3 |
| & | C.SDL_KeyboardEvent | None | 3 |
| & | C.issue67517struct | None | 3 |
| & | rawFile | None | 3 |
| & | MultiplePackageError | None | 3 |
| & | cacheprog.Request | None | 3 |
| & | load.ImportStack | None | 3 |
| & | checkCacheProvider | None | 3 |
| & | load.TextPrinter | None | 3 |
| & | UnknownRevisionError | None | 3 |
| & | override | None | 3 |
| & | mvsReqs | None | 3 |
| * | *codehost.Origin | None | 3 |
| != | bool literal | bool literal | 3 |
| & | emptyThenNonEmptyReader | None | 3 |
| == | *Element | *Element | 3 |
| * | *Table | None | 3 |
| & | maphash.Hash | None | 3 |
| + | float literal (suffix i) | integer literal | 3 |
| * | *LineEntry | None | 3 |
| & | stackEnt | None | 3 |
| & | Rel32 | None | 3 |
| & | RGBA | None | 3 |
| & | RGBA64 | None | 3 |
| & | NRGBA | None | 3 |
| & | NRGBA64 | None | 3 |
| & | Alpha | None | 3 |
| & | Alpha16 | None | 3 |
| & | Gray | None | 3 |
| & | Gray16 | None | 3 |
| & | CMYK | None | 3 |
| & | Paletted | None | 3 |
| & | YCbCr | None | 3 |
| & | NYCbCrA | None | 3 |
| * | uint32 | uint32 | 3 |
| & | image.Point | None | 3 |
| * | *image.Rectangle | None | 3 |
| * | int32 | int32 | 3 |
| & | block | None | 3 |
| - | float literal | float64 | 3 |
| > | Word | Word | 3 |
| > | Word | integer literal | 3 |
| & | big.Int | None | 3 |
| | | uint | uint | 3 |
| % | uint64 | uint64 | 3 |
| * | *int8 | None | 3 |
| & | idnaTrie | None | 3 |
| & | [16]uint32 | None | 3 |
| != | float32 | float32 | 3 |
| & | [16]uint8 | None | 3 |
| & | [2]uint64 | None | 3 |
| & | [2]float64 | None | 3 |
| & | [16]int16 | None | 3 |
| & | [32]int16 | None | 3 |
| ^ | T | None | 3 |
| & | InsertMap[string, int] | None | 3 |
| & | struct{ Tuple Tuple } | None | 3 |
| & | Tuple | None | 3 |
| & | InvalidTextError | None | 3 |
| & | ValueFlags | None | 3 |
| & | struct {
				A int
				X jsontext.Value `json:",embed"`
			} | None | 3 |
| & | struct {
				A int
				X jsonObject `json:",embed"`
			} | None | 3 |
| * | *any | None | 3 |
| * | *stringCache | None | 3 |
| * | *stringSlice | None | 3 |
| & | stringCache | None | 3 |
| & | Feed | None | 3 |
| & | TableAttrs | None | 3 |
| & | Parent | None | 3 |
| & | PresenceTest | None | 3 |
| & | SecretAgent | None | 3 |
| & | Domain | None | 3 |
| & | NameInField | None | 3 |
| & | AttrsTest | None | 3 |
| & | IgnoreTest | None | 3 |
| & | DirectChardata | None | 3 |
| & | DirectCDATA | None | 3 |
| & | IndirElement | None | 3 |
| & | RawValue | None | 3 |
| & | decOp | None | 3 |
| * | **decEngine | None | 3 |
| & | RT1 | None | 3 |
| & | encOp | None | 3 |
| & | NewType0 | None | 3 |
| & | Tx | None | 3 |
| & | NullInt32 | None | 3 |
| & | NullInt64 | None | 3 |
| & | NullFloat64 | None | 3 |
| & | NullBool | None | 3 |
| & | VariableNode | None | 3 |
| & | customCauseContext | None | 3 |
| & | myDoneCtx | None | 3 |
| & | ast.InterfaceType | None | 3 |
| != | types.ImportMode | integer literal | 3 |
| & | types.Package | None | 3 |
| * | *types.Type | None | 3 |
| & | ifacePair | None | 3 |
| & | Array | None | 3 |
| & | TypeParamList | None | 3 |
| * | *operand | None | 3 |
| & | [128]byte | None | 3 |
| & | noGCM | None | 3 |
| & | p256Table | None | 3 |
| > | uint8 | integer literal | 3 |
| * | *Block | None | 3 |
| & | GCMWithCounterNonce | None | 3 |
| & | [CiphertextSize1024]byte | None | 3 |
| == | Scalar | Scalar | 3 |
| != | Element | Element | 3 |
| & | dsa.PrivateKey | None | 3 |
| & | dsa.PublicKey | None | 3 |
| & | ed25519.Options | None | 3 |
| & | ecdsa.PublicKey | None | 3 |
| & | keyGenTestReader | None | 3 |
| & | asn1.ObjectIdentifier | None | 3 |
| & | pkcs1PublicKey | None | 3 |
| & | pkcs8 | None | 3 |
| & | ecPrivateKey | None | 3 |
| & | pkcs1PrivateKey | None | 3 |
| & | rsa.PrivateKey | None | 3 |
| & | CFRef | None | 3 |
| & | certificateRequestMsg | None | 3 |
| & | encryptedExtensionsMsg | None | 3 |
| & | recordingConn | None | 3 |
| & | replayingConn | None | 3 |
| & | hybridKeyExchange | None | 3 |
| & | cryptobyte.Builder | None | 3 |
| & | hybridKEM | None | 3 |
| & | hybridPrivateKey | None | 3 |
| & | mlkemPublicKey | None | 3 |
| & | aead | None | 3 |
| & | hkdfKDF | None | 3 |
| & | nistCurve | None | 3 |
| & | testFile | None | 3 |
| * | *uint | None | 2 |
| * | *float64 | None | 2 |
| & | boolFlagVar | None | 2 |
| & | zeroPanicker | None | 2 |
| & | net.IP | None | 2 |
| & | WordDecoder | None | 2 |
| & | Part | None | 2 |
| & | openDir | None | 2 |
| & | [64]byte | None | 2 |
| & | [1024]byte | None | 2 |
| & | maps.Iter | None | 2 |
| & | abi.EmptyInterface | None | 2 |
| != | Type | Type | 2 |
| & | embed | None | 2 |
| & | S4 | None | 2 |
| & | Embed | None | 2 |
| & | *int32 | None | 2 |
| & | []T | None | 2 |
| & | WC | None | 2 |
| & | io.WriteCloser | None | 2 |
| & | base64.Encoding | None | 2 |
| & | struct {
		X, Y int
	} | None | 2 |
| & | [1]byte | None | 2 |
| & | MyBytesArray | None | 2 |
| & | struct {
		buf []byte
	} | None | 2 |
| & | LimitedReader | None | 2 |
| & | dataAndErrorBuffer | None | 2 |
| & | subFS | None | 2 |
| & | netConn | None | 2 |
| & | Source | None | 2 |
| * | *HandlerOptions | None | 2 |
| & | handlerWriter | None | 2 |
| > | T | T | 2 |
| & | cloneSeq | None | 2 |
| & | SockaddrInet6 | None | 2 |
| & | SockaddrInet4 | None | 2 |
| & | Rlimit | None | 2 |
| & | LazyProc | None | 2 |
| & | *Dirent | None | 2 |
| & | *SID | None | 2 |
| & | fdstat | None | 2 |
| & | Errno | None | 2 |
| & | BpfInsn | None | 2 |
| & | ivalue | None | 2 |
| & | BpfStat | None | 2 |
| / | timestamp | float literal | 2 |
| % | timestamp | float literal | 2 |
| & | syscall.Ucred | None | 2 |
| & | int8 | None | 2 |
| & | syscall.Dirent | None | 2 |
| == | _Socklen | integer literal | 2 |
| & | Dir | None | 2 |
| & | SecurityAttributes | None | 2 |
| & | _FILE_END_OF_FILE_INFO | None | 2 |
| & | Filetime | None | 2 |
| * | *IPMreq | None | 2 |
| & | SockFilter | None | 2 |
| & | iflags | None | 2 |
| & | _C_long | None | 2 |
| >> | ref | integer literal | 2 |
| * | *ref | None | 2 |
| & | Recur | None | 2 |
| & | IntString | None | 2 |
| & | complex128 | None | 2 |
| & | interface{} | None | 2 |
| != | *uint16 | integer literal | 2 |
| & | syscall.WSAData | None | 2 |
| & | NTUnicodeString | None | 2 |
| & | utsname | None | 2 |
| & | splicePipe | None | 2 |
| & | windows.FILE_BASIC_INFO | None | 2 |
| * | *syscall.RawSockaddrAny | None | 2 |
| & | generation | None | 2 |
| & | ClockSnapshot | None | 2 |
| & | bandUtilHeap | None | 2 |
| & | batchCursor | None | 2 |
| & | mState | None | 2 |
| & | GoroutineSummary | None | 2 |
| & | goroutineSummary | None | 2 |
| & | UserRegionSummary | None | 2 |
| & | txtar.Archive | None | 2 |
| & | Batch | None | 2 |
| * | *rawEvent | None | 2 |
| & | Event | None | 2 |
| & | *Event | None | 2 |
| & | format.HeapCountersArg | None | 2 |
| & | format.NameArg | None | 2 |
| & | format.SortIndexArg | None | 2 |
| & | table | None | 2 |
| != | *Map | integer literal | 2 |
| - | integer literal | uintptr | 2 |
| & | gc.PtrMask | None | 2 |
| == | *uint32 | uint32 | 2 |
| * | uintptr | uintptr | 2 |
| >= | float64 | float64 | 2 |
| & | contextReader | None | 2 |
| & | call | None | 2 |
| & | crashError | None | 2 |
| == | reflect.Type | reflect.Type | 2 |
| > | SectionKind | integer literal | 2 |
| - | SectionKind | integer literal | 2 |
| & | HashTrieMap[K, V] | None | 2 |
| == | P | any | 2 |
| == | any | P | 2 |
| < | P | any | 2 |
| & | LRU[int, string] | None | 2 |
| & | struct {
	m func()
} | None | 2 |
| & | M | None | 2 |
| || | bool | bool literal | 2 |
| && | bool | bool literal | 2 |
| || | mybool | bool literal | 2 |
| && | mybool | bool literal | 2 |
| + | myint | float literal | 2 |
| + | uint | float literal | 2 |
| * | uint | uint | 2 |
| << | uint | uint | 2 |
| + | myuint | float literal | 2 |
| + | myfloat64 | integer literal | 2 |
| + | myfloat64 | float literal | 2 |
| & | integer literal | None | 2 |
| + | integer literal | string literal | 2 |
| & | Map[K, V] | None | 2 |
| & | node[K, V] | None | 2 |
| & | Iterator[K, V] | None | 2 |
| << | float literal (suffix i) | integer literal | 2 |
| >> | float literal | integer literal | 2 |
| == | float literal | integer literal | 2 |
| < | integer literal | integer literal | 2 |
| ! | bool literal | None | 2 |
| - | T | T | 2 |
| == | bool literal | bool literal | 2 |
| < | float32 | float32 | 2 |
| < | *int | *int | 2 |
| > | *int | *int | 2 |
| == | interface{ m() int } | S1 | 2 |
| == | interface{ m() int } | S2 | 2 |
| + | T | integer literal | 2 |
| & | [4]uint64 | None | 2 |
| &^ | uint64 | integer literal | 2 |
| | | uint32 | integer literal | 2 |
| & | stringtab.Writer | None | 2 |
| & | WriteSeeker | None | 2 |
| & | ctrVis | None | 2 |
| & | profileMerger | None | 2 |
| & | Edge | None | 2 |
| & | NodeInfo | None | 2 |
| & | testState | None | 2 |
| & | matcher | None | 2 |
| & | fuzzState | None | 2 |
| + | rune | char literal | 2 |
| & | trieNode | None | 2 |
| > | int | float literal | 2 |
| & | localServer | None | 2 |
| & | localPacketServer | None | 2 |
| & | dnsmessage.OPTResource | None | 2 |
| & | routeStats | None | 2 |
| & | *syscall.AddrinfoW | None | 2 |
| & | UDPConn | None | 2 |
| & | UnixListener | None | 2 |
| & | rawConn | None | 2 |
| & | syscall.IPMreqn | None | 2 |
| & | notFoundError | None | 2 |
| & | *_C_struct_addrinfo | None | 2 |
| & | *syscall.RawSockaddrAny | None | 2 |
| & | mime.WordDecoder | None | 2 |
| & | Userinfo | None | 2 |
| != | AddrPort | AddrPort | 2 |
| & | AddrPort | None | 2 |
| & | Status | None | 2 |
| & | transferWriter | None | 2 |
| & | byteReader | None | 2 |
| & | transferReader | None | 2 |
| <= | integer literal | byte | 2 |
| & | httptest.Server | None | 2 |
| & | testTLSConn | None | 2 |
| & | closeChecker | None | 2 |
| & | multipart.Form | None | 2 |
| & | socksAddr | None | 2 |
| & | contextCounter | None | 2 |
| & | wgReadCloser | None | 2 |
| & | stateLog | None | 2 |
| & | countCloseListener | None | 2 |
| & | fakeNetConn | None | 2 |
| & | routingIndex | None | 2 |
| & | timeoutHandler | None | 2 |
| * | *func() | None | 2 |
| & | contextKey | None | 2 |
| & | conn | None | 2 |
| & | ServeMux | None | 2 |
| & | net.Listener | None | 2 |
| & | net.Dialer | None | 2 |
| & | readTrackingBody | None | 2 |
| == | any | bool literal | 2 |
| & | request | None | 2 |
| & | record | None | 2 |
| & | funcReader | None | 2 |
| & | testRoundTrip | None | 2 |
| & | strconv.NumError | None | 2 |
| & | SettingsFrame | None | 2 |
| & | PingFrame | None | 2 |
| & | GoAwayFrame | None | 2 |
| & | WindowUpdateFrame | None | 2 |
| & | RSTStreamFrame | None | 2 |
| & | PushPromiseFrame | None | 2 |
| & | MetaHeadersFrame | None | 2 |
| & | noteCloseConn | None | 2 |
| & | chunkReader | None | 2 |
| & | trackingReader | None | 2 |
| & | synctestNetConn | None | 2 |
| & | responseWriter | None | 2 |
| <= | byte | integer literal | 2 |
| + | int32 | char literal | 2 |
| & | limitWriter | None | 2 |
| & | staticTransport | None | 2 |
| & | testResponseWriter | None | 2 |
| * | *http.Request | None | 2 |
| & | Reply | None | 2 |
| * | *map[int]int | None | 2 |
| * | *[2]int | None | 2 |
| * | uintptr | integer literal | 2 |
| & | *uint32 | None | 2 |
| & | *stackt | None | 2 |
| * | *gQueue | None | 2 |
| / | int32 | integer literal | 2 |
| % | uint32 | uint32 | 2 |
| & | mt | None | 2 |
| >= | uint32 | uint32 | 2 |
| & | heapStatsDelta | None | 2 |
| & | pthreadkey | None | 2 |
| & | *[]*moduledata | None | 2 |
| & | tbFrame | None | 2 |
| & | [bufSize]byte | None | 2 |
| & | bitvector | None | 2 |
| * | uint8 | integer literal | 2 |
| == | uintptr | uintptr | 2 |
| & | _panic | None | 2 |
| & | itimerspec32 | None | 2 |
| & | [2]uintptr | None | 2 |
| * | *windows.Context | None | 2 |
| / | integer literal | int32 | 2 |
| == | typeOff | integer literal | 2 |
| != | F | integer literal | 2 |
| > | F | F | 2 |
| * | *semt | None | 2 |
| & | mts | None | 2 |
| * | *tmpBuf | None | 2 |
| * | *heapArena | None | 2 |
| & | *notInHeap | None | 2 |
| * | *iface | None | 2 |
| & | windows.ExceptionRecord | None | 2 |
| & | itimerval | None | 2 |
| & | gsignalStack | None | 2 |
| / | uint64 | float literal | 2 |
| <= | uintptr | uintptr | 2 |
| & | []*mspan | None | 2 |
| & | [8]byte | None | 2 |
| & | Int32Key | None | 2 |
| & | Int64Key | None | 2 |
| & | smallPointer | None | 2 |
| * | *[2]uint64 | None | 2 |
| & | objWith[*uintptr] | None | 2 |
| != | objptr | integer literal | 2 |
| & | char literal | integer literal | 2 |
| >= | int64 | float literal | 2 |
| & | async | None | 2 |
| > | size | integer literal | 2 |
| ^ | integer literal | integer literal | 2 |
| & | [129]float64 | None | 2 |
| & | atomic.Bool | None | 2 |
| & | Rect | None | 2 |
| & | ThreadEntry32 | None | 2 |
| / | uint64 | uint64 | 2 |
| & | OsFile | None | 2 |
| & | AddrT | None | 2 |
| & | stack | None | 2 |
| & | Task | None | 2 |
| & | Region | None | 2 |
| & | [64]secretType | None | 2 |
| + | *int | integer literal | 2 |
| & | sync.RWMutex | None | 2 |
| & | PageWithoutContent_hugo5379 | None | 2 |
| & | DevInfo_moby4951 | None | 2 |
| & | Replica_cockroach3710 | None | 2 |
| & | Type_kubernetes58107 | None | 2 |
| & | Replica_cockroach10214 | None | 2 |
| & | RowChannel_cockroach35931 | None | 2 |
| & | plugin_moby25348 | None | 2 |
| & | Obj | None | 2 |
| & | GCStats | None | 2 |
| & | errWriter | None | 2 |
| - | time.Duration | time.Duration | 2 |
| & | syscall.ProcAttr | None | 2 |
| & | syscall.Waitmsg | None | 2 |
| & | dirInfo | None | 2 |
| & | windows.FILE_MODE_INFORMATION | None | 2 |
| & | _REPARSE_DATA_BUFFER | None | 2 |
| & | prefixSuffixSaver | None | 2 |
| * | *_C_int | None | 2 |
| * | *[]_C_gid_t | None | 2 |
| & | *_C_struct_passwd | None | 2 |
| & | *_C_struct_group | None | 2 |
| & | _C_struct_passwd | None | 2 |
| & | _C_struct_group | None | 2 |
| & | zone | None | 2 |
| & | syscall.Timezoneinformation | None | 2 |
| & | Ticker | None | 2 |
| / | Duration | integer literal | 2 |
| * | Duration | integer literal | 2 |
| == | Time | Time | 2 |
| != | Time | Time | 2 |
| <= | integer literal | string | 2 |
| == | Large | Large | 2 |
| + | I | integer literal | 2 |
| & | huffmanDecoder | None | 2 |
| & | decompressor | None | 2 |
| & | lazyFlag | None | 2 |
| != | printFlags | integer literal | 2 |
| & | printer.Config | None | 2 |
| & | templateFile | None | 2 |
| & | visitor | None | 2 |
| + | integer literal | int64 | 2 |
| & | symOnce | None | 2 |
| * | *obj.Reloc | None | 2 |
| * | *obj.Prog | None | 2 |
| | | uint8 | integer literal | 2 |
| * | *RotateParams | None | 2 |
| < | obj.As | integer literal | 2 |
| - | obj.As | None | 2 |
| - | integer literal | int64 | 2 |
| & | [5]uint32 | None | 2 |
| | | int32 | integer literal | 2 |
| & | PosBase | None | 2 |
| & | GoObj | None | 2 |
| != | lex.ScanToken | char literal | 2 |
| & | Macro | None | 2 |
| & | [pprofMaxStack]uint64 | None | 2 |
| & | wasmFunc | None | 2 |
| & | wasmFuncType | None | 2 |
| & | elf.Section64 | None | 2 |
| & | ElfSym | None | 2 |
| & | builtFile | None | 2 |
| & | dwtest.Examiner | None | 2 |
| * | *loader.Sym | None | 2 |
| * | *[]*sym.Library | None | 2 |
| & | dwctxt | None | 2 |
| & | pe.FileHeader | None | 2 |
| & | peBaseRelocTable | None | 2 |
| & | macho.Section64 | None | 2 |
| + | goobj.CUFileIndex | integer literal | 2 |
| & | xcoffLoaderSymbol | None | 2 |
| & | XcoffLdRel64 | None | 2 |
| & | XcoffLdImportFile64 | None | 2 |
| & | oReader | None | 2 |
| & | SymbolBuilder | None | 2 |
| & | percentDStruct | None | 2 |
| & | notPercentDStruct | None | 2 |
| & | chan bool | None | 2 |
| & | FakeFile | None | 2 |
| * | *line | None | 2 |
| & | HardBreak | None | 2 |
| & | Code | None | 2 |
| & | openPlain | None | 2 |
| & | AutoLink | None | 2 |
| > | byte | char literal | 2 |
| & | Table | None | 2 |
| & | CodeBlock | None | 2 |
| & | Paragraph | None | 2 |
| + | int | char literal | 2 |
| & | NTString | None | 2 |
| * | **uint16 | None | 2 |
| & | DrvInfoData | None | 2 |
| & | SockaddrVM | None | 2 |
| & | IfreqMTU | None | 2 |
| & | TCPConnectionInfo | None | 2 |
| & | KinfoProc | None | 2 |
| * | *PtraceRegsArm64 | None | 2 |
| & | CapRights | None | 2 |
| & | RTCTime | None | 2 |
| & | RTCWkAlrm | None | 2 |
| ^ | int | None | 2 |
| & | PtpClockCaps | None | 2 |
| & | PtpSysOffsetPrecise | None | 2 |
| & | WatchdogInfo | None | 2 |
| & | HIDRawDevInfo | None | 2 |
| & | KCMClone | None | 2 |
| & | LoopInfo64 | None | 2 |
| & | Termio | None | 2 |
| & | Clockinfo | None | 2 |
| * | *Inet4Pktinfo | None | 2 |
| * | *Inet6Pktinfo | None | 2 |
| & | Ptmget | None | 2 |
| & | direntLE | None | 2 |
| & | TpacketStats | None | 2 |
| & | TpacketStatsV3 | None | 2 |
| & | md.Link | None | 2 |
| & | md.Code | None | 2 |
| & | Operation | None | 2 |
| == | ast.Node | ast.Node | 2 |
| * | *Options | None | 2 |
| & | parameter | None | 2 |
| & | paramInfo | None | 2 |
| != | types.Type | types.Type | 2 |
| & | stringSetFlag | None | 2 |
| & | goFixInlineFuncFact | None | 2 |
| & | isWrapper | None | 2 |
| & | analysis.Module | None | 2 |
| < | token.Pos | token.Pos | 2 |
| * | *[]ast.Stmt | None | 2 |
| & | CommentBlock | None | 2 |
| & | Require | None | 2 |
| & | Exclude | None | 2 |
| & | Retract | None | 2 |
| & | Tool | None | 2 |
| & | Ignore | None | 2 |
| & | Replace | None | 2 |
| & | Use | None | 2 |
| & | printer | None | 2 |
| & | Note | None | 2 |
| & | struct {
			Error string
		} | None | 2 |
| & | mappedFile | None | 2 |
| - | T | integer literal | 2 |
| * | *counterStateBits | None | 2 |
| + | string literal | float64 | 2 |
| >> | uint32 | uint32 | 2 |
| & | haveTag | None | 2 |
| & | normWriter | None | 2 |
| & | normReader | None | 2 |
| & | caseTrie | None | 2 |
| & | simpleCaser | None | 2 |
| & | chain | None | 2 |
| == | uint64 | uint64 | 2 |
| * | *elf.ProgHeader | None | 2 |
| & | binrep | None | 2 |
| & | elfMapping | None | 2 |
| & | plugin.Sym | None | 2 |
| & | graph.Options | None | 2 |
| & | graph.Tag | None | 2 |
| & | graph.DotAttributes | None | 2 |
| & | sourceFile | None | 2 |
| * | *profile.Function | None | 2 |
| & | source | None | 2 |
| & | settings | None | 2 |
| & | plugin.Options | None | 2 |
| & | Typed | None | 2 |
| & | TemplateParamQualifiedArg | None | 2 |
| & | Qualifiers | None | 2 |
| & | PointerType | None | 2 |
| & | RvalueReferenceType | None | 2 |
| & | ComplexType | None | 2 |
| & | ImaginaryType | None | 2 |
| & | TransformedType | None | 2 |
| & | VendorQualifier | None | 2 |
| & | FunctionType | None | 2 |
| & | PtrMem | None | 2 |
| & | FixedType | None | 2 |
| & | BitIntType | None | 2 |
| & | VectorType | None | 2 |
| & | ElaboratedType | None | 2 |
| & | Decltype | None | 2 |
| & | Constructor | None | 2 |
| & | TaggedName | None | 2 |
| & | ArgumentPack | None | 2 |
| & | SizeofPack | None | 2 |
| & | SizeofArgs | None | 2 |
| & | TypeTemplateParam | None | 2 |
| & | NonTypeTemplateParam | None | 2 |
| & | TemplateTemplateParam | None | 2 |
| & | ConstrainedTypeTemplateParam | None | 2 |
| & | TemplateParamPack | None | 2 |
| & | Cast | None | 2 |
| & | Nullary | None | 2 |
| & | Trinary | None | 2 |
| & | Subobject | None | 2 |
| & | PtrMemCast | None | 2 |
| & | New | None | 2 |
| & | Literal | None | 2 |
| & | StringLiteral | None | 2 |
| & | LambdaExpr | None | 2 |
| & | InitializerList | None | 2 |
| & | DefaultArg | None | 2 |
| & | StructuredBindings | None | 2 |
| & | Clone | None | 2 |
| & | Special2 | None | 2 |
| & | EnableIf | None | 2 |
| & | ModuleName | None | 2 |
| & | ModuleEntity | None | 2 |
| & | Friend | None | 2 |
| & | Constraint | None | 2 |
| & | RequiresExpr | None | 2 |
| & | ExprRequirement | None | 2 |
| & | TypeRequirement | None | 2 |
| & | NestedRequirement | None | 2 |
| & | ExplicitObjectParameter | None | 2 |
| * | *[]AST | None | 2 |
| & | testJSONFilter | None | 2 |
| & | argstate | None | 2 |
| == | *string | string literal | 2 |
| & | FuncType | None | 2 |
| & | ast.Expr | None | 2 |
| / | uint32 | uint32 | 2 |
| & | config | None | 2 |
| + | C.int | integer literal | 2 |
| & | C.S29748 | None | 2 |
| & | [256]byte | None | 2 |
| & | tracer | None | 2 |
| & | cgi.Handler | None | 2 |
| & | scanner.Error | None | 2 |
| & | []struct {
		Name  string
		Bool  bool
		Usage string
	} | None | 2 |
| & | load.PackageError | None | 2 |
| & | coverProvider | None | 2 |
| & | Tags | None | 2 |
| & | VCSError | None | 2 |
| & | resolver | None | 2 |
| & | importError | None | 2 |
| & | NoGoError | None | 2 |
| * | *Package | None | 2 |
| & | mainPackageError | None | 2 |
| & | jsonBuildEvent | None | 2 |
| & | invalidImportError | None | 2 |
| & | AmbiguousImportError | None | 2 |
| & | ImportMissingSumError | None | 2 |
| & | sumMissingError | None | 2 |
| & | DirectImportFromImplicitDependencyError | None | 2 |
| & | loadPkg | None | 2 |
| & | QueryMatchesMainModulesError | None | 2 |
| & | modfetch.Versions | None | 2 |
| & | ModuleGraph | None | 2 |
| & | cachedGraph | None | 2 |
| & | printer.CommentedNode | None | 2 |
| == | io.Writer | bytes.Buffer | 2 |
| < | byte | char literal | 2 |
| * | *urlpkg.URL | None | 2 |
| & | writeCountingDiscard | None | 2 |
| & | Cond | None | 2 |
| & | RWMutexMap | None | 2 |
| & | DeepCopyMap | None | 2 |
| & | isync.HashTrieMap[any, any] | None | 2 |
| & | sync.Map | None | 2 |
| & | struct {
		_ uint32
		i Int64
	} | None | 2 |
| & | struct {
		_ uint32
		i Uint64
	} | None | 2 |
| & | digest | None | 2 |
| == | Offset | integer literal | 2 |
| & | typeUnitReader | None | 2 |
| & | OptionalHeader32 | None | 2 |
| & | OptionalHeader64 | None | 2 |
| & | COFFSymbol | None | 2 |
| & | LineTable | None | 2 |
| & | *FormatError | None | 2 |
| == | DynTag | DynTag | 2 |
| & | Rpath | None | 2 |
| & | machoExe | None | 2 |
| & | image.YCbCr | None | 2 |
| & | slowestRGBA | None | 2 |
| & | slowerRGBA | None | 2 |
| & | image.Rectangle | None | 2 |
| * | *image.Point | None | 2 |
| << | int32 | integer literal | 2 |
| * | integer literal | quantIndex | 2 |
| * | integer literal | float64 | 2 |
| == | float32 | float32 | 2 |
| == | float32 | integer literal | 2 |
| + | float literal | float64 | 2 |
| << | uint64 | uint | 2 |
| * | complex128 | complex128 | 2 |
| - | float32 | None | 2 |
| == | *Int | *Int | 2 |
| / | float literal | float literal | 2 |
| * | *V | None | 2 |
| & | runtimeSource | None | 2 |
| & | netUDPConn | None | 2 |
| + | packetNumber | integer literal | 2 |
| & | labelError | None | 2 |
| & | bodyReader | None | 2 |
| & | quic.ApplicationError | None | 2 |
| & | bidiTrie | None | 2 |
| != | level | integer literal | 2 |
| & | [TagSize]byte | None | 2 |
| & | Cipher | None | 2 |
| * | *time.Time | None | 2 |
| & | asn1.Tag | None | 2 |
| != | asn1.Tag | asn1.Tag | 2 |
| & | [32]int8 | None | 2 |
| & | [8]int32 | None | 2 |
| & | [4]int64 | None | 2 |
| & | [16]uint16 | None | 2 |
| & | [64]int8 | None | 2 |
| & | [16]int32 | None | 2 |
| & | [8]int64 | None | 2 |
| & | [32]uint16 | None | 2 |
| & | int32 | int32 | 2 |
| ^ | int32 | None | 2 |
| & | T | T | 2 |
| | | T | T | 2 |
| & | asConversion | None | 2 |
| * | *opData | None | 2 |
| & | unify.DefBuilder | None | 2 |
| & | unifier | None | 2 |
| & | traceTree | None | 2 |
| & | yamlEncoder | None | 2 |
| & | decodeError | None | 2 |
| & | struct {
		NonPtr strMarshaler
		Ptr    strPtrMarshaler
	} | None | 2 |
| & | struct {
		Name string
	} | None | 2 |
| != | any | float literal | 2 |
| & | []Color | None | 2 |
| & | jsonv2.SemanticError | None | 2 |
| / | float64 | integer literal | 2 |
| & | []Size | None | 2 |
| & | OptionalsEmpty | None | 2 |
| & | OptionalsZero | None | 2 |
| & | OptionalsEmptyZero | None | 2 |
| & | StringTag | None | 2 |
| & | PointerCycle | None | 2 |
| & | PointerCycleIndirect | None | 2 |
| & | s1 | None | 2 |
| & | stringPointer | None | 2 |
| & | struct{ X RawMessage } | None | 2 |
| & | struct{ X *RawMessage } | None | 2 |
| & | marshalPanic | None | 2 |
| & | scanner | None | 2 |
| & | VOuter | None | 2 |
| & | struct {
			A chan int
			B complex128
			C int
			D func()
		} | None | 2 |
| & | Top | None | 2 |
| & | WrongString | None | 2 |
| & | map[stringKind]int | None | 2 |
| & | byteKind | None | 2 |
| & | []Uint8 | None | 2 |
| & | Time3339 | None | 2 |
| & | [0]any | None | 2 |
| & | S5 | None | 2 |
| & | S6 | None | 2 |
| & | S7 | None | 2 |
| & | S8 | None | 2 |
| & | S9 | None | 2 |
| & | unmarshalPanic | None | 2 |
| & | AllTypes | None | 2 |
| & | [2]int | None | 2 |
| != | [2]int | [2]int | 2 |
| & | decodeBuffer | None | 2 |
| & | pointerSuffixError | None | 2 |
| == | Kind | char literal | 2 |
| != | Kind | char literal | 2 |
| * | *[]objectMember | None | 2 |
| & | time.ParseError | None | 2 |
| & | jsonopts.Struct | None | 2 |
| & | structOmitZeroAll | None | 2 |
| & | structNestedAddr | None | 2 |
| & | allMethodsExceptJSONv2 | None | 2 |
| & | allMethodsExceptJSONv1 | None | 2 |
| & | allMethodsExceptText | None | 2 |
| & | onlyMethodJSONv2 | None | 2 |
| & | onlyMethodJSONv1 | None | 2 |
| & | onlyMethodText | None | 2 |
| * | *namedString | None | 2 |
| * | *[14]any | None | 2 |
| & | structField | None | 2 |
| == | uint64 | float literal | 2 |
| & | Marshalers | None | 2 |
| & | Unmarshalers | None | 2 |
| + | float literal | integer literal | 2 |
| & | struct{ N int64 } | None | 2 |
| & | struct {
		// GoStruct does not implement proto.Message and
		// should use the default behavior of the "json" package.
		GoStruct struct {
			Name string
			Age  int
		}

		// ProtoMessage implements proto.Message and
		// should be handled using protojson.Marshal.
		ProtoMessage *foopbMyMessage
	} | None | 2 |
| & | Tables | None | 2 |
| & | Child | None | 2 |
| & | NamePrecedence | None | 2 |
| & | AttrTest | None | 2 |
| & | OmitAttrTest | None | 2 |
| & | OmitFieldTest | None | 2 |
| & | AnySliceTest | None | 2 |
| & | RecurseA | None | 2 |
| & | DirectComment | None | 2 |
| & | DirectElement | None | 2 |
| & | DirectOmitEmpty | None | 2 |
| & | Passenger | None | 2 |
| & | Person | None | 2 |
| & | typeInfo | None | 2 |
| * | *fieldInfo | None | 2 |
| & | newlineFilteringReader | None | 2 |
| & | BlankFieldsProbe | None | 2 |
| & | N1 | None | 2 |
| & | Pythagoras | None | 2 |
| < | typeId | integer literal | 2 |
| & | arrayType | None | 2 |
| & | mapType | None | 2 |
| & | sliceType | None | 2 |
| & | structType | None | 2 |
| & | outi8 | None | 2 |
| & | outi16 | None | 2 |
| & | outi32 | None | 2 |
| & | InterfaceItem | None | 2 |
| & | BasicInterfaceItem | None | 2 |
| & | PtrInterfaceItem | None | 2 |
| & | ArrayStruct | None | 2 |
| & | GobTest1 | None | 2 |
| & | LargeSliceByte | None | 2 |
| & | LargeSliceInt8 | None | 2 |
| & | LargeSliceStruct | None | 2 |
| & | LargeSliceString | None | 2 |
| & | Gobber | None | 2 |
| & | error | None | 2 |
| & | struct{ Hello int } | None | 2 |
| & | Q | None | 2 |
| & | [7]int | None | 2 |
| & | NonStruct | None | 2 |
| & | interfaceIndirectTestT | None | 2 |
| & | struct{ A int } | None | 2 |
| & | Bug0Outer | None | 2 |
| * | *[]E | None | 2 |
| & | driverConn | None | 2 |
| & | fakeDriverCtx | None | 2 |
| & | row | None | 2 |
| & | rowsCursor | None | 2 |
| & | *Rows | None | 2 |
| & | *string | None | 2 |
| & | nvcConn | None | 2 |
| & | nvcDriver | None | 2 |
| << | rune | integer literal | 2 |
| & | W | None | 2 |
| & | map[string]string | None | 2 |
| & | TextNode | None | 2 |
| & | CommentNode | None | 2 |
| & | FieldNode | None | 2 |
| & | ChainNode | None | 2 |
| & | countReader | None | 2 |
| != | countReader | integer literal | 2 |
| | | char literal | rune | 2 |
| * | *rune | None | 2 |
| & | CommentedNode | None | 2 |
| & | ast.TypeAssertExpr | None | 2 |
| & | ast.LabeledStmt | None | 2 |
| & | ast.IncDecStmt | None | 2 |
| & | ast.GoStmt | None | 2 |
| & | ast.DeferStmt | None | 2 |
| & | ast.BranchStmt | None | 2 |
| & | ast.CaseClause | None | 2 |
| & | ast.SwitchStmt | None | 2 |
| & | ast.TypeSwitchStmt | None | 2 |
| & | ast.CommClause | None | 2 |
| & | ast.SelectStmt | None | 2 |
| & | ast.RangeStmt | None | 2 |
| & | ast.ForStmt | None | 2 |
| & | ast.TypeSpec | None | 2 |
| & | ast.BadDecl | None | 2 |
| & | ast.Package | None | 2 |
| < | Value | integer literal | 2 |
| - | Value | None | 2 |
| * | *Value | None | 2 |
| * | *[]Directive | None | 2 |
| & | NotExpr | None | 2 |
| & | exprParser | None | 2 |
| == | *Func | *Func | 2 |
| & | ArgumentError | None | 2 |
| & | Scope | None | 2 |
| & | Chan | None | 2 |
| & | Selection | None | 2 |
| * | *Func | None | 2 |
| & | typeWriter | None | 2 |
| & | StdSizes | None | 2 |
| & | typeError | None | 2 |
| & | Var | None | 2 |
| & | Named | None | 2 |
| & | types.StdSizes | None | 2 |
| & | indexedExpr | None | 2 |
| & | Comment | None | 2 |
| & | CommentGroup | None | 2 |
| == | uint8 | uint8 | 2 |
| * | *[4]uint64 | None | 2 |
| & | wycheproof.MacTestSchemaV1Json | None | 2 |
| & | ecdsa.Signature | None | 2 |
| & | C.size_t | None | 2 |
| == | crypto.Hash | integer literal | 2 |
| & | PublicKeyECDH | None | 2 |
| & | PrivateKeyECDH | None | 2 |
| & | aesCBC | None | 2 |
| * | *SHAKE | None | 2 |
| * | *p256Element | None | 2 |
| & | [43 * 32 * 2 * 4]uint64 | None | 2 |
| & | [p256UncompressedLength]byte | None | 2 |
| & | [p256ElementLength]byte | None | 2 |
| & | [p256CompressedLength]byte | None | 2 |
| ^ | uint | None | 2 |
| & | [p384ElementLen]byte | None | 2 |
| & | [p224ElementLen]byte | None | 2 |
| & | [p256ElementLen]byte | None | 2 |
| & | [p521ElementLen]byte | None | 2 |
| & | ExporterMasterSecret | None | 2 |
| * | *aes.Block | None | 2 |
| + | fieldElement | fieldElement | 2 |
| & | [4096]byte | None | 2 |
| & | Curve[*nistec.P224Point] | None | 2 |
| & | Curve[*nistec.P256Point] | None | 2 |
| & | Curve[*nistec.P384Point] | None | 2 |
| & | Curve[*nistec.P521Point] | None | 2 |
| & | [messageSize]byte | None | 2 |
| >> | int8 | integer literal | 2 |
| / | int8 | integer literal | 2 |
| & | fiatScalarNonMontgomeryDomainFieldElement | None | 2 |
| & | fiatScalarMontgomeryDomainFieldElement | None | 2 |
| & | dsa.Parameters | None | 2 |
| & | wycheproof.AeadTestSchemaV1Json | None | 2 |
| * | **key | None | 2 |
| & | mldsa.Options | None | 2 |
| & | wycheproof.MldsaSignSeedSchemaJson | None | 2 |
| & | sha3.SHA3 | None | 2 |
| & | cryptobyte_asn1.Tag | integer literal | 2 |
| & | net.IPNet | None | 2 |
| & | ecdh.PrivateKey | None | 2 |
| & | nameConstraintsSet[*net.IPNet, net.IP] | None | 2 |
| & | dnsConstraints | None | 2 |
| & | brokenSigner | None | 2 |
| & | pkix.AlgorithmIdentifier | None | 2 |
| & | certificateRequest | None | 2 |
| & | echServerContext | None | 2 |
| & | keySharePrivateKeys | None | 2 |
| & | CertificateRequestInfo | None | 2 |
| & | certificateMsg | None | 2 |
| & | certificateStatusMsg | None | 2 |
| & | clientKeyExchangeMsg | None | 2 |
| & | newSessionTicketMsg | None | 2 |
| & | endOfEarlyDataMsg | None | 2 |
| & | newSessionTicketMsgTLS13 | None | 2 |
| & | certificateRequestMsgTLS13 | None | 2 |
| & | testQUICConn | None | 2 |
| & | xorNonceAEAD | None | 2 |
| & | ecdheKeyAgreement | None | 2 |
| & | PKCS1v15DecryptOptions | None | 2 |
| & | mlkemKEM | None | 2 |
| & | mlkemPrivateKey | None | 2 |
| & | dhKEMPublicKey | None | 2 |
| & | shakeKDF | None | 2 |
| & | countingReader | None | 2 |
| & | Plugin | None | 2 |
| & | fs.FileMode | integer literal | 2 |
| & | dirReader | None | 2 |
| & | suffixSaver | None | 2 |
| & | sparseFile | None | 2 |
| * | *sparseSpan | None | 2 |
| & | header | None | 2 |
| & | fileWriter | None | 2 |
| & | sparseFileWriter | None | 2 |
| & | sparseFileReader | None | 2 |
| & | readSeeker | None | 2 |
| & | readBadSeeker | None | 2 |
| & | nameSpace | None | 2 |
| & | rangeContext | None | 2 |
| & | URLValue | None | 1 |
| * | *time.Duration | None | 1 |
| & | Flag | None | 1 |
| & | FlagSet | None | 1 |
| & | interval | None | 1 |
| != | integer literal | integer literal | 1 |
| & | Form | None | 1 |
| & | maliciousReader | None | 1 |
| & | sentinelReader | None | 1 |
| & | stickyErrorReader | None | 1 |
| & | part | None | 1 |
| & | failOnReadAfterErrorReader | None | 1 |
| & | mail.Message | None | 1 |
| & | openFile | None | 1 |
| & | visibleFieldsWalker | None | 1 |
| & | rtype | None | 1 |
| * | *structType | None | 1 |
| | | uintptr | integer literal | 1 |
| & | abi.Type | None | 1 |
| & | [4]Small | None | 1 |
| & | [64]Small | None | 1 |
| & | MapIter | None | 1 |
| & | func([]Value) []Value | None | 1 |
| & | unsafeheader.String | None | 1 |
| & | func(int, int) (int, int) | None | 1 |
| & | func(float64, float64) (float64, float64) | None | 1 |
| & | makeFuncImpl | None | 1 |
| & | methodValue | None | 1 |
| != | *int32 | integer literal | 1 |
| & | struct {
		W io.Writer
	} | None | 1 |
| & | interface {
		Dist(int) int
	} | None | 1 |
| & | Tinter | None | 1 |
| & | struct {
		I any
		P interface {
			Dist(int) int
		}
	} | None | 1 |
| & | InnerInt | None | 1 |
| & | OuterInt | None | 1 |
| & | struct {
		B *bool
	} | None | 1 |
| & | Public | None | 1 |
| & | Private | None | 1 |
| & | io.ReadWriter | None | 1 |
| & | Outer | None | 1 |
| & | func(*int, int) int | None | 1 |
| < | any | integer literal | 1 |
| > | any | integer literal | 1 |
| & | SectionReader | None | 1 |
| & | OffsetWriter | None | 1 |
| & | teeReader | None | 1 |
| & | writeStringChecker | None | 1 |
| & | multiReader | None | 1 |
| & | multiWriter | None | 1 |
| & | PipeWriter | None | 1 |
| != | FileMode | FileMode | 1 |
| < | Priority | integer literal | 1 |
| == | Level | integer literal | 1 |
| > | Level | integer literal | 1 |
| & | LevelHandler | None | 1 |
| & | jsonEncoder | None | 1 |
| & | mockFailingHandler | None | 1 |
| & | struct{ A, b int } | None | 1 |
| & | struct {
		M []string `json:"m"`
	} | None | 1 |
| & | handleState | None | 1 |
| & | req | None | 1 |
| & | setVisitor | None | 1 |
| & | Logger | None | 1 |
| & | fastTextHandler | None | 1 |
| & | asyncHandler | None | 1 |
| & | indirect[T] | None | 1 |
| & | entry[T] | None | 1 |
| & | uniqueMap[T] | None | 1 |
| & | SockaddrDatalink | None | 1 |
| <= | char literal | int | 1 |
| <= | int | char literal | 1 |
| & | prestat | None | 1 |
| == | oflags | integer literal | 1 |
| == | fdflags | integer literal | 1 |
| & | iovec | None | 1 |
| & | filesize | None | 1 |
| & | BpfProgram | None | 1 |
| & | BpfVersion | None | 1 |
| & | waitErr | None | 1 |
| * | *Waitmsg | None | 1 |
| & | NetlinkRouteRequest | None | 1 |
| & | SockaddrNetlink | None | 1 |
| & | ByHandleFileInformation | None | 1 |
| * | *IPv6Mreq | None | 1 |
| & | procThreadAttributeListContainer | None | 1 |
| & | jsFile | None | 1 |
| & | syscall.Timeval | None | 1 |
| & | syscall.Statfs_t | None | 1 |
| & | SockaddrLinklayer | None | 1 |
| & | SockFprog | None | 1 |
| & | statx_t | None | 1 |
| & | cloneArgs | None | 1 |
| & | sigInfo | None | 1 |
| & | syscall.StartupInfo | None | 1 |
| & | readRune | None | 1 |
| & | wrapError | None | 1 |
| & | wrapErrors | None | 1 |
| & | [3]byte | None | 1 |
| & | reflect.Value | None | 1 |
| & | flagPrinter | None | 1 |
| * | Xs | None | 1 |
| & | eofCounter | None | 1 |
| * | string | None | 1 |
| & | hexBytes | None | 1 |
| != | addrAttrs | addrAttrs | 1 |
| > | addrAttrs | addrAttrs | 1 |
| & | rulesParser | None | 1 |
| / | integer literal | uint64 | 1 |
| & | FILE_DISPOSITION_INFORMATION_EX | None | 1 |
| & | FILE_BASIC_INFO | None | 1 |
| & | FILE_DISPOSITION_INFO | None | 1 |
| & | FILE_DISPOSITION_INFORMATION | None | 1 |
| & | TOKEN_PRIVILEGES | None | 1 |
| & | *windows.ACL | None | 1 |
| & | windows.TOKEN_MANDATORY_LABEL | None | 1 |
| & | FILE_MODE_INFORMATION | None | 1 |
| & | DynamicTimezoneinformation | None | 1 |
| & | KeyInfo | None | 1 |
| == | syscall.Errno | integer literal | 1 |
| & | DeadlineExceededError | None | 1 |
| & | asyncIO | None | 1 |
| & | windows.WSAMsg | None | 1 |
| & | _TCP_INFO_v0 | None | 1 |
| & | syscall.Overlapped | None | 1 |
| & | spilledBatch | None | 1 |
| == | extraStringID | integer literal | 1 |
| - | extraStringID | integer literal | 1 |
| == | EI | integer literal | 1 |
| / | EI | integer literal | 1 |
| % | EI | integer literal | 1 |
| & | MMUCurve | None | 1 |
| & | pState | None | 1 |
| & | Summarizer | None | 1 |
| & | UserTaskSummary | None | 1 |
| & | Summary | None | 1 |
| & | traceV1Converter | None | 1 |
| & | Trace | None | 1 |
| & | Generation | None | 1 |
| & | parser | None | 1 |
| * | *Event | None | 1 |
| & | Version | None | 1 |
| & | Validator | None | 1 |
| & | goState | None | 1 |
| & | procState | None | 1 |
| & | schedContext | None | 1 |
| & | TextWriter | None | 1 |
| & | TextReader | None | 1 |
| & | Emitter | None | 1 |
| & | format.GoroutineCountersArg | None | 1 |
| & | format.ThreadCountersArg | None | 1 |
| & | profile.Profile | None | 1 |
| & | mmu | None | 1 |
| & | bigarFileHeader | None | 1 |
| & | bigarMemberHeader | None | 1 |
| & | [2]byte | None | 1 |
| & | Bubble | None | 1 |
| & | goexperiment.Flags | None | 1 |
| & | [hashRandomBytes]byte | None | 1 |
| & | bitset | integer literal | 1 |
| >> | bitset | integer literal | 1 |
| ^ | uintptr | uintptr | 1 |
| & | fifo | None | 1 |
| & | lineReader | None | 1 |
| != | [8]mat8x8 | [8]mat8x8 | 1 |
| & | [8]mat8x8 | None | 1 |
| + | *uintptr | uintptr | 1 |
| & | *uint8 | uint8 | 1 |
| | | *uint8 | uint8 | 1 |
| & | *uint32 | uint32 | 1 |
| | | *uint32 | uint32 | 1 |
| == | *int32 | int32 | 1 |
| == | *int64 | int64 | 1 |
| == | *unsafe.Pointer | unsafe.Pointer | 1 |
| == | *uintptr | uintptr | 1 |
| + | *int32 | int32 | 1 |
| + | *int64 | int64 | 1 |
| & | mockRand | None | 1 |
| & | worker | None | 1 |
| & | workerClient | None | 1 |
| & | minimizeArgs | None | 1 |
| & | fuzzArgs | None | 1 |
| & | pingArgs | None | 1 |
| & | pingResponse | None | 1 |
| & | coordinator | None | 1 |
| & | MalformedCorpusError | None | 1 |
| & | CgroupV2 | None | 1 |
| & | []listEntry | None | 1 |
| & | zstdError | None | 1 |
| & | isync.HashTrieMap[string, int] | None | 1 |
| & | indirect[K, V] | None | 1 |
| & | entry[K, V] | None | 1 |
| >= | string | string literal | 1 |
| >> | uint32 | int | 1 |
| == | B | B | 1 |
| == | A | A | 1 |
| == | L | L | 1 |
| == | S | S | 1 |
| == | F | F | 1 |
| == | I | I | 1 |
| == | J | J | 1 |
| == | M | M | 1 |
| == | C | C | 1 |
| < | B | B | 1 |
| < | A | A | 1 |
| < | L | L | 1 |
| < | S | S | 1 |
| < | I | I | 1 |
| < | J | J | 1 |
| < | M | M | 1 |
| < | C | C | 1 |
| / | integer literal | struct{ x int } | 1 |
| & | concreteF /* ERROR "not enough type arguments for type concreteF: have 1, want 2" */ [RCT] | None | 1 |
| & | [10]bool | None | 1 |
| / | float literal (suffix i) | integer literal | 1 |
| == | *interface{} | interface{} | 1 |
| < | integer literal | *int | 1 |
| & | Fooable[*FooerImpl[F]] | None | 1 |
| & | FooerImpl[F] | None | 1 |
| == | thing1 | thing1 | 1 |
| == | thing2 | thing2 | 1 |
| & | G[int] | None | 1 |
| << | integer literal | float64 | 1 |
| & | ImplA[T] | None | 1 |
| + | string | int | 1 |
| || | mybool | bool | 1 |
| && | mybool | bool | 1 |
| << | int | int | 1 |
| >> | int | int | 1 |
| + | myint | integer literal | 1 |
| + | myint | int | 1 |
| - | myint | int | 1 |
| * | myint | int | 1 |
| / | myint | int | 1 |
| % | myint | int | 1 |
| << | myint | int | 1 |
| >> | myint | int | 1 |
| / | uint | uint | 1 |
| % | uint | uint | 1 |
| + | myuint | integer literal | 1 |
| + | myuint | uint | 1 |
| - | myuint | uint | 1 |
| * | myuint | uint | 1 |
| / | myuint | uint | 1 |
| % | myuint | uint | 1 |
| << | myuint | uint | 1 |
| >> | myuint | uint | 1 |
| % | float64 | float64 | 1 |
| << | float64 | float64 | 1 |
| >> | float64 | float64 | 1 |
| + | myfloat64 | float64 | 1 |
| - | myfloat64 | float64 | 1 |
| * | myfloat64 | float64 | 1 |
| / | myfloat64 | float64 | 1 |
| % | myfloat64 | float64 | 1 |
| << | myfloat64 | float64 | 1 |
| >> | myfloat64 | float64 | 1 |
| - | string | string literal | 1 |
| + | string | integer literal | 1 |
| - | string | string | 1 |
| * | string | integer literal | 1 |
| && | bool literal | bool literal | 1 |
| << | integer literal | string literal | 1 |
| << | char literal | integer literal | 1 |
| >> | float literal | float literal | 1 |
| * | T | None | 1 |
| << | integer literal | uint64 | 1 |
| / | interface{} | integer literal | 1 |
| == | bool literal | integer literal | 1 |
| % | integer literal | float literal | 1 |
| == | [iota-1]int | [iota]int | 1 |
| == | [Two]int | [iota]int | 1 |
| == | [2]int | [iota]int | 1 |
| == | b | b | 1 |
| & | bool literal | None | 1 |
| + | string literal | None | 1 |
| & | map[string]T | None | 1 |
| & | Sender[T] | None | 1 |
| & | Receiver[T] | None | 1 |
| & | T14 | None | 1 |
| == | [10]int | [10]int | 1 |
| != | [10]int | [10]int | 1 |
| < | [10]int | [10]int | 1 |
| == | [10]int | C | 1 |
| == | C | D | 1 |
| == | [10]func() int | [10]func() int | 1 |
| == | struct {
		x int
		a [10]float32
		_ bool
	} | struct {
		x int
		a [10]float32
		_ bool
	} | 1 |
| != | struct {
		x int
		a [10]float32
		_ bool
	} | struct {
		x int
		a [10]float32
		_ bool
	} | 1 |
| < | struct {
		x int
		a [10]float32
		_ bool
	} | struct {
		x int
		a [10]float32
		_ bool
	} | 1 |
| == | struct {
		x int
		a [10]float32
		_ bool
	} | S | 1 |
| == | S | T | 1 |
| == | struct {
		x int
		a [10]map[string]int
	} | struct {
		x int
		a [10]map[string]int
	} | 1 |
| != | *int | *int | 1 |
| <= | *int | *int | 1 |
| >= | *int | *int | 1 |
| == | chan int | chan int | 1 |
| != | chan int | chan int | 1 |
| < | chan int | chan int | 1 |
| == | interface{ m() int } | interface{ m() int } | 1 |
| != | interface{ m() int } | interface{ m() int } | 1 |
| < | interface{ m() int } | interface{ m() int } | 1 |
| == | interface{ m() int } | interface { m() int; n() } | 1 |
| == | interface{ m() int } | interface { m() float32 } | 1 |
| == | interface{ m() int } | integer literal | 1 |
| == | interface{ m() int } | S11 | 1 |
| & | S11 | None | 1 |
| == | interface{} | []int | 1 |
| == | []int | interface{} | 1 |
| < | interface{} | int | 1 |
| < | int | interface{} | 1 |
| == | []int | []int | 1 |
| < | []int | []int | 1 |
| == | map[string]int | map[string]int | 1 |
| < | map[string]int | map[string]int | 1 |
| == | func(int) float32 | func(int) float32 | 1 |
| < | func(int) float32 | func(int) float32 | 1 |
| == | AB | interface {
	A
	B
} | 1 |
| & | hasMethods1 | None | 1 |
| & | hasMethods2 | None | 1 |
| & | ExperimentFlags | None | 1 |
| & | connHalf | None | 1 |
| & | PacketNet | None | 1 |
| & | PacketConn | None | 1 |
| & | packet | None | 1 |
| & | Listener | None | 1 |
| & | Setting | None | 1 |
| & | runtimeStderr | None | 1 |
| + | int | None | 1 |
| == | complex128 | complex128 | 1 |
| % | uint64 | float literal | 1 |
| | | byte | char literal | 1 |
| & | PtyError | None | 1 |
| & | CoverageDataWriter | None | 1 |
| & | CoverageMetaDataDecoder | None | 1 |
| & | CoverageMetaFileReader | None | 1 |
| & | Formatter | None | 1 |
| & | CoverageMetaFileWriter | None | 1 |
| & | CoverageMetaDataBuilder | None | 1 |
| & | tstate | None | 1 |
| & | coverage.MetaFileCollection | None | 1 |
| & | failingWriter | None | 1 |
| & | CounterDataReader | None | 1 |
| & | packedInts | None | 1 |
| != | float64 | float literal | 1 |
| & | benchState | None | 1 |
| & | PB | None | 1 |
| == | highPrecisionTime | highPrecisionTime | 1 |
| != | highPrecisionTime | highPrecisionTime | 1 |
| & | funcWriter | None | 1 |
| & | chattyPrinter | None | 1 |
| & | outputWriter | None | 1 |
| & | slog.Record | None | 1 |
| & | testLog | None | 1 |
| & | oneByteReader | None | 1 |
| & | halfReader | None | 1 |
| & | dataErrReader | None | 1 |
| & | timeoutReader | None | 1 |
| & | errReader | None | 1 |
| & | truncateWriter | None | 1 |
| & | writeLogger | None | 1 |
| & | readLogger | None | 1 |
| & | CheckError | None | 1 |
| & | CheckEqualError | None | 1 |
| & | openMapFile | None | 1 |
| & | mapDir | None | 1 |
| & | shuffledFile | None | 1 |
| & | lockedReader | None | 1 |
| & | Replacer | None | 1 |
| & | singleStringReplacer | None | 1 |
| & | stringFinder | None | 1 |
| >= | *int | integer literal | 1 |
| & | nonDeterministicTestingData | None | 1 |
| & | testingData | None | 1 |
| & | adversaryTestingData | None | 1 |
| & | reverse | None | 1 |
| - | float literal | int | 1 |
| & | multiSorter | None | 1 |
| & | planetSorter | None | 1 |
| * | *dnsmessage.Parser | None | 1 |
| & | dualStackServer | None | 1 |
| - | time.Duration | integer literal | 1 |
| + | time.Duration | time.Duration | 1 |
| * | *Interface | None | 1 |
| & | resolvConfTest | None | 1 |
| & | fakeDNSConn | None | 1 |
| & | fakeDNSPacketConn | None | 1 |
| & | dnsmessage.CNAMEResource | None | 1 |
| & | ifStats | None | 1 |
| & | syscall.IPv6Mreq | None | 1 |
| & | syscall.AddrinfoW | None | 1 |
| & | IPConn | None | 1 |
| & | UnixConn | None | 1 |
| & | rawListener | None | 1 |
| & | onlyValuesCtx | None | 1 |
| & | DNSConfigError | None | 1 |
| & | Buffers | None | 1 |
| & | ifreq | None | 1 |
| & | syscall.Linger | None | 1 |
| & | syscall.SockaddrInet6 | None | 1 |
| & | fakeNetFD | None | 1 |
| & | packetQueue | None | 1 |
| & | deadlineTimer | None | 1 |
| & | resolverDialHandler | None | 1 |
| & | resolverFuncConn | None | 1 |
| & | syscall.IPMreq | None | 1 |
| & | AddressParser | None | 1 |
| * | *URL | None | 1 |
| & | Prefix | None | 1 |
| & | net.UDPAddr | None | 1 |
| & | Stat | None | 1 |
| & | textproto.Error | None | 1 |
| & | dataCloser | None | 1 |
| & | plainAuth | None | 1 |
| & | cramMD5Auth | None | 1 |
| & | populateResponse | None | 1 |
| & | http2.Server | None | 1 |
| & | http2.ServeConnOpts | None | 1 |
| & | http2.ServerRequest | None | 1 |
| & | http2.ClientRequest | None | 1 |
| * | *HTTP2Config | None | 1 |
| * | integer literal | time.Duration | 1 |
| & | internal.FlushAfterChunkWriter | None | 1 |
| & | TestJar | None | 1 |
| & | roundTripperGetBody | None | 1 |
| & | issue40382Body | None | 1 |
| & | CrossOriginProtection | None | 1 |
| & | noopHandler | None | 1 |
| & | clientServerTest | None | 1 |
| * | *Response | None | 1 |
| & | testListener | None | 1 |
| * | *multipart.FileHeader | None | 1 |
| & | transportDialTester | None | 1 |
| & | transportDialTesterConn | None | 1 |
| & | transportDialTesterRoundTrip | None | 1 |
| & | cancelTimerBody | None | 1 |
| & | infiniteReader | None | 1 |
| & | socksConn | None | 1 |
| & | socksDialer | None | 1 |
| & | testConnSet | None | 1 |
| & | testCloseConn | None | 1 |
| & | transport100ContinueTest | None | 1 |
| & | writerFuncConn | None | 1 |
| & | funcConn | None | 1 |
| & | logWritesConn | None | 1 |
| & | testMockTCPConn | None | 1 |
| & | bodyCloser | None | 1 |
| ! | bodyCloser | None | 1 |
| & | breakableConn | None | 1 |
| & | http1ServerTest | None | 1 |
| & | http1TestConn | None | 1 |
| & | byteAtATimeReader | None | 1 |
| != | *Cookie | string literal | 1 |
| + | *Cookie | string literal | 1 |
| & | maxBytesReader | None | 1 |
| & | MaxBytesError | None | 1 |
| & | testConn | None | 1 |
| & | blockingRemoteAddrConn | None | 1 |
| & | blockingRemoteAddrListener | None | 1 |
| & | fakeConnectionStateConn | None | 1 |
| & | slowTestConn | None | 1 |
| & | bodyLimitReader | None | 1 |
| & | errorListener | None | 1 |
| & | closeWriteTestConn | None | 1 |
| & | fakeNetListener | None | 1 |
| & | fakeNetConnHalf | None | 1 |
| & | asyncResult[T] | None | 1 |
| & | ResponseController | None | 1 |
| & | pattern | None | 1 |
| & | fileHandler | None | 1 |
| & | countingWriter | None | 1 |
| & | testFileSystem | None | 1 |
| & | fakeFile | None | 1 |
| & | mockTransferWriter | None | 1 |
| > | ConnState | integer literal | 1 |
| < | ConnState | integer literal | 1 |
| & | connReader | None | 1 |
| & | expectContinueReader | None | 1 |
| & | redirectHandler | None | 1 |
| & | onceCloseListener | None | 1 |
| & | http3ServerHandler | None | 1 |
| & | timeoutWriter | None | 1 |
| & | loggingConn | None | 1 |
| & | http09Writer | None | 1 |
| & | streamReader | None | 1 |
| & | arrayReader | None | 1 |
| & | wantConn | None | 1 |
| & | socksUsernamePassword | None | 1 |
| & | bodyEOFSignal | None | 1 |
| & | readWriteCloserBody | None | 1 |
| & | readerAndCloser | None | 1 |
| == | error | any | 1 |
| & | ResponseRecorder | None | 1 |
| & | streamWriter | None | 1 |
| & | bufWriter | None | 1 |
| & | child | None | 1 |
| & | nilCloser | None | 1 |
| & | signalingNopWriteCloser | None | 1 |
| & | chunkedReader | None | 1 |
| & | chunkedWriter | None | 1 |
| & | bufferedWriter | None | 1 |
| & | httpError | None | 1 |
| & | testClientConn | None | 1 |
| & | testRequestBody | None | 1 |
| & | testTransport | None | 1 |
| & | outflow | None | 1 |
| & | frameCache | None | 1 |
| & | DataFrame | None | 1 |
| & | Framer | None | 1 |
| & | UnknownFrame | None | 1 |
| & | roundRobinWriteScheduler | None | 1 |
| == | bool | bool literal | 1 |
| & | blockingWriteConn | None | 1 |
| & | slowWriteConn | None | 1 |
| & | slowCloser | None | 1 |
| & | tls.Certificate | None | 1 |
| & | priorityWriteSchedulerRFC9218 | None | 1 |
| & | handlerPanicRST | None | 1 |
| & | synctestNetConnHalf | None | 1 |
| & | transportTestHooks | None | 1 |
| & | dialCall | None | 1 |
| & | addConnCall | None | 1 |
| < | *T | T | 1 |
| > | *T | T | 1 |
| & | responseWriterState | None | 1 |
| & | ServeConnOpts | None | 1 |
| & | writePing | None | 1 |
| & | writeGoAway | None | 1 |
| * | *ServerRequest | None | 1 |
| & | requestBody | None | 1 |
| & | startPushRequest | None | 1 |
| & | writePushPromise | None | 1 |
| & | serverTester | None | 1 |
| & | serverHandlerCall | None | 1 |
| == | *uint32 | integer literal | 1 |
| & | clientConnReadLoop | None | 1 |
| & | tls.Dialer | None | 1 |
| >= | byte | integer literal | 1 |
| & | Jar | None | 1 |
| & | cookiejar.Options | None | 1 |
| & | customWriterRecorder | None | 1 |
| & | mockFlusher | None | 1 |
| & | wrappedRW | None | 1 |
| & | testReadWriteCloser | None | 1 |
| - | time.Duration | None | 1 |
| & | ServerConn | None | 1 |
| & | httputil.ReverseProxy | None | 1 |
| & | ProxyRequest | None | 1 |
| & | maxLatencyWriter | None | 1 |
| & | nettrace.Trace | None | 1 |
| & | dotReader | None | 1 |
| & | dotWriter | None | 1 |
| & | shutdownCodec | None | 1 |
| * | *R | None | 1 |
| & | gobClientCodec | None | 1 |
| & | methodType | None | 1 |
| & | gobServerCodec | None | 1 |
| & | writeCrasher | None | 1 |
| & | clientCodec | None | 1 |
| & | serverCodec | None | 1 |
| & | [1]any | None | 1 |
| * | *[1]int | None | 1 |
| & | rpc.Response | None | 1 |
| & | vdsoInfo | None | 1 |
| & | [_CTL_MAXNAME]uint32 | None | 1 |
| & | umtx_time | None | 1 |
| * | *umtx_time | None | 1 |
| * | *gList | None | 1 |
| & | gQueue | None | 1 |
| * | *heapStatsDelta | None | 1 |
| & | *pthreadkey | None | 1 |
| & | Frames | None | 1 |
| & | funcinl | None | 1 |
| & | [8192]byte | None | 1 |
| & | goroutineState | None | 1 |
| & | synctestBubble | None | 1 |
| & | ttiResult | None | 1 |
| & | ttiWrapper | None | 1 |
| & | traceback | None | 1 |
| & | [10]byte | None | 1 |
| & | childInfo | None | 1 |
| & | [typeCacheBuckets]typeCacheBucket | None | 1 |
| & | *abi.Type | None | 1 |
| & | stkframe | None | 1 |
| & | interface {
	F()
} | None | 1 |
| & | struct {
		SizeOfOpaqueState uint32
		MmapProt          uint32
		MmapFlags         uint32
		reserved          [13]uint32
	} | None | 1 |
| | | int | integer literal | 1 |
| >> | uintptr | uintptr | 1 |
| & | windows.Context | None | 1 |
| & | notInHeapSlice | None | 1 |
| * | **_type | None | 1 |
| != | uintptr | uintptr | 1 |
| == | *uint8 | integer literal | 1 |
| - | uintptr | None | 1 |
| & | runtime.TraceStackTable | None | 1 |
| & | savedOpenDeferState | None | 1 |
| & | timespec32 | None | 1 |
| & | Y | None | 1 |
| & | *int | None | 1 |
| == | any | string literal | 1 |
| == | memHdrPtr | integer literal | 1 |
| << | integer literal | uintptr | 1 |
| == | nameOff | integer literal | 1 |
| == | textOff | integer literal | 1 |
| & | nameOff | None | 1 |
| == | *_type | *_type | 1 |
| > | string | string | 1 |
| != | uint64 | uint64 | 1 |
| & | contentionWorker | None | 1 |
| & | addrRanges | None | 1 |
| * | *[tmpStringBufSize]rune | None | 1 |
| & | stringStruct | None | 1 |
| & | *[]arenaIdx | None | 1 |
| / | statDep | integer literal | 1 |
| % | statDep | integer literal | 1 |
| & | statAggregate | None | 1 |
| & | buildexe | None | 1 |
| & | [256]uint64 | None | 1 |
| & | TintPointer | None | 1 |
| / | float literal | int32 | 1 |
| & | sigevent | None | 1 |
| & | linux.Utsname | None | 1 |
| & | *libFunc | None | 1 |
| >= | uint64 | float literal | 1 |
| & | PIController | None | 1 |
| & | UserArena | None | 1 |
| & | TimeHistogram | None | 1 |
| != | *T | T | 1 |
| & | [32]*int | None | 1 |
| & | ucontextt | None | 1 |
| & | xtreeNode | None | 1 |
| & | stkobjT | None | 1 |
| == | *g | *g | 1 |
| * | *S | None | 1 |
| & | *funcval | None | 1 |
| & | [2048]byte | None | 1 |
| & | [20]byte | None | 1 |
| & | libcCallInfo | None | 1 |
| & | pthread | None | 1 |
| & | struct {
		t            int64  // raw timer
		numer, denom uint32 // conversion factors. nanoseconds = t * numer / denom.
	} | None | 1 |
| & | machMsgTypeNumber | None | 1 |
| & | machPort | None | 1 |
| & | bigValue | None | 1 |
| & | Object2 | None | 1 |
| & | Object1 | None | 1 |
| & | [callbackMaxFrame]byte | None | 1 |
| * | *mSpanList | None | 1 |
| == | lockRank | integer literal | 1 |
| < | lockRank | lockRank | 1 |
| & | HashSet | None | 1 |
| & | EfaceKey | None | 1 |
| & | IfaceKey | None | 1 |
| & | smallScalar | None | 1 |
| & | smallPointerMix | None | 1 |
| & | []struct{} | None | 1 |
| & | []S | None | 1 |
| != | int | any | 1 |
| != | *int | int | 1 |
| & | debugCallWrapArgs | None | 1 |
| & | listedValManual | None | 1 |
| & | objWith[unsafe.Pointer] | None | 1 |
| & | objWith[*objWith[*obj]] | None | 1 |
| & | sockaddr_un | None | 1 |
| & | subscription | None | 1 |
| / | timestamp | integer literal | 1 |
| % | timestamp | integer literal | 1 |
| & | randstate | None | 1 |
| & | stackArgs | None | 1 |
| & | struct {
		in  [N]int
		out [N]int
	} | None | 1 |
| * | **runtime.G | None | 1 |
| & | *runtime.G | None | 1 |
| * | *[]*byte | None | 1 |
| & | listedVal | None | 1 |
| == | *note | *note | 1 |
| & | timeoutEvent | None | 1 |
| & | func(frame unsafe.Pointer) | None | 1 |
| == | Writer | Writer | 1 |
| * | *Item | None | 1 |
| & | msg | None | 1 |
| == | MyI | integer literal | 1 |
| & | RpcChan | None | 1 |
| * | **inltype | None | 1 |
| & | struct{ b bool } | None | 1 |
| & | P2 | None | 1 |
| & | recorder | None | 1 |
| ^ | uintptr | None | 1 |
| * | *tiny | None | 1 |
| & | panicError | None | 1 |
| & | C.pthread_key_t | None | 1 |
| + | *int | *int | 1 |
| & | addrConn_grpc862 | None | 1 |
| & | ClientConn_grpc862 | None | 1 |
| & | httpMembersAPI_etcd6708 | None | 1 |
| & | httpClusterClient_etcd6708 | None | 1 |
| & | HugoSites_hugo5379 | None | 1 |
| & | PageCollections_hugo5379 | None | 1 |
| & | Site_hugo5379 | None | 1 |
| & | shortcodeHandler_hugo5379 | None | 1 |
| & | sitesBuilder_hugo5379 | None | 1 |
| & | Page_hugo5379 | None | 1 |
| & | pageInit_hugo5379 | None | 1 |
| & | pageContentInit_hugo5379 | None | 1 |
| & | serviceVM_moby36114 | None | 1 |
| & | Stream_grpc1460 | None | 1 |
| & | http2Client_grpc1460 | None | 1 |
| & | simpleTokenTTLKeeper_etcd7492 | None | 1 |
| & | tokenSimple_etcd7492 | None | 1 |
| & | authStore_etcd7492 | None | 1 |
| & | benchmarkClient_grpc660 | None | 1 |
| & | loggingT_cockroach9935 | None | 1 |
| & | Breaker_serving2137 | None | 1 |
| & | DeviceSet_moby4951 | None | 1 |
| & | Rows_cockroach13755 | None | 1 |
| & | statusManager_kubernetes10182 | None | 1 |
| & | federatedInformerImpl_kubernetes30872 | None | 1 |
| & | DeltaFIFO_kubernetes30872 | None | 1 |
| & | Config_kubernetes30872 | None | 1 |
| & | Controller_kubernetes30872 | None | 1 |
| & | NamespaceController_kubernetes30872 | None | 1 |
| & | DelayingDeliverer_kubernetes30872 | None | 1 |
| * | *watchCacheEvent_kubernetes38669 | None | 1 |
| & | cacheWatcher_kubernetes38669 | None | 1 |
| & | raftLogQueue | None | 1 |
| & | baseQueue | None | 1 |
| & | Store_cockroach3710 | None | 1 |
| & | lessor_etcd10492 | None | 1 |
| & | Container_moby28462 | None | 1 |
| & | State_moby28462 | None | 1 |
| & | Health_moby28462 | None | 1 |
| & | Daemon_moby28462 | None | 1 |
| & | idleAwareFramer_kubernetes6632 | None | 1 |
| & | Connection_kubernetes6632 | None | 1 |
| & | Stream_grpc1275 | None | 1 |
| & | recvBufferReader_grpc1275 | None | 1 |
| & | recvBuffer_grpc1275 | None | 1 |
| & | http2Client_grpc1275 | None | 1 |
| & | Stopper_cockroach1055 | None | 1 |
| & | Reflector_kubernetes13135 | None | 1 |
| & | WatchCache_kubernetes13135 | None | 1 |
| & | Cacher_kubernetes13135 | None | 1 |
| & | node_etcd6857 | None | 1 |
| & | ResourceQuotaController_kubernetes58107 | None | 1 |
| & | watchChan_kubernetes25331 | None | 1 |
| & | Stopper_cockroach24808 | None | 1 |
| & | Compactor_cockroach24808 | None | 1 |
| & | Stopper_cockroach1462 | None | 1 |
| & | localInterceptableTransport_cockroach1462 | None | 1 |
| & | LeaseManager_cockroach7504 | None | 1 |
| & | LeaseSet_cockroach7504 | None | 1 |
| & | tableNameCache_cockroach7504 | None | 1 |
| & | tableState_cockroach7504 | None | 1 |
| & | Store_cockroach10214 | None | 1 |
| & | Session_cockroach16167 | None | 1 |
| & | Executor_cockroach16167 | None | 1 |
| & | Stopper_cockroach25456 | None | 1 |
| & | Replica_cockroach25456 | None | 1 |
| & | consistencyQueue_cockroach25456 | None | 1 |
| & | Store_cockroach25456 | None | 1 |
| & | ClientConn_grpc1424 | None | 1 |
| & | roundRobin_grpc1424 | None | 1 |
| & | subConnCacheEntry_grpc3017 | None | 1 |
| & | lbCacheClientConn_grpc3017 | None | 1 |
| & | Server_grpc795 | None | 1 |
| & | test_grpc795 | None | 1 |
| & | TransferManager_moby21233 | None | 1 |
| & | Transfer_moby21233 | None | 1 |
| & | Watcher_moby21233 | None | 1 |
| & | watchBroadcasts_etcd6873 | None | 1 |
| & | watchBroadcast_etcd6873 | None | 1 |
| & | UDPProxy_moby7559 | None | 1 |
| & | Mux_kubernetes1321 | None | 1 |
| & | muxWatcher_kubernetes1321 | None | 1 |
| & | Worker_istio18454 | None | 1 |
| & | Strategy_istio18454 | None | 1 |
| & | Processor_istio18454 | None | 1 |
| & | notifier_kubernetes11298 | None | 1 |
| & | testDescriptorDB_cockroach6181 | None | 1 |
| & | rangeDescriptorCache_cockroach6181 | None | 1 |
| & | DeviceSet_moby17176 | None | 1 |
| & | TestModel_syncthing5795 | None | 1 |
| & | rawConnection_syncthing5795 | None | 1 |
| & | ClusterConfig_syncthing5795 | None | 1 |
| & | Tx_cockroach13197 | None | 1 |
| & | DB_cockroach13197 | None | 1 |
| & | remoteLock_hugo3251 | None | 1 |
| & | Watcher_moby27782 | None | 1 |
| & | fsNotifyWatcher_moby27782 | None | 1 |
| & | LogWatcher_moby27782 | None | 1 |
| & | JSONFileLogger_moby27782 | None | 1 |
| & | Container_moby27782 | None | 1 |
| & | EventMembershipChangeCommitted_cockroach2448 | None | 1 |
| & | Stopper_cockroach2448 | None | 1 |
| & | MultiRaft_cockroach2448 | None | 1 |
| & | state_cockroach2448 | None | 1 |
| & | Store_cockroach2448 | None | 1 |
| & | agent_istio17860 | None | 1 |
| & | Plugin_moby30408 | None | 1 |
| & | kv_etcd5509 | None | 1 |
| & | remoteClient_etcd5509 | None | 1 |
| & | Client_etcd5509 | None | 1 |
| & | Mapping_syncthing4829 | None | 1 |
| & | Service_syncthing4829 | None | 1 |
| & | stateMemory_kubernetes62464 | None | 1 |
| & | manager_kubernetes62464 | None | 1 |
| & | staticPolicy_kubernetes62464 | None | 1 |
| & | processorListener_kubernetes26980 | None | 1 |
| & | gossip_cockroach584 | None | 1 |
| & | Replica_cockroach10790 | None | 1 |
| & | flowEntry_cockroach35931 | None | 1 |
| & | flowRegistry_cockroach35931 | None | 1 |
| & | Flow_cockroach35931 | None | 1 |
| & | Manager_moby25348 | None | 1 |
| & | configstoreMonitor_istio16224 | None | 1 |
| & | controller_istio16224 | None | 1 |
| & | outbox_cockroach35073 | None | 1 |
| & | struct{ x [1024]byte } | None | 1 |
| & | Obj32 | None | 1 |
| & | labelMap | None | 1 |
| & | keysByCount | None | 1 |
| & | runtimeProfile | None | 1 |
| & | machVMRegionBasicInfoData | None | 1 |
| < | time.Duration | time.Duration | 1 |
| & | inlineWrapperInterface | None | 1 |
| & | inlineWrapper | None | 1 |
| & | profileBuilder | None | 1 |
| & | comment.Doc | None | 1 |
| & | comment.Paragraph | None | 1 |
| & | randReader | None | 1 |
| & | windows.OBJECT_ATTRIBUTES | None | 1 |
| & | windows.FILE_ATTRIBUTE_TAG_INFO | None | 1 |
| & | processHandle | None | 1 |
| & | SyscallError | None | 1 |
| & | *syscall.Dirent | None | 1 |
| & | rootMultiTest | None | 1 |
| & | testFileDesc | None | 1 |
| & | unixDirent | None | 1 |
| & | os.Process | None | 1 |
| * | *syscall.SysProcAttr | None | 1 |
| & | unix.SiginfoChild | None | 1 |
| & | windows.TOKEN_PRIVILEGES | None | 1 |
| & | windows.SERVICE_STATUS | None | 1 |
| & | *syscall.Overlapped | None | 1 |
| & | syscall.WaitStatus | None | 1 |
| & | signalCtx | None | 1 |
| & | ExitError | None | 1 |
| & | tickReader | None | 1 |
| & | struct {
		Name string
		Age  int
	} | None | 1 |
| & | SupplementalData | None | 1 |
| & | tickerTimer | None | 1 |
| != | Duration | Duration | 1 |
| == | bool | bool | 1 |
| & | chan Time | None | 1 |
| < | integer literal | string | 1 |
| == | string | integer literal | 1 |
| % | absCyear | integer literal | 1 |
| != | absCyear | integer literal | 1 |
| / | Duration | float literal | 1 |
| % | Duration | float literal | 1 |
| < | Duration | integer literal | 1 |
| > | Duration | integer literal | 1 |
| >> | Month | integer literal | 1 |
| + | Duration | Duration | 1 |
| & | rune | integer literal | 1 |
| & | huffmanEncoder | None | 1 |
| - | integer literal | byte | 1 |
| - | uint16 | integer literal | 1 |
| & | errorWriter | None | 1 |
| & | advancedState | None | 1 |
| & | sparseReader | None | 1 |
| & | syncBuffer | None | 1 |
| & | fastEncL1 | None | 1 |
| & | fastEncL2 | None | 1 |
| & | fastEncL3 | None | 1 |
| & | fastEncL4 | None | 1 |
| & | fastEncL5 | None | 1 |
| & | fastEncL6 | None | 1 |
| & | huffmanBitWriter | None | 1 |
| & | huffmanTree | None | 1 |
| % | byte | integer literal | 1 |
| / | byte | integer literal | 1 |
| & | queueOnePass | None | 1 |
| & | onePassProg | None | 1 |
| == | printFlags | integer literal | 1 |
| & | map[*Regexp]printFlags | None | 1 |
| == | Flags | Flags | 1 |
| < | rune | rune | 1 |
| + | rune | integer literal | 1 |
| & | reporterState | None | 1 |
| & | sequencer | None | 1 |
| & | reporter | None | 1 |
| & | funcLitFinder | None | 1 |
| & | FuncVisitor | None | 1 |
| & | FuncExtent | None | 1 |
| & | a.Atyp | None | 1 |
| & | CovDataReader | None | 1 |
| & | Queue | None | 1 |
| == | *pvacfgnode | *pvacfgnode | 1 |
| & | struct {
		GOOS         string
		GOARCH       string
		GOEXPERIMENT string
		GODEBUG      string
		CGO_ENABLED  string
	} | None | 1 |
| & | goDirPkg | None | 1 |
| & | LoadCmd | None | 1 |
| | | integer literal | int64 | 1 |
| & | bio.Writer | None | 1 |
| & | profile.Options | None | 1 |
| & | funcCond | None | 1 |
| & | prefixCond | None | 1 |
| & | boolCond | None | 1 |
| & | onceCond | None | 1 |
| & | cachedCond | None | 1 |
| & | CommandError | None | 1 |
| & | funcCmd | None | 1 |
| & | exec.Error | None | 1 |
| & | gorootModule | None | 1 |
| & | elf.Header64 | None | 1 |
| & | elf.Prog64 | None | 1 |
| & | DebugFlag | None | 1 |
| != | error | string literal | 1 |
| & | writer | None | 1 |
| <= | integer literal | uint64 | 1 |
| & | dwarf.FnState | None | 1 |
| & | DwarfFixupTable | None | 1 |
| & | varDecl | None | 1 |
| <= | uint | integer literal | 1 |
| & | ParsedTestData | None | 1 |
| == | *RotateParams | *RotateParams | 1 |
| >> | int32 | int | 1 |
| > | int16 | integer literal | 1 |
| & | *uint32 | integer literal | 1 |
| & | ctxt7 | None | 1 |
| & | int | int | 1 |
| < | integer literal | uint | 1 |
| * | *PosBase | None | 1 |
| == | PosXlogue | integer literal | 1 |
| & | plan9File | None | 1 |
| & | machoFile | None | 1 |
| & | goobjFile | None | 1 |
| & | gosym.Func | None | 1 |
| & | gosym.Sym | None | 1 |
| & | peFile | None | 1 |
| & | elfFile | None | 1 |
| & | xcoffFile | None | 1 |
| & | Disasm | None | 1 |
| & | FileCache | None | 1 |
| & | CachedFile | None | 1 |
| >> | integer literal | integer literal | 1 |
| & | Parser | None | 1 |
| & | Tokenizer | None | 1 |
| & | scanner.Scanner | None | 1 |
| & | Input | None | 1 |
| < | integer literal | int16 | 1 |
| & | struct {
	CompressInstructions int    `help:"use compressed instructions when possible (if supported by architecture)"`
	MayMoreStack         string `help:"call named function before all stack growth checks"`
	PCTab                string `help:"print named pc-value table\nOne of: pctospadj, pctofile, pctoline, pctoinline, pctopcdata"`
} | None | 1 |
| & | procGenerator | None | 1 |
| & | regionFilter | None | 1 |
| & | threadGenerator | None | 1 |
| & | gState[R] | None | 1 |
| & | genOpts | None | 1 |
| & | traceContext | None | 1 |
| & | format.Data | None | 1 |
| & | stackMap | None | 1 |
| & | goroutineGenerator | None | 1 |
| & | taskFilter | None | 1 |
| & | moddataType | None | 1 |
| & | funcEntry | None | 1 |
| & | dataSegment | None | 1 |
| & | ldMachoObj | None | 1 |
| & | Metrics | None | 1 |
| & | mark | None | 1 |
| & | peImportSymsState | None | 1 |
| & | peLoaderState | None | 1 |
| == | objabi.RelocType | integer literal | 1 |
| &^ | int64 | integer literal | 1 |
| & | syscall.Fstore_t | None | 1 |
| & | sym.CompilationUnit | None | 1 |
| != | goobj.FingerprintType | goobj.FingerprintType | 1 |
| & | [][]string | None | 1 |
| & | MachoHdr | None | 1 |
| == | MachoPlatform | integer literal | 1 |
| & | MachoPlatformLoad | None | 1 |
| & | fipsObj | None | 1 |
| & | sym.Library | None | 1 |
| != | *dwarf.DWDie | *dwarf.DWDie | 1 |
| == | *dwarf.DWDie | *dwarf.DWDie | 1 |
| & | relocSymState | None | 1 |
| & | peSection | None | 1 |
| & | [16]pe.SectionHeader32 | None | 1 |
| & | IMAGE_LOAD_CONFIG_DIRECTORY64 | None | 1 |
| & | IMAGE_LOAD_CONFIG_DIRECTORY32 | None | 1 |
| & | IMAGE_IMPORT_DESCRIPTOR | None | 1 |
| & | ElfShdr | None | 1 |
| & | *Elflib | None | 1 |
| & | stackCheck | None | 1 |
| == | loader.Sym | loader.Sym | 1 |
| & | dyldInfoCmd | None | 1 |
| & | macho.SymtabCmd | None | 1 |
| & | macho.DysymtabCmd | None | 1 |
| & | linkEditDataCmd | None | 1 |
| & | encryptionInfoCmd | None | 1 |
| * | *macho.Segment64 | None | 1 |
| * | *imacho.LoadCmdUpdater | None | 1 |
| & | XcoffScnHdr64 | None | 1 |
| & | XcoffAuxFile64 | None | 1 |
| & | XcoffAuxDWARF64 | None | 1 |
| & | XcoffAuxFcn64 | None | 1 |
| & | xcoffLoaderReloc | None | 1 |
| & | XcoffLdHdr64 | None | 1 |
| & | XcoffLdSym64 | None | 1 |
| & | XcoffLdStr64 | None | 1 |
| * | *I | None | 1 |
| != | sym.RelocVariant | integer literal | 1 |
| != | Sym | integer literal | 1 |
| & | goobj.Sym | None | 1 |
| & | goobj.Reloc | None | 1 |
| & | percentSStruct | None | 1 |
| & | someStruct | None | 1 |
| & | RecursiveSlice | None | 1 |
| & | RecursiveStruct | None | 1 |
| & | RecursiveStruct1 | None | 1 |
| << | int8 | integer literal | 1 |
| + | int8 | integer literal | 1 |
| * | *sync.Mutex | None | 1 |
| & | archive.Entry | None | 1 |
| & | Quote | None | 1 |
| & | line | None | 1 |
| & | listBuilder | None | 1 |
| & | itemBuilder | None | 1 |
| & | Emph | None | 1 |
| & | Escaped | None | 1 |
| & | emphPlain | None | 1 |
| & | Emoji | None | 1 |
| & | validDomainChecker | None | 1 |
| & | ThematicBreak | None | 1 |
| & | SoftBreak | None | 1 |
| & | HTMLBlock | None | 1 |
| & | Document | None | 1 |
| & | Text | None | 1 |
| & | rootBuilder | None | 1 |
| & | preBuilder | None | 1 |
| & | fenceBuilder | None | 1 |
| & | Empty | None | 1 |
| & | SECURITY_DESCRIPTOR | None | 1 |
| & | *ACL | None | 1 |
| & | ProcThreadAttributeListContainer | None | 1 |
| == | *uint16 | integer literal | 1 |
| & | OsVersionInfoEx | None | 1 |
| & | ClassInstallHeader | None | 1 |
| & | DevInfoListDetailData | None | 1 |
| & | DEVPROPTYPE | None | 1 |
| & | DevInstallParams | None | 1 |
| * | *PtraceLwpInfoStruct | None | 1 |
| & | SysvShmDesc | None | 1 |
| & | Utsname | None | 1 |
| & | mremapMmapper | None | 1 |
| & | KCMAttach | None | 1 |
| & | KCMUnattach | None | 1 |
| & | EventPort | None | 1 |
| & | Ifreq | None | 1 |
| & | *Pgtha | None | 1 |
| & | Pgtha | None | 1 |
| & | rusage_zos | None | 1 |
| & | timeval_zos | None | 1 |
| * | *nwmTriplet | None | 1 |
| & | [24]byte | None | 1 |
| & | Tms | None | 1 |
| & | struct {
		header W_Mnth
		fsinfo [64]W_Mntent
	} | None | 1 |
| & | *direntLE | None | 1 |
| & | Statx_t | None | 1 |
| & | SockaddrL2 | None | 1 |
| & | SockaddrRFCOMM | None | 1 |
| & | SockaddrXDP | None | 1 |
| & | SockaddrPPPoE | None | 1 |
| & | SockaddrTIPC | None | 1 |
| & | SockaddrIUCV | None | 1 |
| & | SockaddrCANJ1939 | None | 1 |
| & | SockaddrCAN | None | 1 |
| & | SockaddrNFC | None | 1 |
| & | SockaddrNFCLLCP | None | 1 |
| * | *PacketMreq | None | 1 |
| * | *SockFprog | None | 1 |
| * | *TpacketReq | None | 1 |
| * | *TpacketReq3 | None | 1 |
| * | *TCPMD5Sig | None | 1 |
| * | *MountAttr | None | 1 |
| * | *Sigset_t | None | 1 |
| & | sigset_argpack | None | 1 |
| & | SchedAttr | None | 1 |
| & | md.Strong | None | 1 |
| & | md.Emph | None | 1 |
| & | md.Del | None | 1 |
| & | md.Parser | None | 1 |
| & | md.Document | None | 1 |
| & | md.Empty | None | 1 |
| & | md.Heading | None | 1 |
| & | md.Text | None | 1 |
| & | []gobFact | None | 1 |
| & | Set | None | 1 |
| & | hunk | None | 1 |
| & | editGraph | None | 1 |
| & | Directive | None | 1 |
| & | freeVisitor | None | 1 |
| & | scope | None | 1 |
| & | importState | None | 1 |
| & | inlineCallResult | None | 1 |
| & | bindingDeclInfo | None | 1 |
| & | Callee | None | 1 |
| & | falconState | None | 1 |
| & | fixact | None | 1 |
| & | uses | None | 1 |
| != | types.Object | types.Object | 1 |
| * | *entry | None | 1 |
| & | pkgIndex | None | 1 |
| & | traversal | None | 1 |
| & | CycleInRequiresGraphError | None | 1 |
| * | *ast.CallExpr | None | 1 |
| & | namesSeen | None | 1 |
| & | constraint.TagExpr | None | 1 |
| & | CFGs | None | 1 |
| & | analyzer | None | 1 |
| & | inline.Caller | None | 1 |
| & | inline.Options | None | 1 |
| & | checker | None | 1 |
| & | asmFunc | None | 1 |
| == | asmKind | integer literal | 1 |
| != | asmKind | integer literal | 1 |
| & | deadState | None | 1 |
| & | argMatcher | None | 1 |
| & | analysis.Pass | None | 1 |
| & | Inspector | None | 1 |
| <= | token.Pos | token.Pos | 1 |
| > | token.Pos | token.Pos | 1 |
| == | token.Pos | token.Pos | 1 |
| + | token.Pos | integer literal | 1 |
| & | struct{ ast.Node } | None | 1 |
| & | application | None | 1 |
| & | lblock | None | 1 |
| & | CFG | None | 1 |
| & | *ModuleError | None | 1 |
| & | UnrecognizedVCSError | None | 1 |
| & | input | None | 1 |
| * | *Line | None | 1 |
| & | WorkFile | None | 1 |
| & | TestServer | None | 1 |
| & | note.Note | None | 1 |
| & | tileHashReader | None | 1 |
| & | verifier | None | 1 |
| & | signer | None | 1 |
| & | UnknownVerifierError | None | 1 |
| & | ambiguousVerifierError | None | 1 |
| & | InvalidSignatureError | None | 1 |
| & | UnverifiedNoteError | None | 1 |
| & | Weighted | None | 1 |
| & | StartResult | None | 1 |
| & | StackCounter | None | 1 |
| & | mmap.Data | None | 1 |
| * | *work | None | 1 |
| & | telemetry.ProgramReport | None | 1 |
| & | uploader | None | 1 |
| ^ | uint8 | None | 1 |
| << | uint64 | uint8 | 1 |
| & | InstMaskMap | None | 1 |
| * | *InstMaskMap | None | 1 |
| ^ | uint32 | integer literal | 1 |
| + | uint8 | integer literal | 1 |
| & | InheritanceMatcher | None | 1 |
| & | matchHeader | None | 1 |
| & | language.Builder | None | 1 |
| & | tagSort | None | 1 |
| & | coverage | None | 1 |
| & | undUpperCaser | None | 1 |
| & | undLowerCaser | None | 1 |
| & | undLowerIgnoreSigmaCaser | None | 1 |
| & | lowerCaser | None | 1 |
| & | titleCaser | None | 1 |
| & | caseFolder | None | 1 |
| & | windows.ConsoleScreenBufferInfo | None | 1 |
| & | windows.Handle | None | 1 |
| & | Terminal | None | 1 |
| & | stRingBuffer | None | 1 |
| & | addr2LinerNM | None | 1 |
| & | addr2LinerJob | None | 1 |
| & | addr2Liner | None | 1 |
| & | llvmSymbolizerJob | None | 1 |
| & | llvmSymbolizer | None | 1 |
| & | struct {
		Address    string `json:"Address"`
		ModuleName string `json:"ModuleName"`
		Data       struct {
			Start string `json:"Start"`
			Size  string `json:"Size"`
			Name  string `json:"Name"`
		} `json:"Data"`
	} | None | 1 |
| & | struct {
		Address    string `json:"Address"`
		ModuleName string `json:"ModuleName"`
		Symbol     []struct {
			Line         int    `json:"Line"`
			Column       int    `json:"Column"`
			FunctionName string `json:"FunctionName"`
			FileName     string `json:"FileName"`
			StartLine    int    `json:"StartLine"`
		} `json:"Symbol"`
	} | None | 1 |
| & | objSymbol | None | 1 |
| & | graph.DotConfig | None | 1 |
| & | Report | None | 1 |
| & | StackSet | None | 1 |
| & | synthCode | None | 1 |
| & | sourcePrinter | None | 1 |
| & | graph.Node | None | 1 |
| & | sourceReader | None | 1 |
| & | builder | None | 1 |
| * | *NodeInfo | None | 1 |
| * | *Node | None | 1 |
| & | webInterface | None | 1 |
| & | plugin.HTTPServerArgs | None | 1 |
| & | gourl.URL | None | 1 |
| & | errorCatcher | None | 1 |
| & | []*string | None | 1 |
| & | report.Options | None | 1 |
| * | *plugin.Options | None | 1 |
| & | GoFlags | None | 1 |
| & | binutils.Binutils | None | 1 |
| & | stdUI | None | 1 |
| & | symbolizer.Symbolizer | None | 1 |
| & | internalObjTool | None | 1 |
| & | internalSymbolizer | None | 1 |
| & | internalObjFile | None | 1 |
| & | rustState | None | 1 |
| & | []AST | None | 1 |
| & | BinaryFP | None | 1 |
| & | TemplateParamName | None | 1 |
| & | UnnamedType | None | 1 |
| & | Walker | None | 1 |
| & | struct {
				ImportPath, Dir string
				ImportMap       map[string]string
				Standard        bool
			} | None | 1 |
| & | SI | None | 1 |
| & | systeminfo | None | 1 |
| == | io.Writer | io.Writer | 1 |
| & | lockedWriter | None | 1 |
| & | work | None | 1 |
| * | *goTest | None | 1 |
| & | readlineUI | None | 1 |
| & | driver.Options | None | 1 |
| & | driver.Sym | None | 1 |
| & | metaMerge | None | 1 |
| & | podstate | None | 1 |
| & | pkstate | None | 1 |
| * | *coverage.FuncDesc | None | 1 |
| & | mstate | None | 1 |
| & | sstate | None | 1 |
| & | dstate | None | 1 |
| & | typeConv | None | 1 |
| & | debug | None | 1 |
| & | Ref | None | 1 |
| & | Call | None | 1 |
| & | ExpFunc | None | 1 |
| & | Visitor | None | 1 |
| & | C.S | None | 1 |
| & | *v | None | 1 |
| == | elf.DynTag | elf.DynTag | 1 |
| & | dep2.Dep2 | None | 1 |
| & | a.ImplA | None | 1 |
| & | tempDir | None | 1 |
| & | C.struct_ss | None | 1 |
| * | *C.int | None | 1 |
| == | syscall.Signal | integer literal | 1 |
| == | *testing.T | elf.DynTag | 1 |
| & | GoCallback | None | 1 |
| & | C.Issue38408 | None | 1 |
| & | data49633 | None | 1 |
| == | C.int | integer literal | 1 |
| & | C.CheckConstStruct | None | 1 |
| & | C.misaligned | None | 1 |
| & | struct{ p *byte } | None | 1 |
| & | C.issue69086struct | None | 1 |
| & | C.git_merge_file_input | None | 1 |
| & | C.issue27340Struct | None | 1 |
| & | struct{ Short string } | None | 1 |
| & | testgoData | None | 1 |
| &^ | fs.FileMode | integer literal | 1 |
| & | Span | None | 1 |
| & | TrackingWriter | None | 1 |
| != | File | File | 1 |
| & | syscall.Flock_t | None | 1 |
| & | svnState | None | 1 |
| & | accessToken | None | 1 |
| & | svnHandler | None | 1 |
| & | scriptCtx | None | 1 |
| == | any | scriptCtxKey | 1 |
| & | statusWriter | None | 1 |
| & | statusCodeHandler | None | 1 |
| & | rawPackage | None | 1 |
| & | build.Context | None | 1 |
| & | build.NoGoError | None | 1 |
| & | IndexPackage | None | 1 |
| & | jsonTree | None | 1 |
| & | []jsonDiagnostic | None | 1 |
| & | jsonError | None | 1 |
| & | DiskCache | None | 1 |
| != | [HashSize]byte | ActionID | 1 |
| == | OutputID | OutputID | 1 |
| & | ProgCache | None | 1 |
| & | shellShared | None | 1 |
| & | Shell | None | 1 |
| & | cmdError | None | 1 |
| & | actionJSON | None | 1 |
| & | buildActor | None | 1 |
| & | pgoActor | None | 1 |
| & | checkCacheActor | None | 1 |
| & | runCgoActor | None | 1 |
| & | cgoCompileActor | None | 1 |
| & | load.NoGoError | None | 1 |
| & | struct {
			Patterns map[string][]string
			Files    map[string]string
		} | None | 1 |
| & | coverProviderCached | None | 1 |
| & | analysis.ModuleError | None | 1 |
| & | vetConfig | None | 1 |
| & | runCgoProvider | None | 1 |
| & | commentWriter | None | 1 |
| & | overlayJSON | None | 1 |
| & | workfileJSON | None | 1 |
| & | vcs.RepoRoot | None | 1 |
| & | toolchainRepo | None | 1 |
| & | loggingRepo | None | 1 |
| & | proxyRepo | None | 1 |
| & | *module.InvalidVersionError | None | 1 |
| & | codeRepo | None | 1 |
| & | cachingRepo | None | 1 |
| * | *RevInfo | None | 1 |
| & | dbClient | None | 1 |
| & | codehost.Tags | None | 1 |
| & | fixedTagsRepo | None | 1 |
| & | Fetcher | None | 1 |
| & | struct {
		Logentry struct {
			Revision int64  `xml:"revision,attr"`
			Date     string `xml:"date"`
		} `xml:"logentry"`
	} | None | 1 |
| & | struct {
		Entries []listEntry `xml:"entry"`
	} | None | 1 |
| & | testWriter | None | 1 |
| & | gitRepo | None | 1 |
| & | vcsRepo | None | 1 |
| & | deleteCloser | None | 1 |
| & | RunError | None | 1 |
| & | ModuleJSON | None | 1 |
| & | *build.NoGoError | None | 1 |
| & | *build.MultiplePackageError | None | 1 |
| & | fileJSON | None | 1 |
| & | query | None | 1 |
| & | modload.QueryUpgradesAllError | None | 1 |
| & | conflictError | None | 1 |
| & | modload.QueryMatchesPackagesInMainModuleError | None | 1 |
| & | workspace | None | 1 |
| & | unix.Utsname | None | 1 |
| & | Command | None | 1 |
| & | vcsNotFoundError | None | 1 |
| & | urlpkg.URL | None | 1 |
| & | BuildListError | None | 1 |
| & | preload | None | 1 |
| & | EmbedError | None | 1 |
| & | debug.Module | None | 1 |
| & | debug.BuildInfo | None | 1 |
| & | TextPrinter | None | 1 |
| & | JSONPrinter | None | 1 |
| & | testFuncs | None | 1 |
| & | testFunc | None | 1 |
| != | ListMode | integer literal | 1 |
| & | excludedError | None | 1 |
| & | retractionLoadingError | None | 1 |
| & | ModuleRetractedError | None | 1 |
| & | PackageOpts | None | 1 |
| & | packageLoader | None | 1 |
| & | module.Version | None | 1 |
| == | loadPkgFlags | integer literal | 1 |
| * | *modfetch.RevInfo | None | 1 |
| & | NoMatchingVersionError | None | 1 |
| & | queryMatcher | None | 1 |
| & | NoPatchBaseError | None | 1 |
| & | WildcardInFirstElementError | None | 1 |
| & | QueryMatchesPackagesInMainModuleError | None | 1 |
| & | QueryResult | None | 1 |
| & | replacementRepo | None | 1 |
| & | ConstraintError | None | 1 |
| & | MainModuleSet | None | 1 |
| ! | addToolchainRoot | None | 1 |
| & | modfile.Require | None | 1 |
| == | module.Version | module.Version | 1 |
| * | *modinfo.ModulePublic | None | 1 |
| & | Requirements | None | 1 |
| & | moduleJSON | None | 1 |
| * | *flag.FlagSet | None | 1 |
| & | Match | None | 1 |
| & | MatchError | None | 1 |
| & | IgnorePatterns | None | 1 |
| & | load.TestCover | None | 1 |
| & | runTestActor | None | 1 |
| != | io.Writer | bytes.Buffer | 1 |
| != | cache.ActionID | cache.ActionID | 1 |
| & | HTTPError | None | 1 |
| * | *url.URL | None | 1 |
| * | *http.Client | None | 1 |
| & | Scanner | None | 1 |
| & | ReadWriter | None | 1 |
| & | net.UnixAddr | None | 1 |
| & | errorThenGoodReader | None | 1 |
| & | readFromWriter | None | 1 |
| & | IntHeap | None | 1 |
| * | *eface | None | 1 |
| & | poolChainElt | None | 1 |
| != | any | integer literal | 1 |
| & | poolDequeue | None | 1 |
| * | *one | None | 1 |
| != | any | string literal | 1 |
| & | Pointer[int] | None | 1 |
| & | digest | integer literal | 1 |
| >> | digest | integer literal | 1 |
| & | [8]Table | None | 1 |
| & | BloomFilter[V] | None | 1 |
| & | hashSet | None | 1 |
| & | sum32 | None | 1 |
| & | sum32a | None | 1 |
| & | sum64 | None | 1 |
| & | sum64a | None | 1 |
| & | sum128 | None | 1 |
| & | sum128a | None | 1 |
| == | *Table | *Table | 1 |
| < | uint | uint | 1 |
| > | uint | uint | 1 |
| * | *LineFile | None | 1 |
| & | typeFixer | None | 1 |
| & | VoidType | None | 1 |
| & | DotDotDotType | None | 1 |
| & | unit | None | 1 |
| & | typeUnit | None | 1 |
| & | Symbol | None | 1 |
| & | readSeekerFromReader | None | 1 |
| & | Rela32 | None | 1 |
| & | Segment32 | None | 1 |
| & | Section32 | None | 1 |
| & | Segment64 | None | 1 |
| & | Section64 | None | 1 |
| & | Nlist64 | None | 1 |
| & | Nlist32 | None | 1 |
| & | relocInfo | None | 1 |
| & | FatFile | None | 1 |
| & | byteExe | None | 1 |
| & | elfExe | None | 1 |
| & | peExe | None | 1 |
| & | xcoffExe | None | 1 |
| & | plan9objExe | None | 1 |
| & | Uniform | None | 1 |
| >= | uint8 | uint8 | 1 |
| & | modelFunc | None | 1 |
| > | int32 | int32 | 1 |
| == | image.Image | image.Image | 1 |
| & | color.RGBA64 | None | 1 |
| == | *image.RGBA | *image.RGBA | 1 |
| & | pool | None | 1 |
| & | blockReader | None | 1 |
| & | image.Paletted | None | 1 |
| * | *GIF | None | 1 |
| <= | int32 | int32 | 1 |
| & | image.CMYK | None | 1 |
| + | int32 | int | 1 |
| & | Arena | None | 1 |
| <= | float64 | integer literal | 1 |
| > | float32 | float32 | 1 |
| > | float32 | integer literal | 1 |
| - | complex128 | complex128 | 1 |
| != | complex128 | integer literal | 1 |
| == | big.Float | big.Float | 1 |
| == | *Float | *Float | 1 |
| < | Word | Word | 1 |
| == | Word | Word | 1 |
| & | []*Rat | None | 1 |
| >= | Word | Word | 1 |
| - | Word | Word | 1 |
| / | Word | Word | 1 |
| % | Word | Word | 1 |
| ^ | uint | integer literal | 1 |
| & | decimal | None | 1 |
| == | *Rat | *Rat | 1 |
| <= | Word | integer literal | 1 |
| & | []*Int | None | 1 |
| != | Word | integer literal | 1 |
| / | nat | integer literal | 1 |
| % | nat | Word | 1 |
| ^ | uint | uint | 1 |
| - | uint | None | 1 |
| & | Asm | None | 1 |
| & | Pipe | None | 1 |
| & | uint16 | uint16 | 1 |
| - | uint16 | None | 1 |
| << | uint16 | integer literal | 1 |
| ^ | uint32 | uint32 | 1 |
| <= | uint32 | uint32 | 1 |
| & | rngSource | None | 1 |
| & | PCG | None | 1 |
| != | nErr | nErr | 1 |
| * | *[256]byte | None | 1 |
| & | syscallFunc | None | 1 |
| >= | packetNumber | packetNumber | 1 |
| - | packetNumber | integer literal | 1 |
| & | sentPacket | None | 1 |
| == | packetType | integer literal | 1 |
| & | packetType | packetType | 1 |
| & | ApplicationError | None | 1 |
| & | aesHeaderProtection | None | 1 |
| & | Endpoint | None | 1 |
| != | ecnCounts | ecnCounts | 1 |
| & | datagram | None | 1 |
| & | netPacketConn | None | 1 |
| & | Stream | None | 1 |
| != | T | integer literal | 1 |
| &^ | T | T | 1 |
| & | tls.AlertError | None | 1 |
| & | ccReno | None | 1 |
| == | congestionState | congestionState | 1 |
| & | pipebuf | None | 1 |
| - | packetNumber | packetNumber | 1 |
| & | tls.QUICConfig | None | 1 |
| & | roundTripState | None | 1 |
| & | server | None | 1 |
| & | bodyWriter | None | 1 |
| & | clientConn | None | 1 |
| <= | uint16 | uint16 | 1 |
| & | headerFieldTable | None | 1 |
| << | integer literal | byte | 1 |
| & | Inet4Addr | None | 1 |
| & | Inet6Addr | None | 1 |
| & | Transformer | None | 1 |
| & | paragraph | None | 1 |
| & | isolatingRunSequence | None | 1 |
| == | Class | Class | 1 |
| & | level | integer literal | 1 |
| & | MAC | None | 1 |
| & | hkdfReader | None | 1 |
| * | *String | None | 1 |
| & | asn1.Tag | integer literal | 1 |
| * | *encoding_asn1.ObjectIdentifier | None | 1 |
| * | *asn1.Tag | None | 1 |
| & | [32]uint8 | None | 1 |
| & | [8]uint32 | None | 1 |
| & | [8]float32 | None | 1 |
| & | [64]uint8 | None | 1 |
| & | [8]uint64 | None | 1 |
| & | [16]float32 | None | 1 |
| & | [8]float64 | None | 1 |
| << | T | uint64 | 1 |
| >> | T | uint64 | 1 |
| <= | T | T | 1 |
| >= | T | T | 1 |
| / | T | T | 1 |
| ^ | T | T | 1 |
| >= | T | integer literal | 1 |
| & | AsConversion | None | 1 |
| & | TypeDotMethod | None | 1 |
| & | wasmOp | None | 1 |
| & | Comments | None | 1 |
| - | *int | *int | 1 |
| & | opData | None | 1 |
| & | Instruction | None | 1 |
| & | Operand | None | 1 |
| & | dotEncoder | None | 1 |
| & | [2]*Value | None | 1 |
| & | ident | None | 1 |
| & | *http.MaxBytesError | None | 1 |
| & | Number | None | 1 |
| * | rune | integer literal | 1 |
| & | Fields | None | 1 |
| & | V2Types | None | 1 |
| != | [4]byte | [4]byte | 1 |
| & | struct{ Name int } | None | 1 |
| != | struct{ Name int } | struct{ Name int } | 1 |
| & | time.Duration | None | 1 |
| & | encodeState | None | 1 |
| & | Bools | integer literal | 1 |
| ^ | Bools | None | 1 |
| != | float32 | integer literal | 1 |
| & | namedAny | None | 1 |
| * | *map[string]any | None | 1 |
| * | *[]any | None | 1 |
| & | jsonv1.RawMessage | None | 1 |
| & | jsonv1in2.RawMessage | None | 1 |
| & | jsontext.Value | None | 1 |
| + | int64 | float literal | 1 |
| & | typedArshalers[Coder] | None | 1 |
| & | json.SemanticError | None | 1 |
| & | OrderedObject[string] | None | 1 |
| & | map[netip.Addr]string | None | 1 |
| & | []struct {
		X bool `json:"firstName"`
	} | None | 1 |
| & | []struct {
		X bool `json:"firstName,case:ignore"`
	} | None | 1 |
| & | Container | None | 1 |
| & | []Tunnel | None | 1 |
| & | Animal | None | 1 |
| * | *StartElement | None | 1 |
| & | toks | None | 1 |
| & | struct {
					XMLName Name `xml:"test"`
				} | None | 1 |
| & | toksNil | None | 1 |
| & | struct {
				XMLName Name `xml:"test"`
			} | None | 1 |
| & | downCaser | None | 1 |
| & | allScalars | None | 1 |
| & | item | None | 1 |
| & | ExampleConflict | None | 1 |
| & | Failure | None | 1 |
| & | PathTestA | None | 1 |
| & | PathTestB | None | 1 |
| & | PathTestC | None | 1 |
| & | PathTestD | None | 1 |
| & | PathTestE | None | 1 |
| & | BadPathTestA | None | 1 |
| & | BadPathTestB | None | 1 |
| & | BadPathTestC | None | 1 |
| & | BadPathTestD | None | 1 |
| & | TestThree | None | 1 |
| & | ParamPtr | None | 1 |
| & | ParamVal | None | 1 |
| & | ParamStringPtr | None | 1 |
| & | MyStruct | None | 1 |
| & | nested | None | 1 |
| & | struct {
		Things []string
	} | None | 1 |
| & | struct {
		Sizes []Size `xml:"size"`
	} | None | 1 |
| & | Book | None | 1 |
| & | Movie | None | 1 |
| & | Pi | None | 1 |
| & | Universe | None | 1 |
| & | Particle | None | 1 |
| & | Departure | None | 1 |
| & | Generic[int] | None | 1 |
| & | Ship | None | 1 |
| & | NestedOrder | None | 1 |
| & | NilTest | None | 1 |
| & | MixedNested | None | 1 |
| & | struct {
			XMLName struct{} `xml:"space top"`
			A       string   `xml:"x>a"`
			B       string   `xml:"x>b"`
			C       string   `xml:"space x>c"`
			C1      string   `xml:"space1 x>c"`
			D1      string   `xml:"space1 x>d"`
		} | None | 1 |
| & | struct {
			XMLName Name
			A       string `xml:"x>a"`
			B       string `xml:"x>b"`
			C       string `xml:"space x>c"`
			C1      string `xml:"space1 x>c"`
			D1      string `xml:"space1 x>d"`
		} | None | 1 |
| & | struct {
			XMLName struct{} `xml:"top"`
			B       string   `xml:"space x>b"`
			B1      string   `xml:"space1 x>b"`
		} | None | 1 |
| & | EmbedA | None | 1 |
| & | EmbedC | None | 1 |
| & | EmbedB | None | 1 |
| & | PointerAnonFields | None | 1 |
| & | NameCasing | None | 1 |
| & | PointerFieldsTest | None | 1 |
| & | ChardataEmptyTest | None | 1 |
| & | AnyOmitTest | None | 1 |
| & | RecurseB | None | 1 |
| & | EmbedInt | None | 1 |
| & | Strings | None | 1 |
| & | MyMarshalerTest | None | 1 |
| & | MarshalerStruct | None | 1 |
| & | OuterStruct | None | 1 |
| & | OuterNamedStruct | None | 1 |
| & | OuterNamedOrderedStruct | None | 1 |
| & | OuterOuterStruct | None | 1 |
| & | NestedAndChardata | None | 1 |
| & | NestedAndComment | None | 1 |
| & | NestedAndCData | None | 1 |
| & | AttrParent | None | 1 |
| & | limitedBytesWriter | None | 1 |
| & | C | None | 1 |
| & | EndElement | None | 1 |
| & | struct {
		B byte `xml:"b,attr,omitempty"`
	} | None | 1 |
| & | LayerOne | None | 1 |
| & | xml.StartElement | None | 1 |
| & | struct {
		Animals []Animal `xml:"animal"`
	} | None | 1 |
| & | fieldInfo | None | 1 |
| & | lineBreaker | None | 1 |
| & | nTimes | None | 1 |
| & | TestObjectIdentifierStruct | None | 1 |
| & | BitString | None | 1 |
| & | TestContextSpecificTags | None | 1 |
| & | TestContextSpecificTags2 | None | 1 |
| & | TestContextSpecificTags3 | None | 1 |
| & | TestElementsAfterString | None | 1 |
| & | TestBigInt | None | 1 |
| & | TestSet | None | 1 |
| & | rawStructTest | None | 1 |
| & | explicitTaggedTimeTest | None | 1 |
| & | implicitTaggedTimeTest | None | 1 |
| & | truncatedExplicitTagTest | None | 1 |
| & | invalidUTF8Test | None | 1 |
| & | unexported | None | 1 |
| & | taggedRawValue | None | 1 |
| & | untaggedRawValue | None | 1 |
| & | ObjectIdentifier | None | 1 |
| & | tagged | None | 1 |
| & | []struct {
		Id       []int
		Critical bool `asn1:"optional"`
		Value    []byte
	} | None | 1 |
| & | struct {
		Strings []string `asn1:"set"`
	} | None | 1 |
| & | testSetSET | None | 1 |
| & | invalidUnmarshalError | None | 1 |
| & | [100]int8 | None | 1 |
| & | [100]int16 | None | 1 |
| & | [100]int32 | None | 1 |
| & | [100]int64 | None | 1 |
| & | [100]uint8 | None | 1 |
| & | [100]uint16 | None | 1 |
| & | [100]uint32 | None | 1 |
| & | [100]uint64 | None | 1 |
| & | BlankFields | None | 1 |
| & | Unexported | None | 1 |
| & | struct {
		A, B, C, D byte
		E          int32
		F          float64
	} | None | 1 |
| & | struct {
		PI   float64
		Uate uint8
		Mine [3]byte
		Too  uint16
	} | None | 1 |
| & | faultInjectReader | None | 1 |
| & | dumper | None | 1 |
| & | N2 | None | 1 |
| & | Vector | None | 1 |
| != | typeId | typeId | 1 |
| & | CommonType | None | 1 |
| & | peekReader | None | 1 |
| & | debugger | None | 1 |
| & | decBuffer | None | 1 |
| & | encoderState | None | 1 |
| != | bool | bool literal | 1 |
| != | bool | string literal | 1 |
| & | [3]float64 | None | 1 |
| & | [2]string | None | 1 |
| & | []int64 | None | 1 |
| & | outu8 | None | 1 |
| & | outu16 | None | 1 |
| & | outu32 | None | 1 |
| & | outf32 | None | 1 |
| & | outc64 | None | 1 |
| & | RT | None | 1 |
| & | Rec | None | 1 |
| & | Direct | None | 1 |
| & | DT | None | 1 |
| & | []*struct{} | None | 1 |
| & | GobTestValueEncDec | None | 1 |
| & | GobTestArrayEncDec | None | 1 |
| & | GobTest2 | None | 1 |
| != | Gobber | integer literal | 1 |
| & | gobDecoderBug0 | None | 1 |
| & | *gobDecoderBug0 | None | 1 |
| & | isZeroBug | None | 1 |
| & | Type1 | None | 1 |
| & | Type3 | None | 1 |
| & | Type4 | None | 1 |
| & | Type5 | None | 1 |
| & | Type6 | None | 1 |
| & | Type7 | None | 1 |
| & | map[string]int | None | 1 |
| & | []interfaceIndirectTestI | None | 1 |
| & | Struct0 | None | 1 |
| & | Bug0Inner | None | 1 |
| & | Bug2 | None | 1 |
| & | []*Bug3 | None | 1 |
| & | DB | None | 1 |
| & | ColumnType | None | 1 |
| & | fakeDriver | None | 1 |
| & | fakeConn | None | 1 |
| & | fakeDB | None | 1 |
| & | fakeTx | None | 1 |
| & | fakeStmt | None | 1 |
| & | userDefinedBytes | None | 1 |
| & | basicConnector | None | 1 |
| & | rowsColumnScannerConnector | None | 1 |
| & | basicStmt | None | 1 |
| & | basicConn | None | 1 |
| & | TxOptions | None | 1 |
| & | ctxOnlyDriver | None | 1 |
| & | alwaysErrScanner | None | 1 |
| & | testScanner | None | 1 |
| & | pingDriver | None | 1 |
| & | Str | None | 1 |
| & | unknownInputsConnector | None | 1 |
| & | NullTime | None | 1 |
| & | rowsColumnScannerConn | None | 1 |
| & | rowsColumnScannerStmt | None | 1 |
| & | rowsColumnScannerRows | None | 1 |
| & | CustomError | None | 1 |
| + | []byte | integer literal | 1 |
| & | book | None | 1 |
| & | lexer | None | 1 |
| & | ListNode | None | 1 |
| & | PipeNode | None | 1 |
| & | ActionNode | None | 1 |
| & | CommandNode | None | 1 |
| & | IdentifierNode | None | 1 |
| & | DotNode | None | 1 |
| & | NilNode | None | 1 |
| & | BoolNode | None | 1 |
| & | NumberNode | None | 1 |
| & | StringNode | None | 1 |
| & | endNode | None | 1 |
| & | elseNode | None | 1 |
| & | IfNode | None | 1 |
| & | BreakNode | None | 1 |
| & | ContinueNode | None | 1 |
| & | RangeNode | None | 1 |
| & | WithNode | None | 1 |
| & | TemplateNode | None | 1 |
| != | rune | rune | 1 |
| == | *rune | integer literal | 1 |
| & | customDoneContext | None | 1 |
| & | customContext | None | 1 |
| & | cancelCtx | None | 1 |
| & | afterFuncCtx | None | 1 |
| & | timerCtx | None | 1 |
| & | valueCtx | None | 1 |
| & | myCtx | None | 1 |
| & | sizeCounter | None | 1 |
| * | *Config | None | 1 |
| & | trimmer | None | 1 |
| & | gcimports | None | 1 |
| & | gccgoimports | None | 1 |
| & | Importer | None | 1 |
| & | readerDict | None | 1 |
| * | *[]*types.TypeParam | None | 1 |
| >= | Value | integer literal | 1 |
| > | Value | integer literal | 1 |
| ! | Value | None | 1 |
| >> | Value | uint | 1 |
| <= | integer literal | uint32 | 1 |
| & | readNopCloser | None | 1 |
| & | TagExpr | None | 1 |
| & | AndExpr | None | 1 |
| & | OrExpr | None | 1 |
| & | Term | None | 1 |
| * | **TypeParamList | None | 1 |
| & | target | None | 1 |
| & | lazyObject | None | 1 |
| & | subster | None | 1 |
| * | *Var | None | 1 |
| == | Code | integer literal | 1 |
| & | error_ | None | 1 |
| != | Code | integer literal | 1 |
| - | token.Pos | token.Pos | 1 |
| * | *term | None | 1 |
| & | TypeParam | None | 1 |
| & | PkgName | None | 1 |
| & | Const | None | 1 |
| & | TypeName | None | 1 |
| & | Label | None | 1 |
| & | Builtin | None | 1 |
| & | TypeList | None | 1 |
| & | Nil | None | 1 |
| & | instance | None | 1 |
| & | Initializer | None | 1 |
| & | graphNode | None | 1 |
| & | term | None | 1 |
| & | actionDesc | None | 1 |
| & | Checker | None | 1 |
| > | *operand | integer literal | 1 |
| != | ImportMode | integer literal | 1 |
| & | resolveTestImporter | None | 1 |
| & | stdlibChecker | None | 1 |
| & | futurePackage | None | 1 |
| == | *Package | *Package | 1 |
| & | namedType | None | 1 |
| & | comment.Parser | None | 1 |
| & | Example | None | 1 |
| * | *ast.File | None | 1 |
| & | Printer | None | 1 |
| & | mdPrinter | None | 1 |
| & | htmlPrinter | None | 1 |
| & | parseDoc | None | 1 |
| & | LinkDef | None | 1 |
| & | ListItem | None | 1 |
| & | DocLink | None | 1 |
| & | textPrinter | None | 1 |
| & | commentPrinter | None | 1 |
| & | FileSet | None | 1 |
| == | *FileSet | *FileSet | 1 |
| & | serializedFileSet | None | 1 |
| & | Object | None | 1 |
| & | Ident | None | 1 |
| & | joinError | None | 1 |
| & | errorString | None | 1 |
| & | *E | None | 1 |
| & | *poser | None | 1 |
| == | Hash | integer literal | 1 |
| & | messageSignerOnly | None | 1 |
| & | wycheproof.EddsaVerifySchemaV1Json | None | 1 |
| & | []struct {
		A, R, S, M string
		Flags      []string
	} | None | 1 |
| & | [drbg.SeedSize]byte | None | 1 |
| & | rsa.TestingOnlyLargeExponentPublicKey | None | 1 |
| & | [1024]uint8 | None | 1 |
| & | [48]byte | None | 1 |
| & | boringHMAC | None | 1 |
| & | PublicKeyRSA | None | 1 |
| & | PrivateKeyRSA | None | 1 |
| & | aesCipher | None | 1 |
| & | aesCTR | None | 1 |
| & | aesGCM | None | 1 |
| & | PublicKeyECDSA | None | 1 |
| & | PrivateKeyECDSA | None | 1 |
| & | C.uint | None | 1 |
| & | Cache[int, int32] | None | 1 |
| & | cacheEntry[K, V] | None | 1 |
| ^ | uint64 | integer literal | 1 |
| & | P384Point | None | 1 |
| & | [1 + 2*p384ElementLength]byte | None | 1 |
| & | [p384ElementLength]byte | None | 1 |
| & | [1 + p384ElementLength]byte | None | 1 |
| & | P224Point | None | 1 |
| & | [1 + 2*p224ElementLength]byte | None | 1 |
| & | [p224ElementLength]byte | None | 1 |
| & | [1 + p224ElementLength]byte | None | 1 |
| & | p256Element | None | 1 |
| & | P521Point | None | 1 |
| & | [1 + 2*p521ElementLength]byte | None | 1 |
| & | [p521ElementLength]byte | None | 1 |
| & | [1 + p521ElementLength]byte | None | 1 |
| & | EarlySecret | None | 1 |
| & | HandshakeSecret | None | 1 |
| & | MasterSecret | None | 1 |
| & | blockExpanded | None | 1 |
| & | CBCEncrypter | None | 1 |
| & | CBCDecrypter | None | 1 |
| * | *[BlockSize]byte | None | 1 |
| & | CounterKDF | None | 1 |
| & | CMAC | None | 1 |
| & | hmacDRBG | None | 1 |
| & | HMAC | None | 1 |
| & | millerRabin | None | 1 |
| ^ | byte | None | 1 |
| & | TestingOnlyLargeExponentPrivateKey | None | 1 |
| & | TestingOnlyLargeExponentPublicKey | None | 1 |
| * | *projCached | None | 1 |
| * | *affineCached | None | 1 |
| * | *Point | None | 1 |
| * | *Scalar | None | 1 |
| * | uint64 | integer literal | 1 |
| * | *Element | None | 1 |
| ^ | integer literal | choice | 1 |
| & | Modulus | None | 1 |
| != | io.Reader | io.Reader | 1 |
| & | elliptic.CurveParams | None | 1 |
| & | struct {
		Dir string
	} | None | 1 |
| & | struct {
		Dir   string
		Error string
	} | None | 1 |
| & | key | None | 1 |
| & | nistCurve[*nistec.P224Point] | None | 1 |
| & | nistCurve[*nistec.P256Point] | None | 1 |
| & | nistCurve[*nistec.P384Point] | None | 1 |
| & | nistCurve[*nistec.P521Point] | None | 1 |
| & | wycheproof.HkdfTestSchemaV1Json | None | 1 |
| & | wycheproof.PbkdfTestSchemaJson | None | 1 |
| * | *mldsa.PrivateKey | None | 1 |
| * | *mldsa.PublicKey | None | 1 |
| & | wycheproof.MldsaVerifySchemaJson | None | 1 |
| & | wycheproof.MldsaSignNoseedSchemaJson | None | 1 |
| & | wycheproof.DsaVerifySchemaV1Json | None | 1 |
| & | wycheproof.EcdsaVerifySchemaV1Json | None | 1 |
| & | []struct {
		Curve string
		Seed  []byte
		PKCS8 []byte `json:"private_key_pkcs8"`
	} | None | 1 |
| >> | cryptobyte_asn1.Tag | integer literal | 1 |
| & | pkix.RDNSequence | None | 1 |
| & | uint | None | 1 |
| ^ | cryptobyte_asn1.Tag | integer literal | 1 |
| * | *asn1.ObjectIdentifier | None | 1 |
| & | []struct {
		Name                        string
		CertPath                    []string
		InitialPolicySet            []string
		InitialPolicyMappingInhibit bool
		InitialExplicitPolicy       bool
		InitialAnyPolicyInhibit     bool
		ShouldValidate              bool
		Skipped                     bool
	} | None | 1 |
| & | *syscall.CertContext | None | 1 |
| & | syscall.SSLExtraCertChainPolicyPara | None | 1 |
| & | syscall.CertChainPolicyPara | None | 1 |
| & | *syscall.CertChainContext | None | 1 |
| & | ipConstraints | None | 1 |
| & | nameConstraintsSet[string, string] | None | 1 |
| & | emailConstraints | None | 1 |
| & | chainConstraints | None | 1 |
| & | x509limbo.Limbo | None | 1 |
| & | UnknownAuthorityError | None | 1 |
| & | policyGraphNode | None | 1 |
| & | policyGraph | None | 1 |
| & | messageSigner | None | 1 |
| & | pssParameters | None | 1 |
| >> | KeyUsage | integer literal | 1 |
| == | SignatureAlgorithm | integer literal | 1 |
| != | SignatureAlgorithm | SignatureAlgorithm | 1 |
| & | []asn1.RawValue | None | 1 |
| & | pkix.AttributeTypeAndValueSET | None | 1 |
| & | pkcs10Attribute | None | 1 |
| & | []pkix.Extension | None | 1 |
| & | asn1.RawValue | None | 1 |
| * | *RDNSequence | None | 1 |
| & | rsa.PKCS1v15DecryptOptions | None | 1 |
| & | permanentError | None | 1 |
| & | hairpinConn | None | 1 |
| & | changeImplConn | None | 1 |
| & | slowConn | None | 1 |
| & | ConnectionState | None | 1 |
| & | serverHelloDoneMsg | None | 1 |
| * | *serverTest | None | 1 |
| & | serverHandshakeState | None | 1 |
| & | serverHandshakeStateTLS13 | None | 1 |
| & | mlkem1024KeyExchange | None | 1 |
| & | bogoResults | None | 1 |
| & | echClientContext | None | 1 |
| & | clientHandshakeStateTLS13 | None | 1 |
| & | clientHandshakeState | None | 1 |
| & | opensslOutputSink | None | 1 |
| * | *clientTest | None | 1 |
| & | serializingClientCache | None | 1 |
| & | brokenConn | None | 1 |
| & | discardConn | None | 1 |
| & | fipsCertificate | None | 1 |
| == | *Certificate | CurveID | 1 |
| & | lruSessionCache | None | 1 |
| & | lruSessionCacheEntry | None | 1 |
| & | prefixNonceAEAD | None | 1 |
| & | cthWrapper | None | 1 |
| & | ECHRejectionError | None | 1 |
| & | quicState | None | 1 |
| & | QUICConn | None | 1 |
| & | []struct {
		Bits  int
		Seed  []byte
		PKCS8 []byte `json:"private_key_pkcs8"`
	} | None | 1 |
| & | wycheproof.RsaesOaepDecryptSchemaV1Json | None | 1 |
| & | rsa.OAEPOptions | None | 1 |
| & | wycheproof.RsaesPkcs1DecryptSchemaV1Json | None | 1 |
| & | wycheproof.RsassaPkcs1VerifySchemaV1Json | None | 1 |
| & | wycheproof.RsassaPssVerifySchemaV1Json | None | 1 |
| & | wycheproof.MlkemKeygenSeedTestSchemaJson | None | 1 |
| & | wycheproof.MlkemEncapsTestSchemaJson | None | 1 |
| & | wycheproof.MlkemTestSchemaJson | None | 1 |
| & | wycheproof.MlkemSemiExpandedDecapsTestSchemaJson | None | 1 |
| & | dhKEMPrivateKey | None | 1 |
| & | []struct {
		Mode        uint16 `json:"mode"`
		KEM         uint16 `json:"kem_id"`
		KDF         uint16 `json:"kdf_id"`
		AEAD        uint16 `json:"aead_id"`
		Info        string `json:"info"`
		IkmE        string `json:"ikmE"`
		IkmR        string `json:"ikmR"`
		SkRm        string `json:"skRm"`
		PkRm        string `json:"pkRm"`
		Enc         string `json:"enc"`
		Encryptions []struct {
			Aad   string `json:"aad"`
			Ct    string `json:"ct"`
			Nonce string `json:"nonce"`
			Pt    string `json:"pt"`
		} `json:"encryptions"`
		Exports []struct {
			Context string `json:"exporter_context"`
			L       int    `json:"L"`
			Value   string `json:"exported_value"`
		} `json:"exports"`

		// Instead of checking in a very large rfc9180.json, we computed
		// alternative accumulated values.
		AccEncryptions string `json:"encryptions_accumulated"`
		AccExports     string `json:"exports_accumulated"`
	} | None | 1 |
| & | Sender | None | 1 |
| & | Recipient | None | 1 |
| & | gcmFallback | None | 1 |
| & | wycheproof.IndCpaTestSchemaV1Json | None | 1 |
| & | cbc | None | 1 |
| & | ofb | None | 1 |
| & | cfb | None | 1 |
| & | cipher.StreamReader | None | 1 |
| & | cipher.StreamWriter | None | 1 |
| & | ctr | None | 1 |
| & | wycheproof.EcdhEcpointTestSchemaV1Json | None | 1 |
| & | wycheproof.EcdhTestSchemaV1Json | None | 1 |
| & | wycheproof.XdhCompSchemaV1Json | None | 1 |
| & | x25519Curve | None | 1 |
| & | ecdh.PublicKey | None | 1 |
| & | checksumReader | None | 1 |
| & | directoryEnd | None | 1 |
| & | fileListEntry | None | 1 |
| & | sparseSpan | None | 1 |
| == | fs.FileMode | integer literal | 1 |
| + | integer literal | uint16 | 1 |
| & | pooledFlateWriter | None | 1 |
| & | pooledFlateReader | None | 1 |
| & | nopCloser | None | 1 |
| & | captureReporter | None | 1 |
| & | sparseBuffer | None | 1 |
| & | cdSnapshot | None | 1 |
| & | fileInfoNames | None | 1 |
| & | tar.Header | None | 1 |
| & | jsonErrType | None | 1 |
| & | parse.CommandNode | None | 1 |
| & | parse.Tree | None | 1 |
| & | myStringer | None | 1 |
| & | recursiveInvoker | None | 1 |
| & | badMarshaler | None | 1 |
| & | goodMarshaler | None | 1 |
| & | parse.TextNode | None | 1 |

**excerpts, resolved**
- `/sources/golang_src/src/flag/example_value_test.go:33` operator `&` operand types ['url.URL'] resolved against []
- `/sources/golang_src/src/flag/example_value_test.go:37` operator `&` operand types ['URLValue'] resolved against []
- `/sources/golang_src/src/flag/flag.go:129` operator `*` operand types ['*bool'] resolved against ['/sources/golang_src/src/flag/flag.go:128']

**excerpts, unresolved**
- `/sources/golang_src/src/flag/example_value_test.go:25` operator `!=` reason: inferred binding
- `/sources/golang_src/src/flag/example_value_test.go:28` operator `*` reason: inferred binding
- `/sources/golang_src/src/flag/flag.go:113` operator `!` reason: inferred binding
- `/sources/golang_src/src/flag/flag.go:576` operator `+` reason: other (binary_expression)
- `/sources/golang_src/src/flag/flag.go:1080` operator `||` reason: other (binary_expression)
- `/sources/golang_src/src/flag/flag.go:1092` operator `||` reason: other (binary_expression)

## rustc

**unresolved histogram**

| reason | sites | share |
|---|---|---|
| declared in another file or not found | 3666 | 0.424 |
| call result | 995 | 0.115 |
| member access | 961 | 0.111 |
| inferred binding | 903 | 0.104 |
| other (array_expression) | 688 | 0.08 |
| other (binary_expression) | 396 | 0.046 |
| other (mutable_specifier) | 315 | 0.036 |
| other (unary_expression) | 223 | 0.026 |
| other (scoped_identifier) | 200 | 0.023 |
| index expression | 106 | 0.012 |
| macro | 78 | 0.009 |
| other (closure_expression) | 68 | 0.008 |
| other (no operand node found for range_expression) | 18 | 0.002 |
| other (struct_expression) | 12 | 0.001 |
| nested operator, mixed operand types | 9 | 0.001 |
| other (tuple_expression) | 6 | 0.001 |
| other (block) | 3 | 0.0 |
| other (if_expression) | 2 | 0.0 |
| other (generic_function) | 1 | 0.0 |
| other (ERROR) | 1 | 0.0 |
| other (metavariable) | 1 | 0.0 |
| other (const_block) | 1 | 0.0 |
| other (unsafe_block) | 1 | 0.0 |

**resolved variants** (full table; log_210 carries the first 20)

| operator | lhs type | rhs type | sites |
|---|---|---|---|
| - | integer literal | None | 76 |
| ! | bool | None | 26 |
| - | float literal | None | 20 |
| & | &CodegenCx<'ll, '_> | None | 15 |
| & | &Path | None | 12 |
| << | integer literal | integer literal | 10 |
| - | usize | integer literal | 9 |
| + | usize | integer literal | 8 |
| * | integer literal | integer literal | 8 |
| .. | integer literal | None | 7 |
| .. | integer literal | integer literal | 7 |
| & | Vec<_> | None | 7 |
| & | string literal | None | 6 |
| == | &str | string literal | 6 |
| ! | integer literal | None | 6 |
| + | integer literal | integer literal | 6 |
| & | CrateType | None | 6 |
| & | CrateNum | None | 6 |
| & | &[u8] | None | 6 |
| != | u64 | integer literal | 5 |
| && | bool | bool | 5 |
| & | DefId | None | 5 |
| & | String | None | 5 |
| & | LinkerFlavor | None | 5 |
| .. | usize | None | 4 |
| * | *mut _ | None | 4 |
| & | ModuleCodegen<ModuleLlvm> | None | 4 |
| * | &std::ffi::CStr | None | 4 |
| * | &mut Providers | None | 4 |
| >> | u128 | integer literal | 3 |
| * | &mut FunctionCx<'_, '_, 'tcx> | None | 3 |
| & | &[Value] | None | 3 |
| * | String | None | 3 |
| * | u8 | integer literal | 3 |
| & | Foo<usize> | None | 3 |
| & | &'ll Value | None | 3 |
| & | &SimpleCx<'_> | None | 3 |
| >= | u32 | u32 | 3 |
| <= | u32 | u32 | 3 |
| - | u32 | u32 | 3 |
| & | Vec<u64> | None | 3 |
| & | CompiledModules | None | 3 |
| & | CrateInfo | None | 3 |
| & | EncodedMetadata | None | 3 |
| & | &EncodedMetadata | None | 3 |
| & | SharedEmitter | None | 3 |
| & | &CodegenContext | None | 3 |
| & | Option<ArchiveSymbols> | None | 3 |
| * | string literal | None | 2 |
| != | &str | string literal | 2 |
| - | i64 | None | 2 |
| * | i64 | i64 | 2 |
| & | Signature | None | 2 |
| .. | usize | integer literal | 2 |
| & | Ty<'tcx> | None | 2 |
| * | i32 | i32 | 2 |
| ..= | integer literal | integer literal | 2 |
| + | f32 | float literal | 2 |
| * | &u8 | None | 2 |
| * | &u16 | None | 2 |
| * | &u32 | None | 2 |
| * | &u64 | None | 2 |
| * | &u128 | None | 2 |
| * | &usize | None | 2 |
| * | &i8 | None | 2 |
| * | &i32 | None | 2 |
| * | &isize | None | 2 |
| * | &char | None | 2 |
| * | &*const T | None | 2 |
| & | integer literal | None | 2 |
| * | *const *const i8 | None | 2 |
| == | u64 | integer literal | 2 |
| - | i32 | integer literal | 2 |
| & | SimpleCx<'_> | None | 2 |
| & | Symbol | None | 2 |
| == | &'ll Type | &'ll Type | 2 |
| * | *mut LlvmSelfProfiler<'_> | None | 2 |
| & | UniqueTypeId<'tcx> | None | 2 |
| / | u64 | integer literal | 2 |
| & | TyCtxt<'tcx> | None | 2 |
| & | GenericArgsRef<'tcx> | None | 2 |
| & | LinkOutputKind | None | 2 |
| & | Vec<u8> | None | 2 |
| + | integer literal | u16 | 2 |
| & | &RetagPlan<Bx::Value> | None | 2 |
| * | &mir::Rvalue<'tcx> | None | 2 |
| & | abi::Scalar | None | 2 |
| & | &[Spanned<mir::Operand<'tcx>>] | None | 2 |
| & | Option<&str> | None | 1 |
| & | Compiler | None | 1 |
| & | &[InlineAsmOperand<'tcx>] | None | 1 |
| == | TyAndLayout<'tcx> | TyAndLayout<'tcx> | 1 |
| == | i64 | integer literal | 1 |
| & | AnyEntity | None | 1 |
| & | Inst | None | 1 |
| - | u64 | u64 | 1 |
| + | i64 | i64 | 1 |
| + | u32 | u32 | 1 |
| - | u32 | integer literal | 1 |
| >> | ty::ScalarInt | integer literal | 1 |
| == | usize | integer literal | 1 |
| * | usize | usize | 1 |
| < | usize | integer literal | 1 |
| & | Vec<Value> | None | 1 |
| + | i64 | integer literal | 1 |
| + | u64 | u64 | 1 |
| - | i64 | i64 | 1 |
| * | *const SelfProfilerRef | None | 1 |
| - | integer literal (suffix i64) | None | 1 |
| < | integer literal (suffix i128) | integer literal (suffix i128) | 1 |
| << | integer literal (suffix u32) | integer literal (suffix u8) | 1 |
| & | T | None | 1 |
| == | *const u8 | *const u8 | 1 |
| & | &[_] | None | 1 |
| == | char | char | 1 |
| * | *const str | None | 1 |
| + | integer literal | u8 | 1 |
| == | integer literal (suffix u8) | integer literal (suffix u8) | 1 |
| == | isize | integer literal | 1 |
| * | *const *const u8 | None | 1 |
| * | u8 | None | 1 |
| & | u8 | None | 1 |
| * | Box<&str> | None | 1 |
| & | pthread_attr_t | None | 1 |
| & | Baz<usize> | None | 1 |
| & | HasDrop<Baz<[i32; 4]>> | None | 1 |
| & | SmallVec<[&Metadata; 16]> | None | 1 |
| + | u32 | integer literal | 1 |
| == | Size | integer literal | 1 |
| & | &'ll BasicBlock | None | 1 |
| - | i32 | None | 1 |
| > | Align | Align | 1 |
| & | &RustTypeTree | None | 1 |
| & | RustTypeTree | None | 1 |
| & | &[&Type] | None | 1 |
| .. | usize | usize | 1 |
| & | Instance<'tcx> | None | 1 |
| << | u128 | integer literal | 1 |
| & | &[&'ll Type] | None | 1 |
| & | ty::Instance<'tcx> | None | 1 |
| .. | integer literal | i32 | 1 |
| & | Vec<&'ll Type> | None | 1 |
| & | Vec<&Attribute> | None | 1 |
| & | &[OperandRef<'tcx, &'ll Value>] | None | 1 |
| - | u64 | integer literal | 1 |
| & | Option<Vec<_>> | None | 1 |
| * | &mut Option<(&'a Type, TyAndLayout<'tcx>)> | None | 1 |
| >> | u64 | integer literal | 1 |
| * | *const (&CodegenContext, &SharedEmitter) | None | 1 |
| & | ObjectReader | None | 1 |
| * | *mut &mut dyn FnMut(&[u8]) -> io::Result<()> | None | 1 |
| * | &CoverageKind | None | 1 |
| * | u64 | u64 | 1 |
| & | SmallVec<VariantFieldInfo<'ll>> | None | 1 |
| .. | integer literal | u32 | 1 |
| & | &mut Builder<'_, 'll, 'tcx> | None | 1 |
| * | integer literal | u64 | 1 |
| & | &[&'ll Value] | None | 1 |
| == | String | String | 1 |
| & | [u8; 4] | None | 1 |
| == | Ty<'tcx> | Ty<'tcx> | 1 |
| & | LocalDefId | None | 1 |
| & | Option<CrateType> | None | 1 |
| & | &Session | None | 1 |
| - | usize | usize | 1 |
| & | Vec<&str> | None | 1 |
| & | &SelfProfilerRef | None | 1 |
| & | &[String] | None | 1 |
| & | &[PathBuf] | None | 1 |
| & | TargetMachineFactoryFn<B> | None | 1 |
| * | integer literal | usize | 1 |
| > | usize | integer literal | 1 |
| * | &mut Option<VerboseTimingGuard<'a>> | None | 1 |
| & | char literal | None | 1 |
| == | WindowsSubsystemKind | string literal | 1 |
| & | OsString | None | 1 |
| == | ObjectArchiveKind | ObjectArchiveKind | 1 |
| & | AddArchiveKind<'_> | None | 1 |
| & | Box<dyn AsRef<[u8]>> | None | 1 |
| * | &mir::Operand<'tcx> | None | 1 |
| + | Option<String> | string literal | 1 |
| & | &DenseBitSet<mir::BasicBlock> | None | 1 |
| == | abi::Scalar | abi::Scalar | 1 |
| * | &mir::SourceInfo | None | 1 |
| & | TerminatorCodegenHelper<'tcx> | None | 1 |
| & | Vec<(Bx::Value, Size)> | None | 1 |
| & | &[mir::InlineAsmOperand<'tcx>] | None | 1 |

**excerpts, resolved**
- `/sources/rust/compiler/rustc_codegen_cranelift/build_system/bench.rs:148` operator `!=` operand types ['u64', 'integer literal'] resolved against ['/sources/rust/compiler/rustc_codegen_cranelift/build_system/bench.rs:138']
- `/sources/rust/compiler/rustc_codegen_cranelift/build_system/bench.rs:152` operator `!=` operand types ['u64', 'integer literal'] resolved against ['/sources/rust/compiler/rustc_codegen_cranelift/build_system/bench.rs:139']
- `/sources/rust/compiler/rustc_codegen_cranelift/build_system/tests.rs:282` operator `&` operand types ['string literal'] resolved against []

**excerpts, unresolved**
- `/sources/rust/compiler/rustc_codegen_cranelift/build_system/bench.rs:22` operator `!` reason: declared in another file or not found
- `/sources/rust/compiler/rustc_codegen_cranelift/build_system/bench.rs:23` operator `!` reason: declared in another file or not found
- `/sources/rust/compiler/rustc_codegen_cranelift/build_system/bench.rs:38` operator `!` reason: declared in another file or not found
- `/sources/rust/compiler/rustc_codegen_cranelift/build_system/bench.rs:41` operator `&` reason: call result
- `/sources/rust/compiler/rustc_codegen_cranelift/build_system/bench.rs:107` operator `&` reason: call result
- `/sources/rust/compiler/rustc_codegen_cranelift/build_system/bench.rs:131` operator `&` reason: call result

## swiftc (compiler)

**unresolved histogram**

| reason | sites | share |
|---|---|---|
| call result | 48745 | 0.398 |
| declared in another file or not found | 29777 | 0.243 |
| other (binary_expression) | 20740 | 0.169 |
| inferred binding | 15203 | 0.124 |
| member access | 5661 | 0.046 |
| index expression | 722 | 0.006 |
| nested operator, mixed operand types | 680 | 0.006 |
| other (null) | 262 | 0.002 |
| other (type_descriptor) | 249 | 0.002 |
| macro | 183 | 0.001 |
| other (sizeof_expression) | 77 | 0.001 |
| other (assignment_expression) | 75 | 0.001 |
| other (template_function) | 62 | 0.001 |
| other (conditional_expression) | 45 | 0.0 |
| other (alignof_expression) | 31 | 0.0 |
| other (concatenated_string) | 30 | 0.0 |
| other (new_expression) | 30 | 0.0 |
| other (ERROR) | 25 | 0.0 |
| other (initializer_list) | 2 | 0.0 |
| other (offsetof_expression) | 2 | 0.0 |

**resolved variants** (full table; log_210 carries the first 20)

| operator | lhs type | rhs type | sites |
|---|---|---|---|
| ! | bool | None | 1453 |
| ++ | unsigned | None | 1440 |
| + | unsigned | integer literal | 409 |
| != | unsigned | unsigned | 345 |
| < | unsigned | unsigned | 313 |
| << | integer literal | integer literal | 303 |
| == | unsigned | integer literal | 221 |
| ++ | size_t | None | 217 |
| ! | Type | None | 208 |
| && | bool | bool | 184 |
| > | unsigned | integer literal | 177 |
| == | StringRef | string literal | 170 |
| && | bool | string literal | 159 |
| ! | NodePointer | None | 139 |
| - | unsigned | integer literal | 138 |
| << | llvm::raw_ostream | string literal | 133 |
| == | char | char literal | 121 |
| -- | unsigned | None | 111 |
| ++ | int | None | 108 |
| * | SILFunction | None | 102 |
| ! | unsigned | None | 100 |
| || | bool | bool | 100 |
| && | bool literal | string literal | 94 |
| * | char | None | 92 |
| ! | SILValue | None | 91 |
| + | size_t | integer literal | 86 |
| ~ | integer literal (suffix U) | None | 86 |
| ! | SILFunction | None | 84 |
| != | unsigned | integer literal | 78 |
| ! | Expr | None | 78 |
| == | int | int | 67 |
| * | typename Diffs::iterator | None | 65 |
| << | integer literal (suffix ull) | integer literal | 64 |
| ++ | char | None | 60 |
| * | SILInstruction | None | 58 |
| & | StringRef | None | 58 |
| != | int | integer literal | 57 |
| & | bool | None | 56 |
| <= | unsigned | integer literal | 54 |
| + | unsigned | unsigned | 54 |
| * | std::optional<unsigned> | None | 53 |
| * | Added<Stmt *> | None | 52 |
| ! | llvm::cl::opt<bool> | None | 50 |
| == | int | integer literal | 49 |
| - | unsigned | unsigned | 49 |
| * | typename Diffs::const_iterator | None | 49 |
| << | DemanglerPrinter | string literal | 48 |
| ! | ValueDecl | None | 48 |
| ! | SILBasicBlock | None | 47 |
| < | int | int | 46 |
| >= | int | integer literal | 46 |
| == | unsigned | unsigned | 45 |
| < | int | integer literal | 42 |
| < | size_t | size_t | 38 |
| ! | Decl | None | 37 |
| < | unsigned | integer literal | 37 |
| + | int | integer literal | 36 |
| ! | SILInstruction | None | 36 |
| * | integer literal | integer literal | 36 |
| ~ | integer literal (suffix u) | None | 35 |
| * | typename string_t::const_pointer | None | 33 |
| & | char | None | 32 |
| ! | NominalTypeDecl | None | 32 |
| - | int | int | 31 |
| - | size_t | integer literal | 30 |
| == | size_t | integer literal | 30 |
| > | int | integer literal | 29 |
| > | unsigned | unsigned | 29 |
| - | char | integer literal | 29 |
| - | int | integer literal | 27 |
| ! | ModuleDecl | None | 27 |
| & | unsigned | integer literal | 27 |
| >= | unsigned | integer literal | 26 |
| + | string literal | std::string | 26 |
| >> | unsigned | integer literal | 26 |
| != | size_t | size_t | 25 |
| ! | ProtocolDecl | None | 25 |
| ! | TypeRepr | None | 25 |
| + | int | int | 24 |
| ! | llvm::Expected<llvm::BitstreamEntry> | None | 24 |
| - | char | char | 24 |
| -- | int | None | 22 |
| ! | VarDecl | None | 22 |
| ! | DeclContext | None | 22 |
| * | std::optional<ImportedName> | None | 22 |
| * | IRGenModule | None | 22 |
| * | Node | None | 22 |
| > | size_t | integer literal | 21 |
| ! | llvm::ErrorOr<std::unique_ptr<llvm::MemoryBuffer>> | None | 21 |
| * | BuiltinInst | None | 21 |
| ++ | typename string_t::const_pointer | None | 21 |
| * | std::optional<SILDeclRef> | None | 21 |
| != | bool | bool | 20 |
| ! | ClassDecl | None | 20 |
| ! | FuncDecl | None | 20 |
| * | SILModule | None | 20 |
| ~ | integer literal | None | 20 |
| & | uint64_t | None | 20 |
| ! | Node | None | 19 |
| * | SILBasicBlock | None | 19 |
| * | SILBasicBlock::iterator | None | 19 |
| * | std::optional<ActorIsolation> | None | 19 |
| ! | llvm::Expected<unsigned> | None | 19 |
| + | integer literal | None | 19 |
| * | typename string_t::iterator | None | 19 |
| ! | char | None | 18 |
| && | SILValue | string literal | 18 |
| && | Type | string literal | 18 |
| & | SILBasicBlock::iterator | None | 18 |
| << | raw_ostream | string literal | 18 |
| ! | GenericSignature | None | 18 |
| * | unsigned | integer literal | 18 |
| ! | ImportedName | None | 18 |
| != | StringRef | string literal | 18 |
| ! | Expected<llvm::BitstreamEntry> | None | 18 |
| & | StoredPointer | None | 18 |
| ! | clang::Module | None | 17 |
| + | char | integer literal | 17 |
| & | RewritePath | None | 17 |
| & | llvm::Value | None | 17 |
| << | integer literal (suffix U) | integer literal | 17 |
| != | char | char literal | 16 |
| << | DemanglerPrinter | char literal | 16 |
| ! | CanType | None | 16 |
| * | SILValue | None | 16 |
| != | SILType | SILType | 16 |
| + | integer literal | integer literal | 16 |
| & | ASTContext | None | 16 |
| ! | llvm::Value | None | 16 |
| <= | unsigned | unsigned | 15 |
| sizeof | char | None | 15 |
| && | SILFunction | string literal | 15 |
| == | SILValue | SILValue | 15 |
| * | SourceFile | None | 15 |
| << | unsigned | integer literal | 15 |
| & | posix_spawn_file_actions_t | None | 15 |
| ! | Arg | None | 15 |
| & | pthread_attr_t | None | 15 |
| -- | char | None | 14 |
| & | SILFunction | None | 14 |
| >= | unsigned | unsigned | 14 |
| ! | Operand | None | 14 |
| * | Operand | None | 14 |
| ! | std::optional<unsigned> | None | 14 |
| == | uint64_t | integer literal | 14 |
| ! | SourceFile | None | 14 |
| & | ::UUID | None | 14 |
| << | uint64_t | integer literal | 14 |
| + | uint64_t | uint64_t | 14 |
| * | unsigned char | None | 14 |
| && | integer literal | string literal | 13 |
| ! | NameSource | None | 13 |
| ! | std::error_code | None | 13 |
| ! | Pattern | None | 13 |
| ! | ImportedType | None | 13 |
| ++ | unsigned char | None | 13 |
| ! | Expected<Decl *> | None | 13 |
| ++ | typename Diffs::iterator | None | 13 |
| -- | size_t | None | 12 |
| & | SILBasicBlock | None | 12 |
| && | SILInstruction | string literal | 12 |
| & | SILInstruction | None | 12 |
| + | string literal | StringRef | 12 |
| * | std::optional<StringRef> | None | 12 |
| & | void | None | 12 |
| << | integer literal | unsigned | 12 |
| - | int | None | 12 |
| / | unsigned | integer literal | 12 |
| <= | int | integer literal | 11 |
| <= | int | int | 11 |
| - | size_t | size_t | 11 |
| >= | int | int | 11 |
| * | std::optional<SILValue> | None | 11 |
| != | SILValue | SILValue | 11 |
| ! | EnumElementDecl | None | 11 |
| & | Node | None | 11 |
| && | SILBasicBlock | string literal | 11 |
| && | unsigned | string literal | 11 |
| == | unsigned | integer literal (suffix U) | 11 |
| * | std::optional<bool> | None | 11 |
| && | Expr | string literal | 11 |
| != | size_t | integer literal | 11 |
| ! | std::optional<ActorIsolation> | None | 11 |
| ! | AvailableAttr | None | 11 |
| == | SourceLoc | SourceLoc | 11 |
| == | char | char | 11 |
| * | ModuleDecl | None | 11 |
| * | std::optional<std::string> | None | 11 |
| * | BasicBlock::iterator | None | 11 |
| & | Instruction | None | 11 |
| & | SILType | None | 11 |
| > | int | int | 10 |
| ++ | SILBasicBlock::iterator | None | 10 |
| == | bool | bool | 10 |
| - | uint64_t | integer literal | 10 |
| != | int | int | 10 |
| % | unsigned | integer literal | 10 |
| == | SILType | SILType | 10 |
| ! | TypeDecl | None | 10 |
| << | llvm::raw_svector_ostream | string literal | 10 |
| & | PrintingDiagnosticConsumer | None | 10 |
| ! | GenericEnvironment | None | 10 |
| ++ | typename string_t::iterator | None | 10 |
| ! | BuiltType | None | 10 |
| ++ | unsigned long | None | 9 |
| != | unsigned | integer literal (suffix U) | 9 |
| * | std::optional<SourceLoc> | None | 9 |
| ! | CanGenericSignature | None | 9 |
| == | ModuleDecl | ModuleDecl | 9 |
| ! | ParameterList | None | 9 |
| & | llvm::fltSemantics | None | 9 |
| * | std::unique_ptr<DerivedArgList> | None | 9 |
| ! | Expected<unsigned> | None | 9 |
| ++ | BasicBlock::iterator | None | 9 |
| | | SymbolRoleSet | SymbolRoleSet | 9 |
| * | llvm::Value | None | 9 |
| & | TypeInfo | None | 9 |
| ++ | typename Diffs::const_iterator | None | 9 |
| == | Offset | integer literal | 9 |
| - | char | char literal | 8 |
| + | size_t | size_t | 8 |
| ++ | uint32_t | None | 8 |
| & | uint8_t | float literal (suffix F) | 8 |
| ! | ArraySemanticsCall | None | 8 |
| ! | ApplyInst | None | 8 |
| == | SILBasicBlock | SILBasicBlock | 8 |
| ++ | uint64_t | None | 8 |
| ! | Demangle::NodePointer | None | 8 |
| * | SILLoopInfo | None | 8 |
| & | UnreachableUserCodeReportingState | None | 8 |
| ! | ConcreteDeclRef | None | 8 |
| ! | SubstitutionMap | None | 8 |
| * | std::optional<llvm::VersionTuple> | None | 8 |
| ! | ParamDecl | None | 8 |
| != | BraceStmt | BraceStmt | 8 |
| ! | AccessorDecl | None | 8 |
| * | llvm::json::Object | None | 8 |
| & | FILETIME | None | 8 |
| && | Arg | Arg | 8 |
| == | llvm::FoldingSetNodeID | llvm::FoldingSetNodeID | 8 |
| ! | llvm::Function | None | 8 |
| * | typename Patches::const_iterator | None | 8 |
| * | BuilderErrorOr<Buffer<const char>> | None | 8 |
| & | ::pthread_mutexattr_t | None | 8 |
| & | uint32_t | integer literal (suffix u) | 8 |
| + | std::string | string literal | 7 |
| >= | size_t | integer literal | 7 |
| ! | SILDebugScope | None | 7 |
| ! | ConstructorDecl | None | 7 |
| == | StringRef | StringRef | 7 |
| || | unsigned | unsigned | 7 |
| != | StringRef | StringRef | 7 |
| ! | clang::Type | None | 7 |
| << | llvm::raw_ostream | char literal | 7 |
| ! | clang::Decl | None | 7 |
| ! | AbstractFunctionDecl | None | 7 |
| ! | GenericParamList | None | 7 |
| * | ParsedEnum<bool> | None | 7 |
| ! | AssociatedTypeDecl | None | 7 |
| * | std::optional<SILLinkage> | None | 7 |
| - | uintptr_t | uintptr_t | 7 |
| ! | ASTNode | None | 7 |
| && | Added<Stmt *> | Added<Stmt *> | 7 |
| ! | void | None | 7 |
| == | uint32_t | integer literal | 7 |
| & | llvm::StringSet<> | None | 7 |
| < | int64_t | integer literal | 7 |
| != | char | char | 7 |
| >= | char | char | 7 |
| ! | DeclNameRef | None | 7 |
| ! | std::optional<DeclAttrKind> | None | 7 |
| * | std::optional<DeclAttrKind> | None | 7 |
| == | DeclID | integer literal | 7 |
| * | ArrayRef<uint64_t>::iterator | None | 7 |
| ++ | ArrayRef<uint64_t>::iterator | None | 7 |
| & | CallInst | None | 7 |
| * | std::optional<int> | None | 7 |
| && | llvm::Value | string literal | 7 |
| << | integer literal (suffix U) | unsigned | 7 |
| & | WitnessMetadata | None | 7 |
| -- | typename string_t::size_type | None | 7 |
| * | typename string_t::const_reverse_iterator | None | 7 |
| ++ | ValueBaseUseIterator | None | 7 |
| & | ConcurrentFreeListNode | None | 7 |
| ! | BuilderErrorOr<Buffer<const ValueWitnessTable>> | None | 7 |
| * | BuilderErrorOr<Buffer<const ValueWitnessTable>> | None | 7 |
| sizeof | uint8_t | None | 7 |
| & | uint16_t | integer literal | 7 |
| == | CanType | CanType | 6 |
| == | APInt | APInt | 6 |
| * | std::optional<LoadOperation> | None | 6 |
| != | CanType | CanType | 6 |
| & | DeadEndBlocks | None | 6 |
| != | SILBasicBlock | SILBasicBlock | 6 |
| * | std::optional<SILDebugVariable> | None | 6 |
| ! | SILVTable | None | 6 |
| * | irgen::IRGenModule | None | 6 |
| ! | Entry | None | 6 |
| ! | SILWitnessTable | None | 6 |
| ! | StructDecl | None | 6 |
| ! | AssignExpr | None | 6 |
| ! | std::optional<SILValue> | None | 6 |
| & | SILModule | None | 6 |
| * | ParameterList | None | 6 |
| ~ | Bits | None | 6 |
| & | unsigned | None | 6 |
| & | SerializedKind_t | None | 6 |
| * | std::optional<ForeignErrorConvention> | None | 6 |
| ! | LookupResult | None | 6 |
| ! | DeclName | None | 6 |
| ~ | unsigned | None | 6 |
| != | Stmt | Stmt | 6 |
| + | std::string | std::string | 6 |
| ++ | unsigned int | None | 6 |
| && | ModuleDecl | string literal | 6 |
| << | uint32_t | integer literal | 6 |
| & | clang::Token | None | 6 |
| & | llvm::UTF32 | None | 6 |
| < | char | char | 6 |
| * | std::optional<Type> | None | 6 |
| * | std::optional<CodeCompletionCache::ValueRefCntPtr> | None | 6 |
| > | size_t | size_t | 6 |
| * | integer literal | unsigned | 6 |
| & | std::unique_ptr<llvm::MemoryBuffer> | None | 6 |
| == | std::optional<std::string> | string literal | 6 |
| << | integer literal (suffix ULL) | integer literal | 6 |
| ! | ForDefinition_t | None | 6 |
| && | void | string literal | 6 |
| != | typename string_t::const_pointer | typename string_t::const_pointer | 6 |
| > | typename string_t::size_type | integer literal | 6 |
| >> | typename traits::utf32_t | integer literal | 6 |
| == | typename string_t::iterator | typename string_t::iterator | 6 |
| & | typename string_t::iterator | integer literal | 6 |
| & | typename string_t::iterator | float literal (suffix F) | 6 |
| & | CanType | None | 6 |
| & | SmallVector<ManagedValue, 4> | None | 6 |
| * | ValueBaseUseIterator | None | 6 |
| * | Iterator | None | 6 |
| << | integer literal (suffix u) | integer literal | 6 |
| & | uint32_t | float literal (suffix Fu) | 6 |
| & | uintptr_t | uintptr_t | 6 |
| & | Identifier::Aligner | None | 6 |
| == | std::string::const_iterator | std::string::const_iterator | 6 |
| * | std::string::const_iterator | None | 6 |
| ++ | std::string::const_iterator | None | 6 |
| >> | support::ulittle16_t | integer literal | 6 |
| & | int32_t | None | 5 |
| * | int | int | 5 |
| < | uint8_t | integer literal | 5 |
| == | APInt | integer literal | 5 |
| ! | FullApplySite | None | 5 |
| & | SSAPrunedLiveness | None | 5 |
| != | double | float literal | 5 |
| ! | SILType | None | 5 |
| + | integer literal | unsigned | 5 |
| > | uint64_t | integer literal | 5 |
| * | FixedSizeSlab | None | 5 |
| ! | BuiltinInst | None | 5 |
| && | EnumDecl | string literal | 5 |
| ! | size_t | None | 5 |
| + | StringRef | StringRef | 5 |
| << | EditorConsumerInsertStream | string literal | 5 |
| * | std::optional<CounterExpr> | None | 5 |
| && | CanType | string literal | 5 |
| * | std::optional<AccessorKind> | None | 5 |
| ~ | uintptr_t | None | 5 |
| && | FuncDecl | string literal | 5 |
| ! | BraceStmt | None | 5 |
| && | Type | Type | 5 |
| ! | AnyFunctionType | None | 5 |
| && | DeclContext | string literal | 5 |
| && | ValueDecl | string literal | 5 |
| ! | ParsedDeclName | None | 5 |
| * | std::optional<ProtocolConformance *> | None | 5 |
| & | BridgedStringRef | None | 5 |
| * | LazyValue<std::string> | None | 5 |
| * | std::optional<ImportKind> | None | 5 |
| * | std::optional<UnsupportedElt> | None | 5 |
| ! | clang::CXXRecordDecl | None | 5 |
| & | HANDLE | None | 5 |
| & | llvm::UTF8 | None | 5 |
| + | llvm::UTF32 | integer literal | 5 |
| ! | llvm::yaml::Node | None | 5 |
| <= | char | char | 5 |
| > | uint32_t | integer literal | 5 |
| * | Arg | None | 5 |
| - | unsigned | None | 5 |
| - | DeclID | integer literal | 5 |
| * | llvm::ErrorOr<std::unique_ptr<llvm::MemoryBuffer>> | None | 5 |
| sizeof | uint64_t | None | 5 |
| & | uint32_t | None | 5 |
| & | ExternalSourceLocs | None | 5 |
| & | ReferenceCounting | None | 5 |
| >> | unsigned | unsigned | 5 |
| * | std::optional<ConstantAggregateBuilderBase::PlaceholderPosition> | None | 5 |
| * | std::optional<Size> | None | 5 |
| & | int64_t | None | 5 |
| + | typename string_t::size_type | integer literal | 5 |
| != | typename string_t::const_reverse_iterator | typename string_t::const_reverse_iterator | 5 |
| ++ | typename string_t::const_reverse_iterator | None | 5 |
| < | uint32_t | uint32_t | 5 |
| * | std::optional<InnerIterTy> | None | 5 |
| ! | Impl | None | 5 |
| + | T | unsigned | 5 |
| ! | BuilderErrorOr<Buffer<const char>> | None | 5 |
| >> | uint32_t | integer literal | 5 |
| sizeof | GenericContextDescriptorHeader | None | 5 |
| == | support::ulittle32_t | integer literal | 5 |
| ! | SILLoop | None | 4 |
| ! | DestructureTupleInst | None | 4 |
| & | uint64_t | uint64_t | 4 |
| ! | StoreInst | None | 4 |
| * | SILBasicBlock::pred_iterator | None | 4 |
| & | SILBuilderWithScope | None | 4 |
| * | SILBuilder | None | 4 |
| ! | std::optional<SILBasicBlock::iterator> | None | 4 |
| & | SmallVector<SILBasicBlock *, 4> | None | 4 |
| & | SmallVector<Operand *, 4> | None | 4 |
| & | SmallVector<Operand *, 8> | None | 4 |
| & | SmallVector<Operand *, 16> | None | 4 |
| & | Operand | None | 4 |
| ! | ValueBase | None | 4 |
| ! | DominanceInfo | None | 4 |
| ! | NullablePtr<EnumElementDecl> | None | 4 |
| * | BeginAccessInst | None | 4 |
| ! | CopyAddrInst | None | 4 |
| && | SILValue | SILValue | 4 |
| < | unsigned long | unsigned long | 4 |
| & | SILFunction::iterator | None | 4 |
| * | SILFunction::iterator | None | 4 |
| & | SmallVector<SILBasicBlock *, 8> | None | 4 |
| && | AccessStorage | string literal | 4 |
| && | ConstructorDecl | string literal | 4 |
| != | uint64_t | integer literal | 4 |
| ! | IfStmt | None | 4 |
| * | std::optional<SmallString<4>> | None | 4 |
| ! | IndexSubset | None | 4 |
| ! | llvm::Expected<llvm::StringRef> | None | 4 |
| * | std::optional<ObjCReason> | None | 4 |
| * | std::optional<ObjCSelector> | None | 4 |
| * | std::optional<Diag<Type, Type>> | None | 4 |
| ! | GenericTypeDecl | None | 4 |
| || | ProtocolDecl | ProtocolDecl | 4 |
| ! | Constraint | None | 4 |
| & | ptrdiff_t | None | 4 |
| & | SmallVector<ValueDecl *, 4> | None | 4 |
| ! | CaseStmt | None | 4 |
| ! | TypeExpr | None | 4 |
| & | ParameterList | None | 4 |
| ! | T | None | 4 |
| * | clang::NamedDecl::attr_iterator | None | 4 |
| | | integer literal | integer literal | 4 |
| ! | std::optional<StringRef> | None | 4 |
| << | raw_fd_ostream | char literal | 4 |
| & | std::string | None | 4 |
| & | int | None | 4 |
| * | std::unique_ptr<SILModule> | None | 4 |
| == | std::string | string literal | 4 |
| * | std::optional<CopyPropagationOption> | None | 4 |
| * | std::unique_ptr<Compilation> | None | 4 |
| && | unsigned | unsigned | 4 |
| == | double | float literal | 4 |
| -- | uint32_t | None | 4 |
| > | ssize_t | integer literal | 4 |
| & | Lexer | None | 4 |
| * | std::unique_ptr<CompilerInstance> | None | 4 |
| ! | SILDefaultWitnessTable | None | 4 |
| ! | uint8_t | None | 4 |
| ! | Expected<Type> | None | 4 |
| == | uint8_t | integer literal | 4 |
| + | char * | size_t | 4 |
| & | mtx_t | None | 4 |
| * | std::optional<ObjectRef> | None | 4 |
| * | std::optional<std::vector<std::string>> | None | 4 |
| * | FileOrError | None | 4 |
| & | uint8_t | None | 4 |
| & | BasicBlock::iterator | None | 4 |
| & | BasicBlock::const_iterator | None | 4 |
| * | BasicBlock::const_iterator | None | 4 |
| != | BasicBlock::const_iterator | BasicBlock::const_iterator | 4 |
| && | std::optional<innerty> | string literal | 4 |
| * | std::optional<innerty> | None | 4 |
| ! | ExtensionDecl | None | 4 |
| * | std::optional<ParameterConvention> | None | 4 |
| ! | llvm::Type | None | 4 |
| & | unsigned | unsigned | 4 |
| * | std::optional<int64_t> | None | 4 |
| * | std::optional<Address> | None | 4 |
| ! | RequireMetadata_t | None | 4 |
| * | std::optional<CanType> | None | 4 |
| * | typename Patches::iterator | None | 4 |
| * | FailureHandler | None | 4 |
| - | uint32_t | integer literal | 4 |
| && | Impl | bool | 4 |
| ++ | Iterator | None | 4 |
| & | Offset | integer literal | 4 |
| & | struct ::timespec | None | 4 |
| ! | StoredPointer | None | 4 |
| & | typename Runtime::StoredSize | integer literal | 4 |
| * | std::optional<MutableArrayRef<VarDecl *>> | None | 4 |
| ! | PointerUnion<PatternBindingDecl *,
               Stmt *,
               VarDecl *,
               CaptureListExpr *> | None | 4 |
| == | std::string::const_iterator | char literal | 4 |
| == | char | integer literal | 3 |
| * | NodePointer | None | 3 |
| / | int | integer literal | 3 |
| - | uint32_t | uint32_t | 3 |
| == | size_t | size_t | 3 |
| + | uint32_t | integer literal | 3 |
| & | uint8_t | integer literal | 3 |
| * | int | integer literal | 3 |
| != | APInt | APInt | 3 |
| * | std::optional<LoadOwnershipQualifier> | None | 3 |
| == | size_t | unsigned | 3 |
| ++ | SILBasicBlock::pred_iterator | None | 3 |
| & | SmallVector<SILBasicBlock *, 32> | None | 3 |
| ! | std::optional<SILDebugVariable> | None | 3 |
| && | SILType | string literal | 3 |
| & | UserList | None | 3 |
| != | SILBasicBlock::iterator | SILBasicBlock::iterator | 3 |
| ! | WitnessMethodInst | None | 3 |
| && | ClassDecl | string literal | 3 |
| << | RemarkPassed | string literal | 3 |
| * | CondFailInst | None | 3 |
| * | PostDomTreeNode | None | 3 |
| ! | EnumDecl | None | 3 |
| / | double | float literal | 3 |
| > | double | double | 3 |
| ! | irgen::IRGenModule | None | 3 |
| ! | std::optional<uint64_t> | None | 3 |
| * | std::optional<uint64_t> | None | 3 |
| -- | uint64_t | None | 3 |
| * | LoadInst | None | 3 |
| >= | uint32_t | uint32_t | 3 |
| & | SmallVector<SILPhiArgument *, 8> | None | 3 |
| <= | unsigned const | unsigned const | 3 |
| < | unsigned const | unsigned const | 3 |
| * | SuccIterTy | None | 3 |
| * | std::optional<SILType> | None | 3 |
| * | OperandValueArrayRef::iterator | None | 3 |
| ! | std::optional<RecordedAccess> | None | 3 |
| && | ProtocolDecl | string literal | 3 |
| ! | Stmt | None | 3 |
| ! | CanTupleType | None | 3 |
| & | LocWithParent | None | 3 |
| * | MarkDependenceInst | None | 3 |
| ! | IterableDeclContext | None | 3 |
| >= | uint64_t | uint64_t | 3 |
| - | uint64_t | uint64_t | 3 |
| & | llvm::DenseMap<CanType, Identifier> | None | 3 |
| && | NominalTypeDecl | string literal | 3 |
| * | std::optional<LinearLifetimeChecker::ErrorBuilder> | None | 3 |
| & | SILTypeResolutionContext | None | 3 |
| - | int64_t | None | 3 |
| * | SILOptionalAttrValue | None | 3 |
| * | ParsedEnum<SILAccessEnforcement> | None | 3 |
| & | ValueDecl | None | 3 |
| ! | std::optional<SILLinkage> | None | 3 |
| * | T | None | 3 |
| * | std::optional<ForeignAsyncConvention> | None | 3 |
| != | ModuleDecl | ModuleDecl | 3 |
| * | ArgumentList | None | 3 |
| ! | TuplePatternElt | None | 3 |
| * | std::optional<InFlightDiagnostic> | None | 3 |
| > | bool | bool | 3 |
| ! | std::optional<AnyFunctionRef> | None | 3 |
| ! | ConstraintLocator | None | 3 |
| ! | ArgumentList | None | 3 |
| == | DeclBaseName | string literal | 3 |
| != | Expr | Expr | 3 |
| && | ProtocolDecl | ProtocolDecl | 3 |
| * | unsigned | None | 3 |
| * | TypeAttrSet | None | 3 |
| && | Type | bool | 3 |
| - | APInt | None | 3 |
| && | VarDecl | string literal | 3 |
| & | std::optional<PlatformKind> | None | 3 |
| ! | TypeRefinementContext | None | 3 |
| ! | FileOrError | None | 3 |
| || | Type | Type | 3 |
| & | ASTNode | None | 3 |
| && | BraceStmt | string literal | 3 |
| ! | std::optional<Diag<Type, Type>> | None | 3 |
| ! | clang::CXXConstructorDecl | None | 3 |
| && | T | bool | 3 |
| ! | clang::FunctionDecl | None | 3 |
| ! | std::optional<ForeignAsyncConvention> | None | 3 |
| == | Decl | FuncDecl | 3 |
| ! | clang::IdentifierInfo | None | 3 |
| & | ModuleDecl | None | 3 |
| ! | std::optional<StoredContext> | None | 3 |
| && | std::error_code | string literal | 3 |
| * | swift::VisibleDeclConsumer | None | 3 |
| & | size_t | integer literal | 3 |
| * | llvm::yaml::MappingNode | None | 3 |
| * | std::unique_ptr<llvm::Module> | None | 3 |
| * | llvm::Expected<llvm::remarks::Format> | None | 3 |
| * | std::unique_ptr<llvm::opt::InputArgList> | None | 3 |
| + | uint8_t | integer literal | 3 |
| ! | clang::RawComment | None | 3 |
| * | std::optional<ContextualNotRecommendedReason> | None | 3 |
| ! | CodeCompletionMacroRoles | None | 3 |
| * | unsigned | unsigned | 3 |
| * | llvm::Expected<file_types::ID> | None | 3 |
| & | T | None | 3 |
| & | size_t | None | 3 |
| < | unsigned char | integer literal | 3 |
| == | unsigned char | integer literal | 3 |
| ! | std::optional<MacroRole> | None | 3 |
| * | std::optional<MacroRole> | None | 3 |
| & | DefaultArgumentInfo | None | 3 |
| && | SILGlobalVariable | string literal | 3 |
| && | FileUnit | string literal | 3 |
| & | SmallVector<StringRef, 1> | None | 3 |
| << | TypeID | integer literal | 3 |
| == | uint16_t | integer literal | 3 |
| != | uint64_t | uint64_t | 3 |
| & | cnd_t | None | 3 |
| & | SmallVector<StringRef, 2> | None | 3 |
| ! | std::optional<std::vector<std::string>> | None | 3 |
| + | std::size_t | integer literal | 3 |
| ! | Image | None | 3 |
| + | uint64_t | integer literal | 3 |
| ~ | integer literal (suffix ull) | None | 3 |
| == | Value | Value | 3 |
| != | BasicBlock::iterator | BasicBlock::iterator | 3 |
| != | std::vector<WeakTrackingVH>::iterator | std::vector<WeakTrackingVH>::iterator | 3 |
| ++ | std::vector<WeakTrackingVH>::iterator | None | 3 |
| * | std::vector<WeakTrackingVH>::iterator | None | 3 |
| + | unsigned | integer literal (suffix U) | 3 |
| ! | GenericTypeParamType | None | 3 |
| * | ImportSet | None | 3 |
| && | yaml::Node | string literal | 3 |
| / | uint64_t | uint64_t | 3 |
| > | uint64_t | uint64_t | 3 |
| ! | HeapLayout | None | 3 |
| ! | ConstantInit | None | 3 |
| && | GenericEnvironment | string literal | 3 |
| > | int64_t | integer literal | 3 |
| * | std::optional<OperationCost> | None | 3 |
| * | std::optional<StackAddress> | None | 3 |
| * | TypeInfo | None | 3 |
| ! | ClassMetadataLayout | None | 3 |
| && | ClassLayout | string literal | 3 |
| << | integer literal (suffix ull) | unsigned | 3 |
| && | llvm::DIType | string literal | 3 |
| > | uint16_t | integer literal | 3 |
| != | llvm::Type | llvm::Type | 3 |
| - | unsigned int | integer literal | 3 |
| -- | typename Diffs::iterator | None | 3 |
| + | string_t | string_t | 3 |
| - | short | short | 3 |
| * | integer literal | short | 3 |
| > | int | short | 3 |
| >= | typename traits::utf32_t | integer literal | 3 |
| < | typename traits::utf32_t | integer literal | 3 |
| & | typename traits::utf32_t | float literal (suffix F) | 3 |
| ! | std::optional<TemporaryInitialization> | None | 3 |
| & | SmallVector<ManagedValue, 8> | None | 3 |
| && | Expr | Expr | 3 |
| ++ | uint16_t | None | 3 |
| & | FailureHandler | None | 3 |
| && | SILDebugScope | string literal | 3 |
| != | CanAnyFunctionType | CanAnyFunctionType | 3 |
| * | std::optional<SILAccessEnforcement> | None | 3 |
| - | uintptr_t | integer literal | 3 |
| + | char | size_t | 3 |
| < | unsigned | size_t | 3 |
| ! | std::optional<EnumElementDecl *> | None | 3 |
| ! | SmallVectorImpl<SILBasicBlock *> | None | 3 |
| * | SwiftRAII | None | 3 |
| >> | uint64_t | uint64_t | 3 |
| && | T | string literal | 3 |
| * | PtrSet | None | 3 |
| & | ulock_t | None | 3 |
| * | std::unique_ptr<ASTContext> | None | 3 |
| <= | char | char literal | 3 |
| - | intptr_t | intptr_t | 3 |
| & | GenericContextDescriptorHeader | None | 3 |
| != | StoredPointer | integer literal | 3 |
| & | int32_t | integer literal | 3 |
| & | StoredSignedPointer | None | 3 |
| ! | BuiltTypeDecl | None | 3 |
| << | integer literal (suffix U) | integer literal (suffix U) | 3 |
| && | CaseStmt | string literal | 3 |
| ! | ThrownErrorDestination | None | 3 |
| ! | Error | None | 3 |
| * | Error | None | 3 |
| * | integer literal | int | 2 |
| << | DemanglerPrinter | char | 2 |
| && | NodePointer | string literal | 2 |
| < | char | char literal | 2 |
| > | char | char literal | 2 |
| ~ | Node::IndexType | None | 2 |
| * | size_t | integer literal | 2 |
| << | std::string | string literal | 2 |
| & | SmallVector<Projection, 4> | None | 2 |
| == | SILFunction | SILFunction | 2 |
| - | uint8_t | integer literal | 2 |
| ! | DestroyAddrInst | None | 2 |
| ! | SILPhiArgument | None | 2 |
| ! | EndApplyInst | None | 2 |
| ++ | llvm::Statistic | None | 2 |
| ! | std::optional<SymbolicValue> | None | 2 |
| ++ | SILBasicBlock::reverse_iterator | None | 2 |
| ! | std::unique_ptr<AccumulatedOptimizerStats> | None | 2 |
| * | DeadEndBlocks | None | 2 |
| && | DeclRefExpr | string literal | 2 |
| ! | DeclRefExpr | None | 2 |
| == | SILInstruction | SILInstruction | 2 |
| || | SILBasicBlock | bool | 2 |
| ! | EndAccessInst | None | 2 |
| || | SILValue | SILValue | 2 |
| ! | CondFailInst | None | 2 |
| ! | TrampolineDest | None | 2 |
| * | TermInst | None | 2 |
| ! | ApplySite | None | 2 |
| ! | std::optional<StorageStateTracking<LiveValues>> | None | 2 |
| ! | LiteralInst | None | 2 |
| != | unsigned | std::optional<unsigned> | 2 |
| && | ApplySite | string literal | 2 |
| ! | BoundGenericClassType | None | 2 |
| ! | DomAccessStorage | None | 2 |
| ++ | SmallVectorImpl<Edge>::iterator | None | 2 |
| || | SILBasicBlock | SILBasicBlock | 2 |
| ! | StoreBorrowInst | None | 2 |
| ! | AllocStackInst | None | 2 |
| * | SILLoop | None | 2 |
| < | unsigned | unsigned const | 2 |
| & | SwiftPassInvocation | None | 2 |
| ! | std::optional<bool> | None | 2 |
| ! | std::optional<SILDynamicMergedIsolationInfo> | None | 2 |
| ! | FunctionInfo | None | 2 |
| ! | MarkDependenceInst | None | 2 |
| && | SILLocation | string literal | 2 |
| != | SILBasicBlock::pred_iterator | SILBasicBlock::pred_iterator | 2 |
| != | OperandValueArrayRef::iterator | OperandValueArrayRef::iterator | 2 |
| ++ | OperandValueArrayRef::iterator | None | 2 |
| ! | InjectEnumAddrInst | None | 2 |
| ! | InitEnumDataAddrInst | None | 2 |
| * | SwitchEnumTermInst | None | 2 |
| ! | ClangNode | None | 2 |
| ! | uint64_t | None | 2 |
| << | integer literal (suffix L) | unsigned int | 2 |
| << | raw_ostream | char literal | 2 |
| == | ProtocolDecl | ProtocolDecl | 2 |
| * | std::optional<RecordedAccess> | None | 2 |
| != | std::optional<SILValue> | SILValue | 2 |
| -- | SILBasicBlock::iterator | None | 2 |
| ! | AllocationInst | None | 2 |
| * | AllocationInst | None | 2 |
| ! | MethodInst | None | 2 |
| * | LocWithParent | None | 2 |
| * | FullApplySite | None | 2 |
| && | SubscriptDecl | string literal | 2 |
| ! | SubscriptDecl | None | 2 |
| ! | std::optional<AutoDiffConfig> | None | 2 |
| * | PartialApplyInst | None | 2 |
| * | ApplyInst | None | 2 |
| * | SwitchEnumAddrInst | None | 2 |
| * | SelectEnumAddrInst | None | 2 |
| * | AllocStackInst | None | 2 |
| * | InjectEnumAddrInst | None | 2 |
| * | UncheckedTakeEnumDataAddrInst | None | 2 |
| * | DifferentiableFunctionExtractInst | None | 2 |
| * | RefToRawPointerInst | None | 2 |
| ^ | bool | bool | 2 |
| * | std::optional<ConditionPath> | None | 2 |
| ! | ClosureExpr | None | 2 |
| && | CanType | CanType | 2 |
| ! | std::optional<AccessBase::Kind> | None | 2 |
| ! | AccessStorage | None | 2 |
| ! | SILLoopInfo | None | 2 |
| != | Projection | Projection | 2 |
| * | TypeLowering | None | 2 |
| * | std::optional<CapturedValue> | None | 2 |
| && | std::optional<SourceLoc> | string literal | 2 |
| ! | SourceRange | None | 2 |
| ++ | intptr_t | None | 2 |
| & | uintptr_t | None | 2 |
| sizeof | uintptr_t | None | 2 |
| == | unsigned long | unsigned long | 2 |
| == | long | integer literal | 2 |
| > | long | integer literal | 2 |
| ! | std::optional<InstructionContext> | None | 2 |
| ! | SILModule | None | 2 |
| & | AvailabilityContext | None | 2 |
| ! | SILGlobalVariable | None | 2 |
| ! | std::optional<ApplyIsolationCrossing> | None | 2 |
| * | std::optional<T> | None | 2 |
| ! | llvm::Expected<StringRef> | None | 2 |
| * | llvm::Expected<StringRef> | None | 2 |
| & | std::variant<Builder32, Builder64> | None | 2 |
| ! | LookupTypeResult | None | 2 |
| && | std::optional<unsigned> | string literal | 2 |
| ! | DeclAttribute | None | 2 |
| * | std::optional<ConstraintKind> | None | 2 |
| ! | DeclRefTypeRepr | None | 2 |
| ! | TupleType | None | 2 |
| ! | LabeledConditionalStmt | None | 2 |
| == | std::optional<Identifier> | std::optional<Identifier> | 2 |
| ! | OpenedArchetypeType | None | 2 |
| ! | std::optional<PotentialEffectReason> | None | 2 |
| * | std::optional<PotentialEffectReason> | None | 2 |
| * | std::optional<AttributedImport<swift::ImportedModule>> | None | 2 |
| && | FuncDecl | FuncDecl | 2 |
| && | bool | ValueDecl | 2 |
| + | ReferencedActor::Kind | integer literal | 2 |
| ! | LiteralExpr | None | 2 |
| ! | std::optional<AutomaticEnumValueKind> | None | 2 |
| ! | OpaqueValueExpr | None | 2 |
| ! | ApplyExpr | None | 2 |
| ! | std::optional<Fallback> | None | 2 |
| ! | Op | None | 2 |
| + | std::string | char literal | 2 |
| ! | OptionSet<MissingFlags> | None | 2 |
| && | ptrdiff_t | string literal | 2 |
| ! | ptrdiff_t | None | 2 |
| && | bool | AccessorDecl | 2 |
| & | SmallVector<ProtocolDecl *, 2> | None | 2 |
| && | TypeRepr | string literal | 2 |
| * | std::optional<AvailabilityContext> | None | 2 |
| != | PointerTypeKind | PointerTypeKind | 2 |
| ! | TypeBase | None | 2 |
| ! | ReturnStmt | None | 2 |
| ! | FunctionType | None | 2 |
| == | Stmt | Stmt | 2 |
| ! | clang::EnumDecl | None | 2 |
| && | bool | ProtocolDecl | 2 |
| - | llvm::APSInt | None | 2 |
| && | std::optional<ForeignAsyncConvention> | string literal | 2 |
| ! | clang::NamedDecl | None | 2 |
| && | Decl | string literal | 2 |
| || | FuncDecl | FuncDecl | 2 |
| & | clang::CXXCastPath | None | 2 |
| == | clang::Module | clang::Module | 2 |
| * | std::optional<StoredContext> | None | 2 |
| sizeof | llvm::StringLiteral | None | 2 |
| * | std::optional<ForeignErrorConvention::Info> | None | 2 |
| ! | clang::DeclContext | None | 2 |
| * | std::optional<const clang::Decl *> | None | 2 |
| ! | std::optional<AnySwiftNameAttr> | None | 2 |
| * | std::unique_ptr<clang::CompilerInvocation> | None | 2 |
| ! | std::unique_ptr<clang::CompilerInvocation> | None | 2 |
| & | clang::FileManager | None | 2 |
| ! | std::optional<std::string> | None | 2 |
| == | llvm::StringRef | string literal | 2 |
| & | struct rusage | None | 2 |
| != | int64_t | integer literal | 2 |
| ! | Pipe | None | 2 |
| == | pid_t | integer literal | 2 |
| & | SECURITY_ATTRIBUTES | None | 2 |
| == | llvm::UTF32 | llvm::UTF32 | 2 |
| - | llvm::UTF8 | llvm::UTF8 | 2 |
| * | integer literal | std::size_t | 2 |
| < | std::size_t | std::size_t | 2 |
| % | std::size_t | integer literal | 2 |
| ! | TypeToPathMap | None | 2 |
| & | llvm::StringMap<std::vector<BlockListAction>> | None | 2 |
| & | PROCESS_MEMORY_COUNTERS | None | 2 |
| sizeof | PROCESS_MEMORY_COUNTERS | None | 2 |
| < | ssize_t | integer literal | 2 |
| * | std::unique_ptr<Task> | None | 2 |
| == | llvm::SmallString<128> | string literal | 2 |
| ! | std::unique_ptr<llvm::Module> | None | 2 |
| & | SmallVector<std::unique_ptr<llvm::MemoryBuffer>, 4> | None | 2 |
| && | std::optional<bool> | std::optional<bool> | 2 |
| & | llvm::LLVMContext | None | 2 |
| * | std::unique_ptr<ToolChain> | None | 2 |
| & | InterfaceTypeChangeDetector | None | 2 |
| * | llvm::raw_ostream | None | 2 |
| ! | clang::comments::FullComment | None | 2 |
| * | DeclContext | None | 2 |
| & | SynthesizedExtensionInfo | None | 2 |
| & | CodeCompletionMacroRoles | CodeCompletionMacroRoles | 2 |
| * | ContextFreeCodeCompletionResult | None | 2 |
| + | float literal | float literal | 2 |
| * | float literal | float literal | 2 |
| & | ExpectedTypeContext | None | 2 |
| + | SmallString<128> | string literal | 2 |
| + | StringRef | string literal | 2 |
| * | std::unique_ptr<InputArgList> | None | 2 |
| * | JobAction | None | 2 |
| sizeof | SymbolicP | None | 2 |
| ! | TypeAliasDecl | None | 2 |
| && | GenericTypeParamDecl | string literal | 2 |
| >= | unsigned char | integer literal | 2 |
| & | unsigned char | float literal (suffix F) | 2 |
| < | signed char | integer literal | 2 |
| == | uint32_t | integer literal (suffix U) | 2 |
| << | char literal | integer literal | 2 |
| > | char | char | 2 |
| + | char | unsigned | 2 |
| - | integer literal | unsigned | 2 |
| ! | EffectsKind | None | 2 |
| * | EffectsKind | None | 2 |
| != | SourceLoc | SourceLoc | 2 |
| & | IRGenOptions | None | 2 |
| == | TypeID | integer literal | 2 |
| != | DeclID | integer literal | 2 |
| && | TupleType | string literal | 2 |
| > | int32_t | integer literal | 2 |
| < | int32_t | integer literal | 2 |
| - | int32_t | None | 2 |
| ! | FileUnit | None | 2 |
| != | llvm::vfs::directory_iterator | llvm::vfs::directory_iterator | 2 |
| * | std::shared_ptr<const ModuleFileSharedCore> | None | 2 |
| & | llvm::SmallString<256> | None | 2 |
| ! | std::unique_ptr<DeclMembersTable> | None | 2 |
| * | std::unique_ptr<DeclMembersTable> | None | 2 |
| ! | std::unique_ptr<llvm::MemoryBuffer> | None | 2 |
| ! | Expected<Pattern *> | None | 2 |
| && | GenericSignature | string literal | 2 |
| & | DeclAttribute | None | 2 |
| ! | PrecedenceGroupDecl | None | 2 |
| & | intptr_t | None | 2 |
| & | ULONG_PTR | None | 2 |
| & | MEMORY_BASIC_INFORMATION | None | 2 |
| & | SourceManager | None | 2 |
| ! | std::optional<Error> | None | 2 |
| * | std::optional<Error> | None | 2 |
| & | DiagnosticEngine | None | 2 |
| & | ForwardingDiagnosticConsumer | None | 2 |
| ! | std::optional<OutputFilesComputer> | None | 2 |
| ! | std::optional<std::vector<SupplementaryOutputPaths>> | None | 2 |
| * | std::optional<std::vector<SupplementaryOutputPaths>> | None | 2 |
| ! | std::optional<OutputEntry> | None | 2 |
| sizeof | uint32_t | None | 2 |
| ++ | BasicBlock::const_iterator | None | 2 |
| == | BasicBlock::const_iterator | BasicBlock::const_iterator | 2 |
| & | Function::const_iterator | None | 2 |
| * | Function::const_iterator | None | 2 |
| ++ | Function::const_iterator | None | 2 |
| != | Function::const_iterator | Function::const_iterator | 2 |
| & | GlobalNumberState | None | 2 |
| % | uint64_t | float literal (suffix FFFF) | 2 |
| ! | Constant | None | 2 |
| != | uint8_t | integer literal | 2 |
| && | TypeBase | string literal | 2 |
| + | StringRef::size_type | integer literal | 2 |
| && | GenericParamList | string literal | 2 |
| + | integer literal | int | 2 |
| * | std::optional<ClangTypeKind> | None | 2 |
| && | Type | Decl | 2 |
| < | bool | bool | 2 |
| && | LazyMemberLoader | string literal | 2 |
| * | std::optional<MetatypeRepresentation> | None | 2 |
| <= | ssize_t | integer literal | 2 |
| != | ssize_t | uint64_t | 2 |
| != | ConformanceEntryKind | ConformanceEntryKind | 2 |
| - | void | integer literal | 2 |
| == | std::optional<int> | integer literal | 2 |
| > | std::optional<int> | integer literal | 2 |
| < | std::optional<int> | integer literal | 2 |
| != | std::optional<int> | integer literal | 2 |
| / | unsigned | unsigned | 2 |
| ! | SDKNode | None | 2 |
| * | SDKNode | None | 2 |
| * | std::optional<FulfillmentMap> | None | 2 |
| * | iterator | None | 2 |
| ++ | iterator | None | 2 |
| <= | size_t | size_t | 2 |
| * | size_t | size_t | 2 |
| | | LayoutStringFlags | LayoutStringFlags | 2 |
| - | unsigned | integer literal (suffix U) | 2 |
| ~ | uint64_t | None | 2 |
| * | uint32_t | integer literal | 2 |
| * | std::optional<AsyncContextLayout> | None | 2 |
| ! | std::optional<FunctionPointer> | None | 2 |
| ~ | APInt | None | 2 |
| && | llvm::BasicBlock | string literal | 2 |
| || | ForDefinition_t | bool | 2 |
| == | llvm::Value | llvm::GlobalValue | 2 |
| * | std::optional<LinkEntity> | None | 2 |
| ! | Size::int_type | None | 2 |
| >= | int64_t | integer literal | 2 |
| & | OutliningMetadataCollector | None | 2 |
| - | Size | Size | 2 |
| != | llvm::APInt | integer literal | 2 |
| ! | std::optional<OperationCost> | None | 2 |
| ! | CacheEntry | None | 2 |
| ! | llvm::Constant | None | 2 |
| < | std::optional<int64_t> | integer literal | 2 |
| ! | llvm::BasicBlock | None | 2 |
| * | std::optional<GenericSignatureHeaderBuilder> | None | 2 |
| * | std::optional<llvm::vfs::OutputFile> | None | 2 |
| ! | int | None | 2 |
| < | unsigned | integer literal (suffix u) | 2 |
| * | ParamDecl | None | 2 |
| == | int_type | integer literal | 2 |
| ~ | integer literal (suffix ULL) | None | 2 |
| ! | llvm::DIScope | None | 2 |
| == | std::string | StringRef | 2 |
| ! | std::optional<CompletedDebugTypeInfo> | None | 2 |
| * | std::optional<CompletedDebugTypeInfo> | None | 2 |
| | | unsigned | unsigned | 2 |
| << | uint8_t | integer literal | 2 |
| * | std::unique_ptr<llvm::LLVMContext> | None | 2 |
| * | typename std::map<LinePtr, size_t>::const_iterator | None | 2 |
| + | typename string_t::const_pointer | typename string_t::size_type | 2 |
| == | string_t | string_t | 2 |
| - | size_t | int | 2 |
| < | int | short | 2 |
| == | typename string_t::size_type | integer literal | 2 |
| + | typename string_t::const_pointer | integer literal | 2 |
| - | typename string_t::size_type | integer literal | 2 |
| ++ | typename Patches::const_iterator | None | 2 |
| ++ | typename Patches::iterator | None | 2 |
| > | short | int | 2 |
| -- | typename string_t::iterator | None | 2 |
| & | unsigned | float literal (suffix F) | 2 |
| * | std::optional<NodeAnnotation> | None | 2 |
| & | ExistentialInitialization | None | 2 |
| * | std::optional<Conversion> | None | 2 |
| & | SmallVector<ManagedValue, 1> | None | 2 |
| && | std::optional<Callee> | string literal | 2 |
| * | std::optional<Callee> | None | 2 |
| ! | AbstractStorageDecl | None | 2 |
| * | std::optional<ResultPlanPtr> | None | 2 |
| && | DebuggerClient | string literal | 2 |
| * | std::optional<AbstractionPattern> | None | 2 |
| ! | SILProfiler | None | 2 |
| & | VTable | None | 2 |
| * | CompilerArgInstanceCacheMap | None | 2 |
| * | CompilerInstance | None | 2 |
| && | bool | Slab | 2 |
| && | char | char | 2 |
| ! | Slab | None | 2 |
| < | size_t | uint32_t | 2 |
| ! | std::function<void(Operand *use, SILValue newValue)> | None | 2 |
| == | ValueBaseUseIterator | ValueBaseUseIterator | 2 |
| & | SILOptScopeBase | None | 2 |
| ++ | llvm::SmallVectorImpl<SubregionID>::const_iterator | None | 2 |
| -- | llvm::SmallVectorImpl<SubregionID>::const_iterator | None | 2 |
| & | llvm::SmallVector<std::pair<unsigned, unsigned>, 2> | None | 2 |
| << | uintptr_t | unsigned | 2 |
| >> | uintptr_t | unsigned | 2 |
| * | std::optional<EnumElementDecl *> | None | 2 |
| * | SmallVectorImpl<SILBasicBlock *> | None | 2 |
| ~ | SmallBitVector | None | 2 |
| ++ | IteratorBase | None | 2 |
| - | integer literal | None | 2 |
| & | RawType | integer literal | 2 |
| >> | size_t | integer literal | 2 |
| & | std::variant<T, BuilderError> | None | 2 |
| ! | std::optional<LocatorPathElt> | None | 2 |
| ++ | std::size_t | None | 2 |
| == | StoredIndexType | integer literal | 2 |
| - | StoredIndexType | integer literal | 2 |
| != | Iterator | Iterator | 2 |
| == | Iterator | Iterator | 2 |
| ++ | Orig | None | 2 |
| -- | Orig | None | 2 |
| + | uint8_t | uint64_t | 2 |
| >> | uint64_t | integer literal | 2 |
| && | size_t | string literal | 2 |
| & | uint32_t | integer literal | 2 |
| & | struct tls_init_info {
    tls_key_t &k;
    tls_dtor_t d;
  } | None | 2 |
| * | llvm::IntrusiveRefCntPtr<llvm::vfs::OutputBackend> | None | 2 |
| + | uint64_t | int64_t | 2 |
| == | int32_t | integer literal | 2 |
| & | TargetOpaqueExistentialContainer<Runtime> | None | 2 |
| sizeof | TargetOpaqueExistentialContainer<Runtime> | None | 2 |
| sizeof | ExtendedExistentialTypeShapeFlags | None | 2 |
| & | StoredSize | None | 2 |
| >= | char | char literal | 2 |
| ! | swift::Demangle::NodePointer | None | 2 |
| * | std::unique_ptr<SwiftAAResult> | None | 2 |
| * | StoredSize | None | 2 |
| & | uint32_t | float literal (suffix FFFF) | 2 |
| << | float literal (suffix FFu) | integer literal | 2 |
| & | uint8_t | integer literal (suffix u) | 2 |
| & | uint8_t | float literal (suffix Fu) | 2 |
| ! | AsyncTask | None | 2 |
| == | HeapObject | integer literal | 2 |
| ! | Metadata | None | 2 |
| ! | std::optional<MutableArrayRef<VarDecl *>> | None | 2 |
| && | std::optional<
      clang::tooling::dependencies::DependencyScanningFilesystemSharedCache> | string literal | 2 |
| * | std::optional<
      clang::tooling::dependencies::DependencyScanningFilesystemSharedCache> | None | 2 |
| * | llvm::IntrusiveRefCntPtr<llvm::cas::CachingOnDiskFileSystem> | None | 2 |
| >> | uint8_t | integer literal | 2 |
| & | ParamDecl | None | 2 |
| & | RequestKey | None | 2 |
| ! | RequirementRepr | None | 2 |
| & | std::function<void(const void *, DiagnosticEngine &)> | None | 2 |
| && | GenericSignatureImpl | string literal | 2 |
| != | unsigned | integer literal (suffix u) | 2 |
| == | unsigned | integer literal (suffix u) | 2 |
| << | float literal (suffix F) | integer literal | 2 |
| - | It | It | 2 |
| != | It | It | 2 |
| ++ | It | None | 2 |
| * | It | None | 2 |
| && | std::optional<Diagnostic> | string literal | 2 |
| ! | std::optional<Diagnostic> | None | 2 |
| == | Kind | TinyPtrVector<Stmt *> | 2 |
| * | std::optional<uint8_t> | None | 2 |
| ! | MemoryReader::ReadBytesResult | None | 2 |
| - | typename T::Size | uint64_t | 2 |
| & | ReflectionTypeDescriptorFinder | None | 2 |
| << | std::stringstream | string literal | 2 |
| * | ExternalProtocolConformanceDescriptor<ObjCInteropKind, PointerSize> | None | 2 |
| - | make_unsigned_t<value_type> | integer literal | 2 |
| << | make_unsigned_t<value_type> | make_unsigned_t<value_type> | 2 |
| * | Expected<T&> | None | 2 |
| ! | Expected<T> | None | 2 |
| >> | unsigned char | integer literal | 2 |
| & | unsigned char | float literal (suffix f) | 2 |
| >> | Elf32_Word | integer literal | 2 |
| & | Elf32_Word | float literal (suffix ff) | 2 |
| >> | Elf64_Xword | integer literal | 2 |
| & | Elf64_Xword | float literal (suffix ffffffffL) | 2 |
| << | Elf64_Xword | integer literal | 2 |
| * | section_iterator | None | 2 |
| ++ | section_iterator | None | 2 |
| & | support::ulittle16_t | integer literal | 2 |
| / | size_t | integer literal | 1 |
| || | Node | Node | 1 |
| - | int | char literal | 1 |
| + | enum State { Attrs, Inputs, Results } | integer literal | 1 |
| && | bool | NodePointer | 1 |
| == | Node::IndexType | Node::IndexType | 1 |
| + | unsigned | char literal | 1 |
| + | int | char literal | 1 |
| << | std::string | char literal | 1 |
| && | char | string literal | 1 |
| - | char literal | integer literal | 1 |
| < | uint32_t | integer literal | 1 |
| % | int | int | 1 |
| / | int | int | 1 |
| == | uint32_t | uint32_t | 1 |
| > | uint8_t | integer literal | 1 |
| << | uint64_t | unsigned | 1 |
| * | SingleValueInstruction | None | 1 |
| * | Projection | None | 1 |
| || | CanType | CanType | 1 |
| ! | CheckedCastAddrBranchInst | None | 1 |
| ! | CheckedCastBranchInst | None | 1 |
| && | bool | StoreInst | 1 |
| ! | MetatypeInst | None | 1 |
| ! | InitExistentialAddrInst | None | 1 |
| && | bool | InitExistentialAddrInst | 1 |
| & | AvailableValsTy | None | 1 |
| == | CanSILFunctionType | CanSILFunctionType | 1 |
| ! | AbortApplyInst | None | 1 |
| && | bool | llvm::cl::opt<bool> | 1 |
| ! | SpecializedFunction | None | 1 |
| * | CopyValueInst | None | 1 |
| * | std::optional<SymbolicValue> | None | 1 |
| != | SILBasicBlock::reverse_iterator | SILBasicBlock::reverse_iterator | 1 |
| & | SILBasicBlock::reverse_iterator | None | 1 |
| * | SILBasicBlock::reverse_iterator | None | 1 |
| && | NominalTypeDecl | bool | 1 |
| == | NominalTypeDecl | NominalTypeDecl | 1 |
| & | SmallVector<Operand *, 2> | None | 1 |
| && | TermInst | string literal | 1 |
| ! | std::optional<OuterUsers> | None | 1 |
| && | BeginAccessInst | bool | 1 |
| != | BeginAccessInst | BeginAccessInst | 1 |
| || | ActorInstance | ActorInstance | 1 |
| != | ActorInstance | ActorInstance | 1 |
| + | Region | integer literal | 1 |
| & | SmallVector<SILPhiArgument *, 4> | None | 1 |
| && | DestructorDecl | string literal | 1 |
| && | SILInstruction | bool | 1 |
| ! | AliasAnalysis | None | 1 |
| == | SILInstruction | DestroyAddrInst | 1 |
| & | BridgedProperty | None | 1 |
| & | ObjCMethodCall | None | 1 |
| * | DominanceInfoNode::const_iterator | None | 1 |
| ++ | DominanceInfoNode::const_iterator | None | 1 |
| & | ScopedHTType | None | 1 |
| || | WitnessMethodInst | ApplyInst | 1 |
| || | bool | WitnessMethodInst | 1 |
| || | ApplyInst | ApplyInst | 1 |
| * | EndAccessInst | None | 1 |
| * | DominanceInfo | None | 1 |
| * | std::optional<ValueRelation> | None | 1 |
| && | bool | unsigned | 1 |
| != | SILBasicBlock::iterator | TermInst | 1 |
| && | EnumElementDecl | string literal | 1 |
| && | bool | SILBasicBlock | 1 |
| ! | SwitchEnumInst | None | 1 |
| * | SwitchEnumInst | None | 1 |
| && | SILBasicBlock | bool | 1 |
| && | DomTreeNode | string literal | 1 |
| & | BBEnumTagDataflowState | None | 1 |
| ! | ShortestPathAnalysis | None | 1 |
| / | long double | long double | 1 |
| / | int | uint64_t | 1 |
| && | AllocStackInst | string literal | 1 |
| && | std::optional<SILDebugVariable> | string literal | 1 |
| ! | std::optional<int> | None | 1 |
| ! | StringLiteralInst | None | 1 |
| ! | GlobalAddrInst | None | 1 |
| * | SILTransform | None | 1 |
| & | NullablePtr<llvm::SmallPtrSet<SILBasicBlock *, 4>> | None | 1 |
| & | LoopARCPairingContext | None | 1 |
| * | llvm::ManagedStatic<std::vector<unsigned>> | None | 1 |
| > | llvm::cl::opt<unsigned> | integer literal | 1 |
| ++ | SwiftInt | None | 1 |
| ! | BridgedUtilities::VerifyFunctionFn | None | 1 |
| >> | llvm::yaml::Input | std::vector<YAMLPassPipeline> | 1 |
| < | uint64_t | std::optional<uint64_t> | 1 |
| * | SILArgument | None | 1 |
| * | ApplyInst * | None | 1 |
| || | bool | SILBasicBlock | 1 |
| != | llvm::df_iterator<DominanceInfoNode *> | llvm::df_iterator<DominanceInfoNode *> | 1 |
| ++ | llvm::df_iterator<DominanceInfoNode *> | None | 1 |
| & | SmallVector<SingleValueInstruction *, 4> | None | 1 |
| ! | std::optional<SmallVector<SILBasicBlock *, 8>> | None | 1 |
| * | std::optional<SmallVector<SILBasicBlock *, 8>> | None | 1 |
| < | int | llvm::cl::opt<int> | 1 |
| & | CallerAnalysis::FunctionInfo | None | 1 |
| > | unsigned const | integer literal | 1 |
| - | unsigned long | integer literal | 1 |
| && | SILLoopAnalysis | string literal | 1 |
| && | SILLoopInfo | string literal | 1 |
| >= | int | llvm::cl::opt<int> | 1 |
| - | unsigned | int | 1 |
| & | Entry | None | 1 |
| * | Entry | None | 1 |
| ! | std::unique_ptr<ClosureInfo> | None | 1 |
| * | ArraySemanticsCall | None | 1 |
| != | unsigned long | unsigned long | 1 |
| || | BuiltinInst | SILArgument | 1 |
| ! | SILArgument | None | 1 |
| ! | IntegerLiteralInst | None | 1 |
| * | LoopRegion | None | 1 |
| * | LoopRegion::subregion_iterator | None | 1 |
| * | LoopRegion::backedge_iterator | None | 1 |
| ++ | LoopRegion::subregion_iterator | None | 1 |
| ++ | SuccIterTy | None | 1 |
| ++ | LoopRegion::backedge_iterator | None | 1 |
| ++ | alledge_iterator | None | 1 |
| & | LoopRegionFunctionInfoGrapherWrapper | None | 1 |
| ! | DomTreeNode | None | 1 |
| ! | std::optional<SILType> | None | 1 |
| * | std::optional<Partition> | None | 1 |
| & | AccessStorageResult | None | 1 |
| ! | StorageAccessInfo | None | 1 |
| ! | BridgedCalleeAnalysis::IsDeinitBarrierFn | None | 1 |
| && | SILPassManager | string literal | 1 |
| || | SILValue | unsigned | 1 |
| && | value_type | string literal | 1 |
| * | ValueStorage | None | 1 |
| && | std::optional<BorrowedValue> | string literal | 1 |
| ! | std::optional<BorrowedValue> | None | 1 |
| & | ProjectedValues | None | 1 |
| & | SmallVector<SILValue, 2> | None | 1 |
| + | SubElementOffset | TypeSubElementCount | 1 |
| ! | SwitchEnumTermInst | None | 1 |
| ! | SwitchStmt | None | 1 |
| && | SILLocation | Type | 1 |
| ! | SILLocation | None | 1 |
| ! | std::optional<Allocator> | None | 1 |
| * | std::optional<Allocator> | None | 1 |
| ! | PostOrderFunctionInfo | None | 1 |
| * | DebugValueInst | None | 1 |
| & | OSSACanonicalizer | None | 1 |
| ! | SingleValueInstruction | None | 1 |
| != | SILFunction | SILFunction | 1 |
| & | std::optional<StorageMap> | None | 1 |
| * | std::optional<StorageMap> | None | 1 |
| & | SmallVector<SILInstruction *, 4> | None | 1 |
| != | DIKind | DIKind | 1 |
| && | FuncDecl | bool | 1 |
| && | SILInstruction | ApplyInst | 1 |
| && | ApplyInst | MethodInst | 1 |
| ! | EndBorrowInst | None | 1 |
| * | std::optional<DIKind> | None | 1 |
| * | MarkUnresolvedNonCopyableValueInst | None | 1 |
| && | CopyAddrInst | string literal | 1 |
| * | CopyAddrInst | None | 1 |
| & | SmallVector<SILInstruction *, 8> | None | 1 |
| && | MarkUnresolvedMoveAddrInst | string literal | 1 |
| ! | MarkUnresolvedMoveAddrInst | None | 1 |
| & | SmallPtrSet<SILInstruction *, 8> | None | 1 |
| ! | KeyPathInst | None | 1 |
| * | EndApplyInst | None | 1 |
| ! | BuiltinIntegerType | None | 1 |
| || | InitExistentialAddrInst | bool | 1 |
| || | EnumElementDecl | SILType | 1 |
| && | InitExistentialAddrInst | OpenExistentialAddrInst | 1 |
| ! | OpenExistentialAddrInst | None | 1 |
| * | InitExistentialAddrInst | None | 1 |
| || | InitEnumDataAddrInst | InjectEnumAddrInst | 1 |
| == | InjectEnumAddrInst | InjectEnumAddrInst | 1 |
| == | SILInstruction | InitEnumDataAddrInst | 1 |
| * | InitEnumDataAddrInst | None | 1 |
| * | FixLifetimeInst | None | 1 |
| * | EndCOWMutationInst | None | 1 |
| * | UncheckedRefCastAddrInst | None | 1 |
| * | UnconditionalCheckedCastAddrInst | None | 1 |
| * | ThickToObjCMetatypeInst | None | 1 |
| * | ObjCToThickMetatypeInst | None | 1 |
| * | CheckedCastAddrBranchInst | None | 1 |
| ! | OwnershipRAUWHelper | None | 1 |
| == | IsZeroKind | IsZeroKind | 1 |
| && | OwnershipRAUWHelper | string literal | 1 |
| != | MetatypeInst | MetatypeInst | 1 |
| ! | std::optional<RefactorAvailabilityInfo> | None | 1 |
| * | std::optional<RefactorAvailabilityInfo> | None | 1 |
| ! | std::optional<RenameInfo> | None | 1 |
| ! | PatternBindingDecl | None | 1 |
| ! | NumberLiteralExpr | None | 1 |
| ! | GuardStmt | None | 1 |
| ! | CallExpr | None | 1 |
| ! | std::optional<ConditionPath> | None | 1 |
| && | std::optional<ConditionPath> | string literal | 1 |
| != | size_t | unsigned | 1 |
| || | std::optional<SILValue> | std::optional<AccessBase::Kind> | 1 |
| && | DominanceInfo | SILLoopInfo | 1 |
| == | SILLoop | SILLoop | 1 |
| ! | ProjectionTreeNode | None | 1 |
| ! | SwiftMetatype | None | 1 |
| ! | InitBlockStorageHeaderInst | None | 1 |
| * | llvm::Expected<std::unique_ptr<llvm::remarks::RemarkSerializer>> | None | 1 |
| & | Location | None | 1 |
| * | SILDebugScope | None | 1 |
| & | FilenameAndLocation | None | 1 |
| ! | IsTypeExpansionSensitive_t | None | 1 |
| ! | std::optional<CapturedValue> | None | 1 |
| & | std::optional<std::pair<SILValue, SILValue>> | None | 1 |
| * | std::optional<std::pair<SILValue, SILValue>> | None | 1 |
| && | ProtocolConformance | string literal | 1 |
| & | SILFunctionTraceFormatter | None | 1 |
| ! | BridgedFunction::GetEffectInfoFn | None | 1 |
| ! | BridgedFunction::GetMemBehaviorFn | None | 1 |
| ! | BridgedFunction::ArgumentMayReadFn | None | 1 |
| ! | std::optional<SourceLoc> | None | 1 |
| && | std::optional<SourceLoc> | std::optional<SourceLoc> | 1 |
| != | std::optional<SourceLoc> | std::optional<SourceLoc> | 1 |
| && | std::optional<CounterExpr> | string literal | 1 |
| ! | std::optional<CounterExpr> | None | 1 |
| ! | std::optional<SILLocation> | None | 1 |
| ! | std::optional<SILDeclRef> | None | 1 |
| ! | std::optional<FunctionType::ExtInfo> | None | 1 |
| ! | swift::Decl | None | 1 |
| + | string literal | SmallString<32> | 1 |
| && | Entry | string literal | 1 |
| & | CalleeCache | None | 1 |
| & | std::function<void(Operand *)> | None | 1 |
| < | unsigned long | unsigned long long | 1 |
| + | unsigned long | integer literal | 1 |
| - | unsigned long long | None | 1 |
| * | std::optional<InstructionContext> | None | 1 |
| & | SILParserState | None | 1 |
| * | AvailabilityContext | None | 1 |
| || | SILFunction | SILFunction | 1 |
| | | unsigned char | unsigned | 1 |
| ! | std::optional<LoadOwnershipQualifier> | None | 1 |
| ! | std::optional<MarkDependenceKind> | None | 1 |
| ! | std::optional<StoreOwnershipQualifier> | None | 1 |
| ! | std::optional<AssignOwnershipQualifier> | None | 1 |
| * | std::optional<UnresolvedValueName> | None | 1 |
| & | IsThunk_t | None | 1 |
| & | IsDynamicallyReplaceable_t | None | 1 |
| & | IsDistributed_t | None | 1 |
| & | IsRuntimeAccessible_t | None | 1 |
| & | ForceEnableLexicalLifetimes_t | None | 1 |
| & | UseStackForPackMetadata_t | None | 1 |
| & | IsExactSelfClass_t | None | 1 |
| & | Identifier | None | 1 |
| & | SILFunction::Purpose | None | 1 |
| & | Inline_t | None | 1 |
| & | OptimizationMode | None | 1 |
| & | PerformanceConstraints | None | 1 |
| & | SmallVector<std::string, 1> | None | 1 |
| & | SmallVector<ParsedSpecAttr, 4> | None | 1 |
| & | EffectsKind | None | 1 |
| && | SILWitnessTable | RootProtocolConformance | 1 |
| ! | RootProtocolConformance | None | 1 |
| + | intptr_t | intptr_t | 1 |
| ! | MachOFile | None | 1 |
| sizeof | T | None | 1 |
| - | int64_t | int64_t | 1 |
| && | Initializer | string literal | 1 |
| ! | SourceLoc | None | 1 |
| * | std::optional<SyntacticElementContext> | None | 1 |
| ! | std::optional<ObjCReason> | None | 1 |
| ! | std::optional<ObjCSelector> | None | 1 |
| && | SourceFile | bool | 1 |
| == | SourceFile | SourceFile | 1 |
| ! | GenericContext | None | 1 |
| == | Context | Context | 1 |
| ~ | unsigned(TypeResolutionFlags::DirectEscaping) | None | 1 |
| && | ParamDecl | bool | 1 |
| && | EnumElementDecl | VarDecl | 1 |
| && | TupleType | bool | 1 |
| * | CheckedCastKind | None | 1 |
| & | bool | bool | 1 |
| ! | AbstractClosureExpr | None | 1 |
| ! | std::optional<InFlightDiagnostic> | None | 1 |
| ! | AvailabilityContext | None | 1 |
| % | size_t | size_t | 1 |
| && | StructDecl | string literal | 1 |
| < | bool | int | 1 |
| && | AssociatedTypeDecl | Type | 1 |
| & | InferredAssociatedTypesByWitnesses | None | 1 |
| ! | ShouldRecurse_t | None | 1 |
| * | Expr | None | 1 |
| && | ConstraintLocator | string literal | 1 |
| * | std::optional<Requirement> | None | 1 |
| ! | SuperRefExpr | None | 1 |
| != | DeclName | DeclName | 1 |
| * | std::optional<OverloadChoice> | None | 1 |
| * | std::optional<Binding> | None | 1 |
| * | Added<Expr *> | None | 1 |
| ! | std::optional<DeclNameRef> | None | 1 |
| * | std::optional<DeclNameRef> | None | 1 |
| ! | CustomAttr | None | 1 |
| && | bool | FuncDecl | 1 |
| && | ValueDecl | ValueDecl | 1 |
| || | Initializer | Expr | 1 |
| ! | Initializer | None | 1 |
| ! | std::optional<Score> | None | 1 |
| ! | std::unique_ptr<Scope> | None | 1 |
| ! | SILTypeResolutionContext::OpenedPackElement | None | 1 |
| ! | AttributedTypeRepr | None | 1 |
| && | ProtocolConformanceRef | string literal | 1 |
| * | std::optional<LifetimeDependenceInfo> | None | 1 |
| & | std::optional<TypeAttrSet> | None | 1 |
| * | std::optional<TypeAttrSet> | None | 1 |
| ! | ExistentialMetatypeType | None | 1 |
| ! | std::optional<ImplicitlyFinalReason> | None | 1 |
| + | APInt | integer literal | 1 |
| * | std::optional<AutomaticEnumValueKind> | None | 1 |
| && | LiteralExpr | string literal | 1 |
| ! | NullablePtr<OperatorDecl> | None | 1 |
| && | Type | ProtocolDecl | 1 |
| & | SmallVector<TypeVariableType *, 2> | None | 1 |
| == | ValueDecl | ValueDecl | 1 |
| ! | AvailabilitySpec | None | 1 |
| ! | PlatformVersionConstraintAvailabilitySpec | None | 1 |
| & | TypeRefinementContext | None | 1 |
| + | std::string | StringRef | 1 |
| >= | unsigned | size_t | 1 |
| * | std::optional<Diag<StringRef, llvm::VersionTuple>> | None | 1 |
| || | Expr | Expr | 1 |
| != | BraceStmt | Stmt | 1 |
| && | VarDecl | VarDecl | 1 |
| ! | std::optional<EnclosingSelfPropertyWrapperAccess> | None | 1 |
| && | DeclContext | Type | 1 |
| & | OpenedTypeMap | None | 1 |
| + | Attempt | integer literal | 1 |
| || | OptionSet<MissingFlags> | bool | 1 |
| ! | TrailingWhereClause | None | 1 |
| && | bool | ProtocolConformance | 1 |
| ! | std::optional<ProtocolConformance *> | None | 1 |
| && | OpenedArchetypeType | string literal | 1 |
| && | bool | InOutExpr | 1 |
| ! | InOutExpr | None | 1 |
| && | AbstractFunctionDecl | string literal | 1 |
| * | Type | None | 1 |
| * | std::optional<Diag<>> | None | 1 |
| ! | DiagnosticEngine | None | 1 |
| || | ValueDecl | AvailableAttr | 1 |
| != | Version | Version | 1 |
| && | AnyFunctionType | string literal | 1 |
| + | std::optional<unsigned> | integer literal | 1 |
| == | SmallVector<ParamBinding, 4> | SmallVector<ParamBinding, 4> | 1 |
| ! | std::unique_ptr<ArgumentFailureTracker> | None | 1 |
| * | std::unique_ptr<ArgumentFailureTracker> | None | 1 |
| * | std::optional<TypeBase *> | None | 1 |
| ! | ConstraintFix | None | 1 |
| & | Type | None | 1 |
| == | PointerTypeKind | PointerTypeKind | 1 |
| && | ParameterList | ParameterList | 1 |
| && | ASTNode | ParameterList | 1 |
| * | ASTNode | None | 1 |
| && | bool | std::optional<KeyPathCapability> | 1 |
| ! | std::optional<KeyPathCapability> | None | 1 |
| * | std::optional<KeyPathCapability> | None | 1 |
| ! | std::optional<BindingSet> | None | 1 |
| * | std::optional<BindingSet> | None | 1 |
| * | std::optional<Argument> | None | 1 |
| ! | TupleTypeRepr | None | 1 |
| && | bool | PatternBindingDecl | 1 |
| ! | std::optional<ContextualTypePurpose> | None | 1 |
| * | std::optional<ContextualTypePurpose> | None | 1 |
| < | GenericParamKey | GenericParamKey | 1 |
| == | GenericParamKey | GenericParamKey | 1 |
| && | RememberChoice_t | string literal | 1 |
| ! | RememberChoice_t | None | 1 |
| * | std::optional<TrailingClosureMatching> | None | 1 |
| * | std::optional<AccessScope> | None | 1 |
| ! | UnsupportedElt | None | 1 |
| ! | NullablePtr<Stmt> | None | 1 |
| && | bool | EnumDecl | 1 |
| ! | clang::RecordDecl | None | 1 |
| == | unsigned | std::optional<unsigned> | 1 |
| ! | std::optional<AccessorInfo> | None | 1 |
| ! | clang::ObjCPropertyDecl | None | 1 |
| || | clang::ObjCPropertyDecl | bool | 1 |
| && | std::optional<AccessorInfo> | bool | 1 |
| && | bool | ClassDecl | 1 |
| && | bool | VarDecl | 1 |
| != | DeclContext | DeclContext | 1 |
| ! | clang::ObjCProtocolDecl | None | 1 |
| && | SubscriptDecl | bool | 1 |
| && | FuncDecl | SubscriptDecl | 1 |
| == | FuncDecl | Decl | 1 |
| ! | clang::ObjCInterfaceDecl | None | 1 |
| && | std::optional<ImportedName> | string literal | 1 |
| ! | std::optional<ImportedName> | None | 1 |
| * | std::optional<CtorInitializerKind> | None | 1 |
| ! | std::optional<const clang::SwiftAttrAttr *> | None | 1 |
| != | clang::NamedDecl::attr_iterator | clang::NamedDecl::attr_iterator | 1 |
| ++ | clang::NamedDecl::attr_iterator | None | 1 |
| && | clang::ObjCInterfaceDecl | string literal | 1 |
| & | ClangDeclTraceFormatter | None | 1 |
| * | clang::ObjCProtocolList | None | 1 |
| ! | clang::EnumExtensibilityAttr | None | 1 |
| + | const char * | integer literal | 1 |
| ! | std::unique_ptr<SerializedBaseNameToEntitiesTable> | None | 1 |
| && | bool | clang::ModuleMacro | 1 |
| ! | clang::ModuleMacro | None | 1 |
| ! | clang::MacroDirective | None | 1 |
| * | std::unique_ptr<SwiftLookupTable> | None | 1 |
| * | std::unique_ptr<llvm::PrefixMapper> | None | 1 |
| / | llvm::StringLiteral | llvm::StringLiteral | 1 |
| * | llvm::StringLiteral | None | 1 |
| + | llvm::StringLiteral | size_t | 1 |
| * | ClangImporter::Implementation | None | 1 |
| || | std::optional<ForeignAsyncConvention> | std::optional<ForeignErrorConvention> | 1 |
| ! | StableSerializationPath | None | 1 |
| && | clang::NamedDecl | string literal | 1 |
| == | std::optional<AnySwiftNameAttr> | std::optional<AnySwiftNameAttr> | 1 |
| + | llvm::APSInt | llvm::APSInt | 1 |
| - | llvm::APSInt | llvm::APSInt | 1 |
| * | llvm::APSInt | llvm::APSInt | 1 |
| == | llvm::APSInt | integer literal | 1 |
| / | llvm::APSInt | llvm::APSInt | 1 |
| | | llvm::APSInt | llvm::APSInt | 1 |
| & | llvm::APSInt | llvm::APSInt | 1 |
| ^ | llvm::APSInt | llvm::APSInt | 1 |
| == | llvm::APSInt | llvm::APSInt | 1 |
| < | llvm::APSInt | llvm::APSInt | 1 |
| <= | llvm::APSInt | llvm::APSInt | 1 |
| > | llvm::APSInt | llvm::APSInt | 1 |
| >= | llvm::APSInt | llvm::APSInt | 1 |
| ! | clang::MacroInfo | None | 1 |
| & | PCHDeserializationCallbacks | None | 1 |
| * | llvm::IntrusiveRefCntPtr<clang::DiagnosticOptions> | None | 1 |
| * | std::unique_ptr<ClangImporter> | None | 1 |
| * | std::optional<llvm::cas::ObjectRef> | None | 1 |
| ! | llvm::Expected<clang::FileEntryRef> | None | 1 |
| * | llvm::Expected<clang::FileEntryRef> | None | 1 |
| ! | clang::OptionalFileEntryRef | None | 1 |
| != | clang::OptionalFileEntryRef | clang::FileEntryRef | 1 |
| * | clang::OptionalFileEntryRef | None | 1 |
| != | clang::Module | clang::Module | 1 |
| || | ModuleDecl | bool | 1 |
| & | ClangImporter | None | 1 |
| ! | clang::CXXMethodDecl | None | 1 |
| * | OptionalEnum<AccessorKind> | None | 1 |
| && | std::optional<clang::Module *> | string literal | 1 |
| * | std::optional<clang::Module *> | None | 1 |
| ! | std::optional<llvm::iterator_range<WordIterator>> | None | 1 |
| == | Words::iterator | string literal | 1 |
| * | Words::iterator | None | 1 |
| * | StringRef | None | 1 |
| & | struct rusage_info_v4 | None | 1 |
| == | int64_t | integer literal | 1 |
| && | UnifiedStatsReporter::TraceFormatter | void | 1 |
| & | malloc_statistics_t | None | 1 |
| << | raw_fd_ostream | string literal | 1 |
| & | pid_t | None | 1 |
| sizeof | STARTUPINFO | None | 1 |
| ! | llvm::ErrorOr<std::wstring> | None | 1 |
| & | STARTUPINFO | None | 1 |
| & | PROCESS_INFORMATION | None | 1 |
| ++ | ProcessId | None | 1 |
| < | llvm::UTF8 | llvm::UTF8 | 1 |
| * | llvm::UTF8 | None | 1 |
| * | ::UUID * | None | 1 |
| & | RPC_CSTR | None | 1 |
| & | RPC_STATUS | None | 1 |
| << | llvm::raw_ostream | llvm::SmallString<UUID::StringBufferSize> | 1 |
| + | std::size_t | std::size_t | 1 |
| * | TypeToPathMap | None | 1 |
| ! | llvm::yaml::MappingNode | None | 1 |
| & | DWORD | None | 1 |
| ! | BOOL | None | 1 |
| != | DWORD | integer literal | 1 |
| & | DWORD | integer literal (suffix U) | 1 |
| & | DWORD | float literal (suffix FF) | 1 |
| & | DWORD | float literal (suffix FFFFFFF) | 1 |
| & | int | integer literal | 1 |
| ! | std::optional<std::vector<int>> | None | 1 |
| * | std::optional<std::vector<int>> | None | 1 |
| ~ | short | None | 1 |
| & | cache_attributes_t | None | 1 |
| & | cache_t | None | 1 |
| * | std::unique_ptr<Lowering::TypeConverter> | None | 1 |
| & | llvm::ModuleAnalysisManager | None | 1 |
| & | llvm::PassInstrumentationCallbacks | None | 1 |
| * | llvm::Expected<llvm::StringRef> | None | 1 |
| ! | std::unique_ptr<sys::TaskQueue> | None | 1 |
| + | wchar_t | int | 1 |
| * | std::unique_ptr<DiagnosticConsumer> | None | 1 |
| * | std::optional<ValueRefCntPtr> | None | 1 |
| * | std::optional<IndentContext> | None | 1 |
| >= | size_t | size_t | 1 |
| ! | std::optional<TrailingInfo> | None | 1 |
| ++ | ArrayRef<Token>::iterator | None | 1 |
| * | APIDiffItem | None | 1 |
| & | UnresolvedDeclRefExpr | None | 1 |
| >= | llvm::VersionTuple | llvm::VersionTuple | 1 |
| ! | std::optional<Type> | None | 1 |
| & | USRBasedTypeContext | None | 1 |
| ! | ArchetypeType | None | 1 |
| & | CursorInfoTypeCheckSolutionCallback | None | 1 |
| / | integer literal | float literal | 1 |
| + | unsigned | double | 1 |
| < | double | double | 1 |
| == | Expr | Expr | 1 |
| & | SymbolGraph | None | 1 |
| & | SmallPtrSet<const Decl*, 8> | None | 1 |
| < | SmallString<256> | SmallString<256> | 1 |
| ! | std::unique_ptr<Compilation> | None | 1 |
| & | std::optional<OutputFileMap> | None | 1 |
| * | std::optional<OutputFileMap> | None | 1 |
| && | std::unique_ptr<InputArgList> | string literal | 1 |
| * | DerivedArgList | None | 1 |
| * | llvm::Expected<OutputFileMap> | None | 1 |
| & | ToolChain | None | 1 |
| ! | llvm::Expected<file_types::ID> | None | 1 |
| + | string literal | llvm::Twine | 1 |
| << | llvm::raw_fd_ostream | string literal | 1 |
| * | CxxDeclEmissionScope | None | 1 |
| == | bool | bool literal | 1 |
| != | SmallVector<StringRef, 8> | SmallVector<StringRef, 8> | 1 |
| && | llvm::ErrorOr<std::string> | string literal | 1 |
| ++ | Index | None | 1 |
| != | Index | Index | 1 |
| == | SymbolicP | integer literal | 1 |
| & | SymbolicP | None | 1 |
| - | SymbolicP | integer literal | 1 |
| * | std::optional<IRABIDetailsProvider::SizeAndAlignment> | None | 1 |
| ! | std::optional<IRABIDetailsProvider::MethodDispatchInfo> | None | 1 |
| -- | ssize_t | None | 1 |
| ! | std::optional<CancellableBacktrackingScope> | None | 1 |
| ! | std::optional<TuplePatternElt> | None | 1 |
| * | std::optional<TuplePatternElt> | None | 1 |
| <= | unsigned char | integer literal | 1 |
| >> | unsigned char | unsigned char | 1 |
| << | unsigned char | unsigned char | 1 |
| != | unsigned char | unsigned char | 1 |
| <= | unsigned | float literal (suffix FFF) | 1 |
| >= | signed char | integer literal | 1 |
| == | unsigned | char literal | 1 |
| ! | std::optional<EditorPlaceholderData> | None | 1 |
| & | ConsumeTokenReceiver | None | 1 |
| + | string literal | Identifier | 1 |
| + | Identifier | string literal | 1 |
| * | std::optional<PlatformKind> | None | 1 |
| ! | std::optional<AccessLevel> | None | 1 |
| + | uint8_t | uint8_t | 1 |
| * | std::optional<IsolatedTypeAttr::IsolationKind> | None | 1 |
| || | VarDecl | bool | 1 |
| ! | TopLevelCodeDecl | None | 1 |
| ! | PatternBindingInitializer | None | 1 |
| & | SmallVector<Identifier, 4> | None | 1 |
| & | SmallVector<Identifier, 2> | None | 1 |
| ! | std::optional<Parser::BacktrackingScope> | None | 1 |
| && | ASTNode | string literal | 1 |
| & | DiagnosticHelper | None | 1 |
| && | ValueBase | string literal | 1 |
| ! | llvm::Expected<SILFunction *> | None | 1 |
| || | bool | GenericEnvironment | 1 |
| ! | TypeID | None | 1 |
| ! | ValueID | None | 1 |
| & | unsigned | float literal (suffix FF) | 1 |
| == | ValueID | integer literal | 1 |
| && | SILWitnessTable | string literal | 1 |
| && | SILDefaultWitnessTable | string literal | 1 |
| != | int32_t | integer literal | 1 |
| ! | std::unique_ptr<llvm::ErrorInfoBase> | None | 1 |
| * | std::unique_ptr<llvm::ErrorInfoBase> | None | 1 |
| && | std::error_code | bool | 1 |
| ! | llvm::ErrorOr<llvm::vfs::Status> | None | 1 |
| * | std::optional<SerializedModuleBaseName> | None | 1 |
| * | std::unique_ptr<ModuleFile> | None | 1 |
| & | SmallString<256> | None | 1 |
| * | SILGlobalVariable | None | 1 |
| != | ValueID | integer literal | 1 |
| + | unsigned(BAI->hasNoNestedConflict()) | None | 1 |
| * | std::optional<ModuleDependencyInfo> | None | 1 |
| != | IdentifierID | integer literal | 1 |
| * | Expected<unsigned> | None | 1 |
| & | ExtendedValidationInfo | None | 1 |
| != | Decl | NominalTypeDecl | 1 |
| ! | std::unique_ptr<SerializedDeclMembersTable> | None | 1 |
| != | version::Version | version::Version | 1 |
| * | std::optional<ValueDecl*> | None | 1 |
| * | DeclAttribute | None | 1 |
| * | std::optional<BuiltinMacroKind> | None | 1 |
| > | IdentifierID | integer literal | 1 |
| < | unsigned | uint64_t | 1 |
| > | SILLayoutID | integer literal | 1 |
| - | SILLayoutID | integer literal | 1 |
| && | ValueDecl | bool | 1 |
| * | llvm::yaml::SequenceNode | None | 1 |
| & | stack_t | None | 1 |
| >= | intptr_t | integer literal | 1 |
| sizeof | intptr_t | None | 1 |
| sizeof | MEMORY_BASIC_INFORMATION | None | 1 |
| & | std::optional<DiagnosticEngine> | None | 1 |
| * | std::optional<DiagnosticEngine> | None | 1 |
| - | integer literal (suffix U) | integer literal | 1 |
| + | string literal | llvm::StringRef | 1 |
| - | const char * | const char * | 1 |
| ! | std::unique_ptr<DiagnosticSerializer> | None | 1 |
| * | std::unique_ptr<DiagnosticSerializer> | None | 1 |
| * | std::unique_ptr<llvm::raw_fd_ostream> | None | 1 |
| ! | std::optional<FrontendInputsAndOutputs> | None | 1 |
| << | llvm::raw_fd_ostream | std::string | 1 |
| * | std::optional<DiagnosticKind> | None | 1 |
| >> | llvm::yaml::Input | ForwardingModule | 1 |
| && | std::unique_ptr<llvm::MemoryBuffer> | string literal | 1 |
| & | CompilerInstance | None | 1 |
| & | NullDiagnosticConsumer | None | 1 |
| ! | std::optional<std::set<StringRef>> | None | 1 |
| * | std::optional<std::set<StringRef>> | None | 1 |
| ! | std::unique_ptr<ClangImporter> | None | 1 |
| ! | std::optional<IRGenLLVMLTOKind> | None | 1 |
| * | std::optional<DestroyHoistingOption> | None | 1 |
| ! | std::optional<swift::JITDebugArtifact> | None | 1 |
| * | std::optional<swift::JITDebugArtifact> | None | 1 |
| != | ArgStringList::iterator | ArgStringList::iterator | 1 |
| ++ | ArgStringList::iterator | None | 1 |
| * | ArgStringList::iterator | None | 1 |
| & | serialization::ExtendedValidationInfo | None | 1 |
| && | std::optional<OutputEntry> | string literal | 1 |
| & | llvm::SmallSet<StringRef, 4> | None | 1 |
| ! | ObjectFile | None | 1 |
| > | uint64_t | float literal (suffix FFFFFFFFu) | 1 |
| -- | BasicBlock::iterator | None | 1 |
| != | Value | CallInst | 1 |
| * | Instruction | None | 1 |
| ! | ConstantInt | None | 1 |
| * | Module | None | 1 |
| == | std::vector<WeakTrackingVH>::iterator | std::vector<WeakTrackingVH>::iterator | 1 |
| * | Function | None | 1 |
| ! | Function | None | 1 |
| < | unsigned | cl::opt<unsigned> | 1 |
| == | cl::opt<unsigned> | integer literal | 1 |
| & | FunctionEntry | None | 1 |
| * | FunctionInfos::iterator | None | 1 |
| ! | ParamInfo | None | 1 |
| != | Constant | Constant | 1 |
| & | Argument | None | 1 |
| < | unsigned int | unsigned int | 1 |
| * | double | float literal | 1 |
| == | llvm::Value | llvm::Value | 1 |
| * | SymbolTracker | None | 1 |
| && | clang::serialization::ModuleFile | string literal | 1 |
| || | TypeRepr | Expr | 1 |
| ~ | SymbolRoleSet | None | 1 |
| * | ASTContext* | None | 1 |
| >> | llvm::yaml::Input | AccessNotesFile | 1 |
| >= | AccessLevel | AccessLevel | 1 |
| & | ParameterizedProtocolMap | None | 1 |
| && | FunctionType | string literal | 1 |
| >> | llvm::yaml::Input | OverlayFileContents | 1 |
| & | SourceFileTraceFormatter | None | 1 |
| << | BitWord | unsigned | 1 |
| << | BitWord | int | 1 |
| == | SuppressibleFeatureSet::iterator | SuppressibleFeatureSet::iterator | 1 |
| * | SuppressibleFeatureSet::iterator | None | 1 |
| ++ | SuppressibleFeatureSet::iterator | None | 1 |
| * | std::optional<SmallVector<CanType, 4>> | None | 1 |
| || | CanGenericSignature | bool | 1 |
| ! | std::optional<ClangTypeKind> | None | 1 |
| * | std::optional<ProtocolConformanceRef> | None | 1 |
| & | std::vector<ProtocolConformance *> | None | 1 |
| & | SmallVector<ConformanceDiagnostic, 4> | None | 1 |
| & | ProtocolConformanceTraceFormatter | None | 1 |
| & | TypeReprTraceFormatter | None | 1 |
| & | std::optional<TypePrinter> | None | 1 |
| * | std::optional<TypePrinter> | None | 1 |
| & | PatternTraceFormatter | None | 1 |
| == | enum {
        AnyErasure,
        ConcreteErasureOnly,
        ExistentialErasureOnly,
      } | bool literal | 1 |
| == | DeclContext | DeclContext | 1 |
| > | CtorInitializerKind | CtorInitializerKind | 1 |
| < | CtorInitializerKind | CtorInitializerKind | 1 |
| && | std::unique_ptr<ConstraintSolverArena> | string literal | 1 |
| * | std::unique_ptr<ConstraintSolverArena> | None | 1 |
| ! | StructType | None | 1 |
| & | ModuleLoader::ModuleVersionInfo | None | 1 |
| ! | LazyMemberLoader | None | 1 |
| && | AssociatedTypeDecl | string literal | 1 |
| ! | std::optional<ForeignRepresentationInfo> | None | 1 |
| * | std::optional<ForeignRepresentationInfo> | None | 1 |
| ! | std::optional<PropertyWrapperSynthesizedPropertyKind> | None | 1 |
| * | std::optional<PropertyWrapperSynthesizedPropertyKind> | None | 1 |
| & | CaptureInfoStorage | None | 1 |
| ! | BackDeployedAttr | None | 1 |
| <= | std::optional<llvm::VersionTuple> | llvm::VersionTuple | 1 |
| > | std::optional<llvm::VersionTuple> | llvm::VersionTuple | 1 |
| ! | NonSendableAttr | None | 1 |
| ! | std::optional<TypeAttrKind> | None | 1 |
| * | std::optional<TypeAttrKind> | None | 1 |
| == | ssize_t | integer literal | 1 |
| ! | OtherConstructorDeclRefExpr | None | 1 |
| ! | QualifiedIdentTypeRepr | None | 1 |
| & | ExprTraceFormatter | None | 1 |
| sizeof | StoredDiagnosticInfo | None | 1 |
| && | bool | DeclName | 1 |
| || | DeclName | bool | 1 |
| > | AccessLevel | AccessLevel | 1 |
| && | ClangNode | Type | 1 |
| & | DeclTraceFormatter | None | 1 |
| ! | LoadedFile | None | 1 |
| & | StmtTraceFormatter | None | 1 |
| * | std::optional<RequirementSignature> | None | 1 |
| ! | std::optional<std::pair<unsigned, unsigned>> | None | 1 |
| != | MutableTerm | MutableTerm | 1 |
| & | unsigned | float literal (suffix ffff) | 1 |
| * | int | None | 1 |
| && | std::optional<unsigned> | std::optional<unsigned> | 1 |
| != | std::set<DeclAttrKind> | std::set<DeclAttrKind> | 1 |
| != | std::set<TypeAttrKind> | std::set<TypeAttrKind> | 1 |
| ! | SDKNodeRoot | None | 1 |
| && | llvm::Constant | bool | 1 |
| & | ConformanceInfo | None | 1 |
| && | bool | OpaqueTypeArchetypeType | 1 |
| ! | OpaqueTypeArchetypeType | None | 1 |
| ! | ConformanceInfo | None | 1 |
| * | std::optional<PlaceholderPosition> | None | 1 |
| * | std::unique_ptr<const ProtocolInfo> | None | 1 |
| * | ConformanceInfo | None | 1 |
| * | uint64_t | uint64_t | 1 |
| == | unsigned | uint32_t | 1 |
| * | LoadableTypeInfo | None | 1 |
| * | ForeignFunctionInfo | None | 1 |
| && | HeapLayout | bool | 1 |
| * | HeapLayout | None | 1 |
| && | bool | llvm::Value | 1 |
| * | std::optional<FunctionPointer> | None | 1 |
| && | llvm::Value | bool | 1 |
| * | std::optional<llvm::Type *> | None | 1 |
| & | HeapLayout | None | 1 |
| & | APInt | APInt | 1 |
| ~ | integer literal (suffix UL) | None | 1 |
| * | llvm::fltSemantics | None | 1 |
| && | BuiltinInst | string literal | 1 |
| ! | DominanceResolverFunction | None | 1 |
| ! | StructLayout | None | 1 |
| != | Size::int_type | integer literal | 1 |
| == | Size::int_type | integer literal | 1 |
| < | Size::int_type | Size::int_type | 1 |
| ++ | Size::int_type | None | 1 |
| == | llvm::FunctionType | llvm::FunctionType | 1 |
| != | llvm::FunctionType | llvm::FunctionType | 1 |
| && | bool | ForDefinition_t | 1 |
| + | string literal | llvm::SmallString<64> | 1 |
| & | LazyConstantInitializer | None | 1 |
| * | std::optional<ConstantInitBuilder> | None | 1 |
| && | ConstantInit | string literal | 1 |
| & | llvm::UTF16 | None | 1 |
| * | llvm::UTF16 | None | 1 |
| * | Size::int_type | None | 1 |
| >= | int64_t | int64_t | 1 |
| / | unsigned | integer literal (suffix U) | 1 |
| && | llvm::Value | llvm::Value | 1 |
| == | Size | Size | 1 |
| != | ReferenceCounting | ReferenceCounting | 1 |
| << | integer literal (suffix u) | unsigned | 1 |
| == | llvm::BasicBlock | llvm::BasicBlock | 1 |
| ! | CanMetatypeType | None | 1 |
| && | std::optional<int64_t> | std::optional<int64_t> | 1 |
| * | std::optional<LoweredValue> | None | 1 |
| != | SILInstruction | unsigned | 1 |
| ++ | SILInstruction | None | 1 |
| - | APInt | int64_t | 1 |
| != | APInt | integer literal | 1 |
| & | MetadataDependencyCollector | None | 1 |
| ! | std::optional<TypeImportInfo<std::string>> | None | 1 |
| * | std::optional<TypeImportInfo<std::string>> | None | 1 |
| && | SILVTable | string literal | 1 |
| * | llvm::Constant | None | 1 |
| ! | std::optional<SILVTable::Entry> | None | 1 |
| & | ModuleAnalysisManager | None | 1 |
| & | PassInstrumentationCallbacks | None | 1 |
| ! | cl::opt<bool> | None | 1 |
| ! | std::optional<llvm::vfs::OutputFile> | None | 1 |
| ! | Target | None | 1 |
| ! | llvm::TargetMachine | None | 1 |
| * | IRGenerator | None | 1 |
| & | IRGenerator | None | 1 |
| & | llvm::sys::Mutex | None | 1 |
| * | std::optional<const FieldImpl *> | None | 1 |
| * | std::optional<llvm::function_ref<GetAddrOfEntityFn>> | None | 1 |
| * | std::optional<ArrayRef<SILType>> | None | 1 |
| ! | std::optional<ArrayRef<SILType>> | None | 1 |
| || | bool | std::optional<ArrayRef<SILType>> | 1 |
| > | Alignment | Alignment | 1 |
| * | ClassPair | None | 1 |
| && | ExtensionDecl | string literal | 1 |
| ! | ClassLayout | None | 1 |
| & | IsTriviallyDestroyable_t | IsTriviallyDestroyable_t | 1 |
| & | IsFixedSize_t | IsFixedSize_t | 1 |
| & | IsLoadable_t | IsLoadable_t | 1 |
| & | IsBitwiseTakable_t | IsBitwiseTakable_t | 1 |
| & | IsCopyable_t | IsCopyable_t | 1 |
| + | OperationCost | OperationCost | 1 |
| * | int_type | integer literal | 1 |
| != | int_type | integer literal | 1 |
| & | Size::int_type | Size::int_type | 1 |
| - | Size::int_type | None | 1 |
| >> | llvm::yaml::Input | std::vector<YAMLModuleNode> | 1 |
| * | FuncDecl | None | 1 |
| * | std::optional<ASTSourceDescriptor> | None | 1 |
| * | DebugTypeInfo | None | 1 |
| * | std::optional<DebugTypeInfo> | None | 1 |
| ! | llvm::DIType | None | 1 |
| != | unsigned | std::optional<uint64_t> | 1 |
| && | std::optional<uint64_t> | unsigned | 1 |
| > | std::optional<uint64_t> | integer literal | 1 |
| || | llvm::Constant | llvm::Type | 1 |
| ! | llvm::DIExpression | None | 1 |
| % | uint64_t | integer literal | 1 |
| / | uint64_t | integer literal | 1 |
| <= | Size | Size | 1 |
| < | Size | Size | 1 |
| && | clang::Decl | string literal | 1 |
| * | std::optional<NativeConventionSchema> | None | 1 |
| < | clang::CharUnits | clang::CharUnits | 1 |
| && | clang::FieldDecl | string literal | 1 |
| & | SignatureExpansionABIDetails | None | 1 |
| ! | std::optional<llvm::Value *> | None | 1 |
| * | std::optional<llvm::Value *> | None | 1 |
| ! | std::optional<AsyncContextLayout> | None | 1 |
| <= | size_t | integer literal | 1 |
| == | llvm::Type | llvm::Type | 1 |
| ! | llvm::PHINode | None | 1 |
| & | llvm::Function::arg_iterator | None | 1 |
| * | llvm::Function::arg_iterator | None | 1 |
| ++ | llvm::Function::arg_iterator | None | 1 |
| > | Size | Size | 1 |
| >= | Alignment | Alignment | 1 |
| <= | Alignment | Alignment | 1 |
| == | unsigned int | integer literal | 1 |
| == | Alignment::int_type | integer literal | 1 |
| * | std::optional<GenericRequirement> | None | 1 |
| * | std::optional<MetadataSource> | None | 1 |
| * | std::optional<SignatureExpansionABIDetails> | None | 1 |
| * | std::unique_ptr<std::map<std::string, InstallNameStore>> | None | 1 |
| && | IRGenModule | string literal | 1 |
| ! | std::optional<llvm::VersionTuple> | None | 1 |
| & | llvm::MD5::MD5Result | None | 1 |
| sizeof | llvm::MD5::MD5Result | None | 1 |
| == | PointerAuthInfo | PointerAuthInfo | 1 |
| ! | PointerAuthSchema | None | 1 |
| != | uintptr_t | integer literal | 1 |
| & | IRGenModule | None | 1 |
| & | KeyPathPatternComponent | None | 1 |
| ++ | std::atomic<int> | None | 1 |
| && | clang::ASTContext | string literal | 1 |
| * | clang::ASTContext | None | 1 |
| ! | CanArchetypeType | None | 1 |
| - | integer literal | int | 1 |
| & | llvm::SmallPtrSet<ProtocolDecl*, 4> | None | 1 |
| * | std::optional<Failure> | None | 1 |
| ! | std::unique_ptr<IRGenContext> | None | 1 |
| ! | RemoteAddress | None | 1 |
| & | signed_size_t | None | 1 |
| & | typename Runtime::StoredSize | None | 1 |
| <= | float | integer literal | 1 |
| % | int | integer literal | 1 |
| ++ | typename std::map<LinePtr, size_t>::const_iterator | None | 1 |
| < | typename string_t::const_pointer | typename string_t::const_pointer | 1 |
| + | size_t | int | 1 |
| / | short | integer literal | 1 |
| & | typename Diffs::iterator | None | 1 |
| + | string literal | string_t | 1 |
| + | string literal | typename string_t::const_pointer | 1 |
| == | short | integer literal | 1 |
| <= | int | short | 1 |
| << | integer literal | int | 1 |
| <= | double | double | 1 |
| + | int | short | 1 |
| <= | short | short | 1 |
| ++ | short | None | 1 |
| - | int | short | 1 |
| < | size_t | integer literal | 1 |
| sizeof | wchar_t | None | 1 |
| < | unsigned char | unsigned char | 1 |
| & | unsigned char | integer literal | 1 |
| != | typename string_t::iterator | typename string_t::iterator | 1 |
| >> | integer literal | integer literal | 1 |
| & | FixitApplyDiagnosticConsumer | None | 1 |
| ! | SpecialCaseDiffItem | None | 1 |
| ! | TypeMemberDiffItem | None | 1 |
| -- | uint8_t | None | 1 |
| ++ | Line | None | 1 |
| + | Line | integer literal | 1 |
| & | SILValue | None | 1 |
| & | ActivePackExpansion | None | 1 |
| & | std::optional<TemporaryInitialization> | None | 1 |
| * | std::optional<TemporaryInitialization> | None | 1 |
| * | std::optional<SmallVector<ManagedValue, 2>> | None | 1 |
| ! | std::optional<Callee> | None | 1 |
| && | ArgumentSource | string literal | 1 |
| ! | ArgumentSource | None | 1 |
| + | SILParameterInfo | unsigned | 1 |
| - | std::ptrdiff_t | std::ptrdiff_t | 1 |
| ! | ForceValueExpr | None | 1 |
| & | std::optional<ConvertingInitialization> | None | 1 |
| * | std::optional<ConvertingInitialization> | None | 1 |
| * | std::optional<CalleeTypeInfo> | None | 1 |
| * | SILLocation | None | 1 |
| & | ConvertingInitialization | None | 1 |
| ! | NormalProtocolConformance | None | 1 |
| && | SILDebuggerClient | string literal | 1 |
| & | BlackHoleInitialization | None | 1 |
| && | Pattern | string literal | 1 |
| & | PatternMatchContext | None | 1 |
| * | std::optional<R> | None | 1 |
| * | std::optional<FunctionInputGenerator> | None | 1 |
| ! | std::optional<FunctionInputGenerator> | None | 1 |
| ! | ast_scope::ASTScopeImpl | None | 1 |
| || | SILValue | std::optional<ForeignErrorConvention> | 1 |
| ! | std::optional<ForeignErrorConvention> | None | 1 |
| ! | CanSILFunctionType | None | 1 |
| || | std::optional<ForeignErrorConvention> | std::optional<ForeignAsyncConvention> | 1 |
| ! | std::unique_ptr<TemporaryInitialization> | None | 1 |
| + | integer literal | bool | 1 |
| & | std::unique_ptr<LogicalPathComponent> | None | 1 |
| * | std::unique_ptr<LogicalPathComponent> | None | 1 |
| * | LogicalPathComponent | None | 1 |
| ! | std::optional<SILAccessEnforcement> | None | 1 |
| & | PreparedArguments | None | 1 |
| == | llvm::SmallString<128> | llvm::SmallString<128> | 1 |
| & | clang::TextDiagnosticBuffer | None | 1 |
| * | llvm::IntrusiveRefCntPtr<clang::DiagnosticsEngine> | None | 1 |
| != | uint32_t | uint32_t | 1 |
| + | std::string | char | 1 |
| * | ModuleDependenciesCache | None | 1 |
| * | llvm::ErrorOr<swiftscan_dependency_graph_t> | None | 1 |
| && | ModuleDependencyInfo | string literal | 1 |
| + | uintptr_t | size_t | 1 |
| ! | NodeFactory | None | 1 |
| + | Slab | integer literal | 1 |
| + | T | uint32_t | 1 |
| & | TypeLookupError | None | 1 |
| ! | std::optional<typename T::ConventionType> | None | 1 |
| * | std::optional<typename T::ConventionType> | None | 1 |
| * | Demangle::NodePointer | None | 1 |
| ! | ActorInstance | None | 1 |
| & | SILIsolationInfo | None | 1 |
| && | SingleValueInstruction | SILValue | 1 |
| ! | std::optional<ConcreteExistentialInfo> | None | 1 |
| * | BitfieldRef<SSAPrunedLiveness> | None | 1 |
| ! | BitfieldRef<SSAPrunedLiveness> | None | 1 |
| != | SILNode | SILNode | 1 |
| && | SILOptScopeBase | SILValue | 1 |
| ! | SILSSAUpdater | None | 1 |
| && | SILSSAUpdater | string literal | 1 |
| * | std::optional<ClassListMap> | None | 1 |
| ! | std::optional<SILIsolationInfo> | None | 1 |
| * | std::optional<SILIsolationInfo> | None | 1 |
| ! | std::optional<SILAccessKind> | None | 1 |
| ! | std::unique_ptr<CalleeCache> | None | 1 |
| * | llvm::SmallVectorImpl<SubregionID>::const_iterator | None | 1 |
| * | llvm::SmallVectorImpl<std::pair<unsigned, unsigned>> | None | 1 |
| ++ | std::optional<InnerIterTy> | None | 1 |
| ++ | backedge_iterator | None | 1 |
| -- | std::optional<InnerIterTy> | None | 1 |
| -- | backedge_iterator | None | 1 |
| * | AdjointValueBase | None | 1 |
| + | AdjointValueBase | integer literal | 1 |
| * | DominanceInfoNode | None | 1 |
| | | RuntimeEffect | RuntimeEffect | 1 |
| - | UnderlyingType | integer literal | 1 |
| * | ValueBase | None | 1 |
| && | Operand | string literal | 1 |
| ~ | uint32_t | None | 1 |
| * | BitfieldContainer | None | 1 |
| & | BitfieldContainer | None | 1 |
| && | SILProfiler | string literal | 1 |
| & | NonSingleValueInstruction | None | 1 |
| & | SingleValueInstruction | None | 1 |
| && | ValueOwnershipKind | string literal | 1 |
| || | std::optional<EnumElementDecl *> | std::optional<EnumElementDecl *> | 1 |
| & | SILSuccessor | None | 1 |
| == | SubElementOffset | SubElementOffset | 1 |
| - | SubElementOffset | SubElementOffset | 1 |
| ! | std::optional<std::pair<unsigned, IsInterestingUser>> | None | 1 |
| ! | SmallVectorImpl<Operand *> | None | 1 |
| * | std::function<void(Operand *)> | None | 1 |
| ++ | BlockIterTy | None | 1 |
| * | BlockIterTy | None | 1 |
| * | Handler | None | 1 |
| & | llvm::SpecificBumpPtrAllocator<ProjectionTreeNode> | None | 1 |
| ! | OptionalSwiftObject | None | 1 |
| * | IteratorBase | None | 1 |
| != | IteratorBase | IteratorBase | 1 |
| ++ | IteratorT | None | 1 |
| * | IteratorT | None | 1 |
| & | InstListType | None | 1 |
| * | std::optional<SILLocation> | None | 1 |
| + | unsigned(replaceParamWithVoid) | None | 1 |
| + | SILFunction * const * | integer literal | 1 |
| << | int | integer literal | 1 |
| & | SILDIExprOperand | None | 1 |
| * | OwnerTy | None | 1 |
| & | SmallVector<SILInstruction*, N> | None | 1 |
| * | SILNode | None | 1 |
| == | unsigned | size_t | 1 |
| * | std::optional<SmallVector<SILBasicBlock *, 16>> | None | 1 |
| < | size_t | std::atomic<size_t> | 1 |
| & | typename std::aligned_storage<sizeof(ElemTy), alignof(ElemTy)>::type | None | 1 |
| + | ElemTy | size_t | 1 |
| & | RawType | RawType | 1 |
| & | ElemTy | None | 1 |
| << | integer literal (suffix UL) | size_t | 1 |
| ! | ElemTy | None | 1 |
| != | ElementStorage | ElementStorage | 1 |
| & | std::atomic<typename IndexStorage::RawType> | None | 1 |
| != | uint8_t | uint8_t | 1 |
| % | uint64_t | uint64_t | 1 |
| >= | size_t | uint64_t | 1 |
| > | size_t | uint64_t | 1 |
| * | std::optional<LocatorPathElt> | None | 1 |
| && | constraints::ConstraintGraphNode | string literal | 1 |
| ! | constraints::SavedTypeVariableBindings | None | 1 |
| * | constraints::SavedTypeVariableBindings | None | 1 |
| * | ConstraintSystem | None | 1 |
| ! | SolverState | None | 1 |
| == | std::size_t | integer literal | 1 |
| == | base_iterator | base_iterator | 1 |
| & | base_iterator | None | 1 |
| * | base_iterator | None | 1 |
| * | std::optional<std::pair<Key, std::optional<PairToSecondEltRange>>> | None | 1 |
| == | T | integer literal | 1 |
| != | T | integer literal | 1 |
| == | uintptr_t | uintptr_t | 1 |
| != | storage_type | integer literal | 1 |
| - | storage_type | integer literal | 1 |
| == | storage_type | storage_type | 1 |
| != | StorageType | integer literal | 1 |
| -- | Iterator | None | 1 |
| * | std::optional<IndexType> | None | 1 |
| & | struct Data {
    void *address;
    Arg1 &&arg1;

    static void init(void *context) {
      Data *data = static_cast<Data *>(context);
      ::new (data->address) T(static_cast<Arg1&&>(data->arg1));
    }
  } | None | 1 |
| * | Orig | None | 1 |
| - | uint8_t | uint64_t | 1 |
| == | uint64_t | uint8_t | 1 |
| ++ | uint8_t | None | 1 |
| * | unsigned | integer literal (suffix U) | 1 |
| != | std::size_t | std::size_t | 1 |
| == | intptr_t | intptr_t | 1 |
| ~ | Offset | None | 1 |
| ! | std::optional<APInt> | None | 1 |
| == | Node | Node | 1 |
| * | KeyType | None | 1 |
| & | KeyType | None | 1 |
| & | PtrSet | None | 1 |
| == | PtrSet | PtrSet | 1 |
| -- | std::atomic<unsigned> | None | 1 |
| - | difference_type | None | 1 |
| == | T | T | 1 |
| & | uintptr_t | float literal (suffix FF) | 1 |
| >= | size_t | uint16_t | 1 |
| ++ | Chunk | None | 1 |
| << | unsigned | unsigned | 1 |
| != | uintptr_t | uintptr_t | 1 |
| & | uintptr_t | unsigned | 1 |
| * | AllocatorPtr | None | 1 |
| & | USRBasedTypeArena | None | 1 |
| * | USRBasedTypeArena | None | 1 |
| sizeof | union {
    CodeCompletionDeclKind Decl;
    CodeCompletionLiteralKind Literal;
    CodeCompletionKeywordKind Keyword;
    uint8_t Opaque;
  } | None | 1 |
| && | CodeCompletionString | string literal | 1 |
| * | ResolvedLoc | None | 1 |
| * | std::vector<ResolvedLoc> | None | 1 |
| || | AnyFunctionType::Param | bool | 1 |
| && | PointerUnion<Type, const USRBasedType *> | string literal | 1 |
| ! | PointerUnion<Type, const USRBasedType *> | None | 1 |
| == | unsigned | StringRef | 1 |
| > | unsigned int | integer literal | 1 |
| && | ASTWalker | string literal | 1 |
| * | ASTWalker | None | 1 |
| * | std::unique_ptr<llvm::opt::OptTable> | None | 1 |
| * | std::unique_ptr<llvm::opt::DerivedArgList> | None | 1 |
| * | std::unique_ptr<CommandOutput> | None | 1 |
| < | Job::PID | integer literal | 1 |
| -- | Job::PID | None | 1 |
| ! | DoneParsingCallback | None | 1 |
| * | tls_key_t | None | 1 |
| & | tls_key_t | None | 1 |
| * | const Callable* | None | 1 |
| & | Callable | None | 1 |
| * | llvm::IntrusiveRefCntPtr<swift::cas::SwiftCASOutputBackend> | None | 1 |
| * | std::shared_ptr<llvm::cas::ObjectStore> | None | 1 |
| * | std::shared_ptr<llvm::cas::ActionCache> | None | 1 |
| <= | char literal | char | 1 |
| & | TargetValueWitnessTable<Runtime> | None | 1 |
| sizeof | TargetValueWitnessTable<Runtime> | None | 1 |
| - | std::string::size_type | std::string::size_type | 1 |
| + | std::string::size_type | integer literal | 1 |
| ! | ShapeRef | None | 1 |
| ! | BuiltGenericSignature | None | 1 |
| & | ExtendedExistentialTypeShapeFlags | None | 1 |
| & | ContextDescriptorFlags | None | 1 |
| sizeof | ContextDescriptorFlags | None | 1 |
| != | StoredPointer | StoredPointer | 1 |
| & | StoredPointer | StoredPointer | 1 |
| & | ExistentialTypeFlags::int_type | None | 1 |
| + | StoredPointer | ExistentialTypeFlags::int_type | 1 |
| sizeof | ExistentialTypeFlags::int_type | None | 1 |
| >= | uint32_t | integer literal | 1 |
| >= | StoredSize | integer literal | 1 |
| && | Demangle::NodePointer | Demangle::NodePointer | 1 |
| & | GenericRequirementLayoutKind | None | 1 |
| sizeof | GenericRequirementLayoutKind | None | 1 |
| sizeof | StoredPointer | None | 1 |
| ! | ContextDescriptorRef | None | 1 |
| ! | uint32_t | None | 1 |
| & | uint32_t | uint32_t | 1 |
| + | StoredPointer | uint32_t | 1 |
| & | StoredPointer | integer literal | 1 |
| ^ | StoredPointer | integer literal | 1 |
| >> | uint64_t | uint8_t | 1 |
| | | SymbolPropertySet | SymbolProperty | 1 |
| - | typename T::HeaderType* | integer literal | 1 |
| >> | uint16_t | integer literal | 1 |
| != | typename Runtime::StoredSize | integer literal | 1 |
| == | StorageType | integer literal | 1 |
| & | StorageType | uint16_t | 1 |
| ~ | uint16_t | None | 1 |
| != | typename TargetValueWitnessTypes<Runtime>::extraInhabitantCount | integer literal | 1 |
| && | BaseTy | string literal | 1 |
| | | DynamicCastFlags | DynamicCastFlags | 1 |
| | | ClassFlags | ClassFlags | 1 |
| << | float literal (suffix FU) | integer literal (suffix U) | 1 |
| | | ExclusivityFlags | ExclusivityFlags | 1 |
| | | StructLayoutFlags | StructLayoutFlags | 1 |
| | | ClassLayoutFlags | ClassLayoutFlags | 1 |
| | | EnumLayoutFlags | EnumLayoutFlags | 1 |
| >> | uint32_t | integer literal (suffix u) | 1 |
| & | uint32_t | float literal (suffix FFFFu) | 1 |
| == | uintptr_t | integer literal | 1 |
| + | uintptr_t | uintptr_t | 1 |
| ! | TypeOrExtensionDecl | None | 1 |
| != | Expr | integer literal | 1 |
| & | StmtCondition | None | 1 |
| * | UnifiedStatsReporter | None | 1 |
| & | DeclName | None | 1 |
| && | llvm::IntrusiveRefCntPtr<llvm::cas::CachingOnDiskFileSystem> | string literal | 1 |
| ! | llvm::IntrusiveRefCntPtr<llvm::cas::CachingOnDiskFileSystem> | None | 1 |
| ! | std::unique_ptr<llvm::TreePathPrefixMapper> | None | 1 |
| ! | DebuggerClient | None | 1 |
| ! | std::optional<std::vector<ASTNode>> | None | 1 |
| * | std::optional<std::vector<ASTNode>> | None | 1 |
| * | std::optional<ArrayRef<AttributedImport<ImportedModule>>> | None | 1 |
| && | TypeExpr | string literal | 1 |
| || | bool | OptionalTypePosition | 1 |
| >= | uint8_t | integer literal | 1 |
| * | T* | None | 1 |
| & | PerRequestCache | None | 1 |
| & | PerRequestReferences | None | 1 |
| ! | OptionSet<ParameterFlags> | None | 1 |
| == | MatchKind | std::optional<Requirement> | 1 |
| || | std::optional<ZeroArgDiagnostic> | SourceRange | 1 |
| ! | std::optional<ZeroArgDiagnostic> | None | 1 |
| && | TypeRepr | GenericParamList | 1 |
| & | PotentialMacroExpansions | None | 1 |
| || | Type | bool | 1 |
| & | std::function<hash_code(const void *)> | None | 1 |
| & | std::function<bool(const void *, const void *)> | None | 1 |
| & | std::function<void(const void *, llvm::raw_ostream &)> | None | 1 |
| & | std::function<SourceLoc(const void *)> | None | 1 |
| & | AnyRequestVTable | None | 1 |
| ! | std::function<bool (SymbolicReferent)> | None | 1 |
| && | VarDecl | std::optional<Error> | 1 |
| == | GenericSignatureImpl | integer literal | 1 |
| != | GenericSignatureImpl | integer literal | 1 |
| && | std::optional<AutoDiffDerivativeFunctionKind> | string literal | 1 |
| * | std::optional<AutoDiffDerivativeFunctionKind> | None | 1 |
| << | integer literal | size_t | 1 |
| == | unsigned long | integer literal | 1 |
| && | llvm::IntrusiveRefCntPtr<llvm::vfs::OutputBackend> | string literal | 1 |
| | | NLOptions | NLOptions | 1 |
| & | NLOptions | NLOptions | 1 |
| ! | std::optional<DiagnosticBehavior> | None | 1 |
| * | std::optional<DiagnosticBehavior> | None | 1 |
| * | std::optional<Diagnostic> | None | 1 |
| || | ConversionPair | ConversionPair | 1 |
| ! | ConversionPair | None | 1 |
| ! | ProtocolConformanceRef | None | 1 |
| | | uintptr_t | uintptr_t | 1 |
| == | LayoutConstraintInfo | integer literal | 1 |
| != | LayoutConstraintInfo | integer literal | 1 |
| == | TypeBase | integer literal | 1 |
| != | TypeBase | integer literal | 1 |
| * | VectorIt | None | 1 |
| << | size_t | integer literal | 1 |
| * | TargetFieldRecord<Runtime> | None | 1 |
| ++ | TargetFieldRecord<Runtime> | None | 1 |
| * | AssociatedTypeRecord | None | 1 |
| ++ | AssociatedTypeRecord | None | 1 |
| && | AssociatedTypeRecord | AssociatedTypeRecord | 1 |
| & | uint32_t | float literal (suffix ffff) | 1 |
| sizeof | RelativeDirectPointer<const char> | None | 1 |
| * | CaptureTypeRecord | None | 1 |
| ++ | CaptureTypeRecord | None | 1 |
| * | MetadataSourceRecord | None | 1 |
| ++ | MetadataSourceRecord | None | 1 |
| != | std::string::const_iterator | char literal | 1 |
| ! | typename T::SegmentCmd | None | 1 |
| < | unsigned | uint16_t | 1 |
| * | unsigned | uint16_t | 1 |
| + | const char * | uint64_t | 1 |
| ! | std::optional<uint32_t> | None | 1 |
| ! | TypeRef | None | 1 |
| ++ | StoredSize | None | 1 |
| < | int | uint64_t | 1 |
| ! | ExternalOpaqueTypeDescriptor<ObjCInteropKind, PointerSize> | None | 1 |
| << | std::ostringstream | unsigned | 1 |
| ~ | int | None | 1 |
| > | uint8_t | uint32_t | 1 |
| & | value_type | None | 1 |
| | | make_unsigned_t<value_type> | make_unsigned_t<value_type> | 1 |
| * | const detail::packed_endian_specific_integral<T, E, unaligned> * | None | 1 |
| * | detail::packed_endian_specific_integral<T, E, unaligned> * | None | 1 |
| * | std::unique_ptr<raw_ostream> | None | 1 |
| << | raw_ostream | std::optional<T> | 1 |
| * | std::unique_ptr<ErrorInfoBase> | None | 1 |
| && | Error | Error | 1 |
| * | Expected<T> | None | 1 |
| && | std::unique_ptr<ErrorInfoBase> | string literal | 1 |
| * | std::optional<size_t> | None | 1 |
| & | int | float literal (suffix f) | 1 |
| >> | int | integer literal | 1 |
| << | OStream | string literal | 1 |
| & | content_type | None | 1 |
| & | BasicSymbolRef | None | 1 |
| ! | Expected<uint32_t> | None | 1 |
| * | Expected<uint32_t> | None | 1 |
| != | section_iterator | section_iterator | 1 |
| ! | Expected<ArrayRef<uint8_t>> | None | 1 |
| == | support::ulittle16_t | float literal (suffix ffff) | 1 |
| < | IntTy | integer literal | 1 |
| & | IntTy | float literal (suffix FFFF) | 1 |
| & | IntTy | float literal (suffix FFFFFFFF) | 1 |
| + | coff_symbol16 | integer literal | 1 |
| + | coff_symbol32 | integer literal | 1 |
| || | coff_symbol16 | coff_symbol32 | 1 |
| >> | support::ulittle32_t | integer literal | 1 |
| - | integer literal | integer literal | 1 |
| | | union {
    support::ulittle32_t DataEntryOffset;
    support::ulittle32_t SubdirOffset;

    bool isSubDir() const { return SubdirOffset >> 31; }
    uint32_t value() const {
      return maskTrailingOnes<uint32_t>(31) & SubdirOffset;
    }

  } | integer literal | 1 |
| && | coff_symbol16 | coff_symbol32 | 1 |
| ! | coff_symbol16 | None | 1 |
| ! | coff_symbol32 | None | 1 |
| && | pe32_header | pe32plus_header | 1 |
| ! | pe32_header | None | 1 |
| ! | pe32plus_header | None | 1 |
| & | support::ulittle16_t | float literal (suffix F) | 1 |
| | | E | E | 1 |
| & | E | E | 1 |
| ^ | E | E | 1 |

**excerpts, resolved**
- `/sources/swift-6.0.3-RELEASE/lib/Demangling/Demangler.cpp:234` operator `&&` operand types ['integer literal', 'string literal'] resolved against []
- `/sources/swift-6.0.3-RELEASE/lib/Demangling/Demangler.cpp:252` operator `&&` operand types ['integer literal', 'string literal'] resolved against []
- `/sources/swift-6.0.3-RELEASE/lib/Demangling/Demangler.cpp:270` operator `&&` operand types ['integer literal', 'string literal'] resolved against []

**excerpts, unresolved**
- `/sources/swift-6.0.3-RELEASE/lib/Demangling/Demangler.cpp:203` operator `!=` reason: call result
- `/sources/swift-6.0.3-RELEASE/lib/Demangling/Demangler.cpp:213` operator `||` reason: call result
- `/sources/swift-6.0.3-RELEASE/lib/Demangling/Demangler.cpp:456` operator `==` reason: call result
- `/sources/swift-6.0.3-RELEASE/lib/Demangling/Demangler.cpp:75` operator `==` reason: declared in another file or not found
- `/sources/swift-6.0.3-RELEASE/lib/Demangling/Demangler.cpp:165` operator `!` reason: declared in another file or not found
- `/sources/swift-6.0.3-RELEASE/lib/Demangling/Demangler.cpp:400` operator `==` reason: declared in another file or not found

## swift (standard library)

**unresolved histogram**

| reason | sites | share |
|---|---|---|
| declared in another file or not found | 2950 | 0.264 |
| member access | 2456 | 0.22 |
| inferred binding | 1969 | 0.176 |
| other (no operand node found for try_operator) | 1292 | 0.115 |
| call result | 867 | 0.077 |
| other (bang) | 605 | 0.054 |
| other (tuple_expression) | 266 | 0.024 |
| other (additive_expression) | 175 | 0.016 |
| other (hex_literal) | 120 | 0.011 |
| other (infix_expression) | 95 | 0.008 |
| other (equality_expression) | 81 | 0.007 |
| other (comparison_expression) | 80 | 0.007 |
| other (multiplicative_expression) | 73 | 0.007 |
| other (conjunction_expression) | 30 | 0.003 |
| other (bitwise_operation) | 24 | 0.002 |
| other (try_expression) | 20 | 0.002 |
| other (bin_literal) | 20 | 0.002 |
| other (custom_operator) | 19 | 0.002 |
| other (disjunction_expression) | 18 | 0.002 |
| other (ERROR) | 10 | 0.001 |
| other (array_literal) | 7 | 0.001 |
| other (await_expression) | 6 | 0.001 |
| other (constructor_expression) | 5 | 0.0 |
| other (comment) | 1 | 0.0 |

**resolved variants** (full table; log_210 carries the first 20)

| operator | lhs type | rhs type | sites |
|---|---|---|---|
| - | integer literal | None | 139 |
| ..< | integer literal | integer literal | 89 |
| ..< | MinimalIndex | MinimalIndex | 84 |
| == | Int | integer literal | 38 |
| + | string literal | string literal | 37 |
| >= | Int | integer literal | 34 |
| << | integer literal | integer literal | 30 |
| > | Int | integer literal | 23 |
| ..< | integer literal | Int | 23 |
| + | Int | integer literal | 17 |
| ~ | integer literal | None | 14 |
| & | UnsafeRawBufferPointer | None | 13 |
| & | StreamType | None | 13 |
| - | Int | integer literal | 12 |
| ..< | MinimalStrideableIndex | MinimalStrideableIndex | 12 |
| ... | integer literal | integer literal | 11 |
| * | integer literal | integer literal | 10 |
| <= | Int | integer literal | 10 |
| & | Int | None | 8 |
| < | Int | integer literal | 8 |
| / | Int | integer literal | 8 |
| == | String | string literal | 6 |
| & | [ObjectIdentifier: Int] | None | 6 |
| == | Void? | None | 6 |
| == | UInt64 | integer literal | 6 |
| && | Bool | Bool | 6 |
| < | Self | Self | 6 |
| & | T? | None | 6 |
| & | (read: HANDLE?, write: HANDLE?) | None | 6 |
| & | _FDOutputStream | None | 6 |
| ... | integer literal | None | 5 |
| + | Int | Int | 5 |
| - | Int | None | 5 |
| == | UInt | integer literal | 5 |
| != | UInt | integer literal | 5 |
| & | Builtin.BridgeObject | None | 5 |
| & | NativeClass | None | 5 |
| & | DWORD | None | 5 |
| + | string literal | String | 5 |
| & | [String: Set<Unicode.Scalar>] | None | 5 |
| & | Int32 | None | 4 |
| < | Int | Int | 4 |
| >= | Int | Int | 4 |
| ~ | UInt | None | 4 |
| & | CodeUnits | None | 4 |
| / | Self | Self | 4 |
| & | Self | integer literal | 4 |
| & | UInt64 | None | 4 |
| ~ | UInt64 | None | 4 |
| == | UnsafeMutablePointer<AnyObject>? | None | 4 |
| & | Self | None | 4 |
| || | Bool | Bool | 3 |
| != | UInt8 | integer literal | 3 |
| < | ssize_t | integer literal | 3 |
| == | ssize_t | integer literal | 3 |
| == | Unicode.Scalar? | None | 3 |
| != | Int | integer literal | 3 |
| * | Self | Self | 3 |
| % | Self | Self | 3 |
| + | integer literal | UInt64 | 3 |
| & | __ContiguousArrayStorageBase | None | 3 |
| - | float literal | None | 3 |
| == | integer literal | integer literal | 3 |
| ..< | Index | Index | 3 |
| & | UInt8 | None | 3 |
| & | UInt64 | integer literal | 3 |
| + | Self | Self | 3 |
| - | Self | Self | 3 |
| & | SECURITY_ATTRIBUTES | None | 3 |
| & | CInt | None | 3 |
| == | Int? | None | 3 |
| == | Bool | bool literal | 3 |
| & | [Unicode.Scalar: String] | None | 3 |
| & | UInt | None | 3 |
| == | Int32 | integer literal | 2 |
| - | Int? | integer literal | 2 |
| - | integer literal | UInt8 | 2 |
| ?? | Int? | integer literal | 2 |
| * | UInt64 | integer literal | 2 |
| == | Address | integer literal | 2 |
| + | Address | Address | 2 |
| & | Address | integer literal | 2 |
| + | string literal | BacktraceFormattingOptions | 2 |
| & | Index | None | 2 |
| - | UnsafeMutablePointer<Element> | UnsafeMutablePointer<Element> | 2 |
| & | [Range<Index>] | None | 2 |
| ~ | Int | None | 2 |
| & | UnsafeMutableRawPointer? | None | 2 |
| & | Self.RawValue? | None | 2 |
| & | UnsafeRawPointer? | None | 2 |
| >= | Int64 | integer literal | 2 |
| < | RHS | Self | 2 |
| - | Self.Stride | None | 2 |
| <= | Int | Int | 2 |
| & | ClassHolder | None | 2 |
| - | Int | Int | 2 |
| & | Root | None | 2 |
| & | AnyKeyPath | None | 2 |
| != | integer literal | integer literal | 2 |
| & | Set<ObjectIdentifier> | None | 2 |
| == | _NativeSet<Element>.Bucket | _NativeSet<Element>.Bucket | 2 |
| + | UnsafeMutablePointer<_SwiftNSFastEnumerationState> | integer literal | 2 |
| == | _NativeDictionary<Key, Value>.Bucket | _NativeDictionary<Key, Value>.Bucket | 2 |
| < | Other | Self | 2 |
| == | Self | Self | 2 |
| ~ | Self | None | 2 |
| & | [UnsafeRawPointer] | None | 2 |
| & | T | None | 2 |
| == | Bool | Bool | 2 |
| != | Element.Stride | integer literal | 2 |
| / | Self | Scalar | 2 |
| & | Values | None | 2 |
| & | _OpaqueStringSwitchCache | None | 2 |
| == | _Slot | _Slot | 2 |
| + | AnyDerivative | AnyDerivative | 2 |
| - | AnyDerivative | AnyDerivative | 2 |
| & | Int | integer literal | 2 |
| <= | CInt | integer literal | 2 |
| ... | Int | Int | 2 |
| == | pid_t? | None | 2 |
| + | [Substring] | [Substring] | 2 |
| == | (() -> Void)? | None | 2 |
| & | [Unicode.Scalar: [String: String]] | None | 2 |
| != | pid_t | Int64 | 1 |
| & | task_t | None | 1 |
| & | thread_act_array_t? | None | 1 |
| & | mach_msg_type_number_t | None | 1 |
| ..< | integer literal | mach_msg_type_number_t | 1 |
| & | thread_identifier_info_data_t? | None | 1 |
| + | string literal | any Theme | 1 |
| > | String | integer literal | 1 |
| - | integer literal | String | 1 |
| ... | Int | None | 1 |
| > | Traits.Address | Traits.Address | 1 |
| - | Source.Address | Source.Address | 1 |
| <= | Int? | integer literal | 1 |
| < | Int | Int? | 1 |
| & | size_t | None | 1 |
| + | Address | Size | 1 |
| == | UInt | UInt | 1 |
| == | UInt32 | integer literal | 1 |
| - | integer literal | integer literal | 1 |
| == | Unicode.Scalar? | Unicode.Scalar? | 1 |
| < | Unicode.Scalar? | Unicode.Scalar? | 1 |
| & | [CVarArg] | None | 1 |
| & | _NativeDictionary<Key, Value> | None | 1 |
| < | UInt16 | Result | 1 |
| | | UInt32 | UInt32 | 1 |
| - | Self.RawSignificand | integer literal | 1 |
| == | UInt8 | integer literal | 1 |
| + | Self.RawSignificand | integer literal | 1 |
| == | Self.RawSignificand | Self.RawSignificand | 1 |
| ..< | Int | Int | 1 |
| & | (Int, Int, Int, Int) | None | 1 |
| + | integer literal | Int64 | 1 |
| == | Int64 | integer literal | 1 |
| / | float literal | float literal | 1 |
| == | Self | RHS | 1 |
| < | Self | RHS | 1 |
| == | String | Substring | 1 |
| == | Substring | String | 1 |
| == | Bound | Bound | 1 |
| != | T | integer literal | 1 |
| & | State | None | 1 |
| | | UInt | integer literal | 1 |
| & | UInt | integer literal | 1 |
| & | UnsafePointer<CChar>? | None | 1 |
| & | NameFreeFunc? | None | 1 |
| + | UnsafeMutablePointer<UInt8> | Int | 1 |
| == | AnyObject? | None | 1 |
| == | KeyPathComponent | KeyPathComponent | 1 |
| & | UnsafeMutablePointer<CurValue> | None | 1 |
| + | UnsafeRawPointer | Int | 1 |
| == | KeyPathPatternComputedArguments? | None | 1 |
| || | integer literal | Bool | 1 |
| + | UnsafeMutablePointer<Element> | Int | 1 |
| <= | UInt32 | integer literal | 1 |
| & | (UInt16, UInt16) | None | 1 |
| & | CUnsignedLong | None | 1 |
| + | UnsafeMutablePointer<AnyObject?> | integer literal | 1 |
| >> | UInt16 | integer literal | 1 |
| << | UInt32 | integer literal | 1 |
| >> | UInt32 | integer literal | 1 |
| - | UInt64 | integer literal | 1 |
| | | integer literal | UInt64 | 1 |
| < | UInt64 | integer literal | 1 |
| == | Builtin.NativeObject | Builtin.NativeObject | 1 |
| == | Builtin.RawPointer | Builtin.RawPointer | 1 |
| == | Any.Type? | Any.Type? | 1 |
| | | UInt | UInt | 1 |
| & | (Int, Int, Int, Int, UInt8, UInt8, UInt16, UInt32, Int, Int, Int, Int) | None | 1 |
| == | Self | Other | 1 |
| < | Self | Other | 1 |
| | | UInt64 | UInt64 | 1 |
| & | Counters | None | 1 |
| + | Index | integer literal | 1 |
| - | Index | integer literal | 1 |
| & | UnsafeMutablePointer<UInt8>? | None | 1 |
| / | integer literal | integer literal | 1 |
| & | _BridgeableMetatype? | None | 1 |
| + | string literal | Range<Int> | 1 |
| ~ | SIMDMask | None | 1 |
| & | Self | Self | 1 |
| ^ | Self | Self | 1 |
| | | Self | Self | 1 |
| & | Self | Scalar | 1 |
| ^ | Self | Scalar | 1 |
| | | Self | Scalar | 1 |
| % | Self | Scalar | 1 |
| - | integer literal | Self | 1 |
| + | Self | Scalar | 1 |
| - | Self | Scalar | 1 |
| * | Self | Scalar | 1 |
| + | integer literal | None | 1 |
| + | integer literal | integer literal | 1 |
| != | Index | Index | 1 |
| & | (Int, Int, Int, Int, UInt8, UInt8, UInt16, UInt32, Int, Int, Int) | None | 1 |
| == | T | T | 1 |
| == | Error? | None | 1 |
| == | UnsafeBufferPointer<Element>? | None | 1 |
| == | UnsafeMutableBufferPointer<Element>? | None | 1 |
| < | _Slot | _Slot | 1 |
| & | ObservationTracking._AccessList? | None | 1 |
| >> | Int64 | integer literal | 1 |
| & | InvocationDecoder | None | 1 |
| >> | Int | integer literal | 1 |
| < | DWORD | DWORD | 1 |
| - | DWORD | DWORD | 1 |
| & | [CInt] | None | 1 |
| & | Storage | None | 1 |
| * | Int | Int | 1 |
| == | Int | Int | 1 |
| & | UnsafeMutablePointer<CChar>? | None | 1 |
| == | String? | None | 1 |
| ?? | OSVersion? | OSVersion | 1 |
| < | T | T | 1 |
| > | T | T | 1 |
| + | [StringComparisonTest] | [StringComparisonTest] | 1 |
| & | [Unicode.Scalar: Unicode.NumericType] | None | 1 |
| & | [Unicode.Scalar: Double] | None | 1 |
| & | [Unicode.Scalar: Unicode.Version] | None | 1 |
| & | [Unicode.Scalar: Unicode.GeneralCategory] | None | 1 |
| & | [(String, [String])] | None | 1 |

**excerpts, resolved**
- `/sources/swift-6.0.3-RELEASE/stdlib/public/libexec/swift-backtrace/TargetLinux.swift:60` operator `-` operand types ['integer literal'] resolved against []
- `/sources/swift-6.0.3-RELEASE/stdlib/public/libexec/swift-backtrace/TargetLinux.swift:111` operator `!=` operand types ['pid_t', 'Int64'] resolved against ['/sources/swift-6.0.3-RELEASE/stdlib/public/libexec/swift-backtrace/TargetLinux.swift:51', '/sources/swift-6.0.3-RELEASE/stdlib/public/libexec/swift-backtrace/TargetLinux.swift:101']
- `/sources/swift-6.0.3-RELEASE/stdlib/public/libexec/swift-backtrace/TargetMacOS.swift:77` operator `-` operand types ['integer literal'] resolved against []

**excerpts, unresolved**
- `/sources/swift-6.0.3-RELEASE/stdlib/public/libexec/swift-backtrace/TargetMacOS.swift:120` operator `<` reason: declared in another file or not found
- `/sources/swift-6.0.3-RELEASE/stdlib/public/libexec/swift-backtrace/TargetMacOS.swift:120` operator `>` reason: declared in another file or not found
- `/sources/swift-6.0.3-RELEASE/stdlib/public/libexec/swift-backtrace/TargetMacOS.swift:138` operator `<` reason: declared in another file or not found
- `/sources/swift-6.0.3-RELEASE/stdlib/public/libexec/swift-backtrace/TargetLinux.swift:111` operator `&&` reason: member access
- `/sources/swift-6.0.3-RELEASE/stdlib/public/libexec/swift-backtrace/TargetLinux.swift:224` operator `==` reason: member access
- `/sources/swift-6.0.3-RELEASE/stdlib/public/libexec/swift-backtrace/TargetLinux.swift:224` operator `!=` reason: member access
