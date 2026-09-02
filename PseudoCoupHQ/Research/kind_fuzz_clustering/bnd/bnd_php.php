<?php
// this php has neither ext-gmp nor ext-bcmath, so the reference
// arithmetic is decimal strings, done here.  bi_* take and give
// strings like "-9223372036854775808".
function bi_norm($s) {
  $s = trim($s); $neg = false;
  if ($s !== "" && ($s[0] === "-" || $s[0] === "+")) {
    $neg = $s[0] === "-"; $s = substr($s, 1);
  }
  $s = ltrim($s, "0"); if ($s === "") { $s = "0"; $neg = false; }
  return ($neg ? "-" : "") . $s;
}
function bi_neg($a) {
  $a = bi_norm($a);
  if ($a === "0") return "0";
  return $a[0] === "-" ? substr($a, 1) : "-" . $a;
}
function bi_ucmp($a, $b) {
  if (strlen($a) != strlen($b)) return strlen($a) < strlen($b) ? -1 : 1;
  return strcmp($a, $b) <=> 0;
}
function bi_uadd($a, $b) {
  $r = ""; $c = 0; $i = strlen($a) - 1; $j = strlen($b) - 1;
  while ($i >= 0 || $j >= 0 || $c) {
    $d = $c;
    if ($i >= 0) $d += ord($a[$i--]) - 48;
    if ($j >= 0) $d += ord($b[$j--]) - 48;
    $c = intdiv($d, 10); $r = chr(48 + $d % 10) . $r;
  }
  return bi_norm($r);
}
function bi_usub($a, $b) {          // a >= b
  $r = ""; $c = 0; $i = strlen($a) - 1; $j = strlen($b) - 1;
  while ($i >= 0) {
    $d = (ord($a[$i--]) - 48) - $c - ($j >= 0 ? ord($b[$j--]) - 48 : 0);
    if ($d < 0) { $d += 10; $c = 1; } else { $c = 0; }
    $r = chr(48 + $d) . $r;
  }
  return bi_norm($r);
}
function bi_umul($a, $b) {
  $n = strlen($a); $m = strlen($b); $p = array_fill(0, $n + $m, 0);
  for ($i = $n - 1; $i >= 0; $i--) {
    $x = ord($a[$i]) - 48;
    for ($j = $m - 1; $j >= 0; $j--) {
      $p[$i + $j + 1] += $x * (ord($b[$j]) - 48);
    }
  }
  for ($k = $n + $m - 1; $k > 0; $k--) {
    $p[$k - 1] += intdiv($p[$k], 10); $p[$k] %= 10;
  }
  $s = ""; foreach ($p as $d) $s .= chr(48 + $d);
  return bi_norm($s);
}
function bi_parts($a) {
  $a = bi_norm($a);
  if ($a[0] === "-") return [true, substr($a, 1)];
  return [false, $a];
}
function bi_add($a, $b) {
  list($sa, $ua) = bi_parts($a); list($sb, $ub) = bi_parts($b);
  if ($sa === $sb) { $r = bi_uadd($ua, $ub); return $sa ? bi_neg($r) : $r; }
  $c = bi_ucmp($ua, $ub);
  if ($c === 0) return "0";
  if ($c > 0) { $r = bi_usub($ua, $ub); return $sa ? bi_neg($r) : $r; }
  $r = bi_usub($ub, $ua); return $sb ? bi_neg($r) : $r;
}
function bi_sub($a, $b) { return bi_add($a, bi_neg($b)); }
function bi_mul($a, $b) {
  list($sa, $ua) = bi_parts($a); list($sb, $ub) = bi_parts($b);
  $r = bi_umul($ua, $ub);
  if ($r === "0") return "0";
  return ($sa xor $sb) ? bi_neg($r) : $r;
}
function bi_cmp($a, $b) {
  list($sa, $ua) = bi_parts($a); list($sb, $ub) = bi_parts($b);
  if ($sa !== $sb) return $sa ? -1 : 1;
  $c = bi_ucmp($ua, $ub);
  return $sa ? -$c : $c;
}
function bi_half($a) {              // floor(a / 2), a >= 0
  list($sa, $u) = bi_parts($a); $r = ""; $c = 0;
  for ($i = 0; $i < strlen($u); $i++) {
    $d = $c * 10 + ord($u[$i]) - 48;
    $r .= chr(48 + intdiv($d, 2)); $c = $d % 2;
  }
  return bi_norm($r);
}

$EXACT = ["+", "-", "*", "<", "<=", ">", ">=", "==", "!="];

function wantv($op, $a, $b) {
  global $EXACT;
  if (!in_array($op, $EXACT, true)) return null;
  switch ($op) {
    case "+": return bi_add($a, $b);
    case "-": return bi_sub($a, $b);
    case "*": return bi_mul($a, $b);
    case "<": return bi_cmp($a, $b) < 0;
    case "<=": return bi_cmp($a, $b) <= 0;
    case ">": return bi_cmp($a, $b) > 0;
    case ">=": return bi_cmp($a, $b) >= 0;
    case "==": return bi_cmp($a, $b) == 0;
    case "!=": return bi_cmp($a, $b) != 0;
  }
  return null;
}

function asint($r) {
  if (is_bool($r)) return $r;
  if (is_int($r)) return (string)$r;
  if (is_float($r)) {
    if (is_nan($r) || is_infinite($r)) return null;
    if (floor($r) != $r) return "NONINT";
    return bi_norm(sprintf("%.0f", $r));
  }
  if (is_string($r) && preg_match('/^-?[0-9]+$/', $r)) return bi_norm($r);
  return null;
}

function fidv($r, $op, $a, $b) {
  $w = wantv($op, $a, $b);
  if ($w === null) return "na";
  $g = asint($r);
  if ($g === null) return "na";
  if (is_bool($w)) {
    if (!is_bool($g)) return "na";
    return $w === $g ? "exact" : "inexact";
  }
  if (is_bool($g)) return "na";
  if ($g === "NONINT") return "inexact";
  return bi_cmp($g, $w) == 0 ? "exact" : "inexact";
}

function tname($r) {
  if (is_object($r)) return get_class($r);
  return gettype($r);
}

function sigv($fn, $c, $op, $a, $b) {
  try {
    $r = $fn($c);
  } catch (\Throwable $e) {
    return "raise|" . get_class($e) . "|na";
  }
  return "answer|" . tname($r) . "|" . fidv($r, $op, $a, $b);
}

function bisect($tid, $fn, $op, $lov, $hiv, $fixed, $vary_is_lhs) {
  $s = function ($c) use ($fn, $op, $fixed, $vary_is_lhs) {
    $a = $vary_is_lhs ? $c : $fixed;
    $b = $vary_is_lhs ? $fixed : $c;
    return sigv($fn, $c, $op, $a, $b);
  };
  $lo = bi_norm($lov); $hi = bi_norm($hiv);
  $slo = $s($lo); $shi = $s($hi);
  $probes = 2;
  if ($slo === $shi) { echo "N|$tid|$slo|$shi\n"; return $probes; }
  $other = [];
  while (bi_cmp(bi_sub($hi, $lo), "1") > 0) {
    $mid = bi_half(bi_add($lo, $hi));
    $sm = $s($mid); $probes++;
    if ($sm === $slo) { $lo = $mid; }
    else { if ($sm !== $shi) $other[$sm] = true; $hi = $mid; }
  }
  $o = array_keys($other); sort($o);
  echo "B|$tid|" . $lo . "|" . $hi .
       "|$slo|$shi|$probes|" . implode(";", $o) . "\n";
  return $probes;
}


