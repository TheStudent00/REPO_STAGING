import LeanIM
set_option maxHeartbeats 1_000_000_000
set_option maxRecDepth 1_000_000
set_option linter.unusedVariables false
set_option match.ignoreUnusedAlts true
open Sail
open Sail.ConcurrencyInterfaceV1
noncomputable section
namespace LeanIM
open ConcurrencyInterfaceV1
namespace Functions
open zvk_vsm4r_funct6
open zvk_vsha2_funct6
open zvk_vaesem_funct6
open zvk_vaesef_funct6
open zvk_vaesdm_funct6
open zvk_vaesdf_funct6
open zvabd_vwabda_func6
open zvabd_vabd_func6
open zicondop
open xRET_type
open wxfunct6
open wvxfunct6
open wvvfunct6
open wvfunct6
open wrsop
open write_kind
open wmvxfunct6
open wmvvfunct6
open vxsgfunct6
open vxmsfunct6
open vxmfunct6
open vxmcfunct6
open vxfunct6
open vxcmpfunct6
open vvmsfunct6
open vvmfunct6
open vvmcfunct6
open vvfunct6
open vvcmpfunct6
open vstart_class
open vregno
open vregidx
open vmlsop
open vlewidth
open visgfunct6
open virtaddr
open vimsfunct6
open vimfunct6
open vimcfunct6
open vifunct6
open vicmpfunct6
open vfwunary0
open vfunary1
open vfunary0
open vfnunary0
open vextfunct6
open vector_support
open uop
open stateen_bit
open sopw
open sop
open seed_opst
open rounding_mode
open ropw
open rop
open rmvvfunct6
open rivvfunct6
open rfwvvfunct6
open rfvvfunct6
open regno
open regidx
open read_kind
open pte_check_failure
open pmpAddrMatch
open physaddr
open page_based_mem_type
open option
open nxsfunct6
open nxfunct6
open nvsfunct6
open nvfunct6
open ntl_type
open nisfunct6
open nifunct6
open mvxmafunct6
open mvxfunct6
open mvvmafunct6
open mvvfunct6
open mmfunct6
open misaligned_exception
open mem_payload
open maskfunct3
open landing_pad_expectation
open iop
open instruction
open indexed_mop
open fwvvmafunct6
open fwvvfunct6
open fwvfunct6
open fwvfmafunct6
open fwvffunct6
open fwffunct6
open fvvmfunct6
open fvvmafunct6
open fvvfunct6
open fvfmfunct6
open fvfmafunct6
open fvffunct6
open fregno
open fregidx
open float_class
open f_un_x_op_H
open f_un_x_op_D
open f_un_rm_xf_op_S
open f_un_rm_xf_op_H
open f_un_rm_xf_op_D
open f_un_rm_fx_op_S
open f_un_rm_fx_op_H
open f_un_rm_fx_op_D
open f_un_rm_ff_op_S
open f_un_rm_ff_op_H
open f_un_rm_ff_op_D
open f_un_op_x_S
open f_un_op_f_S
open f_un_f_op_H
open f_un_f_op_D
open f_madd_op_S
open f_madd_op_H
open f_madd_op_D
open f_bin_x_op_H
open f_bin_x_op_D
open f_bin_rm_op_S
open f_bin_rm_op_H
open f_bin_rm_op_D
open f_bin_op_x_S
open f_bin_op_f_S
open f_bin_f_op_H
open f_bin_f_op_D
open extop_zbb
open extension
open exception
open csrop
open cregidx
open checked_cbop
open cfregidx
open cbop_zicbop
open cbop_zicbom
open cbie
open cacheop
open bropw_zbb
open brop_zbs
open brop_zbkb
open brop_zbb
open breakpoint_cause
open bop
open biop_zbs
open biop
open barrier_kind
open amoop
open agtype
open XtvecModeReservedBehavior
open XipReadType
open XenvcfgCbieReservedBehavior
open WaitReason
open VectorHalf
open TrapVectorMode
open TrapCause
open Step
open Splittability
open Software_Check_Code
open Signedness
open SWCheckCodes
open SATPMode
open Reservability
open Register
open RV32ZdinxOddRegisterReservedBehavior
open Privileged_ISA_Version
open Privilege
open PointerMaskingMode
open PmpWriteOnlyReservedBehavior
open PmpAddrMatchType
open PTW_Error
open PTE_Check
open PM_Ext
open OOBVstartReservedBehavior
open MemoryRegionType
open MemoryAccessType
open InterruptType
open IllegalVtypeReservedBehavior
open ISA_Format
open HartState
open FflagsDirtyPolicy
open FetchResult
open FetchBytes_Result
open FeatureEnabledResult
open FcsrRmReservedBehavior
open Ext_DataAddr_Check
open ExtStatus
open ExtContextPolicy
open ExecutionResult
open ExceptionType
open CSRCheckResult
open CSRAccessType
open AtomicSupport
open Architecture
open AmocasOddRegisterReservedBehavior
set_option linter.unusedVariables false

#check (fun (k000_a : BitVec 64) => ((rev8 k000_a)))

#check (fun (k001_a : BitVec 64) => ((k001_a <<< 3)))

#check (fun (k002_a : BitVec 64) => ((k002_a <<< 4)))

#check (fun (k003_a : BitVec 64) => ((k003_a >>> 1)))

#check (fun (k004_a : BitVec 64) => ((k004_a >>> 2)))

#check (fun (k005_a : BitVec 64) => ((k005_a >>> 6)))

