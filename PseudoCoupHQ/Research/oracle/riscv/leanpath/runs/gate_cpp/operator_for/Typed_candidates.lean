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

#check (fun (k026_a : BitVec 64) => (((k026_a >>> 2) ^^^ (k026_a <<< 4))))

#check (fun (k027_a : BitVec 64) => ((Complement.complement k027_a)))

#check (fun (k028_a : BitVec 64) => (((k028_a <<< 18) ^^^ (k028_a <<< 14))))

#check (fun (k029_a : BitVec 64) => (((k029_a <<< 25) ^^^ (k029_a <<< 24))))

#check (fun (k030_a : BitVec 64) => (((k030_a <<< 26) ^^^ (k030_a <<< 13))))

#check (fun (k031_a : BitVec 64) => (((k031_a <<< 31) ^^^ (k031_a <<< 24))))

#check (fun (k032_a : BitVec 64) => (((k032_a >>> 29) ^^^ (k032_a <<< 13))))

#check (fun (k033_a : BitVec 64) => ((BitVec.countLeadingZeros k033_a)))

#check (fun (k034_a : BitVec 64) => ((BitVec.countTrailingZeros k034_a)))

#check (fun (k035_a : BitVec 64) => ((Sail.BitVec.extractLsb k035_a 4 0)))

#check (fun (k036_a : BitVec 64) => ((Sail.BitVec.extractLsb k036_a 5 0)))

#check (fun (k037_a : BitVec 64) => ((Sail.BitVec.extractLsb k037_a 7 0)))

#check (fun (k038_a : BitVec 64) => ((Sail.BitVec.extractLsb k038_a 15 0)))

#check (fun (k039_a : BitVec 64) => ((Sail.BitVec.extractLsb k039_a 31 0)))

#check (fun (k040_a : BitVec 64) => (((k040_a >>> 7) ^^^ ((k040_a >>> 2) ^^^ (k040_a <<< 4)))))

#check (fun (k041_a : BitVec 64) => (((k041_a >>> 9) ^^^ ((k041_a <<< 18) ^^^ (k041_a <<< 14)))))

#check (fun (k042_a : BitVec 64) => (((k042_a <<< 31) ^^^ ((k042_a <<< 25) ^^^ (k042_a <<< 24)))))

#check (fun (k043_a : BitVec 64) => (((k043_a >>> 29) ^^^ ((k043_a <<< 26) ^^^ (k043_a <<< 13)))))

#check (fun (k044_a : BitVec 64) => ((Sail.BitVec.extractLsb k044_a (log2_xlen -i 1) 0)))

#check (fun (k045_a : BitVec 64) => ((BitVec.toInt (Sail.BitVec.extractLsb k045_a 31 0))))

#check (fun (k046_a : BitVec 64) => ((to_bits (l := 64) (BitVec.countLeadingZeros k046_a))))

#check (fun (k047_a : BitVec 64) => ((BitVec.toNatInt (Sail.BitVec.extractLsb k047_a 31 0))))

#check (fun (k048_a : BitVec 64) => ((to_bits (l := 64) (BitVec.countTrailingZeros k048_a))))

#check (fun (k049_a : BitVec 64) => ((Sail.BitVec.extractLsb k049_a ((xlen_bytes *i 4) -i 1) 0)))

#check (fun (k050_a : BitVec 64) => ((sign_extend (m := 64) (Sail.BitVec.extractLsb k050_a 7 0))))

#check (fun (k051_a : BitVec 64) => ((zero_extend (m := 64) (Sail.BitVec.extractLsb k051_a 7 0))))

#check (fun (k052_a : BitVec 64) => ((sign_extend (m := 64) (Sail.BitVec.extractLsb k052_a 15 0))))

#check (fun (k053_a : BitVec 64) => ((zero_extend (m := 64) (Sail.BitVec.extractLsb k053_a 15 0))))

#check (fun (k054_a : BitVec 64) => ((zero_extend (m := 64) (Sail.BitVec.extractLsb k054_a 31 0))))

#check (fun (k055_a : BitVec 64) => ((BitVec.countLeadingZeros (Sail.BitVec.extractLsb k055_a 31 0))))

#check (fun (k056_a : BitVec 64) => ((BitVec.countTrailingZeros (Sail.BitVec.extractLsb k056_a 31 0))))