$TARGETS = [
  function () { $f = 42; return bisect(6066, function ($c) { $f = 42; return ((intval($c)) + ($f)); }, "+", "9007199254740993", "9223372036854775807", "42", true); },
  function () { $f = 42; return bisect(6067, function ($c) { $f = 42; return ((intval($c)) * ($f)); }, "*", "9007199254740993", "9223372036854775807", "42", true); },
  function () { $f = 42; return bisect(6068, function ($c) { $f = 42; return ((intval($c)) / ($f)); }, "/", "42", "9007199254740993", "42", true); },
  function () { $f = 9223372036854775807; return bisect(6070, function ($c) { $f = 9223372036854775807; return ((intval($c)) + ($f)); }, "+", "0", "42", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6071, function ($c) { $f = 9223372036854775807; return ((intval($c)) * ($f)); }, "*", "0", "42", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6072, function ($c) { $f = 9223372036854775807; return ((intval($c)) / ($f)); }, "/", "0", "42", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6073, function ($c) { $f = 9223372036854775807; return ((intval($c)) / ($f)); }, "/", "9007199254740993", "9223372036854775807", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6074, function ($c) { $f = 9223372036854775807; return ((intval($c)) <= ($f)); }, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6075, function ($c) { $f = 9223372036854775807; return ((intval($c)) > ($f)); }, ">", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6076, function ($c) { $f = 9223372036854775807; return ((intval($c)) == ($f)); }, "==", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6077, function ($c) { $f = 9223372036854775807; return ((intval($c)) != ($f)); }, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); },
  function () { $f = 9223372036854775808; return bisect(6079, function ($c) { $f = 9223372036854775808; return ((intval($c)) - ($f)); }, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); },
  function () { $f = 9223372036854775808; return bisect(6080, function ($c) { $f = 9223372036854775808; return ((intval($c)) * ($f)); }, "*", "0", "42", "9223372036854775808", true); },
  function () { $f = 9223372036854775808; return bisect(6081, function ($c) { $f = 9223372036854775808; return ((intval($c)) < ($f)); }, "<", "9007199254740993", "9223372036854775807", "9223372036854775808", true); },
  function () { $f = 9223372036854775808; return bisect(6082, function ($c) { $f = 9223372036854775808; return ((intval($c)) >= ($f)); }, ">=", "9007199254740993", "9223372036854775807", "9223372036854775808", true); },
  function () { $f = 9223372036854775808; return bisect(6083, function ($c) { $f = 9223372036854775808; return ((intval($c)) == ($f)); }, "==", "9007199254740993", "9223372036854775807", "9223372036854775808", true); },
  function () { $f = 9223372036854775808; return bisect(6084, function ($c) { $f = 9223372036854775808; return ((intval($c)) != ($f)); }, "!=", "9007199254740993", "9223372036854775807", "9223372036854775808", true); },
  function () { $f = 9007199254740993; return bisect(6085, function ($c) { $f = 9007199254740993; return ((intval($c)) + ($f)); }, "+", "9007199254740993", "9223372036854775807", "9007199254740993", true); },
  function () { $f = 9007199254740993; return bisect(6086, function ($c) { $f = 9007199254740993; return ((intval($c)) * ($f)); }, "*", "42", "9007199254740993", "9007199254740993", true); },
  function () { $f = 9007199254740993; return bisect(6087, function ($c) { $f = 9007199254740993; return ((intval($c)) / ($f)); }, "/", "0", "42", "9007199254740993", true); },
  function () { $f = 9007199254740993; return bisect(6088, function ($c) { $f = 9007199254740993; return ((intval($c)) / ($f)); }, "/", "42", "9007199254740993", "9007199254740993", true); },
  function () { $f = 9007199254740993; return bisect(6089, function ($c) { $f = 9007199254740993; return ((intval($c)) / ($f)); }, "/", "9007199254740993", "9223372036854775807", "9007199254740993", true); },
  function () { $f = 18446744073709551615; return bisect(6091, function ($c) { $f = 18446744073709551615; return ((intval($c)) - ($f)); }, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); },
  function () { $f = 18446744073709551615; return bisect(6092, function ($c) { $f = 18446744073709551615; return ((intval($c)) * ($f)); }, "*", "0", "42", "18446744073709551615", true); },
  function () { $f = "42"; return bisect(6093, function ($c) { $f = "42"; return ((intval($c)) + ($f)); }, "+", "9007199254740993", "9223372036854775807", "42", true); },
  function () { $f = "42"; return bisect(6094, function ($c) { $f = "42"; return ((intval($c)) * ($f)); }, "*", "9007199254740993", "9223372036854775807", "42", true); },
  function () { $f = "42"; return bisect(6095, function ($c) { $f = "42"; return ((intval($c)) / ($f)); }, "/", "42", "9007199254740993", "42", true); },
  function () { $f = "9223372036854775807"; return bisect(6097, function ($c) { $f = "9223372036854775807"; return ((intval($c)) + ($f)); }, "+", "0", "42", "9223372036854775807", true); },
  function () { $f = "9223372036854775807"; return bisect(6098, function ($c) { $f = "9223372036854775807"; return ((intval($c)) * ($f)); }, "*", "0", "42", "9223372036854775807", true); },
  function () { $f = "9223372036854775807"; return bisect(6099, function ($c) { $f = "9223372036854775807"; return ((intval($c)) / ($f)); }, "/", "0", "42", "9223372036854775807", true); },
  function () { $f = "9223372036854775807"; return bisect(6100, function ($c) { $f = "9223372036854775807"; return ((intval($c)) / ($f)); }, "/", "9007199254740993", "9223372036854775807", "9223372036854775807", true); },
  function () { $f = "9223372036854775807"; return bisect(6101, function ($c) { $f = "9223372036854775807"; return ((intval($c)) <= ($f)); }, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); },
  function () { $f = "9223372036854775807"; return bisect(6102, function ($c) { $f = "9223372036854775807"; return ((intval($c)) > ($f)); }, ">", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); },
  function () { $f = "9223372036854775807"; return bisect(6103, function ($c) { $f = "9223372036854775807"; return ((intval($c)) == ($f)); }, "==", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); },
  function () { $f = "9223372036854775807"; return bisect(6104, function ($c) { $f = "9223372036854775807"; return ((intval($c)) != ($f)); }, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); },
  function () { $f = "9223372036854775808"; return bisect(6106, function ($c) { $f = "9223372036854775808"; return ((intval($c)) - ($f)); }, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); },
  function () { $f = "9223372036854775808"; return bisect(6107, function ($c) { $f = "9223372036854775808"; return ((intval($c)) * ($f)); }, "*", "0", "42", "9223372036854775808", true); },
  function () { $f = "9223372036854775808"; return bisect(6108, function ($c) { $f = "9223372036854775808"; return ((intval($c)) < ($f)); }, "<", "9007199254740993", "9223372036854775807", "9223372036854775808", true); },
  function () { $f = "9223372036854775808"; return bisect(6109, function ($c) { $f = "9223372036854775808"; return ((intval($c)) >= ($f)); }, ">=", "9007199254740993", "9223372036854775807", "9223372036854775808", true); },
  function () { $f = "9223372036854775808"; return bisect(6110, function ($c) { $f = "9223372036854775808"; return ((intval($c)) == ($f)); }, "==", "9007199254740993", "9223372036854775807", "9223372036854775808", true); },
  function () { $f = "9223372036854775808"; return bisect(6111, function ($c) { $f = "9223372036854775808"; return ((intval($c)) != ($f)); }, "!=", "9007199254740993", "9223372036854775807", "9223372036854775808", true); },
  function () { $f = "9007199254740993"; return bisect(6112, function ($c) { $f = "9007199254740993"; return ((intval($c)) + ($f)); }, "+", "9007199254740993", "9223372036854775807", "9007199254740993", true); },
  function () { $f = "9007199254740993"; return bisect(6113, function ($c) { $f = "9007199254740993"; return ((intval($c)) * ($f)); }, "*", "42", "9007199254740993", "9007199254740993", true); },
  function () { $f = "9007199254740993"; return bisect(6114, function ($c) { $f = "9007199254740993"; return ((intval($c)) / ($f)); }, "/", "0", "42", "9007199254740993", true); },
  function () { $f = "9007199254740993"; return bisect(6115, function ($c) { $f = "9007199254740993"; return ((intval($c)) / ($f)); }, "/", "42", "9007199254740993", "9007199254740993", true); },
  function () { $f = "9007199254740993"; return bisect(6116, function ($c) { $f = "9007199254740993"; return ((intval($c)) / ($f)); }, "/", "9007199254740993", "9223372036854775807", "9007199254740993", true); },
  function () { $f = "18446744073709551615"; return bisect(6118, function ($c) { $f = "18446744073709551615"; return ((intval($c)) - ($f)); }, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); },
  function () { $f = "18446744073709551615"; return bisect(6119, function ($c) { $f = "18446744073709551615"; return ((intval($c)) * ($f)); }, "*", "0", "42", "18446744073709551615", true); },
  function () { $f = 42; return bisect(6130, function ($c) { $f = 42; return ((($c)) + ($f)); }, "+", "9007199254740993", "9223372036854775807", "42", true); },
  function () { $f = 42; return bisect(6131, function ($c) { $f = 42; return ((($c)) * ($f)); }, "*", "9007199254740993", "9223372036854775807", "42", true); },
  function () { $f = 42; return bisect(6132, function ($c) { $f = 42; return ((($c)) / ($f)); }, "/", "42", "9007199254740993", "42", true); },
  function () { $f = 9223372036854775807; return bisect(6134, function ($c) { $f = 9223372036854775807; return ((($c)) + ($f)); }, "+", "0", "42", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6135, function ($c) { $f = 9223372036854775807; return ((($c)) * ($f)); }, "*", "0", "42", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6136, function ($c) { $f = 9223372036854775807; return ((($c)) / ($f)); }, "/", "0", "42", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6137, function ($c) { $f = 9223372036854775807; return ((($c)) / ($f)); }, "/", "9007199254740993", "9223372036854775807", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6138, function ($c) { $f = 9223372036854775807; return ((($c)) <= ($f)); }, "<=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6139, function ($c) { $f = 9223372036854775807; return ((($c)) > ($f)); }, ">", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6140, function ($c) { $f = 9223372036854775807; return ((($c)) == ($f)); }, "==", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); },
  function () { $f = 9223372036854775807; return bisect(6141, function ($c) { $f = 9223372036854775807; return ((($c)) != ($f)); }, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775807", true); },
  function () { $f = 9223372036854775808; return bisect(6143, function ($c) { $f = 9223372036854775808; return ((($c)) - ($f)); }, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); },
  function () { $f = 9223372036854775808; return bisect(6144, function ($c) { $f = 9223372036854775808; return ((($c)) * ($f)); }, "*", "0", "42", "9223372036854775808", true); },
  function () { $f = 9223372036854775808; return bisect(6145, function ($c) { $f = 9223372036854775808; return ((($c)) < ($f)); }, "<", "9007199254740993", "9223372036854775807", "9223372036854775808", true); },
  function () { $f = 9223372036854775808; return bisect(6146, function ($c) { $f = 9223372036854775808; return ((($c)) >= ($f)); }, ">=", "9007199254740993", "9223372036854775807", "9223372036854775808", true); },
  function () { $f = 9223372036854775808; return bisect(6147, function ($c) { $f = 9223372036854775808; return ((($c)) == ($f)); }, "==", "9007199254740993", "9223372036854775807", "9223372036854775808", true); },
  function () { $f = 9223372036854775808; return bisect(6148, function ($c) { $f = 9223372036854775808; return ((($c)) != ($f)); }, "!=", "9007199254740993", "9223372036854775807", "9223372036854775808", true); },
  function () { $f = 9007199254740993; return bisect(6149, function ($c) { $f = 9007199254740993; return ((($c)) + ($f)); }, "+", "9007199254740993", "9223372036854775807", "9007199254740993", true); },
  function () { $f = 9007199254740993; return bisect(6150, function ($c) { $f = 9007199254740993; return ((($c)) * ($f)); }, "*", "42", "9007199254740993", "9007199254740993", true); },
  function () { $f = 9007199254740993; return bisect(6151, function ($c) { $f = 9007199254740993; return ((($c)) / ($f)); }, "/", "0", "42", "9007199254740993", true); },
  function () { $f = 9007199254740993; return bisect(6152, function ($c) { $f = 9007199254740993; return ((($c)) / ($f)); }, "/", "42", "9007199254740993", "9007199254740993", true); },
  function () { $f = 9007199254740993; return bisect(6153, function ($c) { $f = 9007199254740993; return ((($c)) / ($f)); }, "/", "9007199254740993", "9223372036854775807", "9007199254740993", true); },
  function () { $f = 18446744073709551615; return bisect(6155, function ($c) { $f = 18446744073709551615; return ((($c)) - ($f)); }, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); },
  function () { $f = 18446744073709551615; return bisect(6156, function ($c) { $f = 18446744073709551615; return ((($c)) * ($f)); }, "*", "0", "42", "18446744073709551615", true); },
  function () { $f = "42"; return bisect(6157, function ($c) { $f = "42"; return ((($c)) + ($f)); }, "+", "9007199254740993", "9223372036854775807", "42", true); },
  function () { $f = "42"; return bisect(6158, function ($c) { $f = "42"; return ((($c)) * ($f)); }, "*", "9007199254740993", "9223372036854775807", "42", true); },
  function () { $f = "42"; return bisect(6159, function ($c) { $f = "42"; return ((($c)) / ($f)); }, "/", "42", "9007199254740993", "42", true); },
  function () { $f = "9223372036854775807"; return bisect(6161, function ($c) { $f = "9223372036854775807"; return ((($c)) + ($f)); }, "+", "0", "42", "9223372036854775807", true); },
  function () { $f = "9223372036854775807"; return bisect(6162, function ($c) { $f = "9223372036854775807"; return ((($c)) * ($f)); }, "*", "0", "42", "9223372036854775807", true); },
  function () { $f = "9223372036854775807"; return bisect(6163, function ($c) { $f = "9223372036854775807"; return ((($c)) / ($f)); }, "/", "0", "42", "9223372036854775807", true); },
  function () { $f = "9223372036854775807"; return bisect(6164, function ($c) { $f = "9223372036854775807"; return ((($c)) / ($f)); }, "/", "9007199254740993", "9223372036854775807", "9223372036854775807", true); },
  function () { $f = "9223372036854775808"; return bisect(6166, function ($c) { $f = "9223372036854775808"; return ((($c)) - ($f)); }, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", true); },
  function () { $f = "9223372036854775808"; return bisect(6167, function ($c) { $f = "9223372036854775808"; return ((($c)) * ($f)); }, "*", "0", "42", "9223372036854775808", true); },
  function () { $f = "9007199254740993"; return bisect(6168, function ($c) { $f = "9007199254740993"; return ((($c)) + ($f)); }, "+", "9007199254740993", "9223372036854775807", "9007199254740993", true); },
  function () { $f = "9007199254740993"; return bisect(6169, function ($c) { $f = "9007199254740993"; return ((($c)) * ($f)); }, "*", "42", "9007199254740993", "9007199254740993", true); },
  function () { $f = "9007199254740993"; return bisect(6170, function ($c) { $f = "9007199254740993"; return ((($c)) / ($f)); }, "/", "0", "42", "9007199254740993", true); },
  function () { $f = "9007199254740993"; return bisect(6171, function ($c) { $f = "9007199254740993"; return ((($c)) / ($f)); }, "/", "42", "9007199254740993", "9007199254740993", true); },
  function () { $f = "9007199254740993"; return bisect(6172, function ($c) { $f = "9007199254740993"; return ((($c)) / ($f)); }, "/", "9007199254740993", "9223372036854775807", "9007199254740993", true); },
  function () { $f = "18446744073709551615"; return bisect(6174, function ($c) { $f = "18446744073709551615"; return ((($c)) - ($f)); }, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", true); },
  function () { $f = "18446744073709551615"; return bisect(6175, function ($c) { $f = "18446744073709551615"; return ((($c)) * ($f)); }, "*", "0", "42", "18446744073709551615", true); },
  function () { $f = 42; return bisect(6208, function ($c) { $f = 42; return (($f) + (intval($c))); }, "+", "9007199254740993", "9223372036854775807", "42", false); },
  function () { $f = 42; return bisect(6209, function ($c) { $f = 42; return (($f) * (intval($c))); }, "*", "9007199254740993", "9223372036854775807", "42", false); },
  function () { $f = 42; return bisect(6210, function ($c) { $f = 42; return (($f) / (intval($c))); }, "/", "0", "42", "42", false); },
  function () { $f = 42; return bisect(6211, function ($c) { $f = 42; return (($f) / (intval($c))); }, "/", "42", "9007199254740993", "42", false); },
  function () { $f = 42; return bisect(6212, function ($c) { $f = 42; return (($f) % (intval($c))); }, "%", "0", "42", "42", false); },
  function () { $f = 42; return bisect(6213, function ($c) { $f = 42; return (($f) % (intval($c))); }, "%", "9223372036854775808", "18446744073709551615", "42", false); },
  function () { $f = 42; return bisect(6214, function ($c) { $f = 42; return (($f) << (intval($c))); }, "<<", "9223372036854775808", "18446744073709551615", "42", false); },
  function () { $f = 42; return bisect(6215, function ($c) { $f = 42; return (($f) >> (intval($c))); }, ">>", "9223372036854775808", "18446744073709551615", "42", false); },
  function () { $f = 0; return bisect(6217, function ($c) { $f = 0; return (($f) / (intval($c))); }, "/", "0", "42", "0", false); },
  function () { $f = 0; return bisect(6218, function ($c) { $f = 0; return (($f) % (intval($c))); }, "%", "0", "42", "0", false); },
  function () { $f = 0; return bisect(6219, function ($c) { $f = 0; return (($f) % (intval($c))); }, "%", "9223372036854775808", "18446744073709551615", "0", false); },
  function () { $f = 0; return bisect(6220, function ($c) { $f = 0; return (($f) << (intval($c))); }, "<<", "9223372036854775808", "18446744073709551615", "0", false); },
  function () { $f = 0; return bisect(6221, function ($c) { $f = 0; return (($f) >> (intval($c))); }, ">>", "9223372036854775808", "18446744073709551615", "0", false); },
  function () { $f = 9223372036854775807; return bisect(6222, function ($c) { $f = 9223372036854775807; return (($f) + (intval($c))); }, "+", "0", "42", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6223, function ($c) { $f = 9223372036854775807; return (($f) * (intval($c))); }, "*", "0", "42", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6224, function ($c) { $f = 9223372036854775807; return (($f) / (intval($c))); }, "/", "0", "42", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6225, function ($c) { $f = 9223372036854775807; return (($f) / (intval($c))); }, "/", "9007199254740993", "9223372036854775807", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6226, function ($c) { $f = 9223372036854775807; return (($f) % (intval($c))); }, "%", "0", "42", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6227, function ($c) { $f = 9223372036854775807; return (($f) % (intval($c))); }, "%", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6228, function ($c) { $f = 9223372036854775807; return (($f) < (intval($c))); }, "<", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6229, function ($c) { $f = 9223372036854775807; return (($f) >= (intval($c))); }, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6230, function ($c) { $f = 9223372036854775807; return (($f) == (intval($c))); }, "==", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6231, function ($c) { $f = 9223372036854775807; return (($f) != (intval($c))); }, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6232, function ($c) { $f = 9223372036854775807; return (($f) << (intval($c))); }, "<<", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6233, function ($c) { $f = 9223372036854775807; return (($f) >> (intval($c))); }, ">>", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = 9223372036854775808; return bisect(6235, function ($c) { $f = 9223372036854775808; return (($f) - (intval($c))); }, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6236, function ($c) { $f = 9223372036854775808; return (($f) * (intval($c))); }, "*", "0", "42", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6237, function ($c) { $f = 9223372036854775808; return (($f) / (intval($c))); }, "/", "0", "42", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6238, function ($c) { $f = 9223372036854775808; return (($f) % (intval($c))); }, "%", "0", "42", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6239, function ($c) { $f = 9223372036854775808; return (($f) % (intval($c))); }, "%", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6240, function ($c) { $f = 9223372036854775808; return (($f) <= (intval($c))); }, "<=", "9007199254740993", "9223372036854775807", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6241, function ($c) { $f = 9223372036854775808; return (($f) > (intval($c))); }, ">", "9007199254740993", "9223372036854775807", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6242, function ($c) { $f = 9223372036854775808; return (($f) == (intval($c))); }, "==", "9007199254740993", "9223372036854775807", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6243, function ($c) { $f = 9223372036854775808; return (($f) != (intval($c))); }, "!=", "9007199254740993", "9223372036854775807", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6244, function ($c) { $f = 9223372036854775808; return (($f) << (intval($c))); }, "<<", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6245, function ($c) { $f = 9223372036854775808; return (($f) >> (intval($c))); }, ">>", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); },
  function () { $f = 9007199254740993; return bisect(6246, function ($c) { $f = 9007199254740993; return (($f) + (intval($c))); }, "+", "9007199254740993", "9223372036854775807", "9007199254740993", false); },
  function () { $f = 9007199254740993; return bisect(6247, function ($c) { $f = 9007199254740993; return (($f) * (intval($c))); }, "*", "42", "9007199254740993", "9007199254740993", false); },
  function () { $f = 9007199254740993; return bisect(6248, function ($c) { $f = 9007199254740993; return (($f) / (intval($c))); }, "/", "0", "42", "9007199254740993", false); },
  function () { $f = 9007199254740993; return bisect(6249, function ($c) { $f = 9007199254740993; return (($f) / (intval($c))); }, "/", "42", "9007199254740993", "9007199254740993", false); },
  function () { $f = 9007199254740993; return bisect(6250, function ($c) { $f = 9007199254740993; return (($f) / (intval($c))); }, "/", "9007199254740993", "9223372036854775807", "9007199254740993", false); },
  function () { $f = 9007199254740993; return bisect(6251, function ($c) { $f = 9007199254740993; return (($f) % (intval($c))); }, "%", "0", "42", "9007199254740993", false); },
  function () { $f = 9007199254740993; return bisect(6252, function ($c) { $f = 9007199254740993; return (($f) % (intval($c))); }, "%", "9223372036854775808", "18446744073709551615", "9007199254740993", false); },
  function () { $f = 9007199254740993; return bisect(6253, function ($c) { $f = 9007199254740993; return (($f) << (intval($c))); }, "<<", "9223372036854775808", "18446744073709551615", "9007199254740993", false); },
  function () { $f = 9007199254740993; return bisect(6254, function ($c) { $f = 9007199254740993; return (($f) >> (intval($c))); }, ">>", "9223372036854775808", "18446744073709551615", "9007199254740993", false); },
  function () { $f = 18446744073709551615; return bisect(6256, function ($c) { $f = 18446744073709551615; return (($f) - (intval($c))); }, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); },
  function () { $f = 18446744073709551615; return bisect(6257, function ($c) { $f = 18446744073709551615; return (($f) * (intval($c))); }, "*", "0", "42", "18446744073709551615", false); },
  function () { $f = 18446744073709551615; return bisect(6258, function ($c) { $f = 18446744073709551615; return (($f) / (intval($c))); }, "/", "0", "42", "18446744073709551615", false); },
  function () { $f = 18446744073709551615; return bisect(6259, function ($c) { $f = 18446744073709551615; return (($f) % (intval($c))); }, "%", "0", "42", "18446744073709551615", false); },
  function () { $f = 18446744073709551615; return bisect(6260, function ($c) { $f = 18446744073709551615; return (($f) % (intval($c))); }, "%", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); },
  function () { $f = 18446744073709551615; return bisect(6261, function ($c) { $f = 18446744073709551615; return (($f) << (intval($c))); }, "<<", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); },
  function () { $f = 18446744073709551615; return bisect(6262, function ($c) { $f = 18446744073709551615; return (($f) >> (intval($c))); }, ">>", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); },
  function () { $f = 42; return bisect(6263, function ($c) { $f = 42; return (($f) + (($c))); }, "+", "9007199254740993", "9223372036854775807", "42", false); },
  function () { $f = 42; return bisect(6264, function ($c) { $f = 42; return (($f) * (($c))); }, "*", "9007199254740993", "9223372036854775807", "42", false); },
  function () { $f = 42; return bisect(6265, function ($c) { $f = 42; return (($f) / (($c))); }, "/", "0", "42", "42", false); },
  function () { $f = 42; return bisect(6266, function ($c) { $f = 42; return (($f) / (($c))); }, "/", "42", "9007199254740993", "42", false); },
  function () { $f = 42; return bisect(6267, function ($c) { $f = 42; return (($f) % (($c))); }, "%", "0", "42", "42", false); },
  function () { $f = 0; return bisect(6269, function ($c) { $f = 0; return (($f) / (($c))); }, "/", "0", "42", "0", false); },
  function () { $f = 0; return bisect(6270, function ($c) { $f = 0; return (($f) % (($c))); }, "%", "0", "42", "0", false); },
  function () { $f = 9223372036854775807; return bisect(6271, function ($c) { $f = 9223372036854775807; return (($f) + (($c))); }, "+", "0", "42", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6272, function ($c) { $f = 9223372036854775807; return (($f) * (($c))); }, "*", "0", "42", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6273, function ($c) { $f = 9223372036854775807; return (($f) / (($c))); }, "/", "0", "42", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6274, function ($c) { $f = 9223372036854775807; return (($f) / (($c))); }, "/", "9007199254740993", "9223372036854775807", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6275, function ($c) { $f = 9223372036854775807; return (($f) % (($c))); }, "%", "0", "42", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6276, function ($c) { $f = 9223372036854775807; return (($f) < (($c))); }, "<", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6277, function ($c) { $f = 9223372036854775807; return (($f) >= (($c))); }, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6278, function ($c) { $f = 9223372036854775807; return (($f) == (($c))); }, "==", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = 9223372036854775807; return bisect(6279, function ($c) { $f = 9223372036854775807; return (($f) != (($c))); }, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = 9223372036854775808; return bisect(6281, function ($c) { $f = 9223372036854775808; return (($f) - (($c))); }, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6282, function ($c) { $f = 9223372036854775808; return (($f) * (($c))); }, "*", "0", "42", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6283, function ($c) { $f = 9223372036854775808; return (($f) / (($c))); }, "/", "0", "42", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6284, function ($c) { $f = 9223372036854775808; return (($f) % (($c))); }, "%", "0", "42", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6285, function ($c) { $f = 9223372036854775808; return (($f) <= (($c))); }, "<=", "9007199254740993", "9223372036854775807", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6286, function ($c) { $f = 9223372036854775808; return (($f) > (($c))); }, ">", "9007199254740993", "9223372036854775807", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6287, function ($c) { $f = 9223372036854775808; return (($f) == (($c))); }, "==", "9007199254740993", "9223372036854775807", "9223372036854775808", false); },
  function () { $f = 9223372036854775808; return bisect(6288, function ($c) { $f = 9223372036854775808; return (($f) != (($c))); }, "!=", "9007199254740993", "9223372036854775807", "9223372036854775808", false); },
  function () { $f = 9007199254740993; return bisect(6289, function ($c) { $f = 9007199254740993; return (($f) + (($c))); }, "+", "9007199254740993", "9223372036854775807", "9007199254740993", false); },
  function () { $f = 9007199254740993; return bisect(6290, function ($c) { $f = 9007199254740993; return (($f) * (($c))); }, "*", "42", "9007199254740993", "9007199254740993", false); },
  function () { $f = 9007199254740993; return bisect(6291, function ($c) { $f = 9007199254740993; return (($f) / (($c))); }, "/", "0", "42", "9007199254740993", false); },
  function () { $f = 9007199254740993; return bisect(6292, function ($c) { $f = 9007199254740993; return (($f) / (($c))); }, "/", "42", "9007199254740993", "9007199254740993", false); },
  function () { $f = 9007199254740993; return bisect(6293, function ($c) { $f = 9007199254740993; return (($f) / (($c))); }, "/", "9007199254740993", "9223372036854775807", "9007199254740993", false); },
  function () { $f = 9007199254740993; return bisect(6294, function ($c) { $f = 9007199254740993; return (($f) % (($c))); }, "%", "0", "42", "9007199254740993", false); },
  function () { $f = 18446744073709551615; return bisect(6296, function ($c) { $f = 18446744073709551615; return (($f) - (($c))); }, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); },
  function () { $f = 18446744073709551615; return bisect(6297, function ($c) { $f = 18446744073709551615; return (($f) * (($c))); }, "*", "0", "42", "18446744073709551615", false); },
  function () { $f = 18446744073709551615; return bisect(6298, function ($c) { $f = 18446744073709551615; return (($f) / (($c))); }, "/", "0", "42", "18446744073709551615", false); },
  function () { $f = 18446744073709551615; return bisect(6299, function ($c) { $f = 18446744073709551615; return (($f) % (($c))); }, "%", "0", "42", "18446744073709551615", false); },
  function () { $f = "42"; return bisect(6300, function ($c) { $f = "42"; return (($f) + (intval($c))); }, "+", "9007199254740993", "9223372036854775807", "42", false); },
  function () { $f = "42"; return bisect(6301, function ($c) { $f = "42"; return (($f) * (intval($c))); }, "*", "9007199254740993", "9223372036854775807", "42", false); },
  function () { $f = "42"; return bisect(6302, function ($c) { $f = "42"; return (($f) / (intval($c))); }, "/", "0", "42", "42", false); },
  function () { $f = "42"; return bisect(6303, function ($c) { $f = "42"; return (($f) / (intval($c))); }, "/", "42", "9007199254740993", "42", false); },
  function () { $f = "42"; return bisect(6304, function ($c) { $f = "42"; return (($f) % (intval($c))); }, "%", "0", "42", "42", false); },
  function () { $f = "42"; return bisect(6305, function ($c) { $f = "42"; return (($f) % (intval($c))); }, "%", "9223372036854775808", "18446744073709551615", "42", false); },
  function () { $f = "0"; return bisect(6309, function ($c) { $f = "0"; return (($f) / (intval($c))); }, "/", "0", "42", "0", false); },
  function () { $f = "0"; return bisect(6310, function ($c) { $f = "0"; return (($f) % (intval($c))); }, "%", "0", "42", "0", false); },
  function () { $f = "0"; return bisect(6311, function ($c) { $f = "0"; return (($f) % (intval($c))); }, "%", "9223372036854775808", "18446744073709551615", "0", false); },
  function () { $f = "9223372036854775807"; return bisect(6314, function ($c) { $f = "9223372036854775807"; return (($f) + (intval($c))); }, "+", "0", "42", "9223372036854775807", false); },
  function () { $f = "9223372036854775807"; return bisect(6315, function ($c) { $f = "9223372036854775807"; return (($f) * (intval($c))); }, "*", "0", "42", "9223372036854775807", false); },
  function () { $f = "9223372036854775807"; return bisect(6316, function ($c) { $f = "9223372036854775807"; return (($f) / (intval($c))); }, "/", "0", "42", "9223372036854775807", false); },
  function () { $f = "9223372036854775807"; return bisect(6317, function ($c) { $f = "9223372036854775807"; return (($f) / (intval($c))); }, "/", "9007199254740993", "9223372036854775807", "9223372036854775807", false); },
  function () { $f = "9223372036854775807"; return bisect(6318, function ($c) { $f = "9223372036854775807"; return (($f) % (intval($c))); }, "%", "0", "42", "9223372036854775807", false); },
  function () { $f = "9223372036854775807"; return bisect(6319, function ($c) { $f = "9223372036854775807"; return (($f) % (intval($c))); }, "%", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = "9223372036854775807"; return bisect(6320, function ($c) { $f = "9223372036854775807"; return (($f) < (intval($c))); }, "<", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = "9223372036854775807"; return bisect(6321, function ($c) { $f = "9223372036854775807"; return (($f) >= (intval($c))); }, ">=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = "9223372036854775807"; return bisect(6322, function ($c) { $f = "9223372036854775807"; return (($f) == (intval($c))); }, "==", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = "9223372036854775807"; return bisect(6323, function ($c) { $f = "9223372036854775807"; return (($f) != (intval($c))); }, "!=", "9223372036854775808", "18446744073709551615", "9223372036854775807", false); },
  function () { $f = "9223372036854775808"; return bisect(6327, function ($c) { $f = "9223372036854775808"; return (($f) - (intval($c))); }, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); },
  function () { $f = "9223372036854775808"; return bisect(6328, function ($c) { $f = "9223372036854775808"; return (($f) * (intval($c))); }, "*", "0", "42", "9223372036854775808", false); },
  function () { $f = "9223372036854775808"; return bisect(6329, function ($c) { $f = "9223372036854775808"; return (($f) / (intval($c))); }, "/", "0", "42", "9223372036854775808", false); },
  function () { $f = "9223372036854775808"; return bisect(6330, function ($c) { $f = "9223372036854775808"; return (($f) % (intval($c))); }, "%", "0", "42", "9223372036854775808", false); },
  function () { $f = "9223372036854775808"; return bisect(6331, function ($c) { $f = "9223372036854775808"; return (($f) % (intval($c))); }, "%", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); },
  function () { $f = "9223372036854775808"; return bisect(6332, function ($c) { $f = "9223372036854775808"; return (($f) <= (intval($c))); }, "<=", "9007199254740993", "9223372036854775807", "9223372036854775808", false); },
  function () { $f = "9223372036854775808"; return bisect(6333, function ($c) { $f = "9223372036854775808"; return (($f) > (intval($c))); }, ">", "9007199254740993", "9223372036854775807", "9223372036854775808", false); },
  function () { $f = "9223372036854775808"; return bisect(6334, function ($c) { $f = "9223372036854775808"; return (($f) == (intval($c))); }, "==", "9007199254740993", "9223372036854775807", "9223372036854775808", false); },
  function () { $f = "9223372036854775808"; return bisect(6335, function ($c) { $f = "9223372036854775808"; return (($f) != (intval($c))); }, "!=", "9007199254740993", "9223372036854775807", "9223372036854775808", false); },
  function () { $f = "9007199254740993"; return bisect(6338, function ($c) { $f = "9007199254740993"; return (($f) + (intval($c))); }, "+", "9007199254740993", "9223372036854775807", "9007199254740993", false); },
  function () { $f = "9007199254740993"; return bisect(6339, function ($c) { $f = "9007199254740993"; return (($f) * (intval($c))); }, "*", "42", "9007199254740993", "9007199254740993", false); },
  function () { $f = "9007199254740993"; return bisect(6340, function ($c) { $f = "9007199254740993"; return (($f) / (intval($c))); }, "/", "0", "42", "9007199254740993", false); },
  function () { $f = "9007199254740993"; return bisect(6341, function ($c) { $f = "9007199254740993"; return (($f) / (intval($c))); }, "/", "42", "9007199254740993", "9007199254740993", false); },
  function () { $f = "9007199254740993"; return bisect(6342, function ($c) { $f = "9007199254740993"; return (($f) / (intval($c))); }, "/", "9007199254740993", "9223372036854775807", "9007199254740993", false); },
  function () { $f = "9007199254740993"; return bisect(6343, function ($c) { $f = "9007199254740993"; return (($f) % (intval($c))); }, "%", "0", "42", "9007199254740993", false); },
  function () { $f = "9007199254740993"; return bisect(6344, function ($c) { $f = "9007199254740993"; return (($f) % (intval($c))); }, "%", "9223372036854775808", "18446744073709551615", "9007199254740993", false); },
  function () { $f = "18446744073709551615"; return bisect(6348, function ($c) { $f = "18446744073709551615"; return (($f) - (intval($c))); }, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); },
  function () { $f = "18446744073709551615"; return bisect(6349, function ($c) { $f = "18446744073709551615"; return (($f) * (intval($c))); }, "*", "0", "42", "18446744073709551615", false); },
  function () { $f = "18446744073709551615"; return bisect(6350, function ($c) { $f = "18446744073709551615"; return (($f) / (intval($c))); }, "/", "0", "42", "18446744073709551615", false); },
  function () { $f = "18446744073709551615"; return bisect(6351, function ($c) { $f = "18446744073709551615"; return (($f) % (intval($c))); }, "%", "0", "42", "18446744073709551615", false); },
  function () { $f = "18446744073709551615"; return bisect(6352, function ($c) { $f = "18446744073709551615"; return (($f) % (intval($c))); }, "%", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); },
  function () { $f = "42"; return bisect(6355, function ($c) { $f = "42"; return (($f) + (($c))); }, "+", "9007199254740993", "9223372036854775807", "42", false); },
  function () { $f = "42"; return bisect(6356, function ($c) { $f = "42"; return (($f) * (($c))); }, "*", "9007199254740993", "9223372036854775807", "42", false); },
  function () { $f = "42"; return bisect(6357, function ($c) { $f = "42"; return (($f) / (($c))); }, "/", "0", "42", "42", false); },
  function () { $f = "42"; return bisect(6358, function ($c) { $f = "42"; return (($f) / (($c))); }, "/", "42", "9007199254740993", "42", false); },
  function () { $f = "42"; return bisect(6359, function ($c) { $f = "42"; return (($f) % (($c))); }, "%", "0", "42", "42", false); },
  function () { $f = "0"; return bisect(6361, function ($c) { $f = "0"; return (($f) / (($c))); }, "/", "0", "42", "0", false); },
  function () { $f = "0"; return bisect(6362, function ($c) { $f = "0"; return (($f) % (($c))); }, "%", "0", "42", "0", false); },
  function () { $f = "9223372036854775807"; return bisect(6363, function ($c) { $f = "9223372036854775807"; return (($f) + (($c))); }, "+", "0", "42", "9223372036854775807", false); },
  function () { $f = "9223372036854775807"; return bisect(6364, function ($c) { $f = "9223372036854775807"; return (($f) * (($c))); }, "*", "0", "42", "9223372036854775807", false); },
  function () { $f = "9223372036854775807"; return bisect(6365, function ($c) { $f = "9223372036854775807"; return (($f) / (($c))); }, "/", "0", "42", "9223372036854775807", false); },
  function () { $f = "9223372036854775807"; return bisect(6366, function ($c) { $f = "9223372036854775807"; return (($f) / (($c))); }, "/", "9007199254740993", "9223372036854775807", "9223372036854775807", false); },
  function () { $f = "9223372036854775807"; return bisect(6367, function ($c) { $f = "9223372036854775807"; return (($f) % (($c))); }, "%", "0", "42", "9223372036854775807", false); },
  function () { $f = "9223372036854775808"; return bisect(6369, function ($c) { $f = "9223372036854775808"; return (($f) - (($c))); }, "-", "9223372036854775808", "18446744073709551615", "9223372036854775808", false); },
  function () { $f = "9223372036854775808"; return bisect(6370, function ($c) { $f = "9223372036854775808"; return (($f) * (($c))); }, "*", "0", "42", "9223372036854775808", false); },
  function () { $f = "9223372036854775808"; return bisect(6371, function ($c) { $f = "9223372036854775808"; return (($f) / (($c))); }, "/", "0", "42", "9223372036854775808", false); },
  function () { $f = "9223372036854775808"; return bisect(6372, function ($c) { $f = "9223372036854775808"; return (($f) % (($c))); }, "%", "0", "42", "9223372036854775808", false); },
  function () { $f = "9007199254740993"; return bisect(6373, function ($c) { $f = "9007199254740993"; return (($f) + (($c))); }, "+", "9007199254740993", "9223372036854775807", "9007199254740993", false); },
  function () { $f = "9007199254740993"; return bisect(6374, function ($c) { $f = "9007199254740993"; return (($f) * (($c))); }, "*", "42", "9007199254740993", "9007199254740993", false); },
  function () { $f = "9007199254740993"; return bisect(6375, function ($c) { $f = "9007199254740993"; return (($f) / (($c))); }, "/", "0", "42", "9007199254740993", false); },
  function () { $f = "9007199254740993"; return bisect(6376, function ($c) { $f = "9007199254740993"; return (($f) / (($c))); }, "/", "42", "9007199254740993", "9007199254740993", false); },
  function () { $f = "9007199254740993"; return bisect(6377, function ($c) { $f = "9007199254740993"; return (($f) / (($c))); }, "/", "9007199254740993", "9223372036854775807", "9007199254740993", false); },
  function () { $f = "9007199254740993"; return bisect(6378, function ($c) { $f = "9007199254740993"; return (($f) % (($c))); }, "%", "0", "42", "9007199254740993", false); },
  function () { $f = "18446744073709551615"; return bisect(6380, function ($c) { $f = "18446744073709551615"; return (($f) - (($c))); }, "-", "9223372036854775808", "18446744073709551615", "18446744073709551615", false); },
  function () { $f = "18446744073709551615"; return bisect(6381, function ($c) { $f = "18446744073709551615"; return (($f) * (($c))); }, "*", "0", "42", "18446744073709551615", false); },
  function () { $f = "18446744073709551615"; return bisect(6382, function ($c) { $f = "18446744073709551615"; return (($f) / (($c))); }, "/", "0", "42", "18446744073709551615", false); },
  function () { $f = "18446744073709551615"; return bisect(6383, function ($c) { $f = "18446744073709551615"; return (($f) % (($c))); }, "%", "0", "42", "18446744073709551615", false); },
];
$total = 0;
$n = count($TARGETS);
foreach ($TARGETS as $k => $t) {
  $total += $t();
  if (($k + 1) % 25 == 0 || $k + 1 == $n)
    fwrite(STDERR, "progress " . ($k + 1) . "/$n probes=$total\n");
}
fwrite(STDERR, "DONE targets=$n probes=$total\n");