#check (fun (k006_a : BitVec 64) => ((k006_a >>> 7)))

#check (fun (k007_a : BitVec 64) => ((k007_a >>> 8)))

#check (fun (k008_a : BitVec 64) => ((k008_a >>> 9)))

#check (fun (k009_a : BitVec 64) => ((brev8 k009_a)))

#check (fun (k010_a : BitVec 64) => ((k010_a <<< 13)))

#check (fun (k011_a : BitVec 64) => ((k011_a <<< 14)))

#check (fun (k012_a : BitVec 64) => ((k012_a <<< 18)))

#check (fun (k013_a : BitVec 64) => ((k013_a <<< 23)))

#check (fun (k014_a : BitVec 64) => ((k014_a <<< 24)))

#check (fun (k015_a : BitVec 64) => ((k015_a <<< 25)))

#check (fun (k016_a : BitVec 64) => ((k016_a <<< 26)))

#check (fun (k017_a : BitVec 64) => ((k017_a <<< 30)))

#check (fun (k018_a : BitVec 64) => ((k018_a <<< 31)))

#check (fun (k019_a : BitVec 64) => ((k019_a >>> 14)))

#check (fun (k020_a : BitVec 64) => ((k020_a >>> 18)))

#check (fun (k021_a : BitVec 64) => ((k021_a >>> 19)))

#check (fun (k022_a : BitVec 64) => ((k022_a >>> 28)))

#check (fun (k023_a : BitVec 64) => ((k023_a >>> 29)))

#check (fun (k024_a : BitVec 64) => ((BitVec.toInt k024_a)))

#check (fun (k025_a : BitVec 64) => ((BitVec.toNatInt k025_a)))

#check (fun (k026_a : BitVec 64) => (((BitVec.toInt k026_a) == 0)))

#check (fun (k027_a : BitVec 64) => (((k027_a >>> 2) ^^^ (k027_a <<< 4))))

#check (fun (k028_a : BitVec 64) => ((Complement.complement k028_a)))

#check (fun (k029_a : BitVec 64) => (((BitVec.toNatInt k029_a) == 0)))

#check (fun (k030_a : BitVec 64) => (((k030_a <<< 18) ^^^ (k030_a <<< 14))))

#check (fun (k031_a : BitVec 64) => (((k031_a <<< 25) ^^^ (k031_a <<< 24))))

#check (fun (k032_a : BitVec 64) => (((k032_a <<< 26) ^^^ (k032_a <<< 13))))

#check (fun (k033_a : BitVec 64) => (((k033_a <<< 31) ^^^ (k033_a <<< 24))))

#check (fun (k034_a : BitVec 64) => (((k034_a >>> 29) ^^^ (k034_a <<< 13))))

#check (fun (k035_a : BitVec 64) => ((BitVec.countLeadingZeros k035_a)))

#check (fun (k036_a : BitVec 64) => ((BitVec.countTrailingZeros k036_a)))

#check (fun (k037_a : BitVec 64) => ((Sail.BitVec.extractLsb k037_a 4 0)))

#check (fun (k038_a : BitVec 64) => ((Sail.BitVec.extractLsb k038_a 5 0)))

#check (fun (k039_a : BitVec 64) => ((Sail.BitVec.extractLsb k039_a 7 0)))

#check (fun (k040_a : BitVec 64) => ((Sail.BitVec.extractLsb k040_a 15 0)))

#check (fun (k041_a : BitVec 64) => ((Sail.BitVec.extractLsb k041_a 31 0)))

#check (fun (k042_a : BitVec 64) => (((k042_a >>> 7) ^^^ ((k042_a >>> 2) ^^^ (k042_a <<< 4)))))

#check (fun (k043_a : BitVec 64) => (((k043_a >>> 9) ^^^ ((k043_a <<< 18) ^^^ (k043_a <<< 14)))))

#check (fun (k044_a : BitVec 64) => (((k044_a <<< 31) ^^^ ((k044_a <<< 25) ^^^ (k044_a <<< 24)))))

#check (fun (k045_a : BitVec 64) => (((k045_a >>> 29) ^^^ ((k045_a <<< 26) ^^^ (k045_a <<< 13)))))

#check (fun (k046_a : BitVec 64) => ((Sail.BitVec.extractLsb k046_a (log2_xlen -i 1) 0)))

#check (fun (k047_a : BitVec 64) => ((BitVec.toInt (Sail.BitVec.extractLsb k047_a 31 0))))

#check (fun (k048_a : BitVec 64) => ((to_bits (l := 64) (BitVec.countLeadingZeros k048_a))))

#check (fun (k049_a : BitVec 64) => ((BitVec.toNatInt (Sail.BitVec.extractLsb k049_a 31 0))))

#check (fun (k050_a : BitVec 64) => ((to_bits (l := 64) (BitVec.countTrailingZeros k050_a))))

#check (fun (k051_a : BitVec 64) => (((BitVec.toInt (Sail.BitVec.extractLsb k051_a 31 0)) == 0)))

#check (fun (k052_a : BitVec 64) => ((Sail.BitVec.extractLsb k052_a ((xlen_bytes *i 4) -i 1) 0)))

#check (fun (k053_a : BitVec 64) => ((sign_extend (m := 64) (Sail.BitVec.extractLsb k053_a 7 0))))

#check (fun (k054_a : BitVec 64) => ((zero_extend (m := 64) (Sail.BitVec.extractLsb k054_a 7 0))))

