// probe 536 -- binary +
#[no_mangle]
pub fn op_536(a: i32, b: u64) -> <i32 as core::ops::Add<u64>>::Output {
    a + b
}
