# EMEC — Homepage (Phase 3)

## What this phase actually delivers

The master prompt's phase plan lists "Phase 3: Homepage" as its own step,
but a real homepage for an engineering consultancy isn't self-contained —
it's a shop window onto Services, Industries, Projects, Research,
Testimonials, and Blog. Building it properly meant pulling forward a
**minimal, honest schema** for each of those six apps now, rather than
either (a) hardcoding homepage content in templates (violates "nothing is
hardcoded" from the master prompt) or (b) building all six apps' full
production schema before the homepage can render anything real.

Each app got exactly the fields the homepage needs today, marked
`[BUILT — minimal, Phase X]` in `DATABASE_DESIGN.md`, with its full,
production schema (rich-text bodies, galleries, downloads, tagging, real FK
relationships) specified and scheduled for that app's own dedicated phase.
Nothing here needs to be thrown away later — later phases *extend* these
same models, they don't replace them.

## What was pulled forward, per app

| App | Phase 3 minimal model | Powers | Full build |
|---|---|---|---|
| `services` | `Service`, `ServiceCategory` | Capabilities section | Phase 5 |
| `industries` | `Industry` | Industries grid | Phase 6 |
| `projects` | `Project` | Featured Work | Phase 7 |
| `research` | `ResearchItem`, `ResearchCategory` | Research highlights | Phase 8 |
| `testimonials` | `Client`, `Testimonial` | Trusted By | Phase 11 |
| `blog` | `Post`, `BlogCategory` | Latest News | Phase 12 |

Each of these six apps also got working list + detail views/templates
(`/services/`, `/services/<slug>/`, etc.) — not just homepage cards — so
the site is genuinely browsable today, not a homepage floating in front of
dead links. Detail pages are intentionally thin (title, summary, one
explanatory line about what the full build adds) rather than pretending to
be finished; each says exactly which phase completes it.

`apps.pages` also gained **`ProcessStep`** — the "How We Engineer Solutions"
sequence. This is the one place on the homepage where numbered markers
(01/02/03/04) are used, because that content is a genuinely ordered process,
consistent with the constraint set in `DESIGN_SYSTEM.md`.

## Homepage behavior

`HomeView` queries each app directly (`Service.objects.filter(is_featured=True)`,
etc.) rather than the `HomePage` model owning denormalized copies of that
data — `HomePage` only supplies framing copy (headings/intros) and the
`show_*` visibility flags. This means:

- Marking a Service, Project, or Research item "featured" in Django Admin
  is what puts it on the homepage — no separate homepage-specific data entry.
- Every section on the homepage independently degrades to a quiet
  "add some in Django Admin" placeholder card if its app has no featured
  content yet, rather than breaking or rendering empty whitespace.
- Toggling `show_research` (etc.) off in `HomePage` hides that section
  immediately, without touching any of the underlying Research content.

## Verified end-to-end

Full migrate → seed → authenticated smoke test cycle, same as Phases 1–2.
`seed_demo_content` now seeds real EMEC-specific starter content across all
six pulled-forward apps (8 industries, 6 services across 3 categories, 3
featured projects, 2 research items, 3 seeded clients with one testimonial,
2 blog posts, 4 process steps) — confirmed rendering through the actual
homepage template, and every new list/detail route confirmed returning
`200` including slug-based detail pages (`/services/engineering-consulting/`,
`/projects/smart-irrigation-controller/`).

## What's next — Phase 4 (About / Team)

`apps.team` gets its full build: `TeamMember`, `Department`, and the
`/about/leadership/` page. The About page (already live since Phase 2)
gets its leadership section wired in, and `ResearchItem.authors` /
`BlogAuthor.team_member` (both currently unbuilt) become real FKs once
`TeamMember` exists.
