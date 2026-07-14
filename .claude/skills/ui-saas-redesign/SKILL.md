---
name: ui-saas-redesign
description: Repo-specific guide for redesigning the Vue 3 client from its top nav bar into a SaaS-style layout with a left sidebar, CSS design tokens, and a 4px/8px spacing scale. Use this skill when redesigning the app shell or navigation, introducing the sidebar layout, standardizing spacing, or restyling views in client/src.
---

# SaaS UI Redesign Guidelines

Guidelines for redesigning the Factory Inventory Management System's Vue 3 client from its current sticky top nav bar into a modern SaaS-style interface: a fixed left sidebar (light aesthetic, Linear/Notion style), CSS design tokens, and consistent spacing on a 4px/8px scale. The de facto design system lives in the unscoped `<style>` block of `client/src/App.vue` — every view depends on its global classes, so the shell rewrite happens there.

## Execution Model

This skill defines WHAT to build. The `vue-expert` subagent defines HOW to write Vue code.

- Per root CLAUDE.md, ANY creation or significant modification of a `.vue` file MUST be delegated to the `vue-expert` subagent.
- Subagents do not inherit this conversation. When delegating, paste the concrete specs from this skill (the design token block, the shell CSS, the relevant per-file step) directly into the agent prompt.
- If you ARE the vue-expert agent, apply this skill directly.
- Locale files (`client/src/locales/en.js`, `client/src/locales/ja.js`) are plain `.js` — edit them directly, no delegation needed.
- After the App.vue shell rewrite (the largest change), run the `code-reviewer` subagent.
- Per CLAUDE.md Code Style: always document non-obvious logic changes with comments.

## Target Layout

```
+----------------+---------------------------------------------+
| SIDEBAR (240px)| FilterBar (sticky, top: 0)                  |
|                +---------------------------------------------+
|  Logo          |                                             |
|  subtitle      |  .main-content                              |
|                |  (max-width 1600px, centered,               |
|  Overview      |   padding 24px 32px)                        |
|  Inventory     |                                             |
|  Orders        |    <router-view />                          |
|  Finance       |                                             |
|  Demand        |                                             |
|  Reports       |                                             |
|                |                                             |
|  ------------  |                                             |
|  LangSwitcher  |                                             |
|  ProfileMenu   |                                             |
+----------------+---------------------------------------------+
```

Anatomy:

- The sidebar is `position: fixed` (top/left/bottom 0), 240px wide, white surface, `border-right: 1px solid var(--color-border)`. Logo block at top, vertical nav below it, and a footer (LanguageSwitcher + ProfileMenu, separated by a top border) pinned to the bottom with `margin-top: auto`.
- The content column is NOT a flex sibling. It gets `margin-left: var(--sidebar-width)`.
- **The body remains the only scroll container.** Do not build a flex-row shell with an inner `overflow-y: auto` panel — that creates a nested scroll context which breaks `position: sticky` on FilterBar and complicates modal overlays. Fixed sidebar + content margin keeps document scrolling intact.
- `ProfileDetailsModal` and `TasksModal` stay mounted at the App root, toggled by ProfileMenu emits, unchanged.
- FilterBar remains the first element of the content column and becomes sticky at `top: 0`.

## Design Tokens (New Convention)

The codebase currently has **zero CSS variables** — every color is hardcoded hex, repeated across App.vue and view scoped styles. This redesign introduces design tokens as a new convention.

Rules:

1. Add this `:root` block at the very top of App.vue's global (unscoped) `<style>` section.
2. All NEW or MODIFIED CSS must use tokens instead of hex values or ad-hoc spacing.
3. Migrating untouched existing hex values is incremental — convert them when you touch a rule for other reasons. Do NOT do a big-bang rewrite of every view's styles.

Every value below is derived from the existing palette (verified against current App.vue styles):

