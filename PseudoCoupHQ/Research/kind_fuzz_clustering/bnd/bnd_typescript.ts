
const EXACT = ["+", "-", "*", "<", "<=", ">", ">=", "==", "!="];

function wantv(op: string, a: bigint, b: bigint): any {
  if (EXACT.indexOf(op) < 0) return null;
  switch (op) {
    case "+": return a + b;
    case "-": return a - b;
    case "*": return a * b;
    case "<": return a < b;
    case "<=": return a <= b;
    case ">": return a > b;
    case ">=": return a >= b;
    case "==": return a === b;
    case "!=": return a !== b;
  }
  return null;
}

function asint(r: any): any {
  if (typeof r === "boolean") return r;
  if (typeof r === "bigint") return r;
  if (typeof r === "number") {
    if (!isFinite(r)) return null;
    if (Math.floor(r) !== r) return "NONINT";
    return BigInt(r);
  }
  return null;
}

function fidv(r: any, op: string, a: bigint, b: bigint): string {
  const w = wantv(op, a, b);
  if (w === null) return "na";
  const g = asint(r);
  if (g === null) return "na";
  if (typeof w === "boolean") {
    if (typeof g !== "boolean") return "na";
    return w === g ? "exact" : "inexact";
  }
  if (typeof g === "boolean") return "na";
  if (g === "NONINT") return "inexact";
  return (g as bigint) === (w as bigint) ? "exact" : "inexact";
}

function tname(r: any): string {
  if (r === null) return "null";
  const t = typeof r;
  if (t === "object") return (r as any).constructor ?
      (r as any).constructor.name : "object";
  return t;
}

function sigv(fn: (c: bigint) => any, c: bigint, op: string,
              a: bigint, b: bigint): string {
  let r: any;
  try { r = fn(c); }
  catch (e: any) {
    return "raise|" + (e && e.constructor ? e.constructor.name : "?") + "|na";
  }
  return "answer|" + tname(r) + "|" + fidv(r, op, a, b);
}

function bisect(tid: number, fn: (c: bigint) => any, op: string,
                lov: bigint, hiv: bigint, fixed: bigint,
                varyIsLhs: boolean): number {
  const s = (c: bigint) => {
    const a = varyIsLhs ? c : fixed;
    const b = varyIsLhs ? fixed : c;
    return sigv(fn, c, op, a, b);
  };
  let lo = lov, hi = hiv;
  const slo = s(lo), shi = s(hi);
  let probes = 2;
  if (slo === shi) { console.log("N|" + tid + "|" + slo + "|" + shi); return probes; }
  const other: any = {};
  while (hi - lo > 1n) {
    const mid = (lo + hi) / 2n;
    const sm = s(mid); probes++;
    if (sm === slo) lo = mid;
    else { if (sm !== shi) other[sm] = true; hi = mid; }
  }
  console.log("B|" + tid + "|" + lo + "|" + hi + "|" + slo + "|" + shi +
              "|" + probes + "|" + Object.keys(other).sort().join(";"));
  return probes;
}

