# The Spokane Employer Scorecard

A resident-run, quarterly-updated public report card on one question: is
Spokane attracting employers that raise wages? Built entirely from cited
public data. Static HTML, no build step. Maintained with Claude Code; the
editorial rules live in CLAUDE.md and the refresh workflow in
`.claude/commands/quarterly-update.md`.

Live site (once deployed): https://spokanescorecard.com

## Structure

- `index.html` — the scorecard
- `methodology.html` — rubric, sources, limitations, append-only change log
- `calculator.html` — employer impact calculator
- `flywheel.svg` — diagram embedded by index.html (must deploy alongside it)
- `press/flywheel.png` — social/press image
- `data/` — pulled datasets and audit files
- `CLAUDE.md` — editorial constitution for Claude Code sessions

## Preview locally

Open index.html in a browser, or `python3 -m http.server` and visit
localhost:8000.

## Deploy (GitHub Pages)

1. Push this repo to GitHub (public or private with Pages enabled):
   `gh repo create spokane-scorecard --public --source=. --push`
2. Repo Settings, Pages: deploy from branch `main`, folder `/ (root)`.
3. Custom domain: at your registrar (Porkbun/Cloudflare), point the apex
   `spokanescorecard.com` at GitHub Pages with A records
   185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153,
   and a CNAME record for `www` to `<your-github-username>.github.io`.
4. Back in Pages settings, enter the custom domain (GitHub creates the CNAME
   file) and check Enforce HTTPS once the certificate issues.

Do this in order; adding the custom domain before DNS resolves makes the site
look broken in the interim.

## Launch checklist

- [ ] Register spokanescorecard.com (and .org, redirected)
- [ ] Push repo, enable Pages, set DNS, enforce HTTPS
- [ ] Replace email placeholders: `grep -rn "your email here" *.html`
- [ ] Tally form (tally.so/r/2E6e8g): set "Anything else?" to optional
- [ ] Get a free Census API key, export as CENSUS_API_KEY (needed for the
      November earnings pull)
- [ ] Private gut-check: send to Patrick Jones (EWU) before wider sharing
- [ ] Then media, in order: RANGE (Sellers/Walters), Spokesman (Dinman or
      Clouse), Journal of Business, SPR
- [ ] Pick a license (CC BY 4.0 fits the project's ethos) and add LICENSE

## Cadence

Quarterly, by hand, via `/quarterly-update` in Claude Code. Next: November
2026, led by pre-registered grade thresholds and the attention audit
(`/attention-audit`).