#check (fun (k055_a : BitVec 64) => ((sign_extend (m := 64) (Sail.BitVec.extractLsb k055_a 15 0))))

#check (fun (k056_a : BitVec 64) => ((zero_extend (m := 64) (Sail.BitVec.extractLsb k056_a 15 0))))

#check (fun (k057_a : BitVec 64) => ((zero_extend (m := 64) (Sail.BitVec.extractLsb k057_a 31 0))))

#check (fun (k058_a : BitVec 64) => (((BitVec.toNatInt (Sail.BitVec.extractLsb k058_a 31 0)) == 0)))

#check (fun (k059_a : BitVec 64) => ((BitVec.countLeadingZeros (Sail.BitVec.extractLsb k059_a 31 0))))

#check (fun (k060_a : BitVec 64) => ((BitVec.countTrailingZeros (Sail.BitVec.extractLsb k060_a 31 0))))

#check (fun (k061_a : BitVec 64) => ((Sail.BitVec.extractLsb (Sail.BitVec.extractLsb k061_a 31 0) 4 0)))

#check (fun (k062_a : BitVec 64) => ((shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k062_a 5 0))))

#check (fun (k063_a : BitVec 64) => ((to_bits (l := 64) (BitVec.countLeadingZeros (Sail.BitVec.extractLsb k063_a 31 0)))))

#check (fun (k064_a : BitVec 64) => ((to_bits (l := 64) (BitVec.countTrailingZeros (Sail.BitVec.extractLsb k064_a 31 0)))))

#check (fun (k065_a : BitVec 64) => ((Complement.complement (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k065_a 5 0)))))

#check (fun (k066_a : BitVec 64) (k066_b : BitVec 64) => ((k066_a + k066_b)))

#check (fun (k067_a : BitVec 64) (k067_b : BitVec 64) => ((k067_a - k067_b)))

#check (fun (k068_a : BitVec 64) (k068_b : BitVec 64) => ((k068_a &&& k068_b)))

#check (fun (k069_a : BitVec 64) (k069_b : BitVec 64) => ((k069_a ^^^ k069_b)))

#check (fun (k070_a : BitVec 64) (k070_b : BitVec 64) => ((k070_a ||| k070_b)))

#check (fun (k071_a : BitVec 64) (k071_b : BitVec 64) => ((zopz0zI_s k071_a k071_b)))

#check (fun (k072_a : BitVec 64) (k072_b : BitVec 64) => ((zopz0zI_u k072_a k072_b)))

#check (fun (k073_a : BitVec 64) (k073_b : BitVec 64) => ((zopz0zK_s k073_a k073_b)))

#check (fun (k074_a : BitVec 64) (k074_b : BitVec 64) => ((zopz0zK_u k074_a k074_b)))

#check (fun (k075_a : BitVec 64) (k075_b : BitVec 64) => ((carryless_mul k075_a k075_b)))

#check (fun (k076_a : BitVec 64) (k076_b : BitVec 64) => ((carryless_mulr k076_a k076_b)))

#check (fun (k077_a : BitVec 64) (k077_b : BitVec 64) => ((bool_to_bit (zopz0zI_s k077_a k077_b))))

#check (fun (k078_a : BitVec 64) (k078_b : BitVec 64) => ((bool_to_bit (zopz0zI_u k078_a k078_b))))

#check (fun (k079_a : BitVec 64) (k079_b : BitVec 64) => ((Complement.complement (k079_a ^^^ k079_b))))

#check (fun (k080_a : BitVec 64) (k080_b : BitVec 64) => ((k080_a &&& (Complement.complement k080_b))))

#check (fun (k081_a : BitVec 64) (k081_b : BitVec 64) => ((k081_a ||| (Complement.complement k081_b))))

#check (fun (k082_a : BitVec 64) (k082_b : BitVec 64) => (((k082_a >>> 8) ^^^ ((k082_b <<< 31) ^^^ (k082_b <<< 24)))))

#check (fun (k083_a : BitVec 64) (k083_b : BitVec 64) => ((if ((zopz0zI_s k083_a k083_b) : Bool) then k083_a else k083_b)))

#check (fun (k084_a : BitVec 64) (k084_b : BitVec 64) => ((if ((zopz0zI_u k084_a k084_b) : Bool) then k084_a else k084_b)))

#check (fun (k085_a : BitVec 64) (k085_b : BitVec 64) => ((if ((zopz0zK_s k085_a k085_b) : Bool) then k085_a else k085_b)))

#check (fun (k086_a : BitVec 64) (k086_b : BitVec 64) => ((if ((zopz0zK_u k086_a k086_b) : Bool) then k086_a else k086_b)))

#check (fun (k087_a : BitVec 64) (k087_b : BitVec 64) => (((k087_a >>> 19) ^^^ ((k087_b >>> 29) ^^^ (k087_b <<< 13)))))

#check (fun (k088_a : BitVec 64) (k088_b : BitVec 64) => ((Int.tdiv (BitVec.toInt k088_a) (BitVec.toInt k088_b))))

#check (fun (k089_a : BitVec 64) (k089_b : BitVec 64) => ((Int.tmod (BitVec.toInt k089_a) (BitVec.toInt k089_b))))

#check (fun (k090_a : BitVec 64) (k090_b : BitVec 64) => ((Int.tdiv (BitVec.toNatInt k090_a) (BitVec.toNatInt k090_b))))