const TARGETS: (() => number)[] = [
  () => { let f: bigint = 42n; return bisect(2935, (c: bigint) => ((Number(c)) && (f)), "&&", 0n, 42n, 42n, true); },
  () => { let f: bigint = 42n; return bisect(2936, (c: bigint) => ((Number(c)) || (f)), "||", 0n, 42n, 42n, true); },
  () => { let f: bigint = 0n; return bisect(2937, (c: bigint) => ((Number(c)) && (f)), "&&", 0n, 42n, 0n, true); },
  () => { let f: bigint = 0n; return bisect(2938, (c: bigint) => ((Number(c)) || (f)), "||", 0n, 42n, 0n, true); },
  () => { let f: bigint = 9223372036854775807n; return bisect(2939, (c: bigint) => ((Number(c)) <= (f)), "<=", 9007199254740993n, 9223372036854775807n, 9223372036854775807n, true); },
  () => { let f: bigint = 9223372036854775807n; return bisect(2940, (c: bigint) => ((Number(c)) > (f)), ">", 9007199254740993n, 9223372036854775807n, 9223372036854775807n, true); },
  () => { let f: bigint = 9223372036854775807n; return bisect(2941, (c: bigint) => ((Number(c)) && (f)), "&&", 0n, 42n, 9223372036854775807n, true); },
  () => { let f: bigint = 9223372036854775807n; return bisect(2942, (c: bigint) => ((Number(c)) || (f)), "||", 0n, 42n, 9223372036854775807n, true); },
  () => { let f: bigint = 9223372036854775808n; return bisect(2943, (c: bigint) => ((Number(c)) < (f)), "<", 9007199254740993n, 9223372036854775807n, 9223372036854775808n, true); },
  () => { let f: bigint = 9223372036854775808n; return bisect(2944, (c: bigint) => ((Number(c)) >= (f)), ">=", 9007199254740993n, 9223372036854775807n, 9223372036854775808n, true); },
  () => { let f: bigint = 9223372036854775808n; return bisect(2945, (c: bigint) => ((Number(c)) && (f)), "&&", 0n, 42n, 9223372036854775808n, true); },
  () => { let f: bigint = 9223372036854775808n; return bisect(2946, (c: bigint) => ((Number(c)) || (f)), "||", 0n, 42n, 9223372036854775808n, true); },
  () => { let f: bigint = 9007199254740993n; return bisect(2947, (c: bigint) => ((Number(c)) < (f)), "<", 42n, 9007199254740993n, 9007199254740993n, true); },
  () => { let f: bigint = 9007199254740993n; return bisect(2948, (c: bigint) => ((Number(c)) < (f)), "<", 9007199254740993n, 9223372036854775807n, 9007199254740993n, true); },
  () => { let f: bigint = 9007199254740993n; return bisect(2949, (c: bigint) => ((Number(c)) >= (f)), ">=", 42n, 9007199254740993n, 9007199254740993n, true); },
  () => { let f: bigint = 9007199254740993n; return bisect(2950, (c: bigint) => ((Number(c)) >= (f)), ">=", 9007199254740993n, 9223372036854775807n, 9007199254740993n, true); },
  () => { let f: bigint = 9007199254740993n; return bisect(2951, (c: bigint) => ((Number(c)) && (f)), "&&", 0n, 42n, 9007199254740993n, true); },
  () => { let f: bigint = 9007199254740993n; return bisect(2952, (c: bigint) => ((Number(c)) || (f)), "||", 0n, 42n, 9007199254740993n, true); },
  () => { let f: bigint = 18446744073709551615n; return bisect(2953, (c: bigint) => ((Number(c)) <= (f)), "<=", 9223372036854775808n, 18446744073709551615n, 18446744073709551615n, true); },
  () => { let f: bigint = 18446744073709551615n; return bisect(2954, (c: bigint) => ((Number(c)) > (f)), ">", 9223372036854775808n, 18446744073709551615n, 18446744073709551615n, true); },
  () => { let f: bigint = 18446744073709551615n; return bisect(2955, (c: bigint) => ((Number(c)) && (f)), "&&", 0n, 42n, 18446744073709551615n, true); },
  () => { let f: bigint = 18446744073709551615n; return bisect(2956, (c: bigint) => ((Number(c)) || (f)), "||", 0n, 42n, 18446744073709551615n, true); },
  () => { let f: bigint = 9223372036854775807n; return bisect(3372, (c: bigint) => ((f) < (Number(c))), "<", 9007199254740993n, 9223372036854775807n, 9223372036854775807n, false); },
  () => { let f: bigint = 9223372036854775807n; return bisect(3373, (c: bigint) => ((f) >= (Number(c))), ">=", 9007199254740993n, 9223372036854775807n, 9223372036854775807n, false); },
  () => { let f: bigint = 9223372036854775808n; return bisect(3374, (c: bigint) => ((f) <= (Number(c))), "<=", 9007199254740993n, 9223372036854775807n, 9223372036854775808n, false); },
  () => { let f: bigint = 9223372036854775808n; return bisect(3375, (c: bigint) => ((f) > (Number(c))), ">", 9007199254740993n, 9223372036854775807n, 9223372036854775808n, false); },
  () => { let f: bigint = 9007199254740993n; return bisect(3376, (c: bigint) => ((f) <= (Number(c))), "<=", 42n, 9007199254740993n, 9007199254740993n, false); },
  () => { let f: bigint = 9007199254740993n; return bisect(3377, (c: bigint) => ((f) <= (Number(c))), "<=", 9007199254740993n, 9223372036854775807n, 9007199254740993n, false); },
  () => { let f: bigint = 9007199254740993n; return bisect(3378, (c: bigint) => ((f) > (Number(c))), ">", 42n, 9007199254740993n, 9007199254740993n, false); },
  () => { let f: bigint = 9007199254740993n; return bisect(3379, (c: bigint) => ((f) > (Number(c))), ">", 9007199254740993n, 9223372036854775807n, 9007199254740993n, false); },
  () => { let f: bigint = 18446744073709551615n; return bisect(3380, (c: bigint) => ((f) < (Number(c))), "<", 9223372036854775808n, 18446744073709551615n, 18446744073709551615n, false); },
  () => { let f: bigint = 18446744073709551615n; return bisect(3381, (c: bigint) => ((f) >= (Number(c))), ">=", 9223372036854775808n, 18446744073709551615n, 18446744073709551615n, false); },
  () => { let f: bigint = 42n; return bisect(3382, (c: bigint) => ((f) / ((c))), "/", 0n, 42n, 42n, false); },
  () => { let f: bigint = 42n; return bisect(3383, (c: bigint) => ((f) % ((c))), "%", 0n, 42n, 42n, false); },
  () => { let f: bigint = 0n; return bisect(3386, (c: bigint) => ((f) / ((c))), "/", 0n, 42n, 0n, false); },
  () => { let f: bigint = 0n; return bisect(3387, (c: bigint) => ((f) % ((c))), "%", 0n, 42n, 0n, false); },
  () => { let f: bigint = 9223372036854775807n; return bisect(3388, (c: bigint) => ((f) / ((c))), "/", 0n, 42n, 9223372036854775807n, false); },
  () => { let f: bigint = 9223372036854775807n; return bisect(3389, (c: bigint) => ((f) % ((c))), "%", 0n, 42n, 9223372036854775807n, false); },
  () => { let f: bigint = 9223372036854775808n; return bisect(3392, (c: bigint) => ((f) / ((c))), "/", 0n, 42n, 9223372036854775808n, false); },
  () => { let f: bigint = 9223372036854775808n; return bisect(3393, (c: bigint) => ((f) % ((c))), "%", 0n, 42n, 9223372036854775808n, false); },
  () => { let f: bigint = 9007199254740993n; return bisect(3396, (c: bigint) => ((f) / ((c))), "/", 0n, 42n, 9007199254740993n, false); },
  () => { let f: bigint = 9007199254740993n; return bisect(3397, (c: bigint) => ((f) % ((c))), "%", 0n, 42n, 9007199254740993n, false); },
  () => { let f: bigint = 18446744073709551615n; return bisect(3400, (c: bigint) => ((f) / ((c))), "/", 0n, 42n, 18446744073709551615n, false); },
  () => { let f: bigint = 18446744073709551615n; return bisect(3401, (c: bigint) => ((f) % ((c))), "%", 0n, 42n, 18446744073709551615n, false); },
];

let total = 0;
for (let k = 0; k < TARGETS.length; k++) {
  total += TARGETS[k]();
  if ((k + 1) % 25 === 0 || k + 1 === TARGETS.length)
    process.stderr.write("progress " + (k + 1) + "/" + TARGETS.length +
                         " probes=" + total + "\n");
}
process.stderr.write("DONE targets=" + TARGETS.length + " probes=" + total + "\n");
