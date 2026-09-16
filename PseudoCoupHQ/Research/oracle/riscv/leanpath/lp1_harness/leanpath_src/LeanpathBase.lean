import Leanpath
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIM LeanIM.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 100000
namespace Leanpath
def S0 : St := stateOf (init default)
attribute [leanpath_base] S0 init
end Leanpath
