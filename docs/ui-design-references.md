# UI/UX Design Reference Index

Status: **Canonical design-reference index**
Last updated: 2026-09-01

Purpose: reusable UI/UX reference sources for XAI-Studio, the tablet review/generation interface, and the future unified AI portal.

This file is intentionally reference-oriented. It does not define the final visual language by itself. Codex/Claude should use it together with project-specific `DESIGN.md`, component rules, and actual user-flow requirements.

## Priority references

### 1. Refero Styles
- URL: https://styles.refero.design/
- Role: AI-readable design-system references and DESIGN.md-style context.
- Best use:
  - establish visual-system direction before implementation
  - inspect color, typography, spacing, and component patterns
  - generate structured design context for Codex / Claude Code / Cursor
- Priority: **highest**
- Notes: Prefer extracting principles and system rules rather than copying a product literally.

### 2. Mobbin
- URL: https://mobbin.com/
- Role: real mobile-product screens and user flows.
- Best use:
  - tablet/mobile interaction patterns
  - gallery/review flows
  - navigation and state transitions
  - selection, compare, favorite/reject, detail panels
- Priority: **high**

### 3. Component Gallery
- URL: https://component.gallery/
- Role: cross-design-system component reference.
- Best use:
  - compare implementations of buttons, popovers, tabs, drawers, trees, badges, forms, etc.
  - select a known component pattern before inventing a new one
- Priority: **high**

### 4. 60fps.design
- URL: https://60fps.design/
- Role: motion and micro-interaction reference.
- Best use:
  - gallery transitions
  - card stack behavior
  - drag/drop
  - loading states
  - sliders
  - player controls
  - subtle feedback motion
- Priority: **high**

## Portal / SaaS references

### 5. Saaspo
- URL: https://saaspo.com/
- Role: SaaS product website and application reference.
- Best use:
  - future AI portal landing page
  - dashboard information architecture
  - product/pricing/onboarding patterns
- Priority: medium-high

### 6. Landing Love
- URL: https://landing.love/
- Role: landing-page visual and motion inspiration.
- Best use:
  - future portal landing page
  - hero sections
  - marketing/product storytelling
- Priority: medium

### 7. Curations Supply
- URL: https://curations.supply/
- Role: broad design curation.
- Best use:
  - aesthetic exploration
  - visual direction discovery
- Priority: medium

## Branding / typography / icon references

### 8. Rebrand Gallery
- URL: https://rebrand.gallery/
- Role: brand-system and identity reference.
- Best use:
  - future XAI-Studio / AI portal brand language
  - logo, typography, visual identity systems
- Priority: medium

### 9. Uncut
- URL: https://uncut.wtf/
- Role: typography reference.
- Best use:
  - font exploration
  - editorial / interface typography ideas
- Priority: medium

### 10. Hugeicons
- URL: https://hugeicons.com/
- Role: icon library / icon-system reference.
- Best use:
  - consistent iconography in production UI
  - avoid mixing unrelated icon sets
- Priority: medium-high

## Experimental / AI-assisted app design

### 11. Sleek.design
- URL: https://sleek.design/
- Role: AI-assisted mobile app creation / exploration.
- Best use:
  - rapid visual experiments
  - alternative layout ideation
- Priority: experimental

## Recommended design workflow

Use these sources in a fixed order rather than browsing randomly:

```text
1. Refero Styles
   -> choose / extract design-system direction
   -> write or update project DESIGN.md

2. Mobbin
   -> verify real-world user flow and interaction patterns

3. Component Gallery
   -> choose known component patterns

4. 60fps.design
   -> add motion only where it improves comprehension / feedback

5. Saaspo + Landing Love
   -> use mainly for the future unified AI portal / public landing pages

6. Rebrand / Uncut / Hugeicons
   -> refine brand, typography, and icon consistency
```

## XAI-Studio-specific guidance

For the tablet image/video studio, prioritize function over decorative styling.

High-value flows to research:
- prompt entry
- generation queue
- image/video grid
- 2-4 item compare
- favorite / reject
- metadata on demand
- prompt / model / seed inspection
- regenerate
- character collection
- reference-pack management
- review comments
- provenance / lineage
- tablet landscape ergonomics

Recommended principle:

> Use real product references for user flow, design-system references for consistency, and motion references only for interaction clarity.

Avoid:
- decorative dashboard complexity
- excessive card nesting
- unnecessary modal chains
- animation that slows review
- consumer-photo-app patterns that hide generation metadata
- copying a reference product literally

## Suggested project structure

```text
design/
├── DESIGN.md
├── references/
│   └── ui-design-references.md
├── decisions/
│   ├── gallery.md
│   ├── image-review.md
│   ├── prompt-panel.md
│   └── character-library.md
└── motion/
    └── interaction-rules.md
```

## Codex / Claude usage rule

Before implementing a substantial new UI flow:

1. Read the project's `DESIGN.md`.
2. Check this reference index.
3. Identify 1-3 relevant real-world patterns.
4. Implement the smallest coherent pattern that fits XAI-Studio.
5. Record durable decisions in `design/decisions/`.
6. Do not add a new abstraction or design pattern when an existing project pattern already fits.

