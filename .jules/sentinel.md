## 2026-10-05 - Security Theater in Meta Tags
**Vulnerability:** Adding security headers as meta tags that browsers ignore.
**Learning:** `X-Content-Type-Options: nosniff` cannot be set via a `<meta http-equiv="...">` tag because modern browsers ignore it in this context. It must be set as an HTTP response header.
**Prevention:** Avoid adding "security theater" meta tags that provide no real benefit. Focus on actual HTTP headers for these directives, or valid meta tags like `Content-Security-Policy`.

## 2026-10-06 - Fragmented Content Security Policies
**Vulnerability:** Having multiple or weak CSP meta tags.
**Learning:** Baseline HTML examples must include a single, comprehensive Content Security Policy (CSP) meta tag to model secure defaults and provide defense-in-depth against XSS. Modern CSPs should explicitly restrict plugins (`object-src 'none'`) and base URLs (`base-uri 'self'`) to establish a strong baseline.
**Prevention:** Ensure a unified, strictly configured CSP meta tag is used in all template/baseline HTML files.