#check (fun (k057_a : BitVec 64) => ((Sail.BitVec.extractLsb (Sail.BitVec.extractLsb k057_a 31 0) 4 0)))

#check (fun (k058_a : BitVec 64) => ((shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k058_a 5 0))))

#check (fun (k059_a : BitVec 64) => ((to_bits (l := 64) (BitVec.countLeadingZeros (Sail.BitVec.extractLsb k059_a 31 0)))))

#check (fun (k060_a : BitVec 64) => ((to_bits (l := 64) (BitVec.countTrailingZeros (Sail.BitVec.extractLsb k060_a 31 0)))))

#check (fun (k061_a : BitVec 64) => ((Complement.complement (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k061_a 5 0)))))

#check (fun (k062_a : BitVec 64) (k062_b : BitVec 64) => ((k062_a + k062_b)))

#check (fun (k063_a : BitVec 64) (k063_b : BitVec 64) => ((k063_a - k063_b)))

#check (fun (k064_a : BitVec 64) (k064_b : BitVec 64) => ((k064_a &&& k064_b)))

#check (fun (k065_a : BitVec 64) (k065_b : BitVec 64) => ((k065_a ^^^ k065_b)))

#check (fun (k066_a : BitVec 64) (k066_b : BitVec 64) => ((k066_a ||| k066_b)))

#check (fun (k067_a : BitVec 64) (k067_b : BitVec 64) => ((zopz0zI_s k067_a k067_b)))

#check (fun (k068_a : BitVec 64) (k068_b : BitVec 64) => ((zopz0zI_u k068_a k068_b)))

#check (fun (k069_a : BitVec 64) (k069_b : BitVec 64) => ((zopz0zK_s k069_a k069_b)))

#check (fun (k070_a : BitVec 64) (k070_b : BitVec 64) => ((zopz0zK_u k070_a k070_b)))

#check (fun (k071_a : BitVec 64) (k071_b : BitVec 64) => ((carryless_mul k071_a k071_b)))

#check (fun (k072_a : BitVec 64) (k072_b : BitVec 64) => ((carryless_mulr k072_a k072_b)))

#check (fun (k073_a : BitVec 64) (k073_b : BitVec 64) => ((bool_to_bit (zopz0zI_s k073_a k073_b))))

#check (fun (k074_a : BitVec 64) (k074_b : BitVec 64) => ((bool_to_bit (zopz0zI_u k074_a k074_b))))

#check (fun (k075_a : BitVec 64) (k075_b : BitVec 64) => ((Complement.complement (k075_a ^^^ k075_b))))

#check (fun (k076_a : BitVec 64) (k076_b : BitVec 64) => ((k076_a &&& (Complement.complement k076_b))))

#check (fun (k077_a : BitVec 64) (k077_b : BitVec 64) => ((k077_a ||| (Complement.complement k077_b))))

#check (fun (k078_a : BitVec 64) (k078_b : BitVec 64) => (((k078_a >>> 8) ^^^ ((k078_b <<< 31) ^^^ (k078_b <<< 24)))))

#check (fun (k079_a : BitVec 64) (k079_b : BitVec 64) => ((if ((zopz0zI_s k079_a k079_b) : Bool) then k079_a else k079_b)))

#check (fun (k080_a : BitVec 64) (k080_b : BitVec 64) => ((if ((zopz0zI_u k080_a k080_b) : Bool) then k080_a else k080_b)))

#check (fun (k081_a : BitVec 64) (k081_b : BitVec 64) => ((if ((zopz0zK_s k081_a k081_b) : Bool) then k081_a else k081_b)))

#check (fun (k082_a : BitVec 64) (k082_b : BitVec 64) => ((if ((zopz0zK_u k082_a k082_b) : Bool) then k082_a else k082_b)))

#check (fun (k083_a : BitVec 64) (k083_b : BitVec 64) => (((k083_a >>> 19) ^^^ ((k083_b >>> 29) ^^^ (k083_b <<< 13)))))

#check (fun (k084_a : BitVec 64) (k084_b : BitVec 64) => ((zero_extend (m := 64) (bool_to_bit (zopz0zI_s k084_a k084_b)))))

#check (fun (k085_a : BitVec 64) (k085_b : BitVec 64) => ((zero_extend (m := 64) (bool_to_bit (zopz0zI_u k085_a k085_b)))))