#check (fun (k091_a : BitVec 64) (k091_b : BitVec 64) => ((Int.tmod (BitVec.toNatInt k091_a) (BitVec.toNatInt k091_b))))

#check (fun (k092_a : BitVec 64) (k092_b : BitVec 64) => ((zero_extend (m := 64) (bool_to_bit (zopz0zI_s k092_a k092_b)))))

#check (fun (k093_a : BitVec 64) (k093_b : BitVec 64) => ((zero_extend (m := 64) (bool_to_bit (zopz0zI_u k093_a k093_b)))))

#check (fun (k094_a : BitVec 64) (k094_b : BitVec 64) => (((k094_a >>> 28) ^^^ ((k094_b >>> 7) ^^^ ((k094_b >>> 2) ^^^ (k094_b <<< 4))))))

#check (fun (k095_a : BitVec 64) (k095_b : BitVec 64) => ((Sail.BitVec.extractLsb (carryless_mul k095_a k095_b) (xlen -i 1) 0)))

#check (fun (k096_a : BitVec 64) (k096_b : BitVec 64) => (((k096_a >>> 7) ^^^ ((k096_a >>> 8) ^^^ ((k096_b <<< 31) ^^^ (k096_b <<< 24))))))

#check (fun (k097_a : BitVec 64) (k097_b : BitVec 64) => (((k097_a >>> 18) ^^^ ((k097_b >>> 9) ^^^ ((k097_b <<< 18) ^^^ (k097_b <<< 14))))))

#check (fun (k098_a : BitVec 64) (k098_b : BitVec 64) => (((k098_a >>> 6) ^^^ ((k098_a >>> 19) ^^^ ((k098_b >>> 29) ^^^ (k098_b <<< 13))))))

#check (fun (k099_a : BitVec 64) (k099_b : BitVec 64) => (((k099_a >>> 8) ^^^ ((k099_b <<< 31) ^^^ ((k099_b <<< 25) ^^^ (k099_b <<< 24))))))

#check (fun (k100_a : BitVec 64) (k100_b : BitVec 64) => (((k100_a >>> 19) ^^^ ((k100_b >>> 29) ^^^ ((k100_b <<< 26) ^^^ (k100_b <<< 13))))))

#check (fun (k101_a : BitVec 64) (k101_b : BitVec 64) => ((shift_bits_left k101_a (Sail.BitVec.extractLsb k101_b (log2_xlen -i 1) 0))))

#check (fun (k102_a : BitVec 64) (k102_b : BitVec 64) => ((rotate_bits_left k102_a (Sail.BitVec.extractLsb k102_b (log2_xlen -i 1) 0))))

#check (fun (k103_a : BitVec 64) (k103_b : BitVec 64) => ((shift_bits_right k103_a (Sail.BitVec.extractLsb k103_b (log2_xlen -i 1) 0))))

#check (fun (k104_a : BitVec 64) (k104_b : BitVec 64) => (((Sail.BitVec.extractLsb k104_a 31 0) + (Sail.BitVec.extractLsb k104_b 31 0))))

#check (fun (k105_a : BitVec 64) (k105_b : BitVec 64) => (((Sail.BitVec.extractLsb k105_a 31 0) - (Sail.BitVec.extractLsb k105_b 31 0))))

#check (fun (k106_a : BitVec 64) (k106_b : BitVec 64) => (((Sail.BitVec.extractLsb k106_b 7 0) +++ (Sail.BitVec.extractLsb k106_a 7 0))))

#check (fun (k107_a : BitVec 64) (k107_b : BitVec 64) => ((rotate_bits_right k107_a (Sail.BitVec.extractLsb k107_b (log2_xlen -i 1) 0))))

#check (fun (k108_a : BitVec 64) (k108_b : BitVec 64) => ((Sail.BitVec.extractLsb (carryless_mul k108_a k108_b) ((2 *i xlen) -i 1) xlen)))

#check (fun (k109_a : BitVec 64) (k109_b : BitVec 64) => ((shift_bits_right_arith k109_a (Sail.BitVec.extractLsb k109_b (log2_xlen -i 1) 0))))

#check (fun (k110_a : BitVec 64) (k110_b : BitVec 64) => (((k110_a <<< 30) ^^^ ((k110_a >>> 28) ^^^ ((k110_b >>> 7) ^^^ ((k110_b >>> 2) ^^^ (k110_b <<< 4)))))))

#check (fun (k111_a : BitVec 64) (k111_b : BitVec 64) => (((k111_a >>> 1) ^^^ ((k111_a >>> 7) ^^^ ((k111_a >>> 8) ^^^ ((k111_b <<< 31) ^^^ (k111_b <<< 24)))))))

#check (fun (k112_a : BitVec 64) (k112_b : BitVec 64) => (((k112_a <<< 3) ^^^ ((k112_a >>> 6) ^^^ ((k112_a >>> 19) ^^^ ((k112_b >>> 29) ^^^ (k112_b <<< 13)))))))

#check (fun (k113_a : BitVec 64) (k113_b : BitVec 64) => (((k113_a >>> 7) ^^^ ((k113_a >>> 8) ^^^ ((k113_b <<< 31) ^^^ ((k113_b <<< 25) ^^^ (k113_b <<< 24)))))))

#check (fun (k114_a : BitVec 64) (k114_b : BitVec 64) => (((k114_a >>> 14) ^^^ ((k114_a >>> 18) ^^^ ((k114_b >>> 9) ^^^ ((k114_b <<< 18) ^^^ (k114_b <<< 14)))))))

