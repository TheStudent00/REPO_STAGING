// probe 780 -- binary ...
#[no_mangle]
pub fn op_780(a: bool, b: i32) -> bool {
    a ... b
}
