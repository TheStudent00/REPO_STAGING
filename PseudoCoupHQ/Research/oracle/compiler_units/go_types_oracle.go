// go_types_oracle.go -- task o6, arch_unit_oracle line, compiler_units node.
//
// WHAT THIS IS, in relation: the go standard library's own type checker
// (go/parser + go/types) run once over the go compiler's source tree
// (src/cmd/compile/...) as a TYPE ORACLE for task o4's operator sites --
// o4 resolved operand types by search alone and left 78% of go's sites
// unresolved (log_210); this program records what go's front end says
// the operand types are at every operator node, so go_types_join.py can
// join the two by (file, line, column) and complete o4's variant row.
//
// It is a MEASUREMENT of that route's yield and cost. It is not the
// Hub's front end.
//
// WHAT IT PRINTS. One json object (go_types_sites.json) whose `sites`
// array holds ONE JSON LINE PER SITE: file, line, column, the node kind,
// the operator token AS A LABEL ONLY (`operator` field on a per-unit
// object carrying `lang` + `unit`, the one place the spelling ban
// allows a token), the go/types type string of each operand (on its own
// per-unit label object, `spelling`, exactly as types.TypeString prints
// it with a nil qualifier -- package paths in full, no normalization),
// the type string of the result, the enclosing function's name, the
// package, and the file's bin (how the file was typed). No site is
// grouped, paired or keyed by its operator anywhere in this program;
// grouping into variants happens downstream, in go_types_join.py, by
// the recorded type strings.
//
// WHICH NODES. Every *ast.BinaryExpr, *ast.UnaryExpr (incl. `&`, `<-`),
// *ast.StarExpr used as a VALUE (deref; a StarExpr that is a type
// expression `*T` is skipped), *ast.IncDecStmt, and *ast.AssignStmt
// whose token is an operator-assignment (`+=` ... `&^=`; plain `=` and
// `:=` are not operators here). A BinaryExpr or UnaryExpr that go/types
// records as a TYPE expression is skipped and counted
// (`type_expression_nodes_skipped` per package): go/ast spells a type
// constraint union `int8 | int16` as a BinaryExpr and a tilde term
// `~int` as a UnaryExpr, and neither is an operator applied to values
// (the first join found 134 `|` and 108 `~` such nodes; tree-sitter
// reads them as types, so task o4 never counted them).
//
// POSITIONS are PHYSICAL (token.FileSet.PositionFor with adjusted =
// false): a `//line` directive in a file moves go/token's adjusted
// positions to what the directive says, and the join to task o4's
// tree-sitter positions needs the byte position in the file on disk
// (loopvar/testdata/range_esc_closure_linedir.go carries such a
// directive).
//
// HOW FILES ARE TYPED, by bin (the brief: "measure it, file by file and
// package by package, and report what typed and what did not, by
// cause"):
//
//	package        go/build's GoFiles (+ TestGoFiles, the in-package
//	               tests) of a directory, checked together as ONE
//	               package -- what `go vet` would see.
//	xtest          the directory's XTestGoFiles (package foo_test),
//	               checked as their own package, importing the package
//	               under test through the same importer.
//	alone          a file typed on its own as a one-file package: every
//	               file of a `testdata` directory (not a package the go
//	               command builds; many are single-file programs, some
//	               are deliberately broken), every file go/build lists
//	               as excluded by a build constraint (IgnoredGoFiles),
//	               and every file of a directory go/build reports as
//	               holding more than one package. Such a file types
//	               with errors where it references the rest of its
//	               package; the errors are counted and classified.
//
// GOROOT. The importer is go/importer's "source" importer over
// build.Default with GOROOT pointed at the SOURCE TREE (-goroot), so
// that cmd/compile's own imports (cmd/internal/..., internal/...,
// runtime, ...) are typed from the same 1.28-dev checkout, not from the
// image's go1.26.0 GOROOT. If that does not type, the lane re-runs with
// -goroot at the image's GOROOT (the brief's fallback) and the log says
// which was used and why. Cgo is disabled in the build context so no
// `cgo` tool is ever run; release tags are extended through go1.28 so a
// file constrained `//go:build go1.27`/`go1.28` in this tree is not
// excluded by the go1.26 toolchain's own tag list.
//
// COST. Per package: wall clock of that package's check (which includes
// the first-time import of every dependency it pulled into the shared
// importer cache -- said once here, so a big first package is not read
// as an expensive package) and ru_maxrss AFTER it (the process's
// running peak, so the column is monotone). Total at the end.
//
// MEMORY. Bound 12 GB (ABORT_MEMORY_O6; the first run's bound was 3 GB
// and the no-overlay full pass aborted on it at 6,114.7 MB -- a flag,
// re-run with more room, see the log): after every package check the
// process's ru_maxrss is read; over the bound it prints
// `ABORT_MEMORY_O6: ...` and exits 97 without writing a partial json.
// Sites are never held for the whole run: each package's sites are
// written to a scratch file (-scratch, one json line per site) as that
// package finishes and copied into the output's `sites` array at the
// end, so resident memory is the type checker's, not the record's.
//
// WHY THE NO-OVERLAY PASS COST 6 GB AND 28 MINUTES FOR ONE PACKAGE (read
// off go1.26's src/go/internal/srcimporter/srcimporter.go, ImportFrom):
// the source importer caches a package ONLY when it type-checked
// without a hard error (`p.packages[bp.ImportPath] = pkg` is reached
// only on success; the deferred cleanup resets a failed entry to nil).
// With internal/buildcfg failing (undefined: defaultGOARCH), every
// import edge into any package whose closure reaches buildcfg --
// cmd/compile/internal/base and so nearly all of cmd/compile -- re-parses
// and re-checks that closure again, into the one shared token.FileSet
// that never releases a file. That is the failure mode's price, not the
// route's; the overlay removes the failure and the closure is checked
// once.
//
// SHAPE (-shape). Two ways to run the same checks, both measured:
//
//	tree      one token.FileSet and one source importer shared by every
//	          package check, so each dependency is parsed and checked
//	          once and stays resident until the end -- the peak RSS is
//	          the tree's.
//	package   a fresh token.FileSet and a fresh source importer for EVERY
//	          package check; after the check the package's sites are
//	          flushed to scratch and runtime.GC + debug.FreeOSMemory
//	          run, so the peak RSS is one package's closure, and every
//	          package pays the full first-time import of its own
//	          closure again (wall clock is the price of the memory).
//
// OVERLAY (-overlay). Measured in lane 1: the checked-in tree lacks
// the files make.bash GENERATES (src/internal/buildcfg/zbootstrap.go,
// which defines defaultGOARCH & co.), so with GOROOT at the source tree
// every package importing cmd/compile/internal/base fails to import
// ("undefined: defaultGOARCH"). -overlay takes `<path in the source
// tree>=<file to read instead>` pairs; each named path is presented to
// go/build's directory listing and file opening hooks as if it existed
// in the source tree, read from the image's own GOROOT copy of the same
// generated file. The source tree on disk is never touched (its mount
// is read-only); the overlay list is recorded in the output's meta.
//
// No edits to the source tree; nothing fetched; nothing installed.
package main

