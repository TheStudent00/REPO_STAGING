// probe 65 -- unary .await
#[no_mangle]
pub fn op_65(a: bool) -> bool {
    a.await
}