#check (fun (k086_a : BitVec 64) (k086_b : BitVec 64) => (((k086_a >>> 28) ^^^ ((k086_b >>> 7) ^^^ ((k086_b >>> 2) ^^^ (k086_b <<< 4))))))

#check (fun (k087_a : BitVec 64) (k087_b : BitVec 64) => ((Sail.BitVec.extractLsb (carryless_mul k087_a k087_b) (xlen -i 1) 0)))

#check (fun (k088_a : BitVec 64) (k088_b : BitVec 64) => (((k088_a >>> 7) ^^^ ((k088_a >>> 8) ^^^ ((k088_b <<< 31) ^^^ (k088_b <<< 24))))))

#check (fun (k089_a : BitVec 64) (k089_b : BitVec 64) => (((k089_a >>> 18) ^^^ ((k089_b >>> 9) ^^^ ((k089_b <<< 18) ^^^ (k089_b <<< 14))))))

#check (fun (k090_a : BitVec 64) (k090_b : BitVec 64) => (((k090_a >>> 6) ^^^ ((k090_a >>> 19) ^^^ ((k090_b >>> 29) ^^^ (k090_b <<< 13))))))

#check (fun (k091_a : BitVec 64) (k091_b : BitVec 64) => (((k091_a >>> 8) ^^^ ((k091_b <<< 31) ^^^ ((k091_b <<< 25) ^^^ (k091_b <<< 24))))))

#check (fun (k092_a : BitVec 64) (k092_b : BitVec 64) => (((k092_a >>> 19) ^^^ ((k092_b >>> 29) ^^^ ((k092_b <<< 26) ^^^ (k092_b <<< 13))))))

#check (fun (k093_a : BitVec 64) (k093_b : BitVec 64) => ((shift_bits_left k093_a (Sail.BitVec.extractLsb k093_b (log2_xlen -i 1) 0))))

#check (fun (k094_a : BitVec 64) (k094_b : BitVec 64) => ((rotate_bits_left k094_a (Sail.BitVec.extractLsb k094_b (log2_xlen -i 1) 0))))

#check (fun (k095_a : BitVec 64) (k095_b : BitVec 64) => ((shift_bits_right k095_a (Sail.BitVec.extractLsb k095_b (log2_xlen -i 1) 0))))

#check (fun (k096_a : BitVec 64) (k096_b : BitVec 64) => (((Sail.BitVec.extractLsb k096_a 31 0) + (Sail.BitVec.extractLsb k096_b 31 0))))

#check (fun (k097_a : BitVec 64) (k097_b : BitVec 64) => (((Sail.BitVec.extractLsb k097_a 31 0) - (Sail.BitVec.extractLsb k097_b 31 0))))

#check (fun (k098_a : BitVec 64) (k098_b : BitVec 64) => (((Sail.BitVec.extractLsb k098_a 7 0) +++ (Sail.BitVec.extractLsb k098_b 7 0))))

#check (fun (k099_a : BitVec 64) (k099_b : BitVec 64) => ((rotate_bits_right k099_a (Sail.BitVec.extractLsb k099_b (log2_xlen -i 1) 0))))

#check (fun (k100_a : BitVec 64) (k100_b : BitVec 64) => ((Sail.BitVec.extractLsb (carryless_mul k100_a k100_b) ((2 *i xlen) -i 1) xlen)))

#check (fun (k101_a : BitVec 64) (k101_b : BitVec 64) => ((shift_bits_right_arith k101_a (Sail.BitVec.extractLsb k101_b (log2_xlen -i 1) 0))))

#check (fun (k102_a : BitVec 64) (k102_b : BitVec 64) => (((k102_a <<< 30) ^^^ ((k102_a >>> 28) ^^^ ((k102_b >>> 7) ^^^ ((k102_b >>> 2) ^^^ (k102_b <<< 4)))))))

#check (fun (k103_a : BitVec 64) (k103_b : BitVec 64) => (((k103_a >>> 1) ^^^ ((k103_a >>> 7) ^^^ ((k103_a >>> 8) ^^^ ((k103_b <<< 31) ^^^ (k103_b <<< 24)))))))

#check (fun (k104_a : BitVec 64) (k104_b : BitVec 64) => (((k104_a <<< 3) ^^^ ((k104_a >>> 6) ^^^ ((k104_a >>> 19) ^^^ ((k104_b >>> 29) ^^^ (k104_b <<< 13)))))))