```css
:root {
  /* Color - surfaces */
  --color-bg: #f8fafc;            /* page background (body) */
  --color-surface: #ffffff;       /* cards, sidebar, tables */
  --color-hover: #f1f5f9;         /* hover fills */

  /* Color - borders */
  --color-border: #e2e8f0;
  --color-border-strong: #cbd5e1; /* inputs, hovered cards */

  /* Color - text */
  --color-text: #0f172a;
  --color-text-secondary: #334155;
  --color-text-muted: #64748b;

  /* Color - brand/accent */
  --color-primary: #2563eb;
  --color-primary-soft: #eff6ff;  /* active nav tint */

  /* Color - status */
  --color-success: #059669;
  --color-warning: #ea580c;
  --color-danger: #dc2626;
  --color-info: #2563eb;

  /* Color - badge tints (existing badge pairs) */
  --tint-success-bg: #d1fae5;  --tint-success-text: #065f46;
  --tint-warning-bg: #fed7aa;  --tint-warning-text: #92400e;
  --tint-danger-bg: #fecaca;   --tint-danger-text: #991b1b;
  --tint-info-bg: #dbeafe;     --tint-info-text: #1e40af;

  /* Spacing - 4px/8px scale (rem, 16px base) */
  --space-1: 0.25rem;  /* 4px  */
  --space-2: 0.5rem;   /* 8px  */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-5: 1.5rem;   /* 24px */
  --space-6: 2rem;     /* 32px */
  --space-7: 3rem;     /* 48px */

  /* Layout */
  --sidebar-width: 240px;
  --sidebar-width-collapsed: 64px;

  /* Radius & shadow */
  --radius-sm: 6px;    /* buttons, badges, nav links */
  --radius-md: 10px;   /* cards, dropdowns */
  --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.06);
}
```

## App Shell Specification

### Template structure

Rebuild the App.vue template into this structure. The `<script>` block stays untouched — App.vue uses Options API with `setup()`; do NOT convert it to `<script setup>`. This is a template + CSS restructure only.

```html
<div class="app-shell">
  <aside class="sidebar">
    <div class="logo">
      <h1>{{ t('nav.companyName') }}</h1>
      <span class="subtitle">{{ t('nav.subtitle') }}</span>
    </div>
    <nav class="sidebar-nav">
      <router-link to="/" :class="{ active: $route.path === '/' }" :title="t('nav.overview')">
        <svg><!-- icon --></svg>
        <span class="nav-label">{{ t('nav.overview') }}</span>
      </router-link>
      <!-- ...same pattern for the other 5 links... -->
    </nav>
    <div class="sidebar-footer">
      <LanguageSwitcher />
      <ProfileMenu @show-profile-details="showProfileDetails = true" @show-tasks="showTasks = true" />
    </div>
  </aside>
  <div class="main-area">
    <FilterBar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
  <!-- modals stay here at the root, unchanged -->
</div>
```

Template rules:

- **Keep the six router-links' manual active bindings verbatim**: `:class="{ active: $route.path === '/inventory' }"` etc. Do not switch to `router-link-active` — the manual binding already handles exact matching for `/`. It is easy to drop a binding while restructuring; preserve all six.
- Replace the hardcoded `Reports` label with `{{ t('nav.reports') }}` (see Component Relocation Rules).
- Every nav link is `<svg> + <span class="nav-label">` — this structure is required for the responsive icon rail. Add a `:title` on each link for rail-mode tooltips/accessibility.
- The logo stacks vertically (h1 above subtitle); remove the subtitle's old `border-left` separator styling.

### Nav icons

Inline SVGs, 18px, `stroke: currentColor`, `fill: none`, stroke-width 2 — they inherit link color automatically. Icon choices:

| Route | Icon |
|---|---|
| `/` Overview | grid / home |
| `/inventory` | boxes / package |
| `/orders` | clipboard-list |
| `/spending` Finance | dollar-sign / bar-chart |
| `/demand` | trending-up |
| `/reports` | file-text |

Example (replicate this pattern for all six):

```html
<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
     fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="3" width="7" height="7"></rect>
  <rect x="14" y="3" width="7" height="7"></rect>
  <rect x="14" y="14" width="7" height="7"></rect>
  <rect x="3" y="14" width="7" height="7"></rect>
</svg>
```

No emojis anywhere — this is a business UI (CLAUDE.md rule).

### Shell CSS

Delete the old `.top-nav`, `.nav-container`, `.nav-tabs` rules — including `.nav-tabs a.active::after` (a bottom underline has no meaning on a vertical nav). The active state becomes background tint + text color + a 2px left inset indicator. New shell CSS (global block in App.vue):

```css
.app-shell { min-height: 100vh; }

.sidebar {
  position: fixed;
  top: 0; left: 0; bottom: 0;
  width: var(--sidebar-width);
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  padding: var(--space-4) var(--space-3);
  z-index: 100;
}

.logo h1 { font-size: 1.063rem; font-weight: 700; color: var(--color-text); }
.logo .subtitle { font-size: 0.75rem; color: var(--color-text-muted); }

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  margin-top: var(--space-5);
}

.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  color: var(--color-text-muted);
  font-weight: 500;
  font-size: 0.875rem;
  text-decoration: none;
  transition: all 0.15s ease;
}
.sidebar-nav a:hover { color: var(--color-text); background: var(--color-hover); }
.sidebar-nav a.active {
  color: var(--color-primary);
  background: var(--color-primary-soft);
  box-shadow: inset 2px 0 0 var(--color-primary); /* left indicator replaces the old bottom underline */
}

.sidebar-footer {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border);
}

.main-area {
  /* margin, not flex: keeps the body as the only scroll container */
  margin-left: var(--sidebar-width);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  max-width: 1600px;
  width: 100%;
  margin: 0 auto;
  padding: var(--space-5) var(--space-6);
}
```

## Component Relocation Rules

### 1. FilterBar sticky offset (client/src/components/FilterBar.vue)

The current `.filters-bar` rule is `position: sticky; top: 70px; z-index: 90` — the 70px encoded the height of the top nav that no longer exists.

```css
.filters-bar {
  position: sticky;
  top: 0; /* was 70px: matched the removed top nav's height; FilterBar is now the first sticky element */
  z-index: 90; /* below sidebar (100) */
}
```

Also align `.filters-container` horizontal padding with `.main-content` (`padding: 0 var(--space-6)`; keep `max-width: 1600px; margin: 0 auto`).

### 2. Dropdown re-anchoring (ProfileMenu.vue, LanguageSwitcher.vue)

Both components' dropdowns are absolutely positioned for a top-right anchor: `position: absolute; top: calc(100% + 0.5rem); right: 0; z-index: 1000` (ProfileMenu.vue ~line 171, LanguageSwitcher.vue ~line 136). At the sidebar bottom they would open downward, off-screen.

Re-anchor both to open upward from the trigger:

```css
.dropdown-menu {
  position: absolute;
  top: auto;                          /* was: calc(100% + 0.5rem) - opened downward under the top nav */
  bottom: calc(100% + var(--space-2)); /* opens upward: trigger now sits at the bottom of the sidebar */
  left: 0;                            /* was: right: 0 - anchored to the nav's right edge */
  right: auto;
  z-index: 1000;                      /* keep: must sit above the sidebar (100) */
}
```

Widen the trigger buttons to fill the sidebar width (`width: 100%`) so they don't look orphaned in the footer.

### 3. Reports label i18n (App.vue + locales)

"Reports" is the only hardcoded nav label (App.vue, `<router-link to="/reports">Reports</router-link>`); the other five use `t('nav.*')`.

