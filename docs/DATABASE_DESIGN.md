# EMEC — Database Design

Every model below inherits the relevant abstract base from
`apps.core.models_base` (noted in parentheses). Fields already implemented
in Phase 1 are marked **[BUILT]**; everything else is the specification each
later phase implements against, so schema decisions are made once, up front,
rather than re-litigated app by app.

---

## apps.accounts **[BUILT — Phase 2]**

- **User** (extends `AbstractUser`, Timestamped)
  `role (choices: site_admin/content_editor/research_manager/
  training_coordinator/careers_manager/viewer), job_title, phone, avatar,
  is_department_head`. Custom user model set as `AUTH_USER_MODEL` from the
  first migration (not retrofitted later). `role` seeds the account into a
  matching permission Group via `seed_groups`; fine-grained access is still
  governed by Django's standard Group/Permission system so it stays editable
  from Django Admin without a code change.

## apps.core **[BUILT]**

- **SiteConfiguration** (singleton) — identity, contact defaults, footer
  copy, group intro text, tracking IDs, default SEO, feature flags
- **SocialLink** (Orderable) — platform, url, is_active
- **NavigationMenu** — slot (6 fixed choices), label
- **NavigationItem** (MPTT tree) — menu FK, parent, label, url, icon,
  display_order, is_active
- **Announcement** — message, link, is_active, start/end datetime

## apps.pages **[BUILT]**

- **HomePage** (singleton, SEO) — hero fields, per-section heading/intro
  copy, per-section visibility booleans, closing CTA
- **HomepageStatistic** (Orderable) — value, label, icon, is_active
- **AboutPage** (singleton, SEO) — intro heading, story, vision, mission,
  group_story, hero_image
- **CoreValue** (Orderable) — title, description, icon
- **TimelineEvent** (Orderable) — year_bs, year_ad, title, description,
  image, is_milestone
- **GroupCompany** (Orderable) — name, tagline, description, logo,
  website_url, founded_year, is_active *(Nepal Agro Yantra, Ojas Solutions,
  RC Interior, future ventures)*

---

## apps.team **[BUILT — Phase 4]**

- **Department** `name, slug`
- **TeamMember** (Slug, Orderable, Timestamped)
  `name, role_title, department FK, bio, photo, email, linkedin_url,
  is_leadership (bool), is_active`. Powers the About page's Leadership
  section (`is_leadership=True`) and `/about/leadership/<slug>/` detail
  pages. Becomes the FK target for `ResearchItem.authors` (Phase 8) and
  `BlogAuthor.team_member` (Phase 12).

## apps.services **[BUILT — Phase 5]**

- **ServiceCategory** (Orderable) `name, slug, icon, description`
- **Service** (Slug, SEO, Orderable) `category FK, title, summary,
  description, icon, hero_image, related_industries M2M→Industry,
  is_featured, is_active` — extended from Phase 3's minimal version with
  SEO fields, rich description, hero image, and the industries M2M.
- **ServiceProcessStep** (Orderable) `service FK, step_number, title,
  description` — the *per-service* delivery process, distinct from
  `pages.ProcessStep` (the single global homepage sequence).

## apps.industries **[BUILT — minimal, Phase 3]** → full build Phase 6

- **Industry** (Slug, Orderable) `name, summary, icon, image, is_active` —
  **[BUILT, minimal]**. Phase 6 adds: SEO fields, description (rich text),
  related_services M2M, hero_image

## apps.projects **[BUILT — minimal, Phase 3]** → full build Phase 7

- **Project** (Slug, SEO, Publishable, Orderable)
  `title, summary, industry FK, client_name (free-text), cover_image,
  is_featured, is_confidential` — **[BUILT, minimal]**. Phase 7 adds:
  problem_statement, objectives, challenges, engineering_solution, results,
  lessons_learned, technologies/hardware/software_used (taggit), gallery,
  videos, downloads, related projects, and swaps `client_name` for a real FK
  to `testimonials.Client`.

## apps.research **[BUILT — minimal, Phase 3]** → full build Phase 8

- **ResearchCategory** `name, slug` — **[BUILT]**
- **ResearchItem** (Slug, Publishable, Orderable)
  `category FK, title, abstract, cover_image, publication_date,
  is_featured` — **[BUILT, minimal]**. Phase 8 adds: body (rich text),
  authors M2M→team.TeamMember, PDF uploads, external_url, Patent model.