#check (fun (k105_a : BitVec 64) (k105_b : BitVec 64) => (((k105_a >>> 7) ^^^ ((k105_a >>> 8) ^^^ ((k105_b <<< 31) ^^^ ((k105_b <<< 25) ^^^ (k105_b <<< 24)))))))

#check (fun (k106_a : BitVec 64) (k106_b : BitVec 64) => (((k106_a >>> 14) ^^^ ((k106_a >>> 18) ^^^ ((k106_b >>> 9) ^^^ ((k106_b <<< 18) ^^^ (k106_b <<< 14)))))))

#check (fun (k107_a : BitVec 64) (k107_b : BitVec 64) => (((k107_a >>> 6) ^^^ ((k107_a >>> 19) ^^^ ((k107_b >>> 29) ^^^ ((k107_b <<< 26) ^^^ (k107_b <<< 13)))))))

#check (fun (k108_a : BitVec 64) (k108_b : BitVec 64) => ((rotate_bits_left (Sail.BitVec.extractLsb k108_a 31 0) (Sail.BitVec.extractLsb k108_b 4 0))))

#check (fun (k109_a : BitVec 64) (k109_b : BitVec 64) => ((rotate_bits_right (Sail.BitVec.extractLsb k109_a 31 0) (Sail.BitVec.extractLsb k109_b 4 0))))

#check (fun (k110_a : BitVec 64) (k110_b : BitVec 64) => ((k110_a &&& (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k110_b 5 0)))))

#check (fun (k111_a : BitVec 64) (k111_b : BitVec 64) => ((k111_a ^^^ (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k111_b 5 0)))))

#check (fun (k112_a : BitVec 64) (k112_b : BitVec 64) => ((k112_a ||| (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k112_b 5 0)))))

#check (fun (k113_a : BitVec 64) (k113_b : BitVec 64) => ((mult_to_bits_half (l := xlen) mul_op.signed_rs1 mul_op.signed_rs2 k113_a k113_b mul_op.result_part)))

#check (fun (k114_a : BitVec 64) (k114_b : BitVec 64) => ((zero_extend (m := 64) ((Sail.BitVec.extractLsb k114_a 7 0) +++ (Sail.BitVec.extractLsb k114_b 7 0)))))

#check (fun (k115_a : BitVec 64) (k115_b : BitVec 64) => (((k115_a <<< 25) ^^^ ((k115_a <<< 30) ^^^ ((k115_a >>> 28) ^^^ ((k115_b >>> 7) ^^^ ((k115_b >>> 2) ^^^ (k115_b <<< 4))))))))

#check (fun (k116_a : BitVec 64) (k116_b : BitVec 64) => (((k116_a >>> 1) ^^^ ((k116_a >>> 7) ^^^ ((k116_a >>> 8) ^^^ ((k116_b <<< 31) ^^^ ((k116_b <<< 25) ^^^ (k116_b <<< 24))))))))

#check (fun (k117_a : BitVec 64) (k117_b : BitVec 64) => (((k117_a <<< 3) ^^^ ((k117_a >>> 6) ^^^ ((k117_a >>> 19) ^^^ ((k117_b >>> 29) ^^^ ((k117_b <<< 26) ^^^ (k117_b <<< 13))))))))

#check (fun (k118_a : BitVec 64) (k118_b : BitVec 64) => (((k118_a <<< 23) ^^^ ((k118_a >>> 14) ^^^ ((k118_a >>> 18) ^^^ ((k118_b >>> 9) ^^^ ((k118_b <<< 18) ^^^ (k118_b <<< 14))))))))

#check (fun (k119_a : BitVec 64) (k119_b : BitVec 64) => (((BitVec.toInt (Sail.BitVec.extractLsb k119_a 31 0)) *i (BitVec.toInt (Sail.BitVec.extractLsb k119_b 31 0)))))

#check (fun (k120_a : BitVec 64) (k120_b : BitVec 64) => ((sign_extend (m := 64) ((k120_a >>> 1) ^^^ ((k120_a >>> 7) ^^^ ((k120_a >>> 8) ^^^ ((k120_b <<< 31) ^^^ (k120_b <<< 24))))))))

