# Contrast

## Physiological rule

Do not set body text to `#000000` on `#FFFFFF`. That pair is high ratio and still harmful: it produces visual vibration and text freezing for many dyslexic and fatigued readers.

Use off-black text on off-white canvas on screens. Example only: `#2C2A28` on `#F7F3EE` (12.9:1).

## Screen (WCAG 2.1 AA)

- Normal text ≥ 4.5:1
- Large text and UI components ≥ 3:1

## Print (physical)

CSS luminance is not ink. Target ≥7:1 for printed body text on cheap inkjets. Keep body as dark ink (example `#2C2A28`), not pure black on pure white. Strokes may use a full dark channel.
