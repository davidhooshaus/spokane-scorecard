#!/usr/bin/env python3
"""Flesch-Kincaid grade level for the visible copy on each page.

The site's standard: keep prose at or below 6th grade, except where a term is
load-bearing and simplifying it would change the meaning (taxable retail sales,
labor force participation, traded sector). Clarity, not dumbing down.

Usage:  python3 tools/readability.py [file.html ...]
        python3 tools/readability.py --worst 15
"""
import re, sys, glob, os

VOWELS = "aeiouy"

def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    n = len(re.findall(r"[aeiouy]{1,2}", w))
    return max(1, n)

def strip_html(html):
    html = re.sub(r"<(script|style|svg|head)\b.*?</\1>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    # Tables are data, not prose. Source lines are citations: proper nouns, dates
    # and agency names, which no rewrite should flatten. Neither is measurable copy.
    html = re.sub(r"<table\b.*?</table>", " ", html, flags=re.S | re.I)
    html = re.sub(r'<p class="src".*?</p>', " ", html, flags=re.S | re.I)
    # The change log is append-only. Past entries can never be rewritten, so
    # measuring them just produces a number nobody is allowed to act on.
    html = re.sub(r"<h2[^>]*>\s*Change log.*?</section>", " ", html, flags=re.S | re.I)
    # keep block boundaries so sentences don't run together
    html = re.sub(r"</(p|li|h1|h2|h3|h4|div|section|summary)>", "\n\n", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    ents = {"&rsquo;": "'", "&lsquo;": "'", "&ldquo;": '"', "&rdquo;": '"',
            "&amp;": "&", "&nbsp;": " ", "&middot;": ".", "&minus;": "-",
            "&ndash;": "-", "&mdash;": "-", "&larr;": "", "&rarr;": "", "&uarr;": "", "&darr;": ""}
    for k, v in ents.items():
        html = html.replace(k, v)
    html = re.sub(r"&#?\w+;", " ", html)
    return html

def blocks(text):
    for b in re.split(r"\n\s*\n", text):
        b = re.sub(r"\s+", " ", b).strip()
        if len(b.split()) >= 12 and re.search(r"[a-z]{2}[.!?](\s|$)", b):
            yield b   # needs at least one real sentence ending

def grade(text):
    sents = [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    if not sents or not words:
        return None, 0, 0
    syl = sum(syllables(w) for w in words)
    g = 0.39 * (len(words) / len(sents)) + 11.8 * (syl / len(words)) - 15.59
    return round(g, 1), len(words), round(len(words) / len(sents), 1)

def main():
    argv = sys.argv[1:]
    worst_n = 12
    if "--worst" in argv:
        i = argv.index("--worst")
        worst_n = int(argv[i + 1])
        del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    files = args or [f for f in glob.glob("*.html")] + ["archive/index.html"]
    rows = []
    for f in files:
        if not os.path.isfile(f):
            continue
        text = strip_html(open(f).read())
        for b in blocks(text):
            g, n, wps = grade(b)
            if g is not None:
                rows.append((g, f, n, wps, b))
    if not rows:
        print("no prose blocks found")
        return
    over = [r for r in rows if r[0] > 6.0]
    print(f"{len(rows)} prose blocks. {len(over)} above 6th grade "
          f"({100*len(over)//len(rows)}%). "
          f"Median grade {sorted(r[0] for r in rows)[len(rows)//2]}.\n")
    for g, f, n, wps, b in sorted(rows, reverse=True)[:worst_n]:
        print(f"  grade {g:>4}  {wps:>4} words/sentence  {f}")
        print(f"     {b[:190]}{'...' if len(b) > 190 else ''}\n")

if __name__ == "__main__":
    main()
