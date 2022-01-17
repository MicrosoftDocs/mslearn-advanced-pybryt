import re

from glob import glob
from otter.assign.utils import str_to_doctest
from textwrap import dedent


CODE_WITH_OUTPUT_REGEX = r"```python\n([^`]+)```\n{2,5}    ([\s\S]+?)\n{2,}"


def convert_match(m):
    res = "```python\n"
    lines = [l for l in m.group(1).strip().split("\n") if l.strip()]
    interp = str_to_doctest(lines, [])
    res += "\n".join(interp) + "\n"
    res += dedent("    " + m.group(2))
    res += "\n```\n\n"
    return res


def main():
    mds = glob("*.md")
    for md_path in mds:
        with open(md_path) as f:
            md = f.read()

        clean_md = md
        changes = []
        for m in re.finditer(CODE_WITH_OUTPUT_REGEX, md):
            changes.append((m.span(), convert_match(m)))

        for (s, e), new_md in changes[::-1]:
            clean_md = clean_md[:s] + new_md + clean_md[e:]

        with open(md_path, "w") as f:
            f.write(clean_md)

if __name__ == "__main__":
    main()