import (
	"bufio"
	"compress/gzip"
	"encoding/json"
	"flag"
	"fmt"
	"go/ast"
	"go/build"
	"go/importer"
	"go/parser"
	"go/token"
	"go/types"
	"io"
	"io/fs"
	"os"
	"path/filepath"
	"regexp"
	"runtime"
	"runtime/debug"
	"sort"
	"strings"
	"syscall"
	"time"
)

const memoryBoundMB = 12288 // ABORT_MEMORY_O6 (12 GB; the first run's 3 GB bound fired at 6,114.7 MB)

// ---------------------------------------------------------------------------
// records
// ---------------------------------------------------------------------------

// operandLabel is one operand's type spelling on its OWN per-unit label
// object (lang + unit id present), the same shape task o4's json uses,
// so the spelling guard reads it as a display label and never as a key.
type operandLabel struct {
	Lang     string `json:"lang"`
	Unit     string `json:"unit"`
	Role     string `json:"role"`
	Spelling string `json:"spelling"`
	// TypeParam: the operand's type is a type parameter (generics) --
	// a spelling like `T` cannot say so on its own.
	TypeParam bool `json:"type_param"`
}

type site struct {
	Lang     string         `json:"lang"`
	Unit     string         `json:"unit"`
	File     string         `json:"file"`
	Line     int            `json:"line"`
	Col      int            `json:"col"`
	EndLine  int            `json:"end_line"`
	EndCol   int            `json:"end_col"`
	Kind     string         `json:"kind"`
	Operator string         `json:"operator"`
	Operands []operandLabel `json:"operands"`
	Result   string         `json:"result"`
	Func     string         `json:"func"`
	Package  string         `json:"package"`
	FileBin  string         `json:"file_bin"`
}

