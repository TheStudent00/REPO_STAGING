/-
leanpath -- the simp attributes the harness uses (a registered simp attribute
must live in a module of its own, imported by the module that fills it).

  leanpath_model : every definition of the emitted model, as an unfold lemma
                   (the list is READ from the emitted Lean text by
                   SailModel.harness_names; no name is typed by hand)
  leanpath_run   : the run lemmas of the state monad (EStateM applied to a
                   state), each proved by rfl in Leanpath.lean
  leanpath_base  : the facts about the base state's registers, proved once
-/
import Lean
register_simp_attr leanpath_model
register_simp_attr leanpath_run
register_simp_attr leanpath_base
