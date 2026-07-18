---
date: 2026-07-18
type: feat
topic: natura-garden-color-palette
artifact_contract: ce-unified-plan/v1
artifact_readiness: implementation-ready
product_contract_source: ce-brainstorm
execution: code
---

# Natura Garden Color Palette - Plan

## Goal Capsule

Apply the **Natura Garden** color direction to the GMAHK Serpong Natura v2 site (branch `version2`): a nature-forward, calm palette with forest-green header, cream-and-white alternating body bands, and warm gold accents. Product authority is this document. Planning enriches implementation tokens and SCSS structure in `ce-plan`.

---

## Product Contract

### Summary

Replace the current warm-brown v1 palette on the v2 full-bleed layout with **Palette B — Natura Garden**, aligned to the church name and a peaceful, welcoming tone for newcomers and members.

### Problem Frame

v2 layout structure is in place; color still reflects the older brown “warm earth” scheme. The church wants a cohesive frontend identity that feels natural, calm, and distinct without looking corporate or cold.

### Key Decisions

- **Palette B — Natura Garden** chosen over Warm Welcome (brown) and Dawn Hope (navy/amber).
- **Forest green header** anchors brand; body stays light (cream/white bands) for readability on mobile.
- **Warm gold** reserved for secondary highlights and optional CTA emphasis — not overused.
- **No new fonts or imagery** in this scope — color tokens only.

### Color Tokens

| Token | Role | Hex |
|-------|------|-----|
| `header-bg` | Sticky header / nav background | `#2F5D50` |
| `header-text` | Nav links, brand on header | `#FFFFFF` |
| `body-bg` | Primary section band | `#F4F7F2` |
| `body-bg-alt` | Alternate section band | `#FFFFFF` |
| `text-primary` | Body copy | `#2A2F2A` |
| `text-muted` | Meta, excerpts, captions | `#5C6B5E` |
| `accent-band` | Jadwal block, soft highlights | `#DDE8D6` |
| `accent-secondary` | Attachments, tags, gold highlights | `#E8C872` |
| `cta-bg` | Primary buttons | `#2F5D50` |
| `cta-text` | Button label | `#FFFFFF` |
| `link` | Inline links (body) | `#3A6B5C` |
| `card-bg` | Event/Berita cards | `#FFFFFF` |
| `footer-bg` | Footer | `#E2EAE0` |

### Requirements

- R1. Header and sticky nav use `header-bg` with `header-text`; hover/active nav states remain visible (lighter overlay on green, not brown).
- R2. Alternating `.section-band` backgrounds use `body-bg` and `body-bg-alt` in sequence on Beranda.
- R3. Body copy uses `text-primary`; dates, excerpts, and helper text use `text-muted`.
- R4. Jadwal / schedule highlight areas use `accent-band`; attachment blocks may use `accent-band` or a tint of `accent-secondary` without clashing.
- R5. Primary CTA buttons (e.g. hero “Kunjungi Kami”) use `cta-bg` and `cta-text`.
- R6. Inline links in prose and cards use `link`; visited state may darken slightly but stays in the green family.
- R7. Cards stay white (`card-bg`) with existing shadow; no dark card backgrounds.
- R8. Footer uses `footer-bg` with `text-muted` copy.
- R9. Palette applies consistently on Beranda, Berita/Acara archives, and detail pages (v2 full-bleed layouts).
- R10. Contrast meets readable defaults on mobile — green header with white text; body text on cream/white passes casual readability check.

### Success Criteria

- A visitor perceives the site as calm, natural, and welcoming within the first screen (header + hero).
- Color is consistent across all six nav destinations and archive pages.
- No leftover v1 brown (`#5C4A3A`, `#E8D5C4` as primary brand) on shipped pages after implementation.

### Scope Boundaries

**In scope**

- SCSS/CSS color variable updates and dependent component tweaks (nav, bands, buttons, footer, cards, times-list).

**Deferred for later**

- Custom logo or hero photography color-grading.
- Dark mode.
- Pengurus section styling when that section is enabled.

**Outside scope**

- Layout or information architecture changes (covered by v2 layout plan).
- New fonts or icon sets.

### Outstanding Questions

**Deferred to Planning**

- Exact hover/focus hex values for nav and buttons (derive from `header-bg` / `cta-bg`).
- Whether hero CTA uses green (`cta-bg`) or gold (`accent-secondary`) for stronger contrast — default green per R5.

---

## Planning Contract

### Key Technical Decisions

- **Token remap in `assets/css/main.scss`:** Map Natura Garden hex values onto existing SCSS variables (`$color-header`, `$color-bg`, etc.) rather than introducing a second naming layer.
- **Heading color:** Reuse `$color-header` (forest green) for h1/h2 in bands and page headers.
- **Body links:** New `$color-link` (`#3A6B5C`); header/nav links stay white.
- **Attachments:** Light gold tint `#F2EBD4` derived from `accent-secondary` for PDF blocks.

### Implementation Units

### U1. Remap SCSS color tokens

**Goal:** Apply Natura Garden palette site-wide via SCSS variables.

**Requirements:** R1–R10

**Files:** `assets/css/main.scss`

**Verification:** Built CSS contains no `#5c4a3a` or `#e8d5c4` as primary brand colors.

### U2. Verify build output

**Goal:** Confirm Jekyll build succeeds and specs pass.

**Requirements:** R9, R10

**Files:** `spec/site_build_spec.rb` (run only)

**Verification:** `bundle exec jekyll build` and `bundle exec rspec` green.

---

## Verification Contract

- VC1. Header background is forest green in built HTML/CSS.
- VC2. Section bands alternate cream (`#F4F7F2`) and white.
- VC3. No v1 brown primary colors remain in `main.scss`.

## Definition of Done

- Natura Garden tokens applied in `version2` branch.
- Tests and build pass.
- PR opened against default branch.

---