## apps.training — Phase 9

- **TrainingProgram** (Timestamped, Slug, SEO, Publishable)
  `title, program_type (choices: corporate/university/industrial/technical_course),
  summary, description (rich text), duration_text, price_text, cover_image,
  gallery (→ TrainingGalleryImage), certificate_offered (bool)`
- **Event** (Timestamped, Slug, Publishable)
  `training_program FK (nullable — standalone events allowed), title,
  description, start_datetime, end_datetime, location_text, is_online,
  registration_open (bool), capacity (int, nullable)`
- **EventRegistration**
  `event FK, full_name, email, phone, organization, message, created_at,
  status (pending/confirmed/cancelled)`
- **TrainingGalleryImage** (Orderable) `training_program FK, image, caption`

## apps.careers — Phase 10

- **JobListing** (Timestamped, Slug, SEO, Publishable)
  `title, department FK→team.Department, employment_type (full_time/part_time/
  internship/contract), location_text, is_remote, summary, responsibilities
  (rich text), requirements (rich text), is_internship (bool), application_deadline`
- **JobApplication**
  `job_listing FK, full_name, email, phone, resume_file, portfolio_file,
  portfolio_url, cover_letter (text), status (received/under_review/
  interview/rejected/hired), applied_at`

## apps.testimonials **[BUILT — minimal, Phase 3]** → full build Phase 11

- **Client** (Orderable) `name, logo, website_url, is_featured` — **[BUILT, minimal]**
- **Testimonial** (Orderable) `client FK, author_name, author_role, quote,
  photo, is_featured` — **[BUILT, minimal]**. Phase 11 adds: Partner, Award,
  `Testimonial.project` FK, and wires `Client` as the real FK target for
  `Project.client` (replacing `Project.client_name`).

## apps.blog **[BUILT — minimal, Phase 3]** → full build Phase 12

- **BlogCategory** `name, slug` — **[BUILT]**
- **Post** (Slug, SEO, Publishable) `category FK, title, excerpt,
  featured_image, is_featured` — **[BUILT, minimal]**. Phase 12 adds:
  BlogAuthor, tags (taggit), body (rich text), reading_time_minutes,
  Comment model.

## apps.media_library — Phase 13

- **MediaAsset** (Timestamped, Orderable)
  `title, asset_type (image/video/document/cad/brochure/certificate),
  file, thumbnail, description, related_project FK (nullable),
  is_public (bool — some CAD/internal docs stay staff-only)`
- **Download** (Timestamped) — convenience wrapper for the public "Downloads"
  page: `title, category (brochure/company_profile/certificate/whitepaper),
  file, description, download_count (int, incremented on access)`

## apps.contact — Phase 14

- **Department** `name, notify_email` *(distinct from team.Department — this
  is "who receives which inquiry type", e.g. Consulting, Partnerships, HR)*
- **Office** (Address, Timestamped) `name, is_headquarters, phone, email,
  business_hours_text, map_embed_url, department FK (nullable)`
- **InquiryType** `name, slug` *(General / Consulting Request / Workshop
  Request / Partnership Request / Career Inquiry — matches the master
  prompt's required inquiry categories)*
- **Inquiry** (Timestamped)
  `inquiry_type FK, department FK (nullable, auto-routed from inquiry_type),
  full_name, email, phone, organization, subject, message, status
  (new/in_progress/resolved), source_page (text, for analytics)`

---

## Cross-cutting relationships (why FKs point where they do)

- `Project.client` → `testimonials.Client` (not a free-text field) so a
  client's logo/name stays consistent everywhere it's referenced, and a
  confidential project can still be filtered/reported on internally while
  hiding the client name on the public page (`is_confidential`).
- `Project.industry` and `Service.related_industries` are both FKs/M2M to
  the same `industries.Industry`, so the Industries pages can pull "projects
  in this industry" and "services relevant to this industry" without any
  duplicate data entry.
- `ResearchItem.authors` and `BlogAuthor.team_member` both point back to
  `team.TeamMember`, so a leadership bio page can show "Papers by this
  person" and "Posts by this person" from one canonical profile.
- `contact.Inquiry.inquiry_type` drives routing to `contact.Department`,
  which is how a single public contact form (with a type selector) satisfies
  the master prompt's requirement for separate consulting/workshop/
  partnership/career inquiry flows without four separate form implementations.
