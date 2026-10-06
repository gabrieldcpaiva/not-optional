## 2026-10-05 - Security Theater in Meta Tags
**Vulnerability:** Adding security headers as meta tags that browsers ignore.
**Learning:** `X-Content-Type-Options: nosniff` cannot be set via a `<meta http-equiv="...">` tag because modern browsers ignore it in this context. It must be set as an HTTP response header.
**Prevention:** Avoid adding "security theater" meta tags that provide no real benefit. Focus on actual HTTP headers for these directives, or valid meta tags like `Content-Security-Policy`.
