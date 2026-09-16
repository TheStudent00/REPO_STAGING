// probe 224 -- binary ^
#[no_mangle]
pub fn op_224(a: u64, b: u64) -> <u64 as core::ops::BitXor<u64>>::Output {
    a ^ b
}


#[no_mangle]
pub extern "C" fn emu_RTYPE__XOR(a: u64, b: u64) -> u64 {
    ((op_224((a) as u64, (b) as u64)) as u64)
}
