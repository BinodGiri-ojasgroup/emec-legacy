# EMEC — Wireframes (Phase 1)

Low-fidelity structure for the page types that recur across the site.
Visual execution follows `DESIGN_SYSTEM.md`; these define information
hierarchy only.

## Homepage

```
┌──────────────────────────────────────────────────────────┐
│ [announcement bar — optional, dismissible]                │
│ EMEC   Services  Industries  Projects  Research  ⋯  [Mode]│
├──────────────────────────────────────────────────────────┤
│  SPEC 2070 B.S. — PRESENT                                  │
│  Engineering the foundation of what's next.                │  ← hero
│  [Start a Consultation]  [View Our Work]                   │
│  ┈┈┈●┈┈┈┈┈┈●┈┈┈┈┈┈┈┈●┈┈┈┈  (trace divider)                 │
├──────────────────────────────────────────────────────────┤
│  150+ Projects   40+ Engineers   12 Years   8 Industries    │  ← stats
├──────────────────────────────────────────────────────────┤
│  Engineering Capabilities                                   │
│  [Service] [Service] [Service] [Service] [Service] [Service]│  ← Phase 5
├──────────────────────────────────────────────────────────┤
│  Industries We Serve — icon grid                            │  ← Phase 6
├──────────────────────────────────────────────────────────┤
│  Featured Work — 3-up project cards, image-led               │  ← Phase 7
├──────────────────────────────────────────────────────────┤
│  Research & Innovation — 2-up highlight cards                │  ← Phase 8
├──────────────────────────────────────────────────────────┤
│  How We Engineer Solutions — numbered process (1→2→3→4)      │  ← real sequence, numbers OK here
├──────────────────────────────────────────────────────────┤
│  Training & Knowledge Transfer — promo block                 │  ← Phase 9
├──────────────────────────────────────────────────────────┤
│  Trusted By — client logo strip + 1 featured testimonial     │  ← Phase 11
├──────────────────────────────────────────────────────────┤
│  Latest Research  |  Latest News — 2 columns                 │  ← Phase 8/12
├──────────────────────────────────────────────────────────┤
│  Have an engineering challenge?  [Talk to Our Engineers]     │  ← closing CTA
├──────────────────────────────────────────────────────────┤
│  Footer: About | Company nav | Engineering nav | Contact     │
└──────────────────────────────────────────────────────────┘
```

## Service / Project detail (shared spine)

```
┌──────────────────────────────────────────────────────────┐
│ Eyebrow (category)                                          │
│ Title                                                        │
│ Summary                                                      │
│ Hero image                                                   │
├──────────────────────────────────────────────────────────┤
│ Problem Statement          │  Sidebar: client, industry,     │
│ Objectives                 │  services used, timeline,       │
│ Engineering Solution       │  technologies (tag chips)        │
│ Challenges                 │                                  │
│ Results                    │                                  │
├──────────────────────────────────────────────────────────┤
│ Gallery — image grid                                          │
├──────────────────────────────────────────────────────────┤
│ Downloads (if any)                                             │
├──────────────────────────────────────────────────────────┤
│ Related Projects — 3-up cards                                  │
└──────────────────────────────────────────────────────────┘
```

## Listing pages (Projects, Research, Blog, Training, Careers)

```
┌──────────────────────────────────────────────────────────┐
│ Page heading + intro copy                                    │
│ [Search]  [Category filter]  [Industry filter]  [Sort]        │  ← django-filter + watson
├──────────────────────────────────────────────────────────┤
│ [Card] [Card] [Card]                                          │
│ [Card] [Card] [Card]                                          │
│ [Card] [Card] [Card]                                          │
├──────────────────────────────────────────────────────────┤
│           ‹ Prev   1  2  3 …  Next ›                          │  ← pagination
└──────────────────────────────────────────────────────────┘
```

## Contact

```
┌──────────────────────────────────────────────────────────┐
│ Heading + intro                                               │
├────────────────────────────┬───────────────────────────────┤
│  Inquiry type selector       │  Office list (cards):          │
│  (General / Consulting /     │   - HQ, address, map embed     │
│   Workshop / Partnership /   │   - phone, email, hours        │
│   Career)                    │   - additional offices          │
│  Name / Email / Phone /      │                                 │
│  Organization / Message      │                                 │
│  [Submit Inquiry]             │                                 │
└────────────────────────────┴───────────────────────────────┘
```

## Job listing detail

```
┌──────────────────────────────────────────────────────────┐
│ Title · Department · Type · Location                        │
│ Summary                                                      │
│ Responsibilities                                              │
│ Requirements                                                  │
│ ── Application form ──                                       │
│ Name / Email / Phone / Resume upload / Portfolio / Cover text │
│ [Submit Application]                                          │
└──────────────────────────────────────────────────────────┘
```
