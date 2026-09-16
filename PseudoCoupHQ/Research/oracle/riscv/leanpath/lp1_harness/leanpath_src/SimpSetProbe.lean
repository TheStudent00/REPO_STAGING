import Leanpath
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIM LeanIM.Functions Leanpath
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
set_option pp.maxSteps 10000000
set_option pp.deepTerms true
set_option pp.proofs false
set_option format.width 1000000
set_option profiler true
set_option profiler.threshold 0
#check @leanpath_model
#check @leanpath_run
#check @leanpath_base
#check @simp_sail
#check @Leanpath.decode
#check @Leanpath.walk
#check @Leanpath.results
#check @Leanpath.answer
#check @Leanpath.withRegs
#check @Leanpath.stateOf
#check @EStateM.bind
#check @EStateM.pure
#check @EStateM.get
#check @EStateM.set
#check @EStateM.modifyGet
#check @EStateM.throw
#check @EStateM.map
#check @EStateM.seqRight
#check @EStateM.instMonad
#check @bind
#check @pure
#check @get
#check @getThe
#check @modify
#check @modifyGet
#check @set
#check @throw
#check @throwThe
#check @MonadStateOf.get
#check @MonadStateOf.set
#check @MonadStateOf.modifyGet
#check @MonadState.get
#check @MonadState.set
#check @MonadState.modifyGet
#check @MonadExceptOf.throw
#check @MonadExcept.throw
#check @Functor.map
#check @Seq.seq
#check @SeqRight.seqRight
#check @SeqLeft.seqLeft
#check @ExceptT.run
#check @ExceptT.mk
#check @ExceptT.bind
#check @ExceptT.pure
#check @ExceptT.lift
#check @ExceptT.bindCont
#check @ExceptT.map
#check @ExceptT.instMonad
#check @monadLift
#check @MonadLift.monadLift
#check @MonadLiftT.monadLift
#check @EStateM.instMonadStateOf
#check @EStateM.instMonadExceptOf
#check @EStateM.tryCatch
#check @EStateM.instMonad
