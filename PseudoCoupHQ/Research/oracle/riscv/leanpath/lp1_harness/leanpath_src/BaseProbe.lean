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
theorem base_probe (h_plat_term_write : ∀ x0  (s : Leanpath.St), (plat_term_write x0) s = EStateM.Result.ok () s) (h_load_reservation : ∀ x0 x1  (s : Leanpath.St), (load_reservation x0 x1) s = EStateM.Result.ok () s) (h_cancel_reservation : ∀ x0  (s : Leanpath.St), (cancel_reservation x0) s = EStateM.Result.ok () s) : stateOf (init default) = stateOf (init default) := by
  conv => lhs; simp (config := {decide := true}) only [Leanpath.decode, Leanpath.walk, Leanpath.results, Leanpath.answer, Leanpath.withRegs, Leanpath.stateOf, EStateM.bind, EStateM.pure, EStateM.get, EStateM.set, EStateM.modifyGet, EStateM.throw, EStateM.map, EStateM.seqRight, EStateM.instMonad, bind, pure, get, getThe, modify, modifyGet, set, throw, throwThe, MonadStateOf.get, MonadStateOf.set, MonadStateOf.modifyGet, MonadState.get, MonadState.set, MonadState.modifyGet, MonadExceptOf.throw, MonadExcept.throw, Functor.map, Seq.seq, SeqRight.seqRight, SeqLeft.seqLeft, ExceptT.run, ExceptT.mk, ExceptT.bind, ExceptT.pure, ExceptT.lift, ExceptT.bindCont, ExceptT.map, ExceptT.instMonad, monadLift, MonadLift.monadLift, MonadLiftT.monadLift, EStateM.instMonadStateOf, EStateM.tryCatch, EStateM.instMonad, h_plat_term_write, h_load_reservation, h_cancel_reservation, init, h_plat_term_write, h_load_reservation, h_cancel_reservation]
  leanpath_show_lhs
  rfl
