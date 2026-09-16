// probe 551 -- binary +
#[no_mangle]
pub fn op_551(a: u64, b: bool) -> <u64 as core::ops::Add<bool>>::Output {
    a + b
}