type fileRecord struct {
	Lang          string `json:"lang"`
	Unit          string `json:"unit"`
	File          string `json:"file"`
	Bin           string `json:"bin"`
	Package       string `json:"package"`
	SyntaxError   string `json:"syntax_error"`
	Sites         int    `json:"sites"`
	SitesAllTyped int    `json:"sites_all_operands_typed"`
}

type packageRecord struct {
	Lang                   string         `json:"lang"`
	Unit                   string         `json:"unit"`
	Dir                    string         `json:"dir"`
	ImportPath             string         `json:"import_path"`
	Bin                    string         `json:"bin"`
	Files                  int            `json:"files"`
	Errors                 int            `json:"errors"`
	ErrorCauses            map[string]int `json:"error_causes"`
	ErrorSamples           []string       `json:"error_samples"`
	WallS                  float64        `json:"wall_s"`
	MaxRSSMBAfter          float64        `json:"maxrss_mb_after"`
	Sites                  int            `json:"sites"`
	SitesAllTyped          int            `json:"sites_all_operands_typed"`
	StarExprSkippedUnknown int            `json:"star_expr_skipped_no_type_recorded"`
	TypeExprSkipped        int            `json:"type_expression_nodes_skipped"`
}

type meta struct {
	GeneratedBy    string   `json:"generated_by"`
	Task           string   `json:"task"`
	Line           string   `json:"line"`
	Node           string   `json:"node"`
	Root           string   `json:"root"`
	GOROOTUsed     string   `json:"goroot_used"`
	GoVersion      string   `json:"go_toolchain"`
	ReleaseTags    []string `json:"release_tags"`
	CgoEnabled     bool     `json:"cgo_enabled"`
	Overlay        []string `json:"overlay"`
	TypeStringRule string   `json:"type_string_rule"`
	ElapsedS       float64  `json:"elapsed_s"`
	PeakRSSMB      float64  `json:"peak_rss_mb"`
	MemoryBoundMB  int      `json:"memory_bound_mb"`
	Packages       int      `json:"packages"`
	Files          int      `json:"files"`
	Sites          int      `json:"sites"`
	SitesAllTyped  int      `json:"sites_all_operands_typed"`
	OnlyFilter     string   `json:"only_filter"`
	Shape          string   `json:"shape"`
}

// ---------------------------------------------------------------------------
// memory
// ---------------------------------------------------------------------------

func maxRSSMB() float64 {
	var ru syscall.Rusage
	if err := syscall.Getrusage(syscall.RUSAGE_SELF, &ru); err != nil {
		return -1
	}
	return float64(ru.Maxrss) / 1024.0 // linux: KB
}

func abortIfOverBudget() float64 {
	mb := maxRSSMB()
	if mb > memoryBoundMB {
		fmt.Fprintf(os.Stderr, "ABORT_MEMORY_O6: peak RSS %.1f MB > %d MB bound\n", mb, memoryBoundMB)
		os.Exit(97)
	}
	return mb
}

// ---------------------------------------------------------------------------
// error causes -- classified by the go/types message text, literal
// samples kept
// ---------------------------------------------------------------------------

var causeRules = []struct {
	name string
	re   *regexp.Regexp
}{
	{"missing symbol (undefined)", regexp.MustCompile(`\bundefined: |\bundeclared name\b|has no field or method`)},
	{"import failed", regexp.MustCompile(`could not import|cannot find package|is not in (GOROOT|std)`)},
	{"syntax", regexp.MustCompile(`\bexpected\b|syntax error|\bunexpected\b`)},
	{"unused (declared/imported and not used)", regexp.MustCompile(`declared and not used|imported and not used`)},
	{"language version", regexp.MustCompile(`requires go1\.\d+|go1\.\d+ or later`)},
}

