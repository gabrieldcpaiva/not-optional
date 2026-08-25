# Dual-Layer Color Tokens

Accessibility requires two different color systems depending on the medium.

## Screen (Comfort Mode)
Low-saturation, sensory-friendly palette intended for prolonged viewing:
- Sage `#7A8F7A`
- Sand `#E8D9C8`
- Paper `#F7F3EE`
- Deep Moss `#4A5D4E` (for focus and structure)

## Print (High-Contrast / Low-Ink Mode)
Higher contrast values that remain legible on cheap home inkjet printers and survive ink washout. Target contrast ratios of 7:1 or higher for body text.

## Implementation
Maintain two separate token maps (`tokens.screen` and `tokens.print`). Never force the screen comfort palette onto print, and never force high-contrast print values onto a calm screen interface.