#check (fun (k115_a : BitVec 64) (k115_b : BitVec 64) => (((k115_a >>> 6) ^^^ ((k115_a >>> 19) ^^^ ((k115_b >>> 29) ^^^ ((k115_b <<< 26) ^^^ (k115_b <<< 13)))))))

#check (fun (k116_a : BitVec 64) (k116_b : BitVec 64) => ((rotate_bits_left (Sail.BitVec.extractLsb k116_a 31 0) (Sail.BitVec.extractLsb k116_b 4 0))))

#check (fun (k117_a : BitVec 64) (k117_b : BitVec 64) => ((rotate_bits_right (Sail.BitVec.extractLsb k117_a 31 0) (Sail.BitVec.extractLsb k117_b 4 0))))

#check (fun (k118_a : BitVec 64) (k118_b : BitVec 64) => ((k118_a &&& (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k118_b 5 0)))))

#check (fun (k119_a : BitVec 64) (k119_b : BitVec 64) => ((k119_a ^^^ (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k119_b 5 0)))))

#check (fun (k120_a : BitVec 64) (k120_b : BitVec 64) => ((k120_a ||| (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k120_b 5 0)))))

#check (fun (k121_a : BitVec 64) (k121_b : BitVec 64) => ((mult_to_bits_half (l := xlen) Signedness.Signed Signedness.Signed k121_a k121_b VectorHalf.Low)))

#check (fun (k122_a : BitVec 64) (k122_b : BitVec 64) => ((mult_to_bits_half (l := xlen) Signedness.Signed Signedness.Signed k122_a k122_b VectorHalf.High)))

#check (fun (k123_a : BitVec 64) (k123_b : BitVec 64) => ((mult_to_bits_half (l := xlen) Signedness.Signed Signedness.Unsigned k123_a k123_b VectorHalf.Low)))

#check (fun (k124_a : BitVec 64) (k124_b : BitVec 64) => ((mult_to_bits_half (l := xlen) Signedness.Unsigned Signedness.Signed k124_a k124_b VectorHalf.Low)))

#check (fun (k125_a : BitVec 64) (k125_b : BitVec 64) => ((mult_to_bits_half (l := xlen) Signedness.Signed Signedness.Unsigned k125_a k125_b VectorHalf.High)))

#check (fun (k126_a : BitVec 64) (k126_b : BitVec 64) => ((mult_to_bits_half (l := xlen) Signedness.Unsigned Signedness.Signed k126_a k126_b VectorHalf.High)))

#check (fun (k127_a : BitVec 64) (k127_b : BitVec 64) => ((mult_to_bits_half (l := xlen) Signedness.Unsigned Signedness.Unsigned k127_a k127_b VectorHalf.Low)))

#check (fun (k128_a : BitVec 64) (k128_b : BitVec 64) => ((mult_to_bits_half (l := xlen) Signedness.Unsigned Signedness.Unsigned k128_a k128_b VectorHalf.High)))

#check (fun (k129_a : BitVec 64) (k129_b : BitVec 64) => ((sign_extend (m := 64) ((Sail.BitVec.extractLsb k129_a 31 0) + (Sail.BitVec.extractLsb k129_b 31 0)))))

#check (fun (k130_a : BitVec 64) (k130_b : BitVec 64) => ((sign_extend (m := 64) ((Sail.BitVec.extractLsb k130_a 31 0) - (Sail.BitVec.extractLsb k130_b 31 0)))))

#check (fun (k131_a : BitVec 64) (k131_b : BitVec 64) => ((zero_extend (m := 64) ((Sail.BitVec.extractLsb k131_b 7 0) +++ (Sail.BitVec.extractLsb k131_a 7 0)))))

#check (fun (k132_a : BitVec 64) (k132_b : BitVec 64) => (((k132_a <<< 25) ^^^ ((k132_a <<< 30) ^^^ ((k132_a >>> 28) ^^^ ((k132_b >>> 7) ^^^ ((k132_b >>> 2) ^^^ (k132_b <<< 4))))))))

#check (fun (k133_a : BitVec 64) (k133_b : BitVec 64) => (((k133_a >>> 1) ^^^ ((k133_a >>> 7) ^^^ ((k133_a >>> 8) ^^^ ((k133_b <<< 31) ^^^ ((k133_b <<< 25) ^^^ (k133_b <<< 24))))))))

#check (fun (k134_a : BitVec 64) (k134_b : BitVec 64) => (((k134_a <<< 3) ^^^ ((k134_a >>> 6) ^^^ ((k134_a >>> 19) ^^^ ((k134_b >>> 29) ^^^ ((k134_b <<< 26) ^^^ (k134_b <<< 13))))))))

#check (fun (k135_a : BitVec 64) (k135_b : BitVec 64) => (((k135_a <<< 23) ^^^ ((k135_a >>> 14) ^^^ ((k135_a >>> 18) ^^^ ((k135_b >>> 9) ^^^ ((k135_b <<< 18) ^^^ (k135_b <<< 14))))))))

#check (fun (k136_a : BitVec 64) (k136_b : BitVec 64) => (((BitVec.toInt (Sail.BitVec.extractLsb k136_a 31 0)) *i (BitVec.toInt (Sail.BitVec.extractLsb k136_b 31 0)))))

#check (fun (k137_a : BitVec 64) (k137_b : BitVec 64) => ((sign_extend (m := 64) ((k137_a >>> 1) ^^^ ((k137_a >>> 7) ^^^ ((k137_a >>> 8) ^^^ ((k137_b <<< 31) ^^^ (k137_b <<< 24))))))))