func classify(msg string) string {
	for _, r := range causeRules {
		if r.re.MatchString(msg) {
			return r.name
		}
	}
	return "other"
}

// ---------------------------------------------------------------------------
// the walk over one type-checked file
// ---------------------------------------------------------------------------

type walker struct {
	fset     *token.FileSet
	info     *types.Info
	pkg      string
	bin      string
	funcs    []string // enclosing function stack
	pushed   []bool
	sites    []site
	counter  *int
	starSkip int
	typeSkip int
}

func exprType(info *types.Info, e ast.Expr) (string, bool) {
	tv, ok := info.Types[e]
	if !ok || tv.Type == nil {
		return "", false
	}
	return types.TypeString(tv.Type, nil), true
}

func isTypeParam(info *types.Info, e ast.Expr) bool {
	tv, ok := info.Types[e]
	if !ok || tv.Type == nil {
		return false
	}
	_, tp := tv.Type.(*types.TypeParam)
	return tp
}

func (w *walker) funcName() string {
	if len(w.funcs) == 0 {
		return ""
	}
	return w.funcs[len(w.funcs)-1]
}

func (w *walker) emit(n ast.Node, kind, op string, operands []ast.Expr, result ast.Expr) {
	pos := w.fset.PositionFor(n.Pos(), false)
	end := w.fset.PositionFor(n.End(), false)
	*w.counter++
	unit := fmt.Sprintf("go_types#site%d", *w.counter)
	roles := []string{"lhs", "rhs"}
	if len(operands) == 1 {
		roles = []string{"operand"}
	}
	labels := make([]operandLabel, 0, len(operands))
	for i, e := range operands {
		sp, _ := exprType(w.info, e)
		labels = append(labels, operandLabel{Lang: "go", Unit: unit + "#" + roles[i], Role: roles[i], Spelling: sp, TypeParam: isTypeParam(w.info, e)})
	}
	res := ""
	if result != nil {
		res, _ = exprType(w.info, result)
	}
	w.sites = append(w.sites, site{
		Lang: "go", Unit: unit, File: pos.Filename, Line: pos.Line, Col: pos.Column,
		EndLine: end.Line, EndCol: end.Column, Kind: kind, Operator: op, Operands: labels, Result: res,
		Func: w.funcName(), Package: w.pkg, FileBin: w.bin,
	})
}

func (w *walker) Visit(n ast.Node) ast.Visitor {
	if n == nil {
		if len(w.pushed) > 0 {
			if w.pushed[len(w.pushed)-1] {
				w.funcs = w.funcs[:len(w.funcs)-1]
			}
			w.pushed = w.pushed[:len(w.pushed)-1]
		}
		return nil
	}
	pushed := false
	switch x := n.(type) {
	case *ast.FuncDecl:
		name := x.Name.Name
		if x.Recv != nil && len(x.Recv.List) > 0 {
			name = types.ExprString(x.Recv.List[0].Type) + "." + name
		}
		w.funcs = append(w.funcs, name)
		pushed = true
	case *ast.FuncLit:
		w.funcs = append(w.funcs, w.funcName()+".func")
		pushed = true
	case *ast.BinaryExpr:
		if tv, ok := w.info.Types[x]; ok && tv.IsType() {
			w.typeSkip++
		} else {
			w.emit(x, "BinaryExpr", x.Op.String(), []ast.Expr{x.X, x.Y}, x)
		}
	case *ast.UnaryExpr:
		if tv, ok := w.info.Types[x]; ok && tv.IsType() {
			w.typeSkip++
		} else {
			w.emit(x, "UnaryExpr", x.Op.String(), []ast.Expr{x.X}, x)
		}
	case *ast.StarExpr:
		tv, ok := w.info.Types[x]
		if ok && tv.IsValue() {
			w.emit(x, "StarExpr", "*", []ast.Expr{x.X}, x)
		} else if !ok {
			w.starSkip++
		}
	case *ast.IncDecStmt:
		w.emit(x, "IncDecStmt", x.Tok.String(), []ast.Expr{x.X}, x.X)
	case *ast.AssignStmt:
		if x.Tok != token.ASSIGN && x.Tok != token.DEFINE && len(x.Lhs) == 1 && len(x.Rhs) == 1 {
			w.emit(x, "AssignStmt", x.Tok.String(), []ast.Expr{x.Lhs[0], x.Rhs[0]}, x.Lhs[0])
		}
	}
	w.pushed = append(w.pushed, pushed)
	return w
}

