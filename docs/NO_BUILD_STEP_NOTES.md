# EMEC — No Build Step (Plain CSS)

## What changed

The project originally compiled CSS from Tailwind utility classes via a
small Node.js/npm build step (`package.json`, `tailwind.config.js`,
`static/src/css/input.css` → `static/dist/site.css`). To be clear: **this
was never Next.js, React, or any JavaScript framework** — it was CSS
tooling only, no different in kind from a Sass compiler. But it did require
Node.js installed and a build command to run, which added a tool to learn
for no real benefit at this project's size.

**Removed entirely:**
- `package.json`, `tailwind.config.js`
- `static/src/` (Tailwind input CSS)
- `django-crispy-forms` / `crispy-tailwind` (unused — no forms are built
  yet; when Phase 9/10/14 add them, they'll be plain Django form templates
  styled against the same stylesheet, not a separate theming package)

**Added:**
- `static/css/site.css` — one hand-written, plain CSS file. Every class
  used across every template is defined here. No preprocessor, no build
  step. Edit the file, refresh the browser.
- `static/js/site.js` — unchanged; this was always plain vanilla
  JavaScript (theme toggle + scroll-reveal), never a framework, so nothing
  needed to change here.

## Every template was rewritten

All Tailwind utility classes (`max-w-content`, `md:grid-cols-3`,
`text-[var(--x)]`, etc.) were replaced with semantic class names
(`.container`, `.grid-3`, `.card`, `.hero-title`, `.section--bordered`,
...) defined in `static/css/site.css`. The visual design itself — colors,
typography, the circuit-trace motif, dark-mode-as-default, spacing rhythm
— is unchanged; only the CSS authoring approach changed, from
utility-class composition to a conventional hand-written stylesheet with
one class per component. This is arguably easier to read for anyone not
already fluent in Tailwind's shorthand.

## Verified

Confirmed with a repo-wide search that zero Tailwind-pattern classes
remain in any template (`grep` for `max-w-`, `md:`, `px-`, `grid-cols-`,
etc. across `templates/` returns nothing). Full migrate → seed → audit →
HTTP smoke test cycle re-run against every route — all `200`, and the
rendered HTML confirmed using the new semantic classes
(`.btn.btn-primary`, `.card`, `.card-media`, etc.) instead of Tailwind
utilities.

## Editing the site's look going forward

Open `static/css/site.css`. It's organized top-to-bottom: design tokens
(colors/fonts as CSS variables) → reset → layout helpers → typography →
buttons → cards → header/footer → page-specific sections. Change a value,
save, refresh — no compile step, ever.