#check (fun (k138_a : BitVec 64) (k138_b : BitVec 64) => ((sign_extend (m := 64) ((k138_a <<< 3) ^^^ ((k138_a >>> 6) ^^^ ((k138_a >>> 19) ^^^ ((k138_b >>> 29) ^^^ (k138_b <<< 13))))))))

#check (fun (k139_a : BitVec 64) (k139_b : BitVec 64) => ((Int.tdiv (BitVec.toInt (Sail.BitVec.extractLsb k139_a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb k139_b 31 0)))))

#check (fun (k140_a : BitVec 64) (k140_b : BitVec 64) => ((Int.tmod (BitVec.toInt (Sail.BitVec.extractLsb k140_a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb k140_b 31 0)))))

#check (fun (k141_a : BitVec 64) (k141_b : BitVec 64) => ((if (((BitVec.toInt k141_b) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt k141_a) (BitVec.toInt k141_b)))))

#check (fun (k142_a : BitVec 64) (k142_b : BitVec 64) => ((sign_extend (m := 64) (rotate_bits_left (Sail.BitVec.extractLsb k142_a 31 0) (Sail.BitVec.extractLsb k142_b 4 0)))))

#check (fun (k143_a : BitVec 64) (k143_b : BitVec 64) => ((sign_extend (m := 64) (rotate_bits_right (Sail.BitVec.extractLsb k143_a 31 0) (Sail.BitVec.extractLsb k143_b 4 0)))))

#check (fun (k144_a : BitVec 64) (k144_b : BitVec 64) => (((k144_a &&& (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k144_b 5 0))) != (zeros (n := 64)))))

#check (fun (k145_a : BitVec 64) (k145_b : BitVec 64) => ((k145_a &&& (Complement.complement (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k145_b 5 0))))))

#check (fun (k146_a : BitVec 64) (k146_b : BitVec 64) => ((if (((BitVec.toInt k146_b) == 0) : Bool) then (BitVec.toInt k146_a) else (Int.tmod (BitVec.toInt k146_a) (BitVec.toInt k146_b)))))

#check (fun (k147_a : BitVec 64) (k147_b : BitVec 64) => ((Int.tdiv (BitVec.toNatInt (Sail.BitVec.extractLsb k147_a 31 0)) (BitVec.toNatInt (Sail.BitVec.extractLsb k147_b 31 0)))))

#check (fun (k148_a : BitVec 64) (k148_b : BitVec 64) => ((Int.tmod (BitVec.toNatInt (Sail.BitVec.extractLsb k148_a 31 0)) (BitVec.toNatInt (Sail.BitVec.extractLsb k148_b 31 0)))))

#check (fun (k149_a : BitVec 64) (k149_b : BitVec 64) => ((shift_bits_left (Sail.BitVec.extractLsb k149_a 31 0) (Sail.BitVec.extractLsb (Sail.BitVec.extractLsb k149_b 31 0) 4 0))))

#check (fun (k150_a : BitVec 64) (k150_b : BitVec 64) => ((shift_bits_right (Sail.BitVec.extractLsb k150_a 31 0) (Sail.BitVec.extractLsb (Sail.BitVec.extractLsb k150_b 31 0) 4 0))))

#check (fun (k151_a : BitVec 64) (k151_b : BitVec 64) => (((Sail.BitVec.extractLsb k151_b ((xlen_bytes *i 4) -i 1) 0) +++ (Sail.BitVec.extractLsb k151_a ((xlen_bytes *i 4) -i 1) 0))))

#check (fun (k152_a : BitVec 64) (k152_b : BitVec 64) => ((if (((BitVec.toNatInt k152_b) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toNatInt k152_a) (BitVec.toNatInt k152_b)))))

#check (fun (k153_a : BitVec 64) (k153_b : BitVec 64) => ((sign_extend (m := 64) ((k153_a <<< 25) ^^^ ((k153_a <<< 30) ^^^ ((k153_a >>> 28) ^^^ ((k153_b >>> 7) ^^^ ((k153_b >>> 2) ^^^ (k153_b <<< 4)))))))))

#check (fun (k154_a : BitVec 64) (k154_b : BitVec 64) => ((sign_extend (m := 64) ((k154_a >>> 1) ^^^ ((k154_a >>> 7) ^^^ ((k154_a >>> 8) ^^^ ((k154_b <<< 31) ^^^ ((k154_b <<< 25) ^^^ (k154_b <<< 24)))))))))

#check (fun (k155_a : BitVec 64) (k155_b : BitVec 64) => ((shift_bits_right_arith (Sail.BitVec.extractLsb k155_a 31 0) (Sail.BitVec.extractLsb (Sail.BitVec.extractLsb k155_b 31 0) 4 0))))

#check (fun (k156_a : BitVec 64) (k156_b : BitVec 64) => ((sign_extend (m := 64) ((k156_a <<< 3) ^^^ ((k156_a >>> 6) ^^^ ((k156_a >>> 19) ^^^ ((k156_b >>> 29) ^^^ ((k156_b <<< 26) ^^^ (k156_b <<< 13)))))))))

#check (fun (k157_a : BitVec 64) (k157_b : BitVec 64) => ((sign_extend (m := 64) ((k157_a <<< 23) ^^^ ((k157_a >>> 14) ^^^ ((k157_a >>> 18) ^^^ ((k157_b >>> 9) ^^^ ((k157_b <<< 18) ^^^ (k157_b <<< 14)))))))))