// ---------------------------------------------------------------------------
// checking
// ---------------------------------------------------------------------------

type checkResult struct {
	info   *types.Info
	errs   []error
	syntax map[string]string // file -> parse error text
	files  []*ast.File
	paths  []string
}

func parseFiles(fset *token.FileSet, paths []string) ([]*ast.File, map[string]string) {
	files := make([]*ast.File, 0, len(paths))
	syntax := map[string]string{}
	for _, p := range paths {
		src, rerr := openSource(p)
		if rerr != nil {
			syntax[p] = rerr.Error()
			continue
		}
		f, err := parser.ParseFile(fset, p, src, parser.ParseComments|parser.SkipObjectResolution)
		if err != nil {
			syntax[p] = err.Error()
		}
		if f != nil {
			files = append(files, f)
		}
	}
	return files, syntax
}

func typeCheck(fset *token.FileSet, imp types.Importer, importPath string, paths []string) checkResult {
	files, syntax := parseFiles(fset, paths)
	var errs []error
	conf := types.Config{
		Importer: imp,
		Sizes:    types.SizesFor("gc", "amd64"),
		Error:    func(e error) { errs = append(errs, e) },
	}
	info := &types.Info{Types: map[ast.Expr]types.TypeAndValue{}}
	conf.Check(importPath, fset, files, info)
	return checkResult{info: info, errs: errs, syntax: syntax, files: files, paths: paths}
}

func walkResult(fset *token.FileSet, cr checkResult, pkg, bin string, counter *int, files map[string]*fileRecord, fileUnit *int) ([]site, int, int) {
	var out []site
	starSkip := 0
	typeSkip := 0
	for _, f := range cr.files {
		w := &walker{fset: fset, info: cr.info, pkg: pkg, bin: bin, counter: counter}
		ast.Walk(w, f)
		out = append(out, w.sites...)
		starSkip += w.starSkip
		typeSkip += w.typeSkip
		path := fset.PositionFor(f.Pos(), false).Filename
		typed := 0
		for _, s := range w.sites {
			all := true
			for _, o := range s.Operands {
				if o.Spelling == "" {
					all = false
				}
			}
			if all {
				typed++
			}
		}
		*fileUnit++
		files[path] = &fileRecord{
			Lang: "go", Unit: fmt.Sprintf("go_types#file%d", *fileUnit), File: path, Bin: bin, Package: pkg,
			SyntaxError: cr.syntax[path], Sites: len(w.sites), SitesAllTyped: typed,
		}
	}
	return out, starSkip, typeSkip
}

func summarizeErrors(errs []error) (map[string]int, []string) {
	causes := map[string]int{}
	var samples []string
	for _, e := range errs {
		msg := e.Error()
		causes[classify(msg)]++
		if len(samples) < 5 {
			samples = append(samples, msg)
		}
	}
	return causes, samples
}

// ---------------------------------------------------------------------------
// overlay: generated files the git tree lacks, presented to go/build
// ---------------------------------------------------------------------------

var overlayFiles = map[string]string{} // virtual path in the source tree -> real file read instead

type renamedInfo struct {
	fs.FileInfo
	name string
}

func (r renamedInfo) Name() string { return r.name }

func overlayReadDir(dir string) ([]fs.FileInfo, error) {
	ents, err := os.ReadDir(dir)
	if err != nil {
		return nil, err
	}
	var out []fs.FileInfo
	seen := map[string]bool{}
	for _, e := range ents {
		fi, ierr := e.Info()
		if ierr != nil {
			continue
		}
		out = append(out, fi)
		seen[e.Name()] = true
	}
	for virt, real := range overlayFiles {
		if filepath.Dir(virt) != dir || seen[filepath.Base(virt)] {
			continue
		}
		fi, serr := os.Stat(real)
		if serr != nil {
			continue
		}
		out = append(out, renamedInfo{FileInfo: fi, name: filepath.Base(virt)})
	}
	sort.Slice(out, func(i, j int) bool { return out[i].Name() < out[j].Name() })
	return out, nil
}