- App.vue: `Reports` → `{{ t('nav.reports') }}`
- `client/src/locales/en.js`: add `reports: 'Reports'` to the `nav` block (after `demandForecast`)
- `client/src/locales/ja.js`: add `reports: 'レポート'` in the same position

**This is the ONLY permitted i18n change.** Do not rename or restructure existing keys.

## Spacing Standardization

1. All padding, margin, and gap values must land on the 4px scale via `--space-*` tokens.
2. Font sizes are exempt — existing values like `0.813rem`, `0.875rem`, `0.938rem` stay as they are.
3. Replace off-scale values when you touch a rule: e.g. `.badge` vertical padding `0.313rem` → `var(--space-1)`.
4. When a view's `<style scoped>` block conflicts with a global class from App.vue:
   - **Delete the scoped override** if it merely duplicates or slightly tweaks the global rule (the global, tokenized version wins).
   - **Keep and tokenize** only genuine layout variants — e.g. Dashboard.vue redefines `.page-header` as a flex row with actions; that is a real variant, keep it but convert its values to tokens.

## Responsive Behavior

Pure CSS, no JavaScript toggle state:

- **≥ 1024px**: full 240px sidebar with icon + label.
- **< 1024px**: 64px icon-only rail:

```css
@media (max-width: 1023px) {
  .sidebar { width: var(--sidebar-width-collapsed); padding: var(--space-4) var(--space-2); }
  .sidebar .nav-label,
  .sidebar .logo .subtitle { display: none; }
  .sidebar-nav a { justify-content: center; padding: var(--space-2); }
  .main-area { margin-left: var(--sidebar-width-collapsed); }
  /* logo h1 collapses to a compact mark - truncate or swap to initials */
}
```

- **< 768px**: keep the 64px rail. A hamburger/drawer pattern is explicitly REJECTED for this app — it adds JS state for negligible value on a desktop analytics dashboard. Do not "improve" this later.
- FilterBar: allow `flex-wrap: wrap` below 1024px so the four filters stack gracefully.
- The `:title` attributes on nav links (added in the shell template) provide hover tooltips in rail mode.
- In rail mode the footer dropdowns anchor `left: 0` and open upward — the re-anchoring rule above already produces correct behavior.

## Implementation Order

Execute file by file, one vue-expert delegation per step. Verify in the browser before moving to the next step.

1. **Baseline**: dev servers running (frontend :3000, backend :8001); take a Playwright screenshot of `/` for before/after comparison.
2. **`client/src/App.vue`** (vue-expert): add the `:root` token block; rebuild the template into the `.app-shell` structure (sidebar with logo, icon nav, footer with LanguageSwitcher/ProfileMenu; `.main-area` wrapping FilterBar + main); replace the shell CSS including responsive media queries; delete `.top-nav` / `.nav-container` / `.nav-tabs` / `.active::after` rules; swap hardcoded Reports for `t('nav.reports')`. Script block and modals untouched.
3. **`client/src/locales/en.js` + `ja.js`** (direct edit): add `nav.reports`.
4. **`client/src/components/FilterBar.vue`** (vue-expert): sticky offset `top: 0` + container padding alignment.
5. **`client/src/components/ProfileMenu.vue` + `LanguageSwitcher.vue`** (vue-expert): dropdown re-anchoring, full-width triggers.
6. **Per-view scoped-override audit** (vue-expert, one pass): check the known override sites — `Inventory.vue` (~lines 228–255: `.page-header`, `.card-header`, `.card-title`), `Dashboard.vue` (~line 730: `.page-header`), `Reports.vue` (~lines 324–336, 416: `.card`, `.card-header`, `.card-title`, `.stats-grid`), `Spending.vue` (~line 546: `.stats-grid-finance`). Remove duplicating overrides, tokenize kept variants, then run a spacing pass over remaining view styles.
7. **Verification**: run the full Playwright checklist below, then the `code-reviewer` subagent on the diff.