#check (fun (k158_a : BitVec 64) (k158_b : BitVec 64) => ((bool_to_bit ((k158_a &&& (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k158_b 5 0))) != (zeros (n := 64))))))

#check (fun (k159_a : BitVec 64) (k159_b : BitVec 64) => ((if (((BitVec.toNatInt k159_b) == 0) : Bool) then (BitVec.toNatInt k159_a) else (Int.tmod (BitVec.toNatInt k159_a) (BitVec.toNatInt k159_b)))))

#check (fun (k160_a : BitVec 64) (k160_b : BitVec 64) => ((to_bits_truncate (l := 32) ((BitVec.toInt (Sail.BitVec.extractLsb k160_a 31 0)) *i (BitVec.toInt (Sail.BitVec.extractLsb k160_b 31 0))))))

#check (fun (k161_a : BitVec 64) (k161_b : BitVec 64) => (((if (((BitVec.toInt k161_b) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt k161_a) (BitVec.toInt k161_b))) ≥k161_b (2 ^i (xlen -i 1)))))

#check (fun (k162_a : BitVec 64) (k162_b : BitVec 64) => ((sign_extend (m := 64) (shift_bits_left (Sail.BitVec.extractLsb k162_a 31 0) (Sail.BitVec.extractLsb (Sail.BitVec.extractLsb k162_b 31 0) 4 0)))))

#check (fun (k163_a : BitVec 64) (k163_b : BitVec 64) => ((sign_extend (m := 64) (shift_bits_right (Sail.BitVec.extractLsb k163_a 31 0) (Sail.BitVec.extractLsb (Sail.BitVec.extractLsb k163_b 31 0) 4 0)))))

#check (fun (k164_a : BitVec 64) (k164_b : BitVec 64) => ((to_bits_truncate (l := 64) (if (((BitVec.toInt k164_b) == 0) : Bool) then (BitVec.toInt k164_a) else (Int.tmod (BitVec.toInt k164_a) (BitVec.toInt k164_b))))))

#check (fun (k165_a : BitVec 64) (k165_b : BitVec 64) => ((sign_extend (m := 64) (shift_bits_right_arith (Sail.BitVec.extractLsb k165_a 31 0) (Sail.BitVec.extractLsb (Sail.BitVec.extractLsb k165_b 31 0) 4 0)))))

#check (fun (k166_a : BitVec 64) (k166_b : BitVec 64) => ((to_bits_truncate (l := 64) (if (((BitVec.toNatInt k166_b) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toNatInt k166_a) (BitVec.toNatInt k166_b))))))

#check (fun (k167_a : BitVec 64) (k167_b : BitVec 64) => ((zero_extend (m := 64) (bool_to_bit ((k167_a &&& (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k167_b 5 0))) != (zeros (n := 64)))))))

#check (fun (k168_a : BitVec 64) (k168_b : BitVec 64) => ((to_bits_truncate (l := 64) (if (((BitVec.toNatInt k168_b) == 0) : Bool) then (BitVec.toNatInt k168_a) else (Int.tmod (BitVec.toNatInt k168_a) (BitVec.toNatInt k168_b))))))

#check (fun (k169_a : BitVec 64) (k169_b : BitVec 64) => ((sign_extend (m := 64) (to_bits_truncate (l := 32) ((BitVec.toInt (Sail.BitVec.extractLsb k169_a 31 0)) *i (BitVec.toInt (Sail.BitVec.extractLsb k169_b 31 0)))))))

#check (fun (k170_a : BitVec 64) (k170_b : BitVec 64) => ((if (((BitVec.toInt (Sail.BitVec.extractLsb k170_b 31 0)) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt (Sail.BitVec.extractLsb k170_a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb k170_b 31 0))))))

#check (fun (k171_a : BitVec 64) (k171_b : BitVec 64) => ((if (((BitVec.toNatInt (Sail.BitVec.extractLsb k171_b 31 0)) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toNatInt (Sail.BitVec.extractLsb k171_a 31 0)) (BitVec.toNatInt (Sail.BitVec.extractLsb k171_b 31 0))))))

#check (fun (k172_a : BitVec 64) (k172_b : BitVec 64) => (((if (((BitVec.toInt (Sail.BitVec.extractLsb k172_b 31 0)) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt (Sail.BitVec.extractLsb k172_a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb k172_b 31 0)))) ≥k172_b (2 ^i 31))))

#check (fun (k173_a : BitVec 64) (k173_b : BitVec 64) => ((if (((BitVec.toInt (Sail.BitVec.extractLsb k173_b 31 0)) == 0) : Bool) then (BitVec.toInt (Sail.BitVec.extractLsb k173_a 31 0)) else (Int.tmod (BitVec.toInt (Sail.BitVec.extractLsb k173_a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb k173_b 31 0))))))

#check (fun (k174_a : BitVec 64) (k174_b : BitVec 64) => ((to_bits_truncate (l := 32) (if (((BitVec.toNatInt (Sail.BitVec.extractLsb k174_b 31 0)) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toNatInt (Sail.BitVec.extractLsb k174_a 31 0)) (BitVec.toNatInt (Sail.BitVec.extractLsb k174_b 31 0)))))))