func overlayOpenFile(path string) (io.ReadCloser, error) {
	if real, ok := overlayFiles[path]; ok {
		return os.Open(real)
	}
	return os.Open(path)
}

func openSource(path string) ([]byte, error) {
	if real, ok := overlayFiles[path]; ok {
		return os.ReadFile(real)
	}
	return os.ReadFile(path)
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

// checker is the pair the -shape flag governs: the FileSet every parse
// lands in and the source importer whose cache holds checked packages.
type checker struct {
	fset *token.FileSet
	imp  types.Importer
}

func newChecker() checker {
	fset := token.NewFileSet()
	return checker{fset: fset, imp: importer.ForCompiler(fset, "source", nil)}
}

func main() {
	root := flag.String("root", "/sources/golang_src/src/cmd/compile", "directory tree to walk")
	goroot := flag.String("goroot", "/sources/golang_src", "GOROOT for the source importer")
	out := flag.String("out", "PseudoCoupHQ/Research/oracle/compiler_units/go_types_sites.json", "output json (gzip-compressed when the name ends in .gz)")
	scratch := flag.String("scratch", os.TempDir(), "directory for the per-package site stream (one json line per site, copied into -out at the end)")
	only := flag.String("only", "", "only directories whose path contains this substring (sampling)")
	releaseThrough := flag.Int("release-through", 28, "extend build.Default.ReleaseTags through go1.<n>")
	overlay := flag.String("overlay", "", "comma-separated <virtual path in source tree>=<real file>; generated files the git tree lacks")
	shape := flag.String("shape", "tree", "tree: one FileSet + one importer cache for the whole run; package: a fresh FileSet + importer per package check, GC + FreeOSMemory after each")
	flag.Parse()
	if *shape != "tree" && *shape != "package" {
		fmt.Fprintln(os.Stderr, "bad -shape:", *shape, "(tree | package)")
		os.Exit(2)
	}
	var overlayList []string
	if *overlay != "" {
		for _, pair := range strings.Split(*overlay, ",") {
			kv := strings.SplitN(pair, "=", 2)
			if len(kv) != 2 {
				fmt.Fprintln(os.Stderr, "bad -overlay pair:", pair)
				os.Exit(2)
			}
			overlayFiles[kv[0]] = kv[1]
			overlayList = append(overlayList, pair)
		}
		build.Default.ReadDir = overlayReadDir
		build.Default.OpenFile = overlayOpenFile
	}

	t0 := time.Now()
	build.Default.GOROOT = *goroot
	build.Default.CgoEnabled = false
	for v := 1; v <= *releaseThrough; v++ {
		tag := fmt.Sprintf("go1.%d", v)
		found := false
		for _, t := range build.Default.ReleaseTags {
			if t == tag {
				found = true
			}
		}
		if !found {
			build.Default.ReleaseTags = append(build.Default.ReleaseTags, tag)
		}
	}

	// the site stream: one json line per site, appended as each package finishes
	streamPath := filepath.Join(*scratch, fmt.Sprintf("go_types_sites_stream_%d.jsonl", os.Getpid()))
	streamFile, err := os.Create(streamPath)
	if err != nil {
		fmt.Fprintln(os.Stderr, "cannot create site stream", streamPath, err)
		os.Exit(2)
	}
	stream := bufio.NewWriterSize(streamFile, 1<<20)
	defer os.Remove(streamPath)

	shared := checker{}
	if *shape == "tree" {
		shared = newChecker()
	}

	// every directory under root holding .go files, sorted
	dirSet := map[string]bool{}
	filepath.WalkDir(*root, func(p string, d fs.DirEntry, err error) error {
		if err != nil {
			return nil
		}
		if !d.IsDir() && strings.HasSuffix(p, ".go") {
			dirSet[filepath.Dir(p)] = true
		}
		return nil
	})
	var dirs []string
	for d := range dirSet {
		if *only == "" || strings.Contains(d, *only) {
			dirs = append(dirs, d)
		}
	}
	sort.Strings(dirs)

	var packages []packageRecord
	files := map[string]*fileRecord{}
	siteCounter := 0
	fileCounter := 0
	pkgCounter := 0
	sitesTotal := 0
	typedTotal := 0

	addPackage := func(dir, importPath, bin string, paths []string) {
		if len(paths) == 0 {
			return
		}
		t := time.Now()
		c := shared
		if *shape == "package" {
			c = newChecker()
		}
		cr := typeCheck(c.fset, c.imp, importPath, paths)
		ss, starSkip, typeSkip := walkResult(c.fset, cr, importPath, bin, &siteCounter, files, &fileCounter)
		causes, samples := summarizeErrors(cr.errs)
		for p, msg := range cr.syntax {
			causes["syntax (parser)"]++
			if len(samples) < 5 {
				samples = append(samples, p+": "+msg)
			}
		}
		typed := 0
		for _, s := range ss {
			all := true
			for _, o := range s.Operands {
				if o.Spelling == "" {
					all = false
				}
			}
			if all {
				typed++
			}
			b, _ := json.Marshal(s)
			stream.Write(b)
			stream.WriteByte('\n')
		}
		sitesTotal += len(ss)
		typedTotal += typed
		nSites := len(ss)
		nErr := len(cr.errs) + len(cr.syntax)
		ss = nil
		cr = checkResult{}
		if *shape == "package" {
			c = checker{}
			runtime.GC()
			debug.FreeOSMemory()
		}
		pkgCounter++
		rss := abortIfOverBudget()
		packages = append(packages, packageRecord{
			Lang: "go", Unit: fmt.Sprintf("go_types#pkg%d", pkgCounter),
			Dir: dir, ImportPath: importPath, Bin: bin, Files: len(paths),
			Errors: nErr, ErrorCauses: causes, ErrorSamples: samples,
			WallS: float64(time.Since(t).Milliseconds()) / 1000.0, MaxRSSMBAfter: rss,
			Sites: nSites, SitesAllTyped: typed, StarExprSkippedUnknown: starSkip, TypeExprSkipped: typeSkip,
		})
		fmt.Printf("  [%d/%d dirs] %s bin=%s files=%d errors=%d sites=%d typed=%d wall=%.1fs maxrss=%.0fMB\n",
			doneDirs, len(dirs), importPath, bin, len(paths), nErr, nSites, typed,
			float64(time.Since(t).Milliseconds())/1000.0, rss)
	}

	for i, dir := range dirs {
		doneDirs = i + 1
		rel, _ := filepath.Rel(*goroot+"/src", dir)
		importPath := filepath.ToSlash(rel)
		isTestdata := strings.Contains(dir+"/", "/testdata/")
		if isTestdata {
			ents, _ := os.ReadDir(dir)
			for _, e := range ents {
				if !e.IsDir() && strings.HasSuffix(e.Name(), ".go") {
					p := filepath.Join(dir, e.Name())
					addPackage(dir, importPath+"/"+e.Name(), "alone (testdata)", []string{p})
				}
			}
			continue
		}
		bp, err := build.Default.ImportDir(dir, 0)
		if err != nil {
			if _, multi := err.(*build.MultiplePackageError); multi {
				ents, _ := os.ReadDir(dir)
				for _, e := range ents {
					if !e.IsDir() && strings.HasSuffix(e.Name(), ".go") {
						addPackage(dir, importPath+"/"+e.Name(), "alone (multiple packages in directory)", []string{filepath.Join(dir, e.Name())})
					}
				}
				continue
			}
			if _, nogo := err.(*build.NoGoError); !nogo {
				fmt.Printf("  [%d/%d dirs] %s: go/build error: %v\n", i+1, len(dirs), importPath, err)
			}
		}
		if bp != nil {
			var main []string
			for _, f := range bp.GoFiles {
				main = append(main, filepath.Join(dir, f))
			}
			for _, f := range bp.CgoFiles {
				main = append(main, filepath.Join(dir, f))
			}
			for _, f := range bp.TestGoFiles {
				main = append(main, filepath.Join(dir, f))
			}
			bin := "package"
			if len(bp.TestGoFiles) > 0 {
				bin = "package (+ in-package tests)"
			}
			addPackage(dir, importPath, bin, main)
			var xt []string
			for _, f := range bp.XTestGoFiles {
				xt = append(xt, filepath.Join(dir, f))
			}
			addPackage(dir, importPath+"_test", "xtest", xt)
			for _, f := range bp.IgnoredGoFiles {
				addPackage(dir, importPath+"/"+f, "alone (excluded by build constraint)", []string{filepath.Join(dir, f)})
			}
		} else {
			// NoGoError with every file constrained out, or another error: type each alone
			ents, _ := os.ReadDir(dir)
			for _, e := range ents {
				if !e.IsDir() && strings.HasSuffix(e.Name(), ".go") {
					addPackage(dir, importPath+"/"+e.Name(), "alone (excluded by build constraint)", []string{filepath.Join(dir, e.Name())})
				}
			}
		}
	}

	if err := stream.Flush(); err != nil {
		fmt.Fprintln(os.Stderr, "cannot flush site stream", err)
		os.Exit(2)
	}
	streamFile.Close()

	peak := abortIfOverBudget()
	m := meta{
		GeneratedBy: "go_types_oracle.go", Task: "o6", Line: "arch_unit_oracle",
		Node: "node_0_3_2_arch_unit_oracle/node_0_3_2_0_compiler_units/node_0_3_2_0_1_variants_by_search",
		Root: *root, GOROOTUsed: *goroot, GoVersion: goVersion(),
		ReleaseTags: build.Default.ReleaseTags, CgoEnabled: build.Default.CgoEnabled, Overlay: overlayList,
		TypeStringRule: "types.TypeString(t, nil): package paths in full, no normalization; empty string = no type recorded by go/types for that expression",
		ElapsedS:       float64(time.Since(t0).Milliseconds()) / 1000.0, PeakRSSMB: peak, MemoryBoundMB: memoryBoundMB,
		Packages: len(packages), Files: len(files), Sites: sitesTotal, SitesAllTyped: typedTotal, OnlyFilter: *only,
		Shape: *shape,
	}

	// files as a sorted list
	var fileList []*fileRecord
	for _, fr := range files {
		fileList = append(fileList, fr)
	}
	sort.Slice(fileList, func(i, j int) bool { return fileList[i].File < fileList[j].File })

	raw, err := os.Create(*out)
	if err != nil {
		fmt.Fprintln(os.Stderr, "cannot write", *out, err)
		os.Exit(2)
	}
	defer raw.Close()
	var w io.Writer = raw
	var gz *gzip.Writer
	if strings.HasSuffix(*out, ".gz") {
		gz = gzip.NewWriter(raw)
		w = gz
	}
	f := bufio.NewWriterSize(w, 1<<20)
	enc := func(v interface{}) []byte {
		b, _ := json.Marshal(v)
		return b
	}
	fmt.Fprintf(f, "{\n\"meta\": %s,\n\"packages\": [\n", enc(m))
	for i, p := range packages {
		sep := ",\n"
		if i == len(packages)-1 {
			sep = "\n"
		}
		fmt.Fprintf(f, "%s%s", enc(p), sep)
	}
	fmt.Fprintf(f, "],\n\"files\": [\n")
	for i, fr := range fileList {
		sep := ",\n"
		if i == len(fileList)-1 {
			sep = "\n"
		}
		fmt.Fprintf(f, "%s%s", enc(fr), sep)
	}
	fmt.Fprintf(f, "],\n\"sites\": [\n")
	// copy the stream, line by line, never whole
	in, err := os.Open(streamPath)
	if err != nil {
		fmt.Fprintln(os.Stderr, "cannot reopen site stream", err)
		os.Exit(2)
	}
	sc := bufio.NewScanner(in)
	sc.Buffer(make([]byte, 1<<20), 1<<26)
	n := 0
	for sc.Scan() {
		n++
		sep := ",\n"
		if n == sitesTotal {
			sep = "\n"
		}
		f.WriteString(sc.Text())
		f.WriteString(sep)
	}
	in.Close()
	if n != sitesTotal {
		fmt.Fprintf(os.Stderr, "site stream holds %d lines, expected %d\n", n, sitesTotal)
		os.Exit(2)
	}
	fmt.Fprintf(f, "]\n}\n")
	f.Flush()
	if gz != nil {
		gz.Close()
	}
	fmt.Printf("done in %.1fs, peak RSS %.1f MB, shape=%s, packages=%d files=%d sites=%d sites_all_operands_typed=%d\n",
		m.ElapsedS, peak, *shape, len(packages), len(files), sitesTotal, typedTotal)
}

var doneDirs int

func goVersion() string {
	return "toolchain " + runtime.Version()
}