Comment every non-obvious change (CLAUDE.md Code Style rule) — especially deleted magic numbers, e.g. the FilterBar `top: 0` comment shown above.

## What NOT to Change

- Anything in `server/` — this is a pure frontend redesign.
- `client/src/api.js` request/response contracts.
- Business logic: `useFilters`, `useAuth`, `useI18n` internals; task CRUD logic in App.vue's script block.
- SVG chart internals in the views — restyle their card containers only.
- Router paths or route order in `client/src/main.js`.
- Existing i18n keys — the only addition is `nav.reports`.
- Do NOT add `Backlog.vue` to the nav. It exists in `views/` but has no route — that is intentional.
- Do NOT convert components between Options API / `setup()` / `<script setup>` styles.

## Edge Cases and Gotchas

- **Scoped overrides win over global changes.** Several views redefine App.vue's global classes in their `<style scoped>` blocks. If a global change "doesn't work" on one page, grep the views for the class name before concluding the change failed. Known sites are listed in Implementation Order step 6.
- **Magic offsets derived from the old 70px header.** FilterBar's `top: 70px` is the known one; grep for `70px` to catch any others before finishing.
- **Dropdowns render off-screen** at the sidebar bottom until re-anchored (Component Relocation Rules 2).
- **Active-state bindings are per-link and manual.** When restructuring links to add icons, it is easy to drop a `:class="{ active: ... }"` binding. All six must survive.
- **Japanese locale label widths.** Switch to JA and verify the sidebar: nav labels (e.g. 需要予測) fit 240px easily, but the company name 触媒コンポーネンツ is the longest string — confirm the logo block doesn't wrap badly.
- **Z-index ladder**: sidebar 100, FilterBar 90, dropdowns 1000, modal overlays above everything. Preserve this ordering; check the modals' overlay z-index values when verifying.

## Verification with Playwright

Use `mcp__playwright__*` tools against `http://localhost:3000`:

1. Visit all 6 routes (`/`, `/inventory`, `/orders`, `/spending`, `/demand`, `/reports`): sidebar visible, exactly one link has `.active` and it is the correct one, no horizontal scrollbar.
2. Scroll a long view (Orders): FilterBar sticks at the top of the content column; content never slides under the sidebar.
3. Open the LanguageSwitcher and ProfileMenu dropdowns: both fully visible, opening upward above their triggers.
4. From ProfileMenu, open both ProfileDetailsModal and TasksModal: overlays cover the sidebar too.
5. Switch to Japanese: all sidebar labels and the company name fit without ugly wrapping.
6. Resize viewport to 900px and 700px: icon rail renders, labels hidden, content margin follows, nav still works via icons.
7. Change and reset filters: filtering still updates every view (redesign must not touch filter logic).

## Best Practices

1. Use design tokens for every new or modified CSS value — no new hardcoded hex or off-scale spacing.
2. Keep all spacing on the 4px/8px grid via `--space-*`.
3. Delegate every `.vue` edit to vue-expert with the relevant spec pasted into the prompt.
4. Change one file (one step) at a time and verify in the browser before continuing.
5. Comment non-obvious changes, especially replaced magic numbers.
6. Check for scoped overrides before editing a global class.
7. Keep the body as the only scroll container — never introduce nested scroll panels.
8. No emojis in the UI; icons are inline SVG with `currentColor`.

## Key Reminders

- The body scrolls; the sidebar is `fixed` and the content column uses `margin-left` — never a flex row with inner overflow.
- FilterBar sticks at `top: 0` now, not `top: 70px`.
- Sidebar-footer dropdowns open upward (`bottom: calc(100% + var(--space-2)); left: 0`).
- `nav.reports` is the only i18n addition permitted.
- All six manual `:class="{ active: $route.path === '...' }"` bindings must survive the template rewrite.
- Never touch `server/`, `api.js` contracts, or chart internals.
- vue-expert writes the `.vue` code; this skill supplies the specs.
