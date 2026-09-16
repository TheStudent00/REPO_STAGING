; ModuleID = 'v_loc.ll'
source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"

; Function Attrs: minsize nounwind optsize
define dso_local zeroext i1 @f64_le_value(i64 %0, i64 %1) local_unnamed_addr #0 {
  %3 = and i64 %0, 9218868437227405312
  %4 = icmp ne i64 %3, 9218868437227405312
  %5 = and i64 %0, 4503599627370495
  %6 = icmp eq i64 %5, 0
  %7 = or i1 %4, %6
  br i1 %7, label %8, label %f64_le.exit

8:                                                ; preds = %2
  %9 = and i64 %1, 9218868437227405312
  %10 = icmp ne i64 %9, 9218868437227405312
  %11 = and i64 %1, 4503599627370495
  %12 = icmp eq i64 %11, 0
  %13 = or i1 %10, %12
  br i1 %13, label %14, label %f64_le.exit

14:                                               ; preds = %8
  %15 = xor i64 %1, %0
  %16 = icmp sgt i64 %15, -1
  br i1 %16, label %23, label %17

17:                                               ; preds = %14
  %18 = icmp slt i64 %0, 0
  %19 = and i64 %1, 9223372036854775807
  %20 = or i64 %19, %0
  %21 = icmp eq i64 %20, 0
  %22 = select i1 %18, i1 true, i1 %21
  br label %f64_le.exit

23:                                               ; preds = %14
  %24 = icmp eq i64 %0, %1
  %25 = icmp ult i64 %0, %1
  %26 = icmp slt i64 %0, 0
  %27 = xor i1 %26, %25
  %28 = or i1 %24, %27
  br label %f64_le.exit

f64_le.exit:                                      ; preds = %2, %8, %23, %17
  %29 = phi i1 [ %22, %17 ], [ %28, %23 ], [ false, %8 ], [ false, %2 ]
  ret i1 %29
}

attributes #0 = { minsize nounwind optsize "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="generic-rv64" "target-features"="+64bit,+m,+relax,+zmmul,-a,-b,-c,-d,-e,-experimental-p,-experimental-smctr,-experimental-ssctr,-experimental-svukte,-experimental-xqccmp,-experimental-xqcia,-experimental-xqciac,-experimental-xqcibi,-experimental-xqcibm,-experimental-xqcicli,-experimental-xqcicm,-experimental-xqcics,-experimental-xqcicsr,-experimental-xqciint,-experimental-xqciio,-experimental-xqcilb,-experimental-xqcili,-experimental-xqcilia,-experimental-xqcilo,-experimental-xqcilsm,-experimental-xqcisim,-experimental-xqcisls,-experimental-xqcisync,-experimental-xrivosvisni,-experimental-xrivosvizip,-experimental-xsfmclic,-experimental-xsfsclic,-experimental-zalasr,-experimental-zicfilp,-experimental-zicfiss,-experimental-zvbc32e,-experimental-zvkgs,-experimental-zvqdotq,-f,-h,-q,-sdext,-sdtrig,-sha,-shcounterenw,-shgatpa,-shlcofideleg,-shtvala,-shvsatpa,-shvstvala,-shvstvecd,-smaia,-smcdeleg,-smcntrpmf,-smcsrind,-smdbltrp,-smepmp,-smmpm,-smnpm,-smrnmi,-smstateen,-ssaia,-ssccfg,-ssccptr,-sscofpmf,-sscounterenw,-sscsrind,-ssdbltrp,-ssnpm,-sspm,-ssqosid,-ssstateen,-ssstrict,-sstc,-sstvala,-sstvecd,-ssu64xl,-supm,-svade,-svadu,-svbare,-svinval,-svnapot,-svpbmt,-svvptc,-v,-xandesbfhcvt,-xandesperf,-xandesvbfhcvt,-xandesvdot,-xandesvpackfph,-xandesvsintload,-xcvalu,-xcvbi,-xcvbitmanip,-xcvelw,-xcvmac,-xcvmem,-xcvsimd,-xmipscbop,-xmipscmov,-xmipslsp,-xsfcease,-xsfmm128t,-xsfmm16t,-xsfmm32a16f,-xsfmm32a32f,-xsfmm32a8f,-xsfmm32a8i,-xsfmm32t,-xsfmm64a64f,-xsfmm64t,-xsfmmbase,-xsfvcp,-xsfvfnrclipxfqf,-xsfvfwmaccqqq,-xsfvqmaccdod,-xsfvqmaccqoq,-xsifivecdiscarddlone,-xsifivecflushdlone,-xtheadba,-xtheadbb,-xtheadbs,-xtheadcmo,-xtheadcondmov,-xtheadfmemidx,-xtheadmac,-xtheadmemidx,-xtheadmempair,-xtheadsync,-xtheadvdot,-xventanacondops,-xwchc,-za128rs,-za64rs,-zaamo,-zabha,-zacas,-zalrsc,-zama16b,-zawrs,-zba,-zbb,-zbc,-zbkb,-zbkc,-zbkx,-zbs,-zca,-zcb,-zcd,-zce,-zcf,-zclsd,-zcmop,-zcmp,-zcmt,-zdinx,-zfa,-zfbfmin,-zfh,-zfhmin,-zfinx,-zhinx,-zhinxmin,-zic64b,-zicbom,-zicbop,-zicboz,-ziccamoa,-ziccamoc,-ziccif,-zicclsm,-ziccrse,-zicntr,-zicond,-zicsr,-zifencei,-zihintntl,-zihintpause,-zihpm,-zilsd,-zimop,-zk,-zkn,-zknd,-zkne,-zknh,-zkr,-zks,-zksed,-zksh,-zkt,-ztso,-zvbb,-zvbc,-zve32f,-zve32x,-zve64d,-zve64f,-zve64x,-zvfbfmin,-zvfbfwma,-zvfh,-zvfhmin,-zvkb,-zvkg,-zvkn,-zvknc,-zvkned,-zvkng,-zvknha,-zvknhb,-zvks,-zvksc,-zvksed,-zvksg,-zvksh,-zvkt,-zvl1024b,-zvl128b,-zvl16384b,-zvl2048b,-zvl256b,-zvl32768b,-zvl32b,-zvl4096b,-zvl512b,-zvl64b,-zvl65536b,-zvl8192b" }

!llvm.ident = !{!0, !0, !0, !0}
!llvm.module.flags = !{!1, !2, !3, !5}

!0 = !{!"Ubuntu clang version 21.1.8 (6ubuntu1)"}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 1, !"target-abi", !"lp64"}
!3 = distinct !{i32 6, !"riscv-isa", !4}
!4 = distinct !{!"rv64i2p1_m2p0_zmmul1p0"}
!5 = !{i32 8, !"SmallDataLimit", i32 0}
