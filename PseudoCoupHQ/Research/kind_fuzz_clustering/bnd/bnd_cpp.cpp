#include <variant>
#include <vector>
#include <map>
#include <string>
#include <sstream>
#include <type_traits>
#include <cstddef>
#include <algorithm>
#include <iomanip>
#include <cmath>
#include <limits>
#include <cstdint>
#include <array>
#include <deque>
#include <list>
#include <optional>
#include <tuple>
#include <unordered_map>

#include <cstdint>
#include <cstdio>
#include <cmath>
#include <csetjmp>
#include <csignal>
#include <string>
#include <set>
#include <vector>
#include <type_traits>

typedef __int128 i128;
typedef unsigned __int128 u128;

static sigjmp_buf JB;
static void onfpe(int) { siglongjmp(JB, 1); }

static std::string dec(u128 v) {
  if (v == 0) return "0";
  std::string s;
  while (v) { s.insert(s.begin(), char('0' + (int)(v % 10))); v /= 10; }
  return s;
}
static std::string decs(i128 v) {
  if (v < 0) return "-" + dec((u128)(-v));
  return dec((u128)v);
}
static u128 parse(const char *s) {
  u128 v = 0;
  for (const char *p = s; *p; p++) v = v * 10 + (u128)(*p - '0');
  return v;
}

// the exact result.  kind 0 = none, 1 = integer, 2 = bool,
// 3 = an integer too wide for i128 to hold
struct Want { int kind; i128 v; bool b; };

static Want wantv(const std::string &op, i128 a, i128 b) {
  Want w = {0, 0, false};
  i128 r;
  if (op == "+") {
    if (__builtin_add_overflow(a, b, &r)) { w.kind = 3; return w; }
    w.kind = 1; w.v = r; return w;
  }
  if (op == "-") {
    if (__builtin_sub_overflow(a, b, &r)) { w.kind = 3; return w; }
    w.kind = 1; w.v = r; return w;
  }
  if (op == "*") {
    if (__builtin_mul_overflow(a, b, &r)) { w.kind = 3; return w; }
    w.kind = 1; w.v = r; return w;
  }
  w.kind = 2;
  if (op == "<") { w.b = a < b; return w; }
  if (op == "<=") { w.b = a <= b; return w; }
  if (op == ">") { w.b = a > b; return w; }
  if (op == ">=") { w.b = a >= b; return w; }
  if (op == "==") { w.b = a == b; return w; }
  if (op == "!=") { w.b = a != b; return w; }
  w.kind = 0; return w;
}

template <class T>
static std::string fidv(T r, const std::string &op, i128 a, i128 b) {
  Want w = wantv(op, a, b);
  if (w.kind == 0) return "na";
  if constexpr (std::is_same_v<T, bool>) {
    if (w.kind != 2) return "na";
    return (r == w.b) ? "exact" : "inexact";
  } else if constexpr (std::is_integral_v<T> ||
                       std::is_same_v<T, __int128> ||
                       std::is_same_v<T, unsigned __int128>) {
    if (w.kind == 2) return "na";
    if (w.kind == 3) return "inexact";
    return ((i128)r == w.v) ? "exact" : "inexact";
  } else if constexpr (std::is_floating_point_v<T>) {
    if (w.kind == 2) return "na";
    double d = (double)r;
    if (std::isnan(d) || std::isinf(d)) return "na";
    if (d != std::floor(d)) return "inexact";
    if (w.kind == 3) return "inexact";
    long double L = (long double)r;
    return (L == (long double)w.v) ? "exact" : "inexact";
  } else {
    return "na";
  }
}

template <class T>
static const char *tname(T) {
  if constexpr (std::is_same_v<T, bool>) return "bool";
  else if constexpr (std::is_same_v<T, int32_t>) return "int32_t";
  else if constexpr (std::is_same_v<T, int64_t>) return "int64_t";
  else if constexpr (std::is_same_v<T, uint64_t>) return "uint64_t";
  else if constexpr (std::is_same_v<T, __int128>) return "__int128";
  else if constexpr (std::is_same_v<T, unsigned __int128>) return "u__int128";
  else if constexpr (std::is_same_v<T, int>) return "int";
  else if constexpr (std::is_same_v<T, unsigned>) return "unsigned";
  else if constexpr (std::is_same_v<T, double>) return "double";
  else if constexpr (std::is_same_v<T, float>) return "float";
  else return "other";
}

template <class T>
static std::string sigof(T r, const std::string &op, i128 a, i128 b) {
  return std::string("answer|") + tname(r) + "|" + fidv(r, op, a, b);
}

typedef std::string (*TFN)(u128, i128, i128);

