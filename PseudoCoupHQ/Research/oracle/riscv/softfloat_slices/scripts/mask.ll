source_filename = "llvm-link"
target datalayout = "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128"
target triple = "riscv64-unknown-unknown-elf"
define dso_local zeroext i1 @f64_le_mask(i64 %0, i64 %1) local_unnamed_addr {
  %3 = and i64 %0, 9218868437227405312
  %4 = icmp ne i64 %3, 9218868437227405312
  %5 = and i64 %0, 4503599627370495
  %6 = icmp eq i64 %5, 0
  %7 = or i1 %4, %6
  %9 = and i64 %1, 9218868437227405312
  %10 = icmp ne i64 %9, 9218868437227405312
  %11 = and i64 %1, 4503599627370495
  %12 = icmp eq i64 %11, 0
  %13 = or i1 %10, %12
  %15 = xor i64 %1, %0
  %16 = icmp sgt i64 %15, -1
  %18 = icmp slt i64 %0, 0
  %19 = and i64 %1, 9223372036854775807
  %20 = or i64 %19, %0
  %21 = icmp eq i64 %20, 0
  %22 = or i1 %18, %21
  %24 = icmp eq i64 %0, %1
  %25 = icmp ult i64 %0, %1
  %26 = icmp slt i64 %0, 0
  %27 = xor i1 %26, %25
  %28 = or i1 %24, %27
  ; select as mask arithmetic: (a & m) | (b & ~m)
  %nm = xor i1 %16, true
  %ia = and i1 %28, %16
  %ib = and i1 %22, %nm
  %in = or i1 %ia, %ib
  %md = and i1 %in, %13
  %rs = and i1 %md, %7
  ret i1 %rs
}