#check (fun (k175_a : BitVec 64) (k175_b : BitVec 64) => ((if (((BitVec.toNatInt (Sail.BitVec.extractLsb k175_b 31 0)) == 0) : Bool) then (BitVec.toNatInt (Sail.BitVec.extractLsb k175_a 31 0)) else (Int.tmod (BitVec.toNatInt (Sail.BitVec.extractLsb k175_a 31 0)) (BitVec.toNatInt (Sail.BitVec.extractLsb k175_b 31 0))))))

#check (fun (k176_a : BitVec 64) (k176_b : BitVec 64) => ((sign_extend (m := 64) (to_bits_truncate (l := 32) (if (((BitVec.toNatInt (Sail.BitVec.extractLsb k176_b 31 0)) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toNatInt (Sail.BitVec.extractLsb k176_a 31 0)) (BitVec.toNatInt (Sail.BitVec.extractLsb k176_b 31 0))))))))

#check (fun (k177_a : BitVec 64) (k177_b : BitVec 64) => ((to_bits_truncate (l := 32) (if (((BitVec.toInt (Sail.BitVec.extractLsb k177_b 31 0)) == 0) : Bool) then (BitVec.toInt (Sail.BitVec.extractLsb k177_a 31 0)) else (Int.tmod (BitVec.toInt (Sail.BitVec.extractLsb k177_a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb k177_b 31 0)))))))

#check (fun (k178_a : BitVec 64) (k178_b : BitVec 64) => ((to_bits_truncate (l := 32) (if (((BitVec.toNatInt (Sail.BitVec.extractLsb k178_b 31 0)) == 0) : Bool) then (BitVec.toNatInt (Sail.BitVec.extractLsb k178_a 31 0)) else (Int.tmod (BitVec.toNatInt (Sail.BitVec.extractLsb k178_a 31 0)) (BitVec.toNatInt (Sail.BitVec.extractLsb k178_b 31 0)))))))

#check (fun (k179_a : BitVec 64) (k179_b : BitVec 64) => ((sign_extend (m := 64) (to_bits_truncate (l := 32) (if (((BitVec.toInt (Sail.BitVec.extractLsb k179_b 31 0)) == 0) : Bool) then (BitVec.toInt (Sail.BitVec.extractLsb k179_a 31 0)) else (Int.tmod (BitVec.toInt (Sail.BitVec.extractLsb k179_a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb k179_b 31 0))))))))

#check (fun (k180_a : BitVec 64) (k180_b : BitVec 64) => ((if (((if (((BitVec.toInt k180_b) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt k180_a) (BitVec.toInt k180_b))) ≥k180_b (2 ^i (xlen -i 1))) : Bool) then (Neg.neg (2 ^i (xlen -i 1))) else (if (((BitVec.toInt k180_b) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt k180_a) (BitVec.toInt k180_b))))))

#check (fun (k181_a : BitVec 64) (k181_b : BitVec 64) => ((sign_extend (m := 64) (to_bits_truncate (l := 32) (if (((BitVec.toNatInt (Sail.BitVec.extractLsb k181_b 31 0)) == 0) : Bool) then (BitVec.toNatInt (Sail.BitVec.extractLsb k181_a 31 0)) else (Int.tmod (BitVec.toNatInt (Sail.BitVec.extractLsb k181_a 31 0)) (BitVec.toNatInt (Sail.BitVec.extractLsb k181_b 31 0))))))))

#check (fun (k182_a : BitVec 64) (k182_b : BitVec 64) => ((to_bits_truncate (l := 64) (if (((if (((BitVec.toInt k182_b) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt k182_a) (BitVec.toInt k182_b))) ≥k182_b (2 ^i (xlen -i 1))) : Bool) then (Neg.neg (2 ^i (xlen -i 1))) else (if (((BitVec.toInt k182_b) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt k182_a) (BitVec.toInt k182_b)))))))

#check (fun (k183_a : BitVec 64) (k183_b : BitVec 64) => ((if (((if (((BitVec.toInt (Sail.BitVec.extractLsb k183_b 31 0)) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt (Sail.BitVec.extractLsb k183_a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb k183_b 31 0)))) ≥k183_b (2 ^i 31)) : Bool) then (Neg.neg (2 ^i 31)) else (if (((BitVec.toInt (Sail.BitVec.extractLsb k183_b 31 0)) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt (Sail.BitVec.extractLsb k183_a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb k183_b 31 0)))))))

#check (fun (k184_a : BitVec 64) (k184_b : BitVec 64) => ((to_bits_truncate (l := 32) (if (((if (((BitVec.toInt (Sail.BitVec.extractLsb k184_b 31 0)) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt (Sail.BitVec.extractLsb k184_a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb k184_b 31 0)))) ≥k184_b (2 ^i 31)) : Bool) then (Neg.neg (2 ^i 31)) else (if (((BitVec.toInt (Sail.BitVec.extractLsb k184_b 31 0)) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt (Sail.BitVec.extractLsb k184_a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb k184_b 31 0))))))))

#check (fun (k185_a : BitVec 64) (k185_b : BitVec 64) => ((sign_extend (m := 64) (to_bits_truncate (l := 32) (if (((if (((BitVec.toInt (Sail.BitVec.extractLsb k185_b 31 0)) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt (Sail.BitVec.extractLsb k185_a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb k185_b 31 0)))) ≥k185_b (2 ^i 31)) : Bool) then (Neg.neg (2 ^i 31)) else (if (((BitVec.toInt (Sail.BitVec.extractLsb k185_b 31 0)) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt (Sail.BitVec.extractLsb k185_a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb k185_b 31 0)))))))))

end Functions
end LeanIM
end