static int bisect(int tid, TFN fn, const char *ops, const char *lov,
                  const char *hiv, const char *fixv, bool varyIsLhs) {
  std::string op(ops);
  u128 lo = parse(lov), hi = parse(hiv);
  i128 fx = (i128)parse(fixv);
  auto s = [&](u128 c) {
    i128 a = varyIsLhs ? (i128)c : fx;
    i128 b = varyIsLhs ? fx : (i128)c;
    return fn(c, a, b);
  };
  std::string slo = s(lo), shi = s(hi);
  int probes = 2;
  if (slo == shi) {
    printf("N|%d|%s|%s\n", tid, slo.c_str(), shi.c_str());
    return probes;
  }
  std::set<std::string> other;
  while (hi - lo > 1) {
    u128 mid = lo + (hi - lo) / 2;
    std::string sm = s(mid); probes++;
    if (sm == slo) lo = mid;
    else { if (sm != shi) other.insert(sm); hi = mid; }
  }
  std::string o;
  for (std::set<std::string>::iterator it = other.begin();
       it != other.end(); ++it) { if (!o.empty()) o += ";"; o += *it; }
  printf("B|%d|%s|%s|%s|%s|%d|%s\n", tid, dec(lo).c_str(), dec(hi).c_str(),
         slo.c_str(), shi.c_str(), probes, o.c_str());
  return probes;
}
static std::string T270(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T271(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T272(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T273(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T274(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T275(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T276(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T277(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T278(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T279(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T280(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T281(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T282(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T283(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T284(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T285(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T286(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T287(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T288(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T289(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T290(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T291(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T292(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T293(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T294(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T295(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T296(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T297(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T298(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T299(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T300(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T301(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T302(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T303(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T304(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T305(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T306(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T307(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T308(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T309(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T310(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T311(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T312(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T313(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T314(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T315(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T316(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T317(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T318(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T319(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T320(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T321(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T322(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T323(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T324(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T325(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T326(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T327(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T328(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T329(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T330(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T331(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T332(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T333(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T334(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T335(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T336(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T337(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T338(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T339(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T340(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T341(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T342(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T343(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T344(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T345(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T346(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T347(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T348(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T349(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T350(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T351(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T352(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T353(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T354(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T355(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T356(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T357(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T358(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T359(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T360(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T361(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T362(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T363(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T364(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T365(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T366(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T367(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T368(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T369(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T370(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T371(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T372(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T373(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T374(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T375(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T376(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T377(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T378(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T379(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T380(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T381(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T382(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T383(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T384(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T385(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T386(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T387(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T388(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T389(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T390(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T391(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T392(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T393(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T394(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T395(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T396(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T397(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T398(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T399(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T400(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T401(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T402(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T403(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T404(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T405(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T406(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T407(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T408(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T409(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T410(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T411(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T412(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T413(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T414(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T415(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T416(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T417(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T418(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T419(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T420(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T421(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T422(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T423(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T424(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T425(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T426(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T427(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T428(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T429(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T430(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T431(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T432(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T433(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T434(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T435(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T436(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T437(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T438(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T439(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T440(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T441(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T442(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T443(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T444(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T445(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T446(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T447(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T448(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T449(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T450(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T451(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T452(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T453(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T454(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T455(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T456(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T457(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T458(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T459(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T460(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T461(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T462(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T463(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T464(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T465(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T466(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T467(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T468(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T469(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T470(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T471(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T472(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T473(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T474(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T475(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T476(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T477(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T478(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T479(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T480(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T481(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T482(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T483(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T484(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T485(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T486(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T487(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T488(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T489(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T490(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T491(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T492(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T493(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T494(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = (((int32_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T495(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = (((int32_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T496(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T497(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T498(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T499(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T500(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T501(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = (((int32_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T502(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = (((int32_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T503(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = (((int32_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T504(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = (((int32_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T505(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = (((int32_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T506(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = (((int32_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T507(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = (((int32_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T566(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = (((int64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T567(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = (((int64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T568(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T569(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T570(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) / (f));
  return sigof(r, "/", a, b);
}
static std::string T571(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) % (f));
  return sigof(r, "%", a, b);
}
static std::string T572(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T573(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T574(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T575(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T576(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T577(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T578(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T579(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T580(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T581(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int64_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T582(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int64_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T583(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int64_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T584(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int64_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T585(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T586(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T587(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T588(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((int64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T589(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T590(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int64_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T591(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int64_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T592(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int64_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T593(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int64_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T594(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int64_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T595(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int64_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T596(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int64_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T597(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int64_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T598(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T599(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T600(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T601(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((int64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T602(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T603(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T604(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int64_t)(c)) / (f));
  return sigof(r, "/", a, b);
}
static std::string T605(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((int64_t)(c)) % (f));
  return sigof(r, "%", a, b);
}
static std::string T606(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = (((int64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T607(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = (((int64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T608(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T609(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T610(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T611(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T612(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T613(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T614(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T615(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T616(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T617(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T618(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int64_t)(c)) / (f));
  return sigof(r, "/", a, b);
}
static std::string T619(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((int64_t)(c)) % (f));
  return sigof(r, "%", a, b);
}
static std::string T620(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T621(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T622(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T623(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T624(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T625(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T626(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T627(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T628(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T629(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T630(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((int64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T631(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((int64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T632(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((int64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T633(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = (((int64_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T634(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = (((int64_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T635(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = (((int64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T636(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = (((int64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T637(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = (((int64_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T638(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = (((int64_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T639(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = (((int64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T640(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = (((int64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T671(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = (((uint64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T672(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = (((uint64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T673(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T674(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T675(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T676(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T677(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T678(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T679(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T680(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T681(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T682(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T683(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T684(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((uint64_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T685(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((uint64_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T686(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((uint64_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T687(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((uint64_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T688(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((uint64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T689(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((uint64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T690(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((uint64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T691(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((uint64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T692(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T693(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T694(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T695(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T696(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T697(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T698(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T699(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T700(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T701(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T702(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T703(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T704(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T705(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((uint64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T706(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((uint64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T707(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T708(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = (((uint64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T709(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = (((uint64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T710(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T711(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T712(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T713(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T714(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T715(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T716(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T717(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T718(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((uint64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T719(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((uint64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T720(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T721(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((uint64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T722(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((uint64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T723(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T724(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T725(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T726(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T727(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T728(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T729(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T730(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T731(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((uint64_t)(c)) + (f));
  return sigof(r, "+", a, b);
}
static std::string T732(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((uint64_t)(c)) - (f));
  return sigof(r, "-", a, b);
}
static std::string T733(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T734(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = (((uint64_t)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T773(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((__int128)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T774(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((__int128)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T775(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((__int128)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T776(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((__int128)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T777(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = (((__int128)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T778(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((__int128)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T779(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((__int128)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T780(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((__int128)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T781(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((__int128)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T782(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((__int128)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T783(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((__int128)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T784(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((__int128)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T785(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((__int128)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T786(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = (((__int128)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T787(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((__int128)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T788(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((__int128)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T789(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((__int128)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T790(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((__int128)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T791(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((__int128)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T792(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((__int128)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T793(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((__int128)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T794(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((__int128)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T795(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((__int128)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T796(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((__int128)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T797(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((__int128)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T798(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((__int128)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T799(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = (((__int128)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T800(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((__int128)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T801(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((__int128)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T802(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((__int128)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T803(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((__int128)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T804(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = (((__int128)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T805(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((__int128)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T806(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((__int128)(c)) <= (f));
  return sigof(r, "<=", a, b);
}
static std::string T807(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((__int128)(c)) > (f));
  return sigof(r, ">", a, b);
}
static std::string T808(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((__int128)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T809(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = (((__int128)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T810(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((__int128)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T811(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((__int128)(c)) < (f));
  return sigof(r, "<", a, b);
}
static std::string T812(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((__int128)(c)) >= (f));
  return sigof(r, ">=", a, b);
}
static std::string T813(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((__int128)(c)) == (f));
  return sigof(r, "==", a, b);
}
static std::string T814(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = (((__int128)(c)) != (f));
  return sigof(r, "!=", a, b);
}
static std::string T815(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = (((__int128)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T816(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = (((__int128)(c)) * (f));
  return sigof(r, "*", a, b);
}
static std::string T875(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T876(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T877(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T878(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T879(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T880(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T881(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T882(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T883(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T884(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T885(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T886(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T887(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T888(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T889(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T890(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T891(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T892(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T893(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T894(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T895(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T896(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T897(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T898(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T899(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T900(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T901(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T902(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T903(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T904(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T905(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T906(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T907(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T908(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T909(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T910(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T911(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T912(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T913(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T914(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T915(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T916(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T917(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T918(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T919(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T920(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T921(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T922(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T923(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T924(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T925(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T926(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T927(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T928(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T929(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T930(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T931(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T932(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T933(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T934(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T935(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T936(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T937(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T938(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T939(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T940(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T941(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T942(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T943(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T944(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T945(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T946(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T947(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T948(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T949(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T950(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T951(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T952(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T953(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T954(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T955(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T956(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T957(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T958(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T959(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T960(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T961(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T962(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T963(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T964(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T965(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T966(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T967(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) + ((int64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T968(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) - ((int64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T969(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T970(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T971(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T972(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) - ((int64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T973(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T974(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T975(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T976(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T977(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T978(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) <= ((int64_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T979(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) <= ((int64_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T980(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) > ((int64_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T981(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) > ((int64_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T982(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) == ((int64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T983(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) == ((int64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T984(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) != ((int64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T985(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) != ((int64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T986(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T987(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T988(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T989(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) < ((int64_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T990(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) < ((int64_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T991(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) >= ((int64_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T992(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) >= ((int64_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T993(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) == ((int64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T994(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) == ((int64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T995(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) != ((int64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T996(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) != ((int64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T997(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T998(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T999(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1000(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) < ((int64_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1001(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) < ((int64_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1002(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) <= ((int64_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1003(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) <= ((int64_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1004(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) > ((int64_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1005(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) > ((int64_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1006(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) >= ((int64_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1007(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) >= ((int64_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1008(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) == ((int64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1009(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) == ((int64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1010(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) != ((int64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1011(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) != ((int64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1012(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1013(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1014(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1015(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) + ((uint64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1016(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) - ((uint64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1017(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1018(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1019(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1020(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) - ((uint64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1021(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1022(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1023(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1024(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1025(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1026(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) <= ((uint64_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1027(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) <= ((uint64_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1028(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) > ((uint64_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1029(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) > ((uint64_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1030(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) == ((uint64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1031(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) == ((uint64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1032(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) != ((uint64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1033(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) != ((uint64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1034(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1035(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1036(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1037(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) < ((uint64_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1038(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) < ((uint64_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1039(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) >= ((uint64_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1040(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) >= ((uint64_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1041(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) == ((uint64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1042(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) == ((uint64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1043(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) != ((uint64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1044(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) != ((uint64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1045(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1046(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1047(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1048(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) < ((uint64_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1049(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) < ((uint64_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1050(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) <= ((uint64_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1051(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) <= ((uint64_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1052(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) > ((uint64_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1053(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) > ((uint64_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1054(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) >= ((uint64_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1055(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) >= ((uint64_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1056(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) == ((uint64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1057(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) == ((uint64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1058(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) != ((uint64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1059(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) != ((uint64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1060(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) + ((uint64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1061(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1062(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1063(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1064(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1065(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 42;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1066(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1067(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 0;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1068(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) * ((__int128)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1069(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1070(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1071(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) <= ((__int128)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1072(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) > ((__int128)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1073(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) == ((__int128)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1074(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775807;
  auto r = ((f) != ((__int128)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1075(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) * ((__int128)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1076(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1077(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1078(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) < ((__int128)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1079(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) < ((__int128)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1080(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) >= ((__int128)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1081(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) >= ((__int128)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1082(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) == ((__int128)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1083(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) == ((__int128)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1084(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) != ((__int128)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1085(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9223372036854775808;
  auto r = ((f) != ((__int128)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1086(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) * ((__int128)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1087(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1088(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1089(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) < ((__int128)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1090(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) < ((__int128)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1091(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) <= ((__int128)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1092(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) <= ((__int128)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1093(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) > ((__int128)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1094(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) > ((__int128)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1095(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) >= ((__int128)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1096(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) >= ((__int128)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1097(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) == ((__int128)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1098(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) == ((__int128)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1099(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) != ((__int128)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1100(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 9007199254740993;
  auto r = ((f) != ((__int128)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1101(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) * ((__int128)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1102(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1103(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1104(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) <= ((__int128)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1105(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) > ((__int128)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1106(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) == ((__int128)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1107(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int32_t f = 18446744073709551615;
  auto r = ((f) != ((__int128)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1108(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1109(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1110(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1111(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1112(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1113(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1114(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1115(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1116(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1117(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1118(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1119(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1120(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1121(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1122(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1123(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1124(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1125(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1126(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1127(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1128(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1129(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1130(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1131(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1132(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1133(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1134(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1135(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1136(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1137(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1138(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1139(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1140(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1141(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1142(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1143(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1144(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1145(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1146(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1147(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1148(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1149(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1150(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1151(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1152(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1153(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1154(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1155(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1156(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1157(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1158(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1159(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1160(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1161(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1162(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1163(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1164(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1165(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1166(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1167(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1168(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1169(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1170(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1171(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1172(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1173(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1174(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1175(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1176(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1177(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1178(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1179(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1180(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1181(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1182(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1183(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1184(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1185(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1186(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) + ((int64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1187(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) - ((int64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1188(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1189(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1190(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1191(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) - ((int64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1192(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1193(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1194(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) + ((int64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1195(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1196(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1197(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1198(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) - ((int64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1199(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1200(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1201(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1202(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1203(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1204(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) + ((int64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1205(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) - ((int64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1206(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1207(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1208(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1209(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1210(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1211(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1212(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) + ((uint64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1213(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) - ((uint64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1214(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1215(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1216(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1217(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) - ((uint64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1218(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1219(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1220(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) + ((uint64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1221(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1222(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1223(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1224(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) - ((uint64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1225(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1226(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1227(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1228(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) + ((uint64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1229(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) - ((uint64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1230(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1231(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1232(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1233(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) + ((uint64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1234(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1235(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1236(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1237(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1238(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 42;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1239(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1240(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 0;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1241(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1242(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775807;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1243(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) * ((__int128)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1244(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1245(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1246(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) < ((__int128)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1247(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) >= ((__int128)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1248(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) == ((__int128)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1249(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9223372036854775808;
  auto r = ((f) != ((__int128)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1250(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1251(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 9007199254740993;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1252(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) * ((__int128)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1253(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1254(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1255(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) <= ((__int128)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1256(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) > ((__int128)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1257(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) == ((__int128)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1258(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  int64_t f = 18446744073709551615;
  auto r = ((f) != ((__int128)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1259(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1260(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1261(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1262(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1263(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1264(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1265(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1266(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1267(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1268(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1269(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1270(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1271(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1272(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1273(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1274(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1275(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1276(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1277(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1278(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1279(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1280(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1281(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1282(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1283(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1284(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1285(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1286(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1287(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1288(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1289(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1290(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1291(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1292(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1293(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1294(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1295(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1296(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1297(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1298(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1299(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1300(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1301(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1302(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1303(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1304(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1305(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1306(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1307(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1308(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1309(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1310(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1311(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1312(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1313(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1314(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1315(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1316(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1317(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1318(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1319(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1320(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1321(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1322(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1323(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1324(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1325(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1326(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1327(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1328(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1329(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1330(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1331(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1332(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1333(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1334(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1335(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1336(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1337(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1338(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1339(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1340(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1341(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1342(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1343(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1344(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1345(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1346(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1347(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1348(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1349(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1350(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) + ((int64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1351(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) - ((int64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1352(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1353(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1354(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1355(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) - ((int64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1356(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1357(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1358(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) + ((int64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1359(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1360(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1361(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1362(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) - ((int64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1363(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1364(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1365(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1366(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) + ((int64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1367(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) - ((int64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1368(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1369(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1370(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1371(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) + ((int64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1372(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) * ((int64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1373(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1374(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1375(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) + ((uint64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1376(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) - ((uint64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1377(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1378(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1379(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1380(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) - ((uint64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1381(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1382(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1383(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) + ((uint64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1384(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1385(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1386(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1387(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) - ((uint64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1388(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1389(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1390(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1391(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) + ((uint64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1392(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) - ((uint64_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1393(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1394(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1395(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1396(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) + ((uint64_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1397(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1398(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1399(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1400(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1401(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 42;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1402(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1403(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 0;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1404(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1405(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775807;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1406(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1407(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9223372036854775808;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1408(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1409(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 9007199254740993;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1410(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) * ((__int128)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1411(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1412(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  uint64_t f = 18446744073709551615;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1413(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1414(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1415(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1416(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1417(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1418(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1419(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1420(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1421(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1422(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1423(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1424(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1425(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1426(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1427(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1428(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1429(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1430(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1431(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1432(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1433(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1434(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1435(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1436(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1437(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1438(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1439(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1440(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1441(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1442(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1443(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1444(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1445(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1446(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1447(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1448(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1449(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1450(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1451(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1452(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1453(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1454(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1455(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1456(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1457(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1458(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1459(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1460(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1461(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1462(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1463(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1464(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1465(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1466(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1467(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) < ((int32_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1468(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1469(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1470(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) >= ((int32_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1471(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1472(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1473(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1474(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1475(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) + ((int32_t)(c)));
  return sigof(r, "+", a, b);
}
static std::string T1476(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) - ((int32_t)(c)));
  return sigof(r, "-", a, b);
}
static std::string T1477(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) * ((int32_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1478(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1479(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) / ((int32_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1480(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1481(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) % ((int32_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1482(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) <= ((int32_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1483(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) > ((int32_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1484(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) == ((int32_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1485(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) != ((int32_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1486(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1487(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1488(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1489(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1490(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1491(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1492(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1493(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1494(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) < ((int64_t)(c)));
  return sigof(r, "<", a, b);
}
static std::string T1495(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) >= ((int64_t)(c)));
  return sigof(r, ">=", a, b);
}
static std::string T1496(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) == ((int64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1497(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) != ((int64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1498(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1499(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1500(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) / ((int64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1501(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) % ((int64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1502(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) <= ((int64_t)(c)));
  return sigof(r, "<=", a, b);
}
static std::string T1503(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) > ((int64_t)(c)));
  return sigof(r, ">", a, b);
}
static std::string T1504(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) == ((int64_t)(c)));
  return sigof(r, "==", a, b);
}
static std::string T1505(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) != ((int64_t)(c)));
  return sigof(r, "!=", a, b);
}
static std::string T1506(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1507(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1508(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1509(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1510(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1511(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1512(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1513(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1514(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1515(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1516(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) * ((uint64_t)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1517(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) / ((uint64_t)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1518(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) % ((uint64_t)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1519(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1520(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 42;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1521(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1522(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 0;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1523(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1524(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775807;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1525(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1526(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9223372036854775808;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1527(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1528(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 9007199254740993;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}
static std::string T1529(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) * ((__int128)(c)));
  return sigof(r, "*", a, b);
}
static std::string T1530(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) / ((__int128)(c)));
  return sigof(r, "/", a, b);
}
static std::string T1531(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  __int128 f = 18446744073709551615;
  auto r = ((f) % ((__int128)(c)));
  return sigof(r, "%", a, b);
}

static std::vector<int (*)()> TARGETS;

static void reg() {
  TARGETS.push_back([]() { return bisect(270, T270, "+", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(271, T271, "-", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(272, T272, "*", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(273, T273, "<", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(274, T274, "<=", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(275, T275, ">", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(276, T276, ">=", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(277, T277, "+", "42", "9007199254740993", "0", true); });
  TARGETS.push_back([]() { return bisect(278, T278, "-", "42", "9007199254740993", "0", true); });
  TARGETS.push_back([]() { return bisect(279, T279, "<", "9007199254740993", "9223372036854775807", "0", true); });
  TARGETS.push_back([]() { return bisect(280, T280, "<", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(281, T281, "<=", "9007199254740993", "9223372036854775807", "0", true); });
  TARGETS.push_back([]() { return bisect(282, T282, ">", "9007199254740993", "9223372036854775807", "0", true); });
  TARGETS.push_back([]() { return bisect(283, T283, ">=", "9007199254740993", "9223372036854775807", "0", true); });
  TARGETS.push_back([]() { return bisect(284, T284, ">=", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(285, T285, "==", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(286, T286, "!=", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(287, T287, "-", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(288, T288, "-", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(289, T289, "*", "0", "42", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(290, T290, "<", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(291, T291, "<=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(292, T292, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(293, T293, ">", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(294, T294, ">", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(295, T295, ">=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(296, T296, "==", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(297, T297, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(298, T298, "-", "9007199254740993", "9223372036854775807", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(299, T299, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(300, T300, "*", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(301, T301, "<", "9007199254740993", "9223372036854775807", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(302, T302, "<", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(303, T303, "<=", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(304, T304, "<=", "9007199254740993", "9223372036854775807", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(305, T305, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(306, T306, ">", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(307, T307, ">", "9007199254740993", "9223372036854775807", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(308, T308, ">", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(309, T309, ">=", "9007199254740993", "9223372036854775807", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(310, T310, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(311, T311, "==", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(312, T312, "!=", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(313, T313, "-", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(314, T314, "-", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(315, T315, "*", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(316, T316, "<", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(317, T317, "<", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(318, T318, "<", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(319, T319, "<=", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(320, T320, "<=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(321, T321, "<=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(322, T322, ">", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(323, T323, ">", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(324, T324, ">", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(325, T325, ">=", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(326, T326, ">=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(327, T327, ">=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(328, T328, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(329, T329, "*", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(330, T330, "<", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(331, T331, "<=", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(332, T332, "<=", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(333, T333, ">", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(334, T334, ">", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(335, T335, ">=", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(336, T336, "==", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(337, T337, "!=", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(338, T338, "+", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(339, T339, "-", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(340, T340, "*", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(341, T341, "<", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(342, T342, "<=", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(343, T343, ">", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(344, T344, ">=", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(345, T345, "+", "42", "9007199254740993", "0", true); });
  TARGETS.push_back([]() { return bisect(346, T346, "-", "42", "9007199254740993", "0", true); });
  TARGETS.push_back([]() { return bisect(347, T347, "<", "9007199254740993", "9223372036854775807", "0", true); });
  TARGETS.push_back([]() { return bisect(348, T348, "<", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(349, T349, "<=", "9007199254740993", "9223372036854775807", "0", true); });
  TARGETS.push_back([]() { return bisect(350, T350, ">", "9007199254740993", "9223372036854775807", "0", true); });
  TARGETS.push_back([]() { return bisect(351, T351, ">=", "9007199254740993", "9223372036854775807", "0", true); });
  TARGETS.push_back([]() { return bisect(352, T352, ">=", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(353, T353, "==", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(354, T354, "!=", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(355, T355, "+", "0", "42", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(356, T356, "-", "42", "9007199254740993", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(357, T357, "*", "0", "42", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(358, T358, "<", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(359, T359, ">=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(360, T360, "==", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(361, T361, "!=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(362, T362, "-", "42", "9007199254740993", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(363, T363, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(364, T364, "*", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(365, T365, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(366, T366, ">", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(367, T367, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(368, T368, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(369, T369, "+", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(370, T370, "-", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(371, T371, "*", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(372, T372, "<", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(373, T373, "<=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(374, T374, ">", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(375, T375, ">=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(376, T376, "==", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(377, T377, "==", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(378, T378, "!=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(379, T379, "!=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(380, T380, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(381, T381, "*", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(382, T382, "<", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(383, T383, "<=", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(384, T384, "<=", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(385, T385, ">", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(386, T386, ">", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(387, T387, ">=", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(388, T388, "==", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(389, T389, "!=", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(390, T390, "+", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(391, T391, "-", "0", "42", "42", true); });
  TARGETS.push_back([]() { return bisect(392, T392, "-", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(393, T393, "-", "9223372036854775808", "18446744073709551615", "42", true); });
  TARGETS.push_back([]() { return bisect(394, T394, "*", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(395, T395, "<", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(396, T396, "<", "9007199254740993", "9223372036854775807", "42", true); });
  TARGETS.push_back([]() { return bisect(397, T397, "<", "9223372036854775808", "18446744073709551615", "42", true); });
  TARGETS.push_back([]() { return bisect(398, T398, "<=", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(399, T399, "<=", "9007199254740993", "9223372036854775807", "42", true); });
  TARGETS.push_back([]() { return bisect(400, T400, "<=", "9223372036854775808", "18446744073709551615", "42", true); });
  TARGETS.push_back([]() { return bisect(401, T401, ">", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(402, T402, ">", "9007199254740993", "9223372036854775807", "42", true); });
  TARGETS.push_back([]() { return bisect(403, T403, ">", "9223372036854775808", "18446744073709551615", "42", true); });
  TARGETS.push_back([]() { return bisect(404, T404, ">=", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(405, T405, ">=", "9007199254740993", "9223372036854775807", "42", true); });
  TARGETS.push_back([]() { return bisect(406, T406, ">=", "9223372036854775808", "18446744073709551615", "42", true); });
  TARGETS.push_back([]() { return bisect(407, T407, "+", "42", "9007199254740993", "0", true); });
  TARGETS.push_back([]() { return bisect(408, T408, "+", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(409, T409, "-", "42", "9007199254740993", "0", true); });
  TARGETS.push_back([]() { return bisect(410, T410, "-", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(411, T411, "<=", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(412, T412, ">", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(413, T413, "==", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(414, T414, "!=", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(415, T415, "+", "42", "9007199254740993", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(416, T416, "-", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(417, T417, "*", "0", "42", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(418, T418, "<", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(419, T419, "<=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(420, T420, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(421, T421, ">", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(422, T422, ">", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(423, T423, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(424, T424, "==", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(425, T425, "!=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(426, T426, "+", "42", "9007199254740993", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(427, T427, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(428, T428, "*", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(429, T429, "<", "9007199254740993", "9223372036854775807", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(430, T430, "<", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(431, T431, "<=", "9007199254740993", "9223372036854775807", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(432, T432, ">", "9007199254740993", "9223372036854775807", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(433, T433, ">=", "9007199254740993", "9223372036854775807", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(434, T434, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(435, T435, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(436, T436, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(437, T437, "+", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(438, T438, "-", "9223372036854775808", "18446744073709551615", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(439, T439, "*", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(440, T440, "<", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(441, T441, "<", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(442, T442, "<", "9223372036854775808", "18446744073709551615", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(443, T443, "<=", "9223372036854775808", "18446744073709551615", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(444, T444, ">", "9223372036854775808", "18446744073709551615", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(445, T445, ">=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(446, T446, ">=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(447, T447, ">=", "9223372036854775808", "18446744073709551615", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(448, T448, "==", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(449, T449, "==", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(450, T450, "!=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(451, T451, "!=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(452, T452, "+", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(453, T453, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(454, T454, "*", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(455, T455, "<", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(456, T456, ">=", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(457, T457, "==", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(458, T458, "!=", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(459, T459, "+", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(460, T460, "-", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(461, T461, "*", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(462, T462, "<", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(463, T463, "<=", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(464, T464, ">", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(465, T465, ">=", "42", "9007199254740993", "42", true); });
  TARGETS.push_back([]() { return bisect(466, T466, "+", "42", "9007199254740993", "0", true); });
  TARGETS.push_back([]() { return bisect(467, T467, "-", "42", "9007199254740993", "0", true); });
  TARGETS.push_back([]() { return bisect(468, T468, "<", "9007199254740993", "9223372036854775807", "0", true); });
  TARGETS.push_back([]() { return bisect(469, T469, "<", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(470, T470, "<=", "9007199254740993", "9223372036854775807", "0", true); });
  TARGETS.push_back([]() { return bisect(471, T471, ">", "9007199254740993", "9223372036854775807", "0", true); });
  TARGETS.push_back([]() { return bisect(472, T472, ">=", "9007199254740993", "9223372036854775807", "0", true); });
  TARGETS.push_back([]() { return bisect(473, T473, ">=", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(474, T474, "==", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(475, T475, "!=", "9223372036854775808", "18446744073709551615", "0", true); });
  TARGETS.push_back([]() { return bisect(476, T476, "+", "42", "9007199254740993", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(477, T477, "-", "42", "9007199254740993", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(478, T478, "*", "42", "9007199254740993", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(479, T479, "<", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(480, T480, ">=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(481, T481, "==", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(482, T482, "!=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(483, T483, "+", "42", "9007199254740993", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(484, T484, "-", "42", "9007199254740993", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(485, T485, "*", "42", "9007199254740993", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(486, T486, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(487, T487, ">", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(488, T488, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(489, T489, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(490, T490, "+", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(491, T491, "-", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(492, T492, "*", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(493, T493, "<", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(494, T494, "<=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(495, T495, ">", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(496, T496, ">=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(497, T497, "==", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(498, T498, "==", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(499, T499, "!=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(500, T500, "!=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(501, T501, "+", "42", "9007199254740993", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(502, T502, "-", "42", "9007199254740993", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(503, T503, "*", "42", "9007199254740993", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(504, T504, "<", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(505, T505, ">=", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(506, T506, "==", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(507, T507, "!=", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(566, T566, "+", "9007199254740993", "9223372036854775807", "42", true); });
  TARGETS.push_back([]() { return bisect(567, T567, "-", "9223372036854775808", "18446744073709551615", "42", true); });
  TARGETS.push_back([]() { return bisect(568, T568, "*", "9007199254740993", "9223372036854775807", "42", true); });
  TARGETS.push_back([]() { return bisect(569, T569, "*", "0", "42", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(570, T570, "/", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(571, T571, "%", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(572, T572, "<", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(573, T573, "<", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(574, T574, ">=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(575, T575, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(576, T576, "==", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(577, T577, "==", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(578, T578, "!=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(579, T579, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(580, T580, "*", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(581, T581, "<=", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(582, T582, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(583, T583, ">", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(584, T584, ">", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(585, T585, "==", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(586, T586, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(587, T587, "!=", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(588, T588, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(589, T589, "*", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(590, T590, "<", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(591, T591, "<", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(592, T592, "<=", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(593, T593, "<=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(594, T594, ">", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(595, T595, ">", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(596, T596, ">=", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(597, T597, ">=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(598, T598, "==", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(599, T599, "==", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(600, T600, "!=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(601, T601, "!=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(602, T602, "-", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(603, T603, "*", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(604, T604, "/", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(605, T605, "%", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(606, T606, "+", "9007199254740993", "9223372036854775807", "42", true); });
  TARGETS.push_back([]() { return bisect(607, T607, "-", "9223372036854775808", "18446744073709551615", "42", true); });
  TARGETS.push_back([]() { return bisect(608, T608, "*", "9007199254740993", "9223372036854775807", "42", true); });
  TARGETS.push_back([]() { return bisect(609, T609, "+", "0", "42", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(610, T610, "-", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(611, T611, "*", "0", "42", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(612, T612, "*", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(613, T613, "+", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(614, T614, "-", "9223372036854775808", "18446744073709551615", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(615, T615, "*", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(616, T616, "-", "9007199254740993", "9223372036854775807", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(617, T617, "*", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(618, T618, "/", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(619, T619, "%", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(620, T620, "+", "9223372036854775808", "18446744073709551615", "42", true); });
  TARGETS.push_back([]() { return bisect(621, T621, "-", "0", "42", "42", true); });
  TARGETS.push_back([]() { return bisect(622, T622, "*", "9007199254740993", "9223372036854775807", "42", true); });
  TARGETS.push_back([]() { return bisect(623, T623, "+", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(624, T624, "-", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(625, T625, "*", "0", "42", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(626, T626, "*", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(627, T627, "+", "9223372036854775808", "18446744073709551615", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(628, T628, "-", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(629, T629, "*", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(630, T630, "+", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(631, T631, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(632, T632, "*", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(633, T633, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(634, T634, ">", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(635, T635, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(636, T636, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(637, T637, "<", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(638, T638, ">=", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(639, T639, "==", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(640, T640, "!=", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(671, T671, "+", "9223372036854775808", "18446744073709551615", "42", true); });
  TARGETS.push_back([]() { return bisect(672, T672, "-", "0", "42", "42", true); });
  TARGETS.push_back([]() { return bisect(673, T673, "*", "9007199254740993", "9223372036854775807", "42", true); });
  TARGETS.push_back([]() { return bisect(674, T674, "*", "0", "42", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(675, T675, "<", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(676, T676, "<", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(677, T677, ">=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(678, T678, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(679, T679, "==", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(680, T680, "==", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(681, T681, "!=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(682, T682, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(683, T683, "*", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(684, T684, "<=", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(685, T685, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(686, T686, ">", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(687, T687, ">", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(688, T688, "==", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(689, T689, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(690, T690, "!=", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(691, T691, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(692, T692, "*", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(693, T693, "<", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(694, T694, "<", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(695, T695, "<=", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(696, T696, "<=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(697, T697, ">", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(698, T698, ">", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(699, T699, ">=", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(700, T700, ">=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(701, T701, "==", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(702, T702, "==", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(703, T703, "!=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(704, T704, "!=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(705, T705, "+", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(706, T706, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(707, T707, "*", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(708, T708, "+", "9223372036854775808", "18446744073709551615", "42", true); });
  TARGETS.push_back([]() { return bisect(709, T709, "-", "0", "42", "42", true); });
  TARGETS.push_back([]() { return bisect(710, T710, "*", "9007199254740993", "9223372036854775807", "42", true); });
  TARGETS.push_back([]() { return bisect(711, T711, "+", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(712, T712, "-", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(713, T713, "*", "0", "42", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(714, T714, "*", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(715, T715, "+", "9223372036854775808", "18446744073709551615", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(716, T716, "-", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(717, T717, "*", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(718, T718, "+", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(719, T719, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(720, T720, "*", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(721, T721, "+", "9223372036854775808", "18446744073709551615", "42", true); });
  TARGETS.push_back([]() { return bisect(722, T722, "-", "0", "42", "42", true); });
  TARGETS.push_back([]() { return bisect(723, T723, "*", "9007199254740993", "9223372036854775807", "42", true); });
  TARGETS.push_back([]() { return bisect(724, T724, "+", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(725, T725, "-", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(726, T726, "*", "0", "42", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(727, T727, "*", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(728, T728, "+", "9223372036854775808", "18446744073709551615", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(729, T729, "-", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(730, T730, "*", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(731, T731, "+", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(732, T732, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(733, T733, "*", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(734, T734, "*", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(773, T773, "*", "0", "42", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(774, T774, "<", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(775, T775, ">=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(776, T776, "==", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(777, T777, "!=", "9007199254740993", "9223372036854775807", "9223372036854775807", true); });
  TARGETS.push_back([]() { return bisect(778, T778, "*", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(779, T779, "<=", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(780, T780, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(781, T781, ">", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(782, T782, ">", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(783, T783, "==", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(784, T784, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(785, T785, "!=", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(786, T786, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(787, T787, "*", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(788, T788, "<", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(789, T789, "<", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(790, T790, "<=", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(791, T791, "<=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(792, T792, ">", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(793, T793, ">", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(794, T794, ">=", "0", "42", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(795, T795, ">=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(796, T796, "==", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(797, T797, "==", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(798, T798, "!=", "42", "9007199254740993", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(799, T799, "!=", "9007199254740993", "9223372036854775807", "9007199254740993", true); });
  TARGETS.push_back([]() { return bisect(800, T800, "*", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(801, T801, "<", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(802, T802, ">=", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(803, T803, "==", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(804, T804, "!=", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(805, T805, "*", "0", "42", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(806, T806, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(807, T807, ">", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(808, T808, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(809, T809, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); });
  TARGETS.push_back([]() { return bisect(810, T810, "*", "0", "42", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(811, T811, "<", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(812, T812, ">=", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(813, T813, "==", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(814, T814, "!=", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(815, T815, "*", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(816, T816, "*", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); });
  TARGETS.push_back([]() { return bisect(875, T875, "+", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(876, T876, "-", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(877, T877, "*", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(878, T878, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(879, T879, "/", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(880, T880, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(881, T881, "%", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(882, T882, "<", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(883, T883, "<=", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(884, T884, ">", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(885, T885, ">=", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(886, T886, "+", "42", "9007199254740993", "0", false); });
  TARGETS.push_back([]() { return bisect(887, T887, "-", "42", "9007199254740993", "0", false); });
  TARGETS.push_back([]() { return bisect(888, T888, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(889, T889, "/", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(890, T890, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(891, T891, "%", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(892, T892, "<", "9007199254740993", "9223372036854775807", "0", false); });
  TARGETS.push_back([]() { return bisect(893, T893, "<=", "9007199254740993", "9223372036854775807", "0", false); });
  TARGETS.push_back([]() { return bisect(894, T894, "<=", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(895, T895, ">", "9007199254740993", "9223372036854775807", "0", false); });
  TARGETS.push_back([]() { return bisect(896, T896, ">", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(897, T897, ">=", "9007199254740993", "9223372036854775807", "0", false); });
  TARGETS.push_back([]() { return bisect(898, T898, "==", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(899, T899, "!=", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(900, T900, "-", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(901, T901, "-", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(902, T902, "*", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(903, T903, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(904, T904, "/", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(905, T905, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(906, T906, "%", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(907, T907, "<", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(908, T908, "<", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(909, T909, "<=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(910, T910, ">", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(911, T911, ">=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(912, T912, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(913, T913, "==", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(914, T914, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(915, T915, "-", "9007199254740993", "9223372036854775807", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(916, T916, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(917, T917, "*", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(918, T918, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(919, T919, "/", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(920, T920, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(921, T921, "%", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(922, T922, "<", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(923, T923, "<", "9007199254740993", "9223372036854775807", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(924, T924, "<", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(925, T925, "<=", "9007199254740993", "9223372036854775807", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(926, T926, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(927, T927, ">", "9007199254740993", "9223372036854775807", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(928, T928, ">", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(929, T929, ">=", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(930, T930, ">=", "9007199254740993", "9223372036854775807", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(931, T931, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(932, T932, "==", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(933, T933, "!=", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(934, T934, "-", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(935, T935, "-", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(936, T936, "*", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(937, T937, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(938, T938, "/", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(939, T939, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(940, T940, "%", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(941, T941, "<", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(942, T942, "<", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(943, T943, "<", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(944, T944, "<=", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(945, T945, "<=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(946, T946, "<=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(947, T947, ">", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(948, T948, ">", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(949, T949, ">", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(950, T950, ">=", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(951, T951, ">=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(952, T952, ">=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(953, T953, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(954, T954, "*", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(955, T955, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(956, T956, "/", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(957, T957, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(958, T958, "%", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(959, T959, "<", "9007199254740993", "9223372036854775807", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(960, T960, "<", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(961, T961, "<=", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(962, T962, ">", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(963, T963, ">=", "9007199254740993", "9223372036854775807", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(964, T964, ">=", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(965, T965, "==", "9007199254740993", "9223372036854775807", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(966, T966, "!=", "9007199254740993", "9223372036854775807", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(967, T967, "+", "9007199254740993", "9223372036854775807", "42", false); });
  TARGETS.push_back([]() { return bisect(968, T968, "-", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(969, T969, "*", "9007199254740993", "9223372036854775807", "42", false); });
  TARGETS.push_back([]() { return bisect(970, T970, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(971, T971, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(972, T972, "-", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(973, T973, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(974, T974, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(975, T975, "*", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(976, T976, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(977, T977, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(978, T978, "<=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(979, T979, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(980, T980, ">", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(981, T981, ">", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(982, T982, "==", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(983, T983, "==", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(984, T984, "!=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(985, T985, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(986, T986, "*", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(987, T987, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(988, T988, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(989, T989, "<", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(990, T990, "<", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(991, T991, ">=", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(992, T992, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(993, T993, "==", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(994, T994, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(995, T995, "!=", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(996, T996, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(997, T997, "*", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(998, T998, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(999, T999, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1000, T1000, "<", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1001, T1001, "<", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1002, T1002, "<=", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1003, T1003, "<=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1004, T1004, ">", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1005, T1005, ">", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1006, T1006, ">=", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1007, T1007, ">=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1008, T1008, "==", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1009, T1009, "==", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1010, T1010, "!=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1011, T1011, "!=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1012, T1012, "*", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1013, T1013, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1014, T1014, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1015, T1015, "+", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1016, T1016, "-", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1017, T1017, "*", "9007199254740993", "9223372036854775807", "42", false); });
  TARGETS.push_back([]() { return bisect(1018, T1018, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1019, T1019, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1020, T1020, "-", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1021, T1021, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1022, T1022, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1023, T1023, "*", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1024, T1024, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1025, T1025, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1026, T1026, "<=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1027, T1027, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1028, T1028, ">", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1029, T1029, ">", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1030, T1030, "==", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1031, T1031, "==", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1032, T1032, "!=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1033, T1033, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1034, T1034, "*", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1035, T1035, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1036, T1036, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1037, T1037, "<", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1038, T1038, "<", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1039, T1039, ">=", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1040, T1040, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1041, T1041, "==", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1042, T1042, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1043, T1043, "!=", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1044, T1044, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1045, T1045, "*", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1046, T1046, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1047, T1047, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1048, T1048, "<", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1049, T1049, "<", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1050, T1050, "<=", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1051, T1051, "<=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1052, T1052, ">", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1053, T1053, ">", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1054, T1054, ">=", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1055, T1055, ">=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1056, T1056, "==", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1057, T1057, "==", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1058, T1058, "!=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1059, T1059, "!=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1060, T1060, "+", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1061, T1061, "*", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1062, T1062, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1063, T1063, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1064, T1064, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1065, T1065, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1066, T1066, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1067, T1067, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1068, T1068, "*", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1069, T1069, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1070, T1070, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1071, T1071, "<=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1072, T1072, ">", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1073, T1073, "==", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1074, T1074, "!=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1075, T1075, "*", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1076, T1076, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1077, T1077, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1078, T1078, "<", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1079, T1079, "<", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1080, T1080, ">=", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1081, T1081, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1082, T1082, "==", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1083, T1083, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1084, T1084, "!=", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1085, T1085, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1086, T1086, "*", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1087, T1087, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1088, T1088, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1089, T1089, "<", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1090, T1090, "<", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1091, T1091, "<=", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1092, T1092, "<=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1093, T1093, ">", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1094, T1094, ">", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1095, T1095, ">=", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1096, T1096, ">=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1097, T1097, "==", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1098, T1098, "==", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1099, T1099, "!=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1100, T1100, "!=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1101, T1101, "*", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1102, T1102, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1103, T1103, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1104, T1104, "<=", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1105, T1105, ">", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1106, T1106, "==", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1107, T1107, "!=", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1108, T1108, "+", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1109, T1109, "-", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1110, T1110, "*", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1111, T1111, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1112, T1112, "/", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1113, T1113, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1114, T1114, "%", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1115, T1115, "<", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1116, T1116, "<=", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1117, T1117, ">", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1118, T1118, ">=", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1119, T1119, "+", "42", "9007199254740993", "0", false); });
  TARGETS.push_back([]() { return bisect(1120, T1120, "-", "42", "9007199254740993", "0", false); });
  TARGETS.push_back([]() { return bisect(1121, T1121, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1122, T1122, "/", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1123, T1123, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1124, T1124, "%", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1125, T1125, "<", "9007199254740993", "9223372036854775807", "0", false); });
  TARGETS.push_back([]() { return bisect(1126, T1126, "<=", "9007199254740993", "9223372036854775807", "0", false); });
  TARGETS.push_back([]() { return bisect(1127, T1127, "<=", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1128, T1128, ">", "9007199254740993", "9223372036854775807", "0", false); });
  TARGETS.push_back([]() { return bisect(1129, T1129, ">", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1130, T1130, ">=", "9007199254740993", "9223372036854775807", "0", false); });
  TARGETS.push_back([]() { return bisect(1131, T1131, "==", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1132, T1132, "!=", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1133, T1133, "+", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1134, T1134, "-", "42", "9007199254740993", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1135, T1135, "-", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1136, T1136, "*", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1137, T1137, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1138, T1138, "/", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1139, T1139, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1140, T1140, "%", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1141, T1141, "<=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1142, T1142, ">", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1143, T1143, "==", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1144, T1144, "!=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1145, T1145, "-", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1146, T1146, "-", "42", "9007199254740993", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1147, T1147, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1148, T1148, "*", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1149, T1149, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1150, T1150, "/", "9007199254740993", "9223372036854775807", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1151, T1151, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1152, T1152, "%", "9007199254740993", "9223372036854775807", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1153, T1153, "<", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1154, T1154, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1155, T1155, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1156, T1156, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1157, T1157, "+", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1158, T1158, "-", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1159, T1159, "*", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1160, T1160, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1161, T1161, "/", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1162, T1162, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1163, T1163, "%", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1164, T1164, "<", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1165, T1165, "<=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1166, T1166, ">", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1167, T1167, ">=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1168, T1168, "==", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1169, T1169, "==", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1170, T1170, "!=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1171, T1171, "!=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1172, T1172, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1173, T1173, "*", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1174, T1174, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1175, T1175, "/", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1176, T1176, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1177, T1177, "%", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1178, T1178, "<", "9007199254740993", "9223372036854775807", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1179, T1179, "<", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1180, T1180, "<=", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1181, T1181, ">", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1182, T1182, ">=", "9007199254740993", "9223372036854775807", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1183, T1183, ">=", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1184, T1184, "==", "9007199254740993", "9223372036854775807", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1185, T1185, "!=", "9007199254740993", "9223372036854775807", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1186, T1186, "+", "9007199254740993", "9223372036854775807", "42", false); });
  TARGETS.push_back([]() { return bisect(1187, T1187, "-", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1188, T1188, "*", "9007199254740993", "9223372036854775807", "42", false); });
  TARGETS.push_back([]() { return bisect(1189, T1189, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1190, T1190, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1191, T1191, "-", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1192, T1192, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1193, T1193, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1194, T1194, "+", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1195, T1195, "*", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1196, T1196, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1197, T1197, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1198, T1198, "-", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1199, T1199, "*", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1200, T1200, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1201, T1201, "/", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1202, T1202, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1203, T1203, "%", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1204, T1204, "+", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1205, T1205, "-", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1206, T1206, "*", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1207, T1207, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1208, T1208, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1209, T1209, "*", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1210, T1210, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1211, T1211, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1212, T1212, "+", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1213, T1213, "-", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1214, T1214, "*", "9007199254740993", "9223372036854775807", "42", false); });
  TARGETS.push_back([]() { return bisect(1215, T1215, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1216, T1216, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1217, T1217, "-", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1218, T1218, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1219, T1219, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1220, T1220, "+", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1221, T1221, "*", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1222, T1222, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1223, T1223, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1224, T1224, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1225, T1225, "*", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1226, T1226, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1227, T1227, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1228, T1228, "+", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1229, T1229, "-", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1230, T1230, "*", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1231, T1231, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1232, T1232, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1233, T1233, "+", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1234, T1234, "*", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1235, T1235, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1236, T1236, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1237, T1237, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1238, T1238, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1239, T1239, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1240, T1240, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1241, T1241, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1242, T1242, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1243, T1243, "*", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1244, T1244, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1245, T1245, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1246, T1246, "<", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1247, T1247, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1248, T1248, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1249, T1249, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1250, T1250, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1251, T1251, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1252, T1252, "*", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1253, T1253, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1254, T1254, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1255, T1255, "<=", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1256, T1256, ">", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1257, T1257, "==", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1258, T1258, "!=", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1259, T1259, "+", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1260, T1260, "-", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1261, T1261, "*", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1262, T1262, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1263, T1263, "/", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1264, T1264, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1265, T1265, "%", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1266, T1266, "<", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1267, T1267, "<", "9007199254740993", "9223372036854775807", "42", false); });
  TARGETS.push_back([]() { return bisect(1268, T1268, "<", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1269, T1269, "<=", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1270, T1270, "<=", "9007199254740993", "9223372036854775807", "42", false); });
  TARGETS.push_back([]() { return bisect(1271, T1271, "<=", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1272, T1272, ">", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1273, T1273, ">", "9007199254740993", "9223372036854775807", "42", false); });
  TARGETS.push_back([]() { return bisect(1274, T1274, ">", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1275, T1275, ">=", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1276, T1276, ">=", "9007199254740993", "9223372036854775807", "42", false); });
  TARGETS.push_back([]() { return bisect(1277, T1277, ">=", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1278, T1278, "+", "42", "9007199254740993", "0", false); });
  TARGETS.push_back([]() { return bisect(1279, T1279, "+", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1280, T1280, "-", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1281, T1281, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1282, T1282, "/", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1283, T1283, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1284, T1284, "%", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1285, T1285, "<", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1286, T1286, ">=", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1287, T1287, "==", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1288, T1288, "!=", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1289, T1289, "+", "42", "9007199254740993", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1290, T1290, "-", "42", "9007199254740993", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1291, T1291, "*", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1292, T1292, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1293, T1293, "/", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1294, T1294, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1295, T1295, "%", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1296, T1296, "<", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1297, T1297, "<", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1298, T1298, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1299, T1299, ">", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1300, T1300, ">=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1301, T1301, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1302, T1302, "==", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1303, T1303, "!=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1304, T1304, "+", "42", "9007199254740993", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1305, T1305, "-", "42", "9007199254740993", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1306, T1306, "*", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1307, T1307, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1308, T1308, "/", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1309, T1309, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1310, T1310, "%", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1311, T1311, "<", "9007199254740993", "9223372036854775807", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1312, T1312, "<=", "9007199254740993", "9223372036854775807", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1313, T1313, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1314, T1314, ">", "9007199254740993", "9223372036854775807", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1315, T1315, ">", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1316, T1316, ">=", "9007199254740993", "9223372036854775807", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1317, T1317, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1318, T1318, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1319, T1319, "+", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1320, T1320, "-", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1321, T1321, "*", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1322, T1322, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1323, T1323, "/", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1324, T1324, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1325, T1325, "%", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1326, T1326, "<", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1327, T1327, "<=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1328, T1328, "<=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1329, T1329, "<=", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1330, T1330, ">", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1331, T1331, ">", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1332, T1332, ">", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1333, T1333, ">=", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1334, T1334, "==", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1335, T1335, "==", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1336, T1336, "!=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1337, T1337, "!=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1338, T1338, "+", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1339, T1339, "-", "42", "9007199254740993", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1340, T1340, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1341, T1341, "*", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1342, T1342, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1343, T1343, "/", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1344, T1344, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1345, T1345, "%", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1346, T1346, "<=", "9007199254740993", "9223372036854775807", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1347, T1347, ">", "9007199254740993", "9223372036854775807", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1348, T1348, "==", "9007199254740993", "9223372036854775807", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1349, T1349, "!=", "9007199254740993", "9223372036854775807", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1350, T1350, "+", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1351, T1351, "-", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1352, T1352, "*", "9007199254740993", "9223372036854775807", "42", false); });
  TARGETS.push_back([]() { return bisect(1353, T1353, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1354, T1354, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1355, T1355, "-", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1356, T1356, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1357, T1357, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1358, T1358, "+", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1359, T1359, "*", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1360, T1360, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1361, T1361, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1362, T1362, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1363, T1363, "*", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1364, T1364, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1365, T1365, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1366, T1366, "+", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1367, T1367, "-", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1368, T1368, "*", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1369, T1369, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1370, T1370, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1371, T1371, "+", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1372, T1372, "*", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1373, T1373, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1374, T1374, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1375, T1375, "+", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1376, T1376, "-", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1377, T1377, "*", "9007199254740993", "9223372036854775807", "42", false); });
  TARGETS.push_back([]() { return bisect(1378, T1378, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1379, T1379, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1380, T1380, "-", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1381, T1381, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1382, T1382, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1383, T1383, "+", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1384, T1384, "*", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1385, T1385, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1386, T1386, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1387, T1387, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1388, T1388, "*", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1389, T1389, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1390, T1390, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1391, T1391, "+", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1392, T1392, "-", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1393, T1393, "*", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1394, T1394, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1395, T1395, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1396, T1396, "+", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1397, T1397, "*", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1398, T1398, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1399, T1399, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1400, T1400, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1401, T1401, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1402, T1402, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1403, T1403, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1404, T1404, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1405, T1405, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1406, T1406, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1407, T1407, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1408, T1408, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1409, T1409, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1410, T1410, "*", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1411, T1411, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1412, T1412, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1413, T1413, "+", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1414, T1414, "-", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1415, T1415, "*", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1416, T1416, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1417, T1417, "/", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1418, T1418, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1419, T1419, "%", "9223372036854775808", "18446744073709551615", "42", false); });
  TARGETS.push_back([]() { return bisect(1420, T1420, "<", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1421, T1421, "<=", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1422, T1422, ">", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1423, T1423, ">=", "42", "9007199254740993", "42", false); });
  TARGETS.push_back([]() { return bisect(1424, T1424, "+", "42", "9007199254740993", "0", false); });
  TARGETS.push_back([]() { return bisect(1425, T1425, "-", "42", "9007199254740993", "0", false); });
  TARGETS.push_back([]() { return bisect(1426, T1426, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1427, T1427, "/", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1428, T1428, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1429, T1429, "%", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1430, T1430, "<", "9007199254740993", "9223372036854775807", "0", false); });
  TARGETS.push_back([]() { return bisect(1431, T1431, "<=", "9007199254740993", "9223372036854775807", "0", false); });
  TARGETS.push_back([]() { return bisect(1432, T1432, "<=", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1433, T1433, ">", "9007199254740993", "9223372036854775807", "0", false); });
  TARGETS.push_back([]() { return bisect(1434, T1434, ">", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1435, T1435, ">=", "9007199254740993", "9223372036854775807", "0", false); });
  TARGETS.push_back([]() { return bisect(1436, T1436, "==", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1437, T1437, "!=", "9223372036854775808", "18446744073709551615", "0", false); });
  TARGETS.push_back([]() { return bisect(1438, T1438, "+", "42", "9007199254740993", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1439, T1439, "-", "42", "9007199254740993", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1440, T1440, "*", "42", "9007199254740993", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1441, T1441, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1442, T1442, "/", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1443, T1443, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1444, T1444, "%", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1445, T1445, "<=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1446, T1446, ">", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1447, T1447, "==", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1448, T1448, "!=", "9007199254740993", "9223372036854775807", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1449, T1449, "+", "42", "9007199254740993", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1450, T1450, "-", "42", "9007199254740993", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1451, T1451, "*", "42", "9007199254740993", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1452, T1452, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1453, T1453, "/", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1454, T1454, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1455, T1455, "%", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1456, T1456, "<", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1457, T1457, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1458, T1458, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1459, T1459, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1460, T1460, "+", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1461, T1461, "-", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1462, T1462, "*", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1463, T1463, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1464, T1464, "/", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1465, T1465, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1466, T1466, "%", "9223372036854775808", "18446744073709551615", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1467, T1467, "<", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1468, T1468, "<=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1469, T1469, ">", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1470, T1470, ">=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1471, T1471, "==", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1472, T1472, "==", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1473, T1473, "!=", "42", "9007199254740993", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1474, T1474, "!=", "9007199254740993", "9223372036854775807", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1475, T1475, "+", "42", "9007199254740993", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1476, T1476, "-", "42", "9007199254740993", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1477, T1477, "*", "42", "9007199254740993", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1478, T1478, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1479, T1479, "/", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1480, T1480, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1481, T1481, "%", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1482, T1482, "<=", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1483, T1483, ">", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1484, T1484, "==", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1485, T1485, "!=", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1486, T1486, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1487, T1487, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1488, T1488, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1489, T1489, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1490, T1490, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1491, T1491, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1492, T1492, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1493, T1493, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1494, T1494, "<", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1495, T1495, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1496, T1496, "==", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1497, T1497, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1498, T1498, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1499, T1499, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1500, T1500, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1501, T1501, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1502, T1502, "<=", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1503, T1503, ">", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1504, T1504, "==", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1505, T1505, "!=", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1506, T1506, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1507, T1507, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1508, T1508, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1509, T1509, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1510, T1510, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1511, T1511, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1512, T1512, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1513, T1513, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1514, T1514, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1515, T1515, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1516, T1516, "*", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1517, T1517, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1518, T1518, "%", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1519, T1519, "/", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1520, T1520, "%", "0", "42", "42", false); });
  TARGETS.push_back([]() { return bisect(1521, T1521, "/", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1522, T1522, "%", "0", "42", "0", false); });
  TARGETS.push_back([]() { return bisect(1523, T1523, "/", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1524, T1524, "%", "0", "42", "9223372036854775807", false); });
  TARGETS.push_back([]() { return bisect(1525, T1525, "/", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1526, T1526, "%", "0", "42", "9223372036854775808", false); });
  TARGETS.push_back([]() { return bisect(1527, T1527, "/", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1528, T1528, "%", "0", "42", "9007199254740993", false); });
  TARGETS.push_back([]() { return bisect(1529, T1529, "*", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1530, T1530, "/", "0", "42", "18446744073709551615", false); });
  TARGETS.push_back([]() { return bisect(1531, T1531, "%", "0", "42", "18446744073709551615", false); });
}

int main() {
  signal(SIGFPE, onfpe);
  reg();
  int total = 0;
  int n = (int)TARGETS.size();
  for (int k = 0; k < n; k++) {
    total += TARGETS[k]();
    if ((k + 1) % 25 == 0 || k + 1 == n)
      fprintf(stderr, "progress %d/%d probes=%d\n", k + 1, n, total);
    fflush(stdout);
  }
  fprintf(stderr, "DONE targets=%d probes=%d\n", n, total);
  return 0;
}
