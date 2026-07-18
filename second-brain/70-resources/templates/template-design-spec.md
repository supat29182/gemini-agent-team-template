---
date: YYYY-MM-DD
author: ux-ui
tags:
  - doc/design
  - phase/design
---

# 🎨 Design Specification: [Task/Feature Name]

- **Date:** YYYY-MM-DD
- **Feature Slug:** `<slug>`
- **Related Spec:** `[[system_spec]]` | `[[epics_user_stories]]`
- **Status:** Draft

---

## 1. Design Direction & Rationale

> Describe the overall visual direction, style, mood, and brand identity.
> Explain why this direction was chosen and how it aligns with the product goals.

---

## 2. User Flow Diagram

> Map out the key user journeys step-by-step. Use numbered steps or ASCII flow diagrams.
> Reference the user stories from `[[epics_user_stories]]`.

**Flow 1: [Flow Name]**

1. User lands on → [Screen A]
2. User clicks → [Action]
3. System responds → [Screen B]

---

## 3. Screen Wireframe Descriptions

> For each key screen, describe the layout structure, content placement, and hierarchy in text form.

### Screen: [Screen Name]

- **Layout**: [e.g., Single column / Two-column sidebar / Full-width hero]
- **Header**: [Description of header content and navigation]
- **Main Content**: [Description of primary content area, card layouts, lists, etc.]
- **Sidebar** (if applicable): [Description of sidebar content]
- **Footer**: [Description of footer content]
- **Responsive Behavior**: [How the layout adapts at mobile / tablet / desktop breakpoints]

---

## 4. Component Specifications

> List all reusable UI components, their variants, props, and states.

### Component: [Component Name]

| Property | Details |
| --- | --- |
| **Purpose** | [What this component does] |
| **Variants** | [e.g., primary, secondary, ghost, destructive] |
| **States** | [default, hover, active, focused, disabled, loading, error] |
| **Layout** | [flex / grid, alignment, sizing behavior] |
| **Content** | [What content goes inside: text, icon, badge, etc.] |

---

## 5. Design Tokens

### Colors

| Token | Value | Usage |
| --- | --- | --- |
| `--color-primary` | `#XXXXXX` | Primary actions, links |
| `--color-secondary` | `#XXXXXX` | Secondary actions |
| `--color-bg` | `#XXXXXX` | Page background |
| `--color-surface` | `#XXXXXX` | Card/panel backgrounds |
| `--color-text` | `#XXXXXX` | Body text |
| `--color-text-muted` | `#XXXXXX` | Secondary text |
| `--color-border` | `#XXXXXX` | Borders, dividers |
| `--color-success` | `#XXXXXX` | Success states |
| `--color-warning` | `#XXXXXX` | Warning states |
| `--color-error` | `#XXXXXX` | Error states |

### Typography

| Token | Value | Usage |
| --- | --- | --- |
| `--font-family` | [e.g., Inter, system-ui] | Base font |
| `--font-size-xs` | [e.g., 0.75rem] | Captions |
| `--font-size-sm` | [e.g., 0.875rem] | Small text |
| `--font-size-base` | [e.g., 1rem] | Body text |
| `--font-size-lg` | [e.g., 1.25rem] | Subheadings |
| `--font-size-xl` | [e.g., 1.5rem] | Section headings |
| `--font-size-2xl` | [e.g., 2rem] | Page headings |
| `--font-weight-normal` | [e.g., 400] | Body |
| `--font-weight-medium` | [e.g., 500] | Emphasis |
| `--font-weight-bold` | [e.g., 700] | Headings |

### Spacing

| Token | Value |
| --- | --- |
| `--space-1` | [e.g., 0.25rem] |
| `--space-2` | [e.g., 0.5rem] |
| `--space-3` | [e.g., 0.75rem] |
| `--space-4` | [e.g., 1rem] |
| `--space-6` | [e.g., 1.5rem] |
| `--space-8` | [e.g., 2rem] |
| `--space-12` | [e.g., 3rem] |
| `--space-16` | [e.g., 4rem] |

### Other Tokens

| Token | Value | Usage |
| --- | --- | --- |
| `--radius-sm` | [e.g., 4px] | Inputs, small elements |
| `--radius-md` | [e.g., 8px] | Cards, panels |
| `--radius-lg` | [e.g., 16px] | Modals, large containers |
| `--shadow-sm` | [value] | Subtle elevation |
| `--shadow-md` | [value] | Cards, dropdowns |
| `--shadow-lg` | [value] | Modals, overlays |
| `--transition-fast` | [e.g., 150ms ease] | Micro-interactions |
| `--transition-normal` | [e.g., 250ms ease] | State changes |

---

## 6. Responsive Breakpoints

| Breakpoint | Width | Layout Notes |
| --- | --- | --- |
| Mobile | < 640px | Single column, stacked elements |
| Tablet | 640px – 1024px | Adjusted grid, collapsible sidebar |
| Desktop | > 1024px | Full layout with sidebar |

---

## 7. Interaction & Animation Notes

> Describe micro-interactions, transitions, and motion guidelines.

| Element | Interaction | Animation |
| --- | --- | --- |
| [Button] | Hover | [e.g., Scale 1.02, background color shift, 150ms ease] |
| [Card] | Hover | [e.g., Subtle shadow lift, translateY -2px] |
| [Modal] | Open/Close | [e.g., Fade in + scale from 0.95, 250ms ease-out] |
| [Page transition] | Navigate | [e.g., Slide in from right, 300ms ease] |

---

## 8. Accessibility Considerations

- **Color Contrast**: All text meets WCAG AA minimum (4.5:1 for normal text, 3:1 for large text)
- **Focus Management**: All interactive elements have visible focus indicators
- **Keyboard Navigation**: All flows are completable via keyboard only
- **ARIA Labels**: Specify required ARIA attributes for custom components
- **Screen Reader**: Content order matches visual order
