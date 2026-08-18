# EMEC Design System

## Direction

EMEC's own name is the brief: *Electro* (circuits, current, signal) *Mnemonic*
(memory, recall, the trace a thought leaves behind) *Engineering* (rigor,
proof, precision). The design should look like it was drawn by the engineers
themselves — closer to a schematic sheet or an engineering datasheet than a
marketing site. That is the one real risk this system takes: **the whole
site is built around a literal circuit-trace motif** — hairline routed lines
with right-angle joints and node dots — used as the section divider, the
timeline connector, and the hover state on interactive elements. It is the
single signature element; everything else stays quiet so it reads as
intentional rather than decorative.

Explicitly avoided: warm cream + terracotta (a different brand's default),
pure-black + acid-accent (generic "AI startup" default), and broadsheet
hairline-newspaper layouts. Numbered markers (01/02/03) are used in exactly
one place — the Engineering Process section — because that content is a
real, ordered sequence; nowhere else.

## Color Tokens

| Token | Hex | Role |
|---|---|---|
| `--emec-ink` | `#0B1220` | Primary dark background (near-navy-black, not pure black) |
| `--emec-graphite` | `#151E2B` | Secondary dark surface (cards, elevated panels on dark) |
| `--emec-slate` | `#5B6B7C` | Muted text, borders, disabled states |
| `--emec-steel` | `#3B6EA5` | Primary accent — trust, engineering, primary buttons/links |
| `--emec-circuit` | `#35C7C0` | Signature accent — trace lines, active states, data highlights |
| `--emec-porcelain` | `#F6F8FA` | Primary light background |
| `--emec-silver` | `#D7DCE2` | Light-mode borders, dividers, hairlines |
| `--emec-white` | `#FFFFFF` | Cards / surfaces on light backgrounds |
| `--emec-signal` | `#E8B84B` | Rare — warning/attention only (e.g. draft badges), never decorative |

Dark mode is not an inverted light mode — it is the *primary* mode (`--emec-ink`
background), since it reads as an instrument panel / schematic sheet. Light
mode swaps to `--emec-porcelain` while keeping `--emec-steel` and
`--emec-circuit` as the only accents in both modes, so brand recognition
survives the toggle.

## Typography

| Role | Typeface | Notes |
|---|---|---|
| Display / Headings | **Space Grotesk** | Geometric, technical, distinct from generic corporate serif or humanist sans defaults. Used at large sizes with tight tracking. |
| Body | **Inter** | High legibility at long-form reading sizes (case studies, research abstracts). |
| Utility / Data / Labels | **IBM Plex Mono** | Used for eyebrows, stats, dates, spec labels, timeline years — reinforces the datasheet register without turning body copy into code. |

Type scale (rem, 16px base): `0.75 / 0.875 / 1 / 1.125 / 1.375 / 1.75 / 2.25 / 3 / 4.5`.
Headings use Space Grotesk at `-0.02em` tracking; mono labels are always
uppercase with `+0.08em` tracking to read as annotation, not body text.

## Layout Concept

```
┌───────────────────────────────────────────────┐
│  EMEC   Services  Industries  Projects  ...    │  ← header, hairline bottom border
├───────────────────────────────────────────────┤
│  SPEC 2013—PRESENT                              │  ← mono eyebrow
│  Engineering the foundation                     │  ← Space Grotesk, huge
│  of what's next.                                │
│  [ Start a Consultation ]  [ View Our Work ]    │
│  ┈┈┈┈┈●┈┈┈┈┈┈┈┈●┈┈┈┈┈┈┈┈●┈┈┈┈┈  (trace divider) │
├───────────────────────────────────────────────┤
│  150+          40+           12                │  ← mono stat values
│  Projects      Engineers     Years              │
└───────────────────────────────────────────────┘
```

Section rhythm: generous vertical padding (`py-24`/`py-32`), content capped
at `max-w-7xl`, a consistent 12-column grid. The circuit-trace divider (see
`templates/components/trace_divider.html`) replaces plain `<hr>` between
major sections site-wide.

## Signature Element — the Trace

An SVG horizontal line with 1–3 right-angle joints and small filled circles
("nodes") at each joint and endpoint, rendered in `--emec-circuit` at low
opacity on dark backgrounds. Used as: section dividers, the connector
between Timeline entries, the underline that draws in on nav-link hover, and
the loading/progress indicator on forms. This is the one recurring motif
that makes the site recognizably EMEC's rather than a generic dark-mode
corporate template.

## Motion

Minimal and purposeful: a single orchestrated hero load-in (headline
fades/slides up, trace divider "draws" left to right via stroke-dashoffset),
scroll-reveal on section entry (opacity/translate-y, 400ms, one direction
only), and a trace-draw hover state on links/cards. No ambient/looping
animation, no parallax gimmicks. `prefers-reduced-motion` disables all
transform/opacity transitions and shows content in its final state.

## Accessibility Floor

Minimum 4.5:1 contrast for body text in both modes (verified: `--emec-slate`
on `--emec-porcelain` = 4.6:1; `--emec-porcelain` on `--emec-ink` = 15.8:1).
Visible focus rings using `--emec-circuit` at 2px offset. All interactive
elements reachable by keyboard in visual order. Motion respects
`prefers-reduced-motion`.
