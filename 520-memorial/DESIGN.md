# 520 Memorial - Design System

## Color Strategy: Committed
One saturated color (coral) carries 30-40% of the surface through accents, borders, and interactive elements. Neutrals are tinted warm. No competing accent colors.

## Palette

### Primary
- **Coral**: `#ED6B86` — The heart of the brand. Used for interactive elements, the heartbeat icon, timeline dots, and key accents.
- **Coral Deep**: `#C44D6A` — Hover states, emphasis text.
- **Coral Soft**: `#F5A8B8` — Borders, subtle backgrounds, disabled states.

### Neutrals (tinted warm toward coral)
- **Background**: `#FDF6F3` — Warm cream, not white.
- **Background Warm**: `#FAEDE8` — Slightly deeper for section transitions.
- **Card Background**: `rgba(255,255,255,0.72)` — Frosted glass, not solid.
- **Text**: `#2C1A1E` — Deep warm brown, not black.
- **Text Light**: `#8B6F76` — Secondary text.
- **Text Muted**: `#B8A0A8` — Timestamps, hints.
- **Border**: `rgba(237,107,134,0.10)` — Invisible until you look for it.

### Surface Treatment
- No pure white (`#fff`) or pure black (`#000`).
- Background gradients are subtle: `linear-gradient(to bottom, var(--bg-warm), transparent)`.
- Hero glow: `radial-gradient(circle, rgba(237,107,134,0.12) 0%, transparent 70%)` — soft, diffuse, centered.

## Typography

### Font Stack
- **Display**: `'Playfair Display', 'Noto Serif SC', serif` — For names, section titles. Elegant, high contrast.
- **Body**: `'Noto Serif SC', 'PingFang SC', serif` — For all body text. Warm, readable.
- **Handwriting**: `'Ma Shan Zheng', cursive` — For subtitles, decorative labels, quotes. Used sparingly.

### Scale (ratio 1.25)
| Token | Size | Weight | Usage |
|-------|------|--------|-------|
| `text-hero` | `clamp(2.5rem, 6vw, 4.5rem)` | 700 | Names (TT & CC) |
| `text-section` | `clamp(1.8rem, 4vw, 2.8rem)` | 600 | Section titles |
| `text-quote` | `clamp(1.5rem, 4vw, 2.2rem)` | 400 | Footer quote |
| `text-body` | `0.9375rem` | 400 | Body text |
| `text-small` | `0.875rem` | 400 | Dates, metadata |
| `text-tiny` | `0.75rem` | 400 | Labels, timestamps |

### Rules
- No `letter-spacing` on Chinese text.
- Body line length capped at 65ch.
- Timer numbers use `font-variant-numeric: tabular-nums` to prevent layout shift.

## Spacing
- Section padding: `6rem 2rem` (desktop), `4rem 1rem` (mobile).
- Component gap: `1rem` base unit.
- Timeline items: `3rem` vertical spacing.
- Chat bubbles: `1rem` margin-bottom.

## Components

### Timer (Hero)
- No card container. Pure text on background.
- Numbers in coral-deep, units in muted.
- Separators are small dots (`·`), not colons.

### Timeline
- Central vertical line: 1px, gradient from transparent to coral-soft to transparent.
- Dots: 12px, coral fill, 3px white border, 4px glow shadow.
- Content cards: 45% width, alternating sides. Mobile: left-aligned with offset.

### Photo Grid
- CSS columns (masonry), not flex grid.
- 3 columns desktop, 2 tablet, 1 mobile.
- Images: `border-radius: 12px`, hover scale 1.05.
- Date overlay: gradient from bottom, white text.

### Chat Bubbles
- TT (left): white card, 1px border, sharp bottom-left corner.
- CC (right): coral-soft gradient, sharp bottom-right corner.
- Max-width: 75%.

### Music Player
- Fixed bottom-right, pill shape.
- Vinyl: conic-gradient dark vinyl with coral center label.
- Playing: smooth spin animation.

## Motion

### Principles
- Ease-out with exponential curves (`cubic-bezier(0.36, 0, 0.64, 1)`).
- No bounce, no elastic.
- Don't animate layout properties.

### Key Animations
| Animation | Duration | Easing | Trigger |
|-----------|----------|--------|---------|
| fadeInUp | 1s | ease-out | Page load (staggered 0.2s) |
| heartbeat | 1.2s | cubic-bezier | Infinite after load |
| sakuraFall | 10-18s | linear | Infinite |
| scrollReveal | 0.8s | ease-out | IntersectionObserver |
| photoHover | 0.5s | ease | Hover |

### Scroll Behavior
- `scroll-behavior: smooth` globally.
- Elements fade in + translateY(20px → 0) when entering viewport.
- Photo grid items stagger with 0.1s delay per item.

## Accessibility
- `prefers-reduced-motion`: disable all animations.
- All interactive elements minimum 44x44px touch target.
- `aria-hidden="true"` on decorative particles.
