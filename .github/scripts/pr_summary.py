import argparse, xml.etree.ElementTree as ET, os, time, textwrap, pathlib

def parse_junit(path):
    if not os.path.exists(path):
        return {"tests": 0, "failures": 0, "errors": 0, "skipped": 0, "time": 0.0}
    tree = ET.parse(path)
    root = tree.getroot()
    suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
    totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0, "time": 0.0}
    for s in suites:
        totals["tests"] += int(s.attrib.get("tests", 0))
        totals["failures"] += int(s.attrib.get("failures", 0))
        totals["errors"] += int(s.attrib.get("errors", 0))
        totals["skipped"] += int(s.attrib.get("skipped", 0))
        totals["time"] += float(s.attrib.get("time", 0.0))
    return totals

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--junit", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    totals = parse_junit(args.junit)
    passed = totals["tests"] - totals["failures"] - totals["errors"] - totals["skipped"]
    status = "✅ PASS" if totals["failures"] == 0 and totals["errors"] == 0 else "❌ FAIL"

    pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)

    html = f"""
<!doctype html><meta charset='utf-8'>
<title>PR Test Report</title>
<h1>PR Test Report</h1>
<p><b>Status:</b> {status}</p>
<ul>
<li>Total tests: {totals['tests']}</li>
<li>Passed: {passed}</li>
<li>Failures: {totals['failures']}</li>
<li>Errors: {totals['errors']}</li>
<li>Skipped: {totals['skipped']}</li>
<li>Duration (s): {totals['time']:.2f}</li>
</ul>
<p>Generated at: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}</p>
"""
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(html)

    md = f"""
### CI Summary {status}
- **Total tests:** {totals['tests']}
- **Passed:** {passed}
- **Failures:** {totals['failures']}
- **Errors:** {totals['errors']}
- **Skipped:** {totals['skipped']}
- **Duration (s):** {totals['time']:.2f}
"""
    with open('workspaces/PR_SUMMARY.md', 'w', encoding='utf-8') as f:
        f.write(textwrap.dedent(md).lstrip('\n'))

if __name__ == '__main__':
    main()
