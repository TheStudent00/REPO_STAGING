
use std::collections::BTreeSet;
use std::panic;

#[derive(Clone, Copy)]
enum Want { None, Int(i128), Wide, Bool(bool) }

fn wantv(op: &str, a: i128, b: i128) -> Want {
    match op {
        "+" => match a.checked_add(b) { Some(v) => Want::Int(v), None => Want::Wide },
        "-" => match a.checked_sub(b) { Some(v) => Want::Int(v), None => Want::Wide },
        "*" => match a.checked_mul(b) { Some(v) => Want::Int(v), None => Want::Wide },
        "<" => Want::Bool(a < b),
        "<=" => Want::Bool(a <= b),
        ">" => Want::Bool(a > b),
        ">=" => Want::Bool(a >= b),
        "==" => Want::Bool(a == b),
        "!=" => Want::Bool(a != b),
        _ => Want::None,
    }
}

pub enum Got { I(i128), B(bool), F(f64), Other }

pub trait Val { fn got(&self) -> Got; fn tn(&self) -> &'static str; }
impl Val for i32 { fn got(&self) -> Got { Got::I(*self as i128) } fn tn(&self) -> &'static str { "i32" } }
impl Val for i64 { fn got(&self) -> Got { Got::I(*self as i128) } fn tn(&self) -> &'static str { "i64" } }
impl Val for u64 { fn got(&self) -> Got { Got::I(*self as i128) } fn tn(&self) -> &'static str { "u64" } }
impl Val for i128 { fn got(&self) -> Got { Got::I(*self) } fn tn(&self) -> &'static str { "i128" } }
impl Val for u128 { fn got(&self) -> Got { Got::Other } fn tn(&self) -> &'static str { "u128" } }
impl Val for bool { fn got(&self) -> Got { Got::B(*self) } fn tn(&self) -> &'static str { "bool" } }
impl Val for f64 { fn got(&self) -> Got { Got::F(*self) } fn tn(&self) -> &'static str { "f64" } }
impl Val for f32 { fn got(&self) -> Got { Got::F(*self as f64) } fn tn(&self) -> &'static str { "f32" } }
impl Val for u32 { fn got(&self) -> Got { Got::I(*self as i128) } fn tn(&self) -> &'static str { "u32" } }

pub fn fidv(g: Got, op: &str, a: i128, b: i128) -> &'static str {
    let w = wantv(op, a, b);
    match (w, g) {
        (Want::None, _) => "na",
        (Want::Bool(wb), Got::B(gb)) => if wb == gb { "exact" } else { "inexact" },
        (Want::Bool(_), _) => "na",
        (_, Got::B(_)) => "na",
        (Want::Wide, Got::I(_)) => "inexact",
        (Want::Wide, Got::F(_)) => "inexact",
        (Want::Int(wv), Got::I(gv)) => if wv == gv { "exact" } else { "inexact" },
        (Want::Int(wv), Got::F(f)) => {
            if f.is_nan() || f.is_infinite() { "na" }
            else if f != f.floor() { "inexact" }
            else if (f as i128) == wv { "exact" } else { "inexact" }
        }
        (_, Got::Other) => "na",
    }
}

pub fn sigof<T: Val>(r: T, op: &str, a: i128, b: i128) -> String {
    format!("answer|{}|{}", r.tn(), fidv(r.got(), op, a, b))
}

type TFN = fn(u128, i128, i128) -> String;

fn bisect(tid: i32, f: TFN, op: &str, lov: u128, hiv: u128, fixv: u128,
          vary_is_lhs: bool) -> i32 {
    let fx = fixv as i128;
    let s = |c: u128| -> String {
        let a = if vary_is_lhs { c as i128 } else { fx };
        let b = if vary_is_lhs { fx } else { c as i128 };
        match panic::catch_unwind(|| f(c, a, b)) {
            Ok(v) => v,
            Err(_) => "raise|panic|na".to_string(),
        }
    };
    let mut lo = lov;
    let mut hi = hiv;
    let slo = s(lo);
    let shi = s(hi);
    let mut probes = 2;
    if slo == shi {
        println!("N|{}|{}|{}", tid, slo, shi);
        return probes;
    }
    let mut other: BTreeSet<String> = BTreeSet::new();
    while hi - lo > 1 {
        let mid = lo + (hi - lo) / 2;
        let sm = s(mid);
        probes += 1;
        if sm == slo { lo = mid; }
        else {
            if sm != shi { other.insert(sm); }
            hi = mid;
        }
    }
    let o: Vec<String> = other.into_iter().collect();
    println!("B|{}|{}|{}|{}|{}|{}|{}", tid, lo, hi, slo, shi, probes,
             o.join(";"));
    probes
}
fn t82(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 42;
    sigof(((((c) as i64)) + (f)), "+", a, b)
}
fn t83(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 42;
    sigof(((((c) as i64)) * (f)), "*", a, b)
}
fn t84(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9223372036854775807;
    sigof(((((c) as i64)) + (f)), "+", a, b)
}
fn t85(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9223372036854775807;
    sigof(((((c) as i64)) * (f)), "*", a, b)
}
fn t86(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9007199254740993;
    sigof(((((c) as i64)) + (f)), "+", a, b)
}
fn t87(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9007199254740993;
    sigof(((((c) as i64)) * (f)), "*", a, b)
}
fn t88(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((((c) as u64)) + (f)), "+", a, b)
}
fn t89(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((((c) as u64)) - (f)), "-", a, b)
}
fn t90(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((((c) as u64)) * (f)), "*", a, b)
}
fn t91(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775807;
    sigof(((((c) as u64)) + (f)), "+", a, b)
}
fn t92(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775807;
    sigof(((((c) as u64)) - (f)), "-", a, b)
}
fn t93(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775807;
    sigof(((((c) as u64)) * (f)), "*", a, b)
}
fn t94(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775808;
    sigof(((((c) as u64)) * (f)), "*", a, b)
}
fn t95(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((((c) as u64)) + (f)), "+", a, b)
}
fn t96(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((((c) as u64)) - (f)), "-", a, b)
}
fn t97(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((((c) as u64)) * (f)), "*", a, b)
}
fn t98(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 18446744073709551615;
    sigof(((((c) as u64)) + (f)), "+", a, b)
}
fn t99(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 18446744073709551615;
    sigof(((((c) as u64)) - (f)), "-", a, b)
}
fn t100(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 18446744073709551615;
    sigof(((((c) as u64)) * (f)), "*", a, b)
}
fn t101(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 18446744073709551615;
    sigof(((((c) as i128)) * (f)), "*", a, b)
}
fn t102(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 42;
    sigof(((f) / (((c) as i32))), "/", a, b)
}
fn t103(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 42;
    sigof(((f) % (((c) as i32))), "%", a, b)
}
fn t104(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 42;
    sigof(((f) << (((c) as i32))), "<<", a, b)
}
fn t105(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 42;
    sigof(((f) >> (((c) as i32))), ">>", a, b)
}
fn t106(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 0;
    sigof(((f) / (((c) as i32))), "/", a, b)
}
fn t107(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 0;
    sigof(((f) % (((c) as i32))), "%", a, b)
}
fn t108(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 0;
    sigof(((f) << (((c) as i32))), "<<", a, b)
}
fn t109(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 0;
    sigof(((f) >> (((c) as i32))), ">>", a, b)
}
fn t110(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 42;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t111(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 42;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t112(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 0;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t113(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 0;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t114(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 42;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t115(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 42;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t116(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 0;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t117(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 0;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t118(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 42;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t119(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 42;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t120(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 0;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t121(c: u128, a: i128, b: i128) -> String {
    let f: i32 = 0;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t122(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 42;
    sigof(((f) + (((c) as i64))), "+", a, b)
}
fn t123(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 42;
    sigof(((f) * (((c) as i64))), "*", a, b)
}
fn t124(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 42;
    sigof(((f) / (((c) as i64))), "/", a, b)
}
fn t125(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 42;
    sigof(((f) % (((c) as i64))), "%", a, b)
}
fn t126(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 42;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t127(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 42;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t128(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 0;
    sigof(((f) / (((c) as i64))), "/", a, b)
}
fn t129(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 0;
    sigof(((f) % (((c) as i64))), "%", a, b)
}
fn t130(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 0;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t131(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 0;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t132(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9223372036854775807;
    sigof(((f) + (((c) as i64))), "+", a, b)
}
fn t133(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9223372036854775807;
    sigof(((f) * (((c) as i64))), "*", a, b)
}
fn t134(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9223372036854775807;
    sigof(((f) / (((c) as i64))), "/", a, b)
}
fn t135(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9223372036854775807;
    sigof(((f) % (((c) as i64))), "%", a, b)
}
fn t136(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9223372036854775807;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t137(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9223372036854775807;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t138(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9007199254740993;
    sigof(((f) + (((c) as i64))), "+", a, b)
}
fn t139(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9007199254740993;
    sigof(((f) * (((c) as i64))), "*", a, b)
}
fn t140(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9007199254740993;
    sigof(((f) / (((c) as i64))), "/", a, b)
}
fn t141(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9007199254740993;
    sigof(((f) % (((c) as i64))), "%", a, b)
}
fn t142(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9007199254740993;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t143(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9007199254740993;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t144(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 42;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t145(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 42;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t146(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 0;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t147(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 0;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t148(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9223372036854775807;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t149(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9223372036854775807;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t150(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9007199254740993;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t151(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9007199254740993;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t152(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 42;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t153(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 42;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t154(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 0;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t155(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 0;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t156(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9223372036854775807;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t157(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9223372036854775807;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t158(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9007199254740993;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t159(c: u128, a: i128, b: i128) -> String {
    let f: i64 = 9007199254740993;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t160(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t161(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t162(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 0;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t163(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 0;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t164(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775807;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t165(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775807;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t166(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775808;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t167(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775808;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t168(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t169(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t170(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 18446744073709551615;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t171(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 18446744073709551615;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t172(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((f) + (((c) as u64))), "+", a, b)
}
fn t173(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((f) - (((c) as u64))), "-", a, b)
}
fn t174(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((f) * (((c) as u64))), "*", a, b)
}
fn t175(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((f) / (((c) as u64))), "/", a, b)
}
fn t176(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((f) % (((c) as u64))), "%", a, b)
}
fn t177(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t178(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t179(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 0;
    sigof(((f) - (((c) as u64))), "-", a, b)
}
fn t180(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 0;
    sigof(((f) / (((c) as u64))), "/", a, b)
}
fn t181(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 0;
    sigof(((f) % (((c) as u64))), "%", a, b)
}
fn t182(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 0;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t183(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 0;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t184(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775807;
    sigof(((f) + (((c) as u64))), "+", a, b)
}
fn t185(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775807;
    sigof(((f) * (((c) as u64))), "*", a, b)
}
fn t186(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775807;
    sigof(((f) / (((c) as u64))), "/", a, b)
}
fn t187(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775807;
    sigof(((f) % (((c) as u64))), "%", a, b)
}
fn t188(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775807;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t189(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775807;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t190(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775808;
    sigof(((f) - (((c) as u64))), "-", a, b)
}
fn t191(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775808;
    sigof(((f) * (((c) as u64))), "*", a, b)
}
fn t192(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775808;
    sigof(((f) / (((c) as u64))), "/", a, b)
}
fn t193(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775808;
    sigof(((f) % (((c) as u64))), "%", a, b)
}
fn t194(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775808;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t195(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775808;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t196(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((f) + (((c) as u64))), "+", a, b)
}
fn t197(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((f) - (((c) as u64))), "-", a, b)
}
fn t198(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((f) * (((c) as u64))), "*", a, b)
}
fn t199(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((f) / (((c) as u64))), "/", a, b)
}
fn t200(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((f) % (((c) as u64))), "%", a, b)
}
fn t201(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t202(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t203(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 18446744073709551615;
    sigof(((f) + (((c) as u64))), "+", a, b)
}
fn t204(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 18446744073709551615;
    sigof(((f) * (((c) as u64))), "*", a, b)
}
fn t205(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 18446744073709551615;
    sigof(((f) / (((c) as u64))), "/", a, b)
}
fn t206(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 18446744073709551615;
    sigof(((f) % (((c) as u64))), "%", a, b)
}
fn t207(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 18446744073709551615;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t208(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 18446744073709551615;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t209(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t210(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 42;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t211(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 0;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t212(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 0;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t213(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775807;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t214(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775807;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t215(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775808;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t216(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9223372036854775808;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t217(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t218(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 9007199254740993;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t219(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 18446744073709551615;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t220(c: u128, a: i128, b: i128) -> String {
    let f: u64 = 18446744073709551615;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t221(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 42;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t222(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 42;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t223(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 0;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t224(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 0;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t225(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775807;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t226(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775807;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t227(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775808;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t228(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775808;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t229(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9007199254740993;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t230(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9007199254740993;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t231(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 18446744073709551615;
    sigof(((f) << (((c) as i64))), "<<", a, b)
}
fn t232(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 18446744073709551615;
    sigof(((f) >> (((c) as i64))), ">>", a, b)
}
fn t233(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 42;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t234(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 42;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t235(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 0;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t236(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 0;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t237(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775807;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t238(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775807;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t239(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775808;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t240(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775808;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t241(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9007199254740993;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t242(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9007199254740993;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t243(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 18446744073709551615;
    sigof(((f) << (((c) as u64))), "<<", a, b)
}
fn t244(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 18446744073709551615;
    sigof(((f) >> (((c) as u64))), ">>", a, b)
}
fn t245(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 42;
    sigof(((f) / (((c) as i128))), "/", a, b)
}
fn t246(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 42;
    sigof(((f) % (((c) as i128))), "%", a, b)
}
fn t247(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 42;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t248(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 42;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t249(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 0;
    sigof(((f) / (((c) as i128))), "/", a, b)
}
fn t250(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 0;
    sigof(((f) % (((c) as i128))), "%", a, b)
}
fn t251(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 0;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t252(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 0;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t253(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775807;
    sigof(((f) / (((c) as i128))), "/", a, b)
}
fn t254(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775807;
    sigof(((f) % (((c) as i128))), "%", a, b)
}
fn t255(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775807;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t256(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775807;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t257(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775808;
    sigof(((f) / (((c) as i128))), "/", a, b)
}
fn t258(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775808;
    sigof(((f) % (((c) as i128))), "%", a, b)
}
fn t259(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775808;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t260(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9223372036854775808;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t261(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9007199254740993;
    sigof(((f) / (((c) as i128))), "/", a, b)
}
fn t262(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9007199254740993;
    sigof(((f) % (((c) as i128))), "%", a, b)
}
fn t263(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9007199254740993;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t264(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 9007199254740993;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}
fn t265(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 18446744073709551615;
    sigof(((f) * (((c) as i128))), "*", a, b)
}
fn t266(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 18446744073709551615;
    sigof(((f) / (((c) as i128))), "/", a, b)
}
fn t267(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 18446744073709551615;
    sigof(((f) % (((c) as i128))), "%", a, b)
}
fn t268(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 18446744073709551615;
    sigof(((f) << (((c) as i128))), "<<", a, b)
}
fn t269(c: u128, a: i128, b: i128) -> String {
    let f: i128 = 18446744073709551615;
    sigof(((f) >> (((c) as i128))), ">>", a, b)
}

fn reg() -> Vec<Box<dyn Fn() -> i32>> {
    let mut v: Vec<Box<dyn Fn() -> i32>> = Vec::new();
    v.push(Box::new(|| bisect(82, t82, "+", 9007199254740993u128, 9223372036854775807u128, 42u128, true)));
    v.push(Box::new(|| bisect(83, t83, "*", 9007199254740993u128, 9223372036854775807u128, 42u128, true)));
    v.push(Box::new(|| bisect(84, t84, "+", 0u128, 42u128, 9223372036854775807u128, true)));
    v.push(Box::new(|| bisect(85, t85, "*", 0u128, 42u128, 9223372036854775807u128, true)));
    v.push(Box::new(|| bisect(86, t86, "+", 9007199254740993u128, 9223372036854775807u128, 9007199254740993u128, true)));
    v.push(Box::new(|| bisect(87, t87, "*", 42u128, 9007199254740993u128, 9007199254740993u128, true)));
    v.push(Box::new(|| bisect(88, t88, "+", 9223372036854775808u128, 18446744073709551615u128, 42u128, true)));
    v.push(Box::new(|| bisect(89, t89, "-", 0u128, 42u128, 42u128, true)));
    v.push(Box::new(|| bisect(90, t90, "*", 9007199254740993u128, 9223372036854775807u128, 42u128, true)));
    v.push(Box::new(|| bisect(91, t91, "+", 9223372036854775808u128, 18446744073709551615u128, 9223372036854775807u128, true)));
    v.push(Box::new(|| bisect(92, t92, "-", 9007199254740993u128, 9223372036854775807u128, 9223372036854775807u128, true)));
    v.push(Box::new(|| bisect(93, t93, "*", 0u128, 42u128, 9223372036854775807u128, true)));
    v.push(Box::new(|| bisect(94, t94, "*", 0u128, 42u128, 9223372036854775808u128, true)));
    v.push(Box::new(|| bisect(95, t95, "+", 9223372036854775808u128, 18446744073709551615u128, 9007199254740993u128, true)));
    v.push(Box::new(|| bisect(96, t96, "-", 42u128, 9007199254740993u128, 9007199254740993u128, true)));
    v.push(Box::new(|| bisect(97, t97, "*", 42u128, 9007199254740993u128, 9007199254740993u128, true)));
    v.push(Box::new(|| bisect(98, t98, "+", 0u128, 42u128, 18446744073709551615u128, true)));
    v.push(Box::new(|| bisect(99, t99, "-", 9223372036854775808u128, 18446744073709551615u128, 18446744073709551615u128, true)));
    v.push(Box::new(|| bisect(100, t100, "*", 0u128, 42u128, 18446744073709551615u128, true)));
    v.push(Box::new(|| bisect(101, t101, "*", 9223372036854775808u128, 18446744073709551615u128, 18446744073709551615u128, true)));
    v.push(Box::new(|| bisect(102, t102, "/", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(103, t103, "%", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(104, t104, "<<", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(105, t105, ">>", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(106, t106, "/", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(107, t107, "%", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(108, t108, "<<", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(109, t109, ">>", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(110, t110, "<<", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(111, t111, ">>", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(112, t112, "<<", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(113, t113, ">>", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(114, t114, "<<", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(115, t115, ">>", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(116, t116, "<<", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(117, t117, ">>", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(118, t118, "<<", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(119, t119, ">>", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(120, t120, "<<", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(121, t121, ">>", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(122, t122, "+", 9007199254740993u128, 9223372036854775807u128, 42u128, false)));
    v.push(Box::new(|| bisect(123, t123, "*", 9007199254740993u128, 9223372036854775807u128, 42u128, false)));
    v.push(Box::new(|| bisect(124, t124, "/", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(125, t125, "%", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(126, t126, "<<", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(127, t127, ">>", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(128, t128, "/", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(129, t129, "%", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(130, t130, "<<", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(131, t131, ">>", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(132, t132, "+", 0u128, 42u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(133, t133, "*", 0u128, 42u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(134, t134, "/", 0u128, 42u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(135, t135, "%", 0u128, 42u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(136, t136, "<<", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(137, t137, ">>", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(138, t138, "+", 9007199254740993u128, 9223372036854775807u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(139, t139, "*", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(140, t140, "/", 0u128, 42u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(141, t141, "%", 0u128, 42u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(142, t142, "<<", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(143, t143, ">>", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(144, t144, "<<", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(145, t145, ">>", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(146, t146, "<<", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(147, t147, ">>", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(148, t148, "<<", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(149, t149, ">>", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(150, t150, "<<", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(151, t151, ">>", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(152, t152, "<<", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(153, t153, ">>", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(154, t154, "<<", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(155, t155, ">>", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(156, t156, "<<", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(157, t157, ">>", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(158, t158, "<<", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(159, t159, ">>", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(160, t160, "<<", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(161, t161, ">>", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(162, t162, "<<", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(163, t163, ">>", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(164, t164, "<<", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(165, t165, ">>", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(166, t166, "<<", 42u128, 9007199254740993u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(167, t167, ">>", 42u128, 9007199254740993u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(168, t168, "<<", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(169, t169, ">>", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(170, t170, "<<", 42u128, 9007199254740993u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(171, t171, ">>", 42u128, 9007199254740993u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(172, t172, "+", 9223372036854775808u128, 18446744073709551615u128, 42u128, false)));
    v.push(Box::new(|| bisect(173, t173, "-", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(174, t174, "*", 9007199254740993u128, 9223372036854775807u128, 42u128, false)));
    v.push(Box::new(|| bisect(175, t175, "/", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(176, t176, "%", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(177, t177, "<<", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(178, t178, ">>", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(179, t179, "-", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(180, t180, "/", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(181, t181, "%", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(182, t182, "<<", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(183, t183, ">>", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(184, t184, "+", 9223372036854775808u128, 18446744073709551615u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(185, t185, "*", 0u128, 42u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(186, t186, "/", 0u128, 42u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(187, t187, "%", 0u128, 42u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(188, t188, "<<", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(189, t189, ">>", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(190, t190, "-", 9223372036854775808u128, 18446744073709551615u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(191, t191, "*", 0u128, 42u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(192, t192, "/", 0u128, 42u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(193, t193, "%", 0u128, 42u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(194, t194, "<<", 42u128, 9007199254740993u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(195, t195, ">>", 42u128, 9007199254740993u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(196, t196, "+", 9223372036854775808u128, 18446744073709551615u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(197, t197, "-", 9007199254740993u128, 9223372036854775807u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(198, t198, "*", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(199, t199, "/", 0u128, 42u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(200, t200, "%", 0u128, 42u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(201, t201, "<<", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(202, t202, ">>", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(203, t203, "+", 0u128, 42u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(204, t204, "*", 0u128, 42u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(205, t205, "/", 0u128, 42u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(206, t206, "%", 0u128, 42u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(207, t207, "<<", 42u128, 9007199254740993u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(208, t208, ">>", 42u128, 9007199254740993u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(209, t209, "<<", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(210, t210, ">>", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(211, t211, "<<", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(212, t212, ">>", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(213, t213, "<<", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(214, t214, ">>", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(215, t215, "<<", 42u128, 9007199254740993u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(216, t216, ">>", 42u128, 9007199254740993u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(217, t217, "<<", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(218, t218, ">>", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(219, t219, "<<", 42u128, 9007199254740993u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(220, t220, ">>", 42u128, 9007199254740993u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(221, t221, "<<", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(222, t222, ">>", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(223, t223, "<<", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(224, t224, ">>", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(225, t225, "<<", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(226, t226, ">>", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(227, t227, "<<", 42u128, 9007199254740993u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(228, t228, ">>", 42u128, 9007199254740993u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(229, t229, "<<", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(230, t230, ">>", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(231, t231, "<<", 42u128, 9007199254740993u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(232, t232, ">>", 42u128, 9007199254740993u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(233, t233, "<<", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(234, t234, ">>", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(235, t235, "<<", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(236, t236, ">>", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(237, t237, "<<", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(238, t238, ">>", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(239, t239, "<<", 42u128, 9007199254740993u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(240, t240, ">>", 42u128, 9007199254740993u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(241, t241, "<<", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(242, t242, ">>", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(243, t243, "<<", 42u128, 9007199254740993u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(244, t244, ">>", 42u128, 9007199254740993u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(245, t245, "/", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(246, t246, "%", 0u128, 42u128, 42u128, false)));
    v.push(Box::new(|| bisect(247, t247, "<<", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(248, t248, ">>", 42u128, 9007199254740993u128, 42u128, false)));
    v.push(Box::new(|| bisect(249, t249, "/", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(250, t250, "%", 0u128, 42u128, 0u128, false)));
    v.push(Box::new(|| bisect(251, t251, "<<", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(252, t252, ">>", 42u128, 9007199254740993u128, 0u128, false)));
    v.push(Box::new(|| bisect(253, t253, "/", 0u128, 42u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(254, t254, "%", 0u128, 42u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(255, t255, "<<", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(256, t256, ">>", 42u128, 9007199254740993u128, 9223372036854775807u128, false)));
    v.push(Box::new(|| bisect(257, t257, "/", 0u128, 42u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(258, t258, "%", 0u128, 42u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(259, t259, "<<", 42u128, 9007199254740993u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(260, t260, ">>", 42u128, 9007199254740993u128, 9223372036854775808u128, false)));
    v.push(Box::new(|| bisect(261, t261, "/", 0u128, 42u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(262, t262, "%", 0u128, 42u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(263, t263, "<<", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(264, t264, ">>", 42u128, 9007199254740993u128, 9007199254740993u128, false)));
    v.push(Box::new(|| bisect(265, t265, "*", 9223372036854775808u128, 18446744073709551615u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(266, t266, "/", 0u128, 42u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(267, t267, "%", 0u128, 42u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(268, t268, "<<", 42u128, 9007199254740993u128, 18446744073709551615u128, false)));
    v.push(Box::new(|| bisect(269, t269, ">>", 42u128, 9007199254740993u128, 18446744073709551615u128, false)));
    v
}

fn main() {
    panic::set_hook(Box::new(|_| {}));
    let t = reg();
    let mut total = 0;
    let n = t.len();
    for k in 0..n {
        total += t[k]();
        if (k + 1) % 25 == 0 || k + 1 == n {
            eprintln!("progress {}/{} probes={}", k + 1, n, total);
        }
    }
    eprintln!("DONE targets={} probes={}", n, total);
}
