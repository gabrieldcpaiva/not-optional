## 2026-10-05 - Security Theater in Meta Tags
**Vulnerability:** Adding security headers as meta tags that browsers ignore.
**Learning:** `X-Content-Type-Options: nosniff` cannot be set via a `<meta http-equiv="...">` tag because modern browsers ignore it in this context. It must be set as an HTTP response header.
**Prevention:** Avoid adding "security theater" meta tags that provide no real benefit. Focus on actual HTTP headers for these directives, or valid meta tags like `Content-Security-Policy`.

## 2026-10-06 - Weak and Duplicate CSPs in HTML baselines
**Vulnerability:** Having duplicate `<meta http-equiv="Content-Security-Policy">` tags where one is less restrictive, and omitting critical restrictions like `object-src 'none'` and `base-uri 'self'` in static baselines.
**Learning:** Duplicate CSP tags can lead to confusion or unintentional overrides. Modern CSPs should explicitly lock down plugins (`object-src 'none'`), form submissions (`form-action 'self'`), and base URLs (`base-uri 'self'`) even in simple static examples to establish a strong security baseline.
**Prevention:** Consolidate multiple CSP meta tags into a single, comprehensive declaration. Include `object-src 'none'`, `base-uri 'self'`, and `form-action 'self'` by default unless specifically required otherwise.