#check (fun (k121_a : BitVec 64) (k121_b : BitVec 64) => ((sign_extend (m := 64) ((k121_a <<< 3) ^^^ ((k121_a >>> 6) ^^^ ((k121_a >>> 19) ^^^ ((k121_b >>> 29) ^^^ (k121_b <<< 13))))))))

#check (fun (k122_a : BitVec 64) (k122_b : BitVec 64) => (((k122_a &&& (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k122_b 5 0))) != (zeros (n := 64)))))

#check (fun (k123_a : BitVec 64) (k123_b : BitVec 64) => ((k123_a &&& (Complement.complement (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k123_b 5 0))))))

#check (fun (k124_a : BitVec 64) (k124_b : BitVec 64) => ((shift_bits_left (Sail.BitVec.extractLsb k124_a 31 0) (Sail.BitVec.extractLsb (Sail.BitVec.extractLsb k124_b 31 0) 4 0))))

#check (fun (k125_a : BitVec 64) (k125_b : BitVec 64) => ((shift_bits_right (Sail.BitVec.extractLsb k125_a 31 0) (Sail.BitVec.extractLsb (Sail.BitVec.extractLsb k125_b 31 0) 4 0))))

#check (fun (k126_a : BitVec 64) (k126_b : BitVec 64) => (((Sail.BitVec.extractLsb k126_a ((xlen_bytes *i 4) -i 1) 0) +++ (Sail.BitVec.extractLsb k126_b ((xlen_bytes *i 4) -i 1) 0))))

#check (fun (k127_a : BitVec 64) (k127_b : BitVec 64) => ((sign_extend (m := 64) ((k127_a <<< 25) ^^^ ((k127_a <<< 30) ^^^ ((k127_a >>> 28) ^^^ ((k127_b >>> 7) ^^^ ((k127_b >>> 2) ^^^ (k127_b <<< 4)))))))))

#check (fun (k128_a : BitVec 64) (k128_b : BitVec 64) => ((sign_extend (m := 64) ((k128_a >>> 1) ^^^ ((k128_a >>> 7) ^^^ ((k128_a >>> 8) ^^^ ((k128_b <<< 31) ^^^ ((k128_b <<< 25) ^^^ (k128_b <<< 24)))))))))

#check (fun (k129_a : BitVec 64) (k129_b : BitVec 64) => ((shift_bits_right_arith (Sail.BitVec.extractLsb k129_a 31 0) (Sail.BitVec.extractLsb (Sail.BitVec.extractLsb k129_b 31 0) 4 0))))

#check (fun (k130_a : BitVec 64) (k130_b : BitVec 64) => ((sign_extend (m := 64) ((k130_a <<< 3) ^^^ ((k130_a >>> 6) ^^^ ((k130_a >>> 19) ^^^ ((k130_b >>> 29) ^^^ ((k130_b <<< 26) ^^^ (k130_b <<< 13)))))))))

#check (fun (k131_a : BitVec 64) (k131_b : BitVec 64) => ((sign_extend (m := 64) ((k131_a <<< 23) ^^^ ((k131_a >>> 14) ^^^ ((k131_a >>> 18) ^^^ ((k131_b >>> 9) ^^^ ((k131_b <<< 18) ^^^ (k131_b <<< 14)))))))))

#check (fun (k132_a : BitVec 64) (k132_b : BitVec 64) => ((bool_to_bit ((k132_a &&& (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k132_b 5 0))) != (zeros (n := 64))))))

#check (fun (k133_a : BitVec 64) (k133_b : BitVec 64) => ((to_bits_truncate (l := 32) ((BitVec.toInt (Sail.BitVec.extractLsb k133_a 31 0)) *i (BitVec.toInt (Sail.BitVec.extractLsb k133_b 31 0))))))

#check (fun (k134_a : BitVec 64) (k134_b : BitVec 64) => ((zero_extend (m := 64) (bool_to_bit ((k134_a &&& (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb k134_b 5 0))) != (zeros (n := 64)))))))

#check (fun (k135_a : BitVec 64) (k135_b : BitVec 64) => ((sign_extend (m := 64) (to_bits_truncate (l := 32) ((BitVec.toInt (Sail.BitVec.extractLsb k135_a 31 0)) *i (BitVec.toInt (Sail.BitVec.extractLsb k135_b 31 0)))))))

end Functions
end LeanIM
end
