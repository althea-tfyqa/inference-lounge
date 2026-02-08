# Inference Lounge — Settings Dialog Color Palette

## Design Principle
Cream stage, teal accents, dark inputs. The settings panel should feel like the calm backstage — let the main conversation UI carry the comic book energy.

## Palette

### Backgrounds
- **Dialog background:** `#FAF6EE` (warm cream)
- **Section cards/groups:** `#FFFFFF` with `1px solid #E8E0D4` border (subtle grouping)
- **Dialog title bar:** `#1A1A2E` (dark navy — replaces the red)

### Tab Bar
- **Tab bar background:** `#1A1A2E` (dark navy)
- **Active tab:** background `#FAF6EE`, text `#1A8A7D` (cream bg connects to panel below)
- **Inactive tabs:** text `#7A9A96` (muted gray-teal)

### Section Headers
- **Header text (CONVERSATION MODE, etc.):** `#1A8A7D` (muted teal — keep the energy, lose the scream)

### Input Fields
- **Background:** `#2D3748` (dark charcoal)
- **Text:** `#F0EDE8` (off-white)
- **Border:** `1px solid #3D8B84` (subtle teal)

### Toggle Buttons (Free / Paid / All)
- **Active:** `#22A394` (bright teal), text `#FFFFFF`
- **Inactive:** `#3A4556` (soft charcoal), text `#A0AEC0`

### Action Buttons
- **Save:** background `#22A394`, text `#FFFFFF`
- **Cancel:** background `#E8E0D4`, text `#4A5568`

### Body Text
- **Labels/descriptions:** `#6B7280` (warm gray)
- **Checkbox text:** `#4A5568` (slightly darker gray)

## Notes for Implementation
- Add ~16px padding around section groups to give headers breathing room
- Consider adding subtle `border-radius: 8px` to section cards
- Input fields should have ~8px padding inside for readability
- Keep the comic book fonts (Bangers for headers, Comic Neue for body) — the palette change alone will calm things down significantly
