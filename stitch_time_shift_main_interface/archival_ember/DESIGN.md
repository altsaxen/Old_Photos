# Design System Specification: The Digital Archivist

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Digital Archivist."** 

This system moves away from the cold, clinical nature of modern SaaS and instead embraces the tactile, emotive qualities of a high-end editorial gallery. It is designed to feel like a private viewing room in a world-class museum—hushed, intentional, and deeply respectful of the history it restores. 

To break the "template" look, we reject the rigid grid in favor of **intentional asymmetry**. Layouts should utilize overlapping elements (e.g., a photo slightly bleeding over a container edge) and a high-contrast typography scale to create a sense of curated storytelling. The goal is "Archival Premium": a blend of historical warmth and cutting-edge precision.

---

## 2. Colors
Our palette is a sophisticated "Soft Dark" mode. We avoid pure blacks to maintain a sense of organic depth, using charcoal and sepia-toned neutrals.

### The "No-Line" Rule
**Explicit Instruction:** Do not use 1px solid borders to define sections. Boundaries must be defined solely through background color shifts. For example, a `surface-container-low` section should sit directly on a `surface` background. The transition of tone is the divider.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers—like stacked sheets of heavy vellum.
*   **Base:** `surface` (#131313)
*   **Nesting:** Place a `surface-container-low` (#1c1b1b) card within a `surface` section. If an element needs further prominence inside that card, use `surface-container-high` (#2a2a2a). This creates "nested depth" without visual clutter.

### The "Glass & Gradient" Rule
To elevate the experience, use **Glassmorphism** for floating elements (like photo adjustment panels). Use `surface-variant` at 60% opacity with a `24px` backdrop blur.
*   **Signature Textures:** Apply subtle radial gradients to hero backgrounds, transitioning from `primary` (#f2be8c) at 5% opacity to `surface` at the edges to provide a soft "inner glow" that mimics a darkroom lamp.

---

## 3. Typography
The typography system pairs the intellectual weight of a serif with the functional clarity of a sans-serif.

*   **Display & Headlines (Noto Serif):** Used for storytelling and impact. The serif should feel "inked" and authoritative. Large-scale displays (`display-lg`) should use tighter letter-spacing (-2%) to feel like a premium masthead.
*   **Body & Labels (Inter):** Used for all functional data and tool labels. It provides the "scientific" counterweight to the "artistic" serif.
*   **Hierarchy as Identity:** Use `headline-md` for photo titles and `label-sm` in `primary` color for metadata (e.g., "RESTORED 1924"). This juxtaposition conveys the brand's dual nature: historical heart, digital brain.

---

## 4. Elevation & Depth
We convey hierarchy through **Tonal Layering** rather than structural lines.

*   **The Layering Principle:** Stack `surface-container` tiers. A `surface-container-lowest` (#0e0e0e) card on a `surface-container-low` (#1c1b1b) section creates a natural "well" effect, perfect for the main photo workspace.
*   **Ambient Shadows:** Floating modals must use "Ambient Shadows"—extra-diffused with a `48px` blur and 6% opacity. Use a tinted shadow color based on `on-surface` (#e5e2e1) to mimic natural light scattering.
*   **The Ghost Border:** If a boundary is required for accessibility, use a "Ghost Border": `outline-variant` at **15% opacity**. 100% opaque borders are strictly forbidden.

---

## 5. Components

### Buttons: The "Amber Glow"
*   **Primary:** Background `primary` (#f2be8c), text `on-primary` (#482904). Apply a `0 0 15px` outer glow using `primary` at 30% opacity during hover states to simulate a lightbox turning on.
*   **Secondary:** Background `surface-container-highest`, text `primary`. No border.
*   **Tertiary:** Text `primary`, no background. Use for low-emphasis actions like "Cancel."

### The "Archival" Upload Zone
*   **Visuals:** A large area using `surface-container-low` with a dashed "Ghost Border" (15% opacity `outline-variant`). 
*   **Interaction:** On drag-over, the background shifts to `primary-container` (#d4a373) at 10% opacity with a soft `primary` inner glow.

### The Comparison Slider
*   **Handle:** A vertical line using `primary-fixed` (#ffdcbd) with a circular node. The node should have a `surface-container-highest` fill and a `primary` 1px ghost border. 
*   **Labels:** "Before" and "After" should use `label-sm` typography, pinned to the top corners of the image container.

### Cards & Lists
*   **No Dividers:** Separate list items using `spacing-4` (1.4rem) of vertical white space or a subtle background shift to `surface-container-low` on hover.
*   **Corners:** Use `md` (0.75rem) roundedness for large containers and `sm` (0.25rem) for smaller UI elements like chips.

### Contextual Tool: The "Loupe"
A custom component for this system—a floating circular magnifier that appears when hovering over grain. It uses the Glassmorphism rule (60% opacity `surface` + blur) with a `primary` 1px ghost border.

---

## 6. Do's and Don'ts

### Do:
*   **Do** use asymmetrical margins. If a heading is left-aligned, consider right-aligning the subtext to create an editorial "path for the eye."
*   **Do** use the `primary-container` (#d4a373) for subtle highlights in icons or active states.
*   **Do** prioritize "negative space." If in doubt, increase the spacing by one tier (e.g., shift from `spacing-6` to `spacing-8`).

### Don't:
*   **Don't** use 100% white (#ffffff). It breaks the "Soft Dark" immersion. Use `on-surface` (#e5e2e1) for maximum brightness.
*   **Don't** use standard "drop shadows" (Black, 25% opacity, 4px blur). They feel "default" and cheap.
*   **Don't** use dividers. If the layout feels messy, adjust the `surface-container` tones or increase the spacing scale rather than adding a line.