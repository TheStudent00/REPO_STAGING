// probe 782 -- binary ...
#[no_mangle]
pub fn op_782(a: bool, b: u64) -> bool {
    a ... b
}
