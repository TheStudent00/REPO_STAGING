// probe 62 -- unary .await
#[no_mangle]
pub fn op_62(a: u64) -> u64 {
    a.await
}
