## 2026-10-05 - Security Theater in Meta Tags
**Vulnerability:** Adding security headers as meta tags that browsers ignore.
**Learning:** `X-Content-Type-Options: nosniff` cannot be set via a `<meta http-equiv="...">` tag because modern browsers ignore it in this context. It must be set as an HTTP response header.
**Prevention:** Avoid adding "security theater" meta tags that provide no real benefit. Focus on actual HTTP headers for these directives, or valid meta tags like `Content-Security-Policy`.

## 2026-10-06 - Weak and Duplicate CSPs in HTML baselines
**Vulnerability:** Having duplicate `<meta http-equiv="Content-Security-Policy">` tags where one is less restrictive, and omitting critical restrictions like `object-src 'none'` and `base-uri 'self'` in static baselines.
**Learning:** Duplicate CSP tags can lead to confusion or unintentional overrides. Modern CSPs should explicitly lock down plugins (`object-src 'none'`), form submissions (`form-action 'self'`), and base URLs (`base-uri 'self'`) even in simple static examples to establish a strong security baseline.
**Prevention:** Consolidate multiple CSP meta tags into a single, comprehensive declaration. Include `object-src 'none'`, `base-uri 'self'`, and `form-action 'self'` by default unless specifically required otherwise.

## 2026-10-10 - Potential XSS Vector using `innerHTML`
**Vulnerability:** Using `innerHTML` to dynamically update the DOM (even with hardcoded SVG strings) introduces a potential XSS vector if future code refactoring inadvertently introduces user input into those strings. It's flagged by static analysis tools and violates defense-in-depth principles.
**Learning:** Replacing `innerHTML` with native, secure DOM manipulation methods (like `document.createElementNS` for SVGs and `replaceChildren()`) completely eliminates the XSS attack surface while maintaining full functionality.
**Prevention:** Strictly forbid the use of `innerHTML` for DOM manipulation in all baseline examples. Enforce the use of secure DOM APIs (e.g., `document.createElement`, `replaceChildren`, `textContent`) as the standard pattern.

## 2026-10-14 - Broad Default GitHub Actions Permissions
**Vulnerability:** Relying on default `GITHUB_TOKEN` permissions in CI/CD workflows, which often default to permissive write access. This could allow a compromised dependency or malicious pull request to escalate privileges and alter repository contents or releases.
**Learning:** GitHub Actions workflows should not rely on default permissions. A missing `permissions` block means the token is granted broad access, violating the principle of least privilege.
**Prevention:** Explicitly define a `permissions` block (e.g., `permissions: contents: read`) in all GitHub Actions workflows to establish a secure default and ensure only explicitly necessary capabilities are granted.