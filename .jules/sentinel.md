## 2026-10-05 - [Added Content Security Policy]
**Vulnerability:** Missing Content Security Policy (CSP) headers/meta tags in baseline HTML examples.
**Learning:** Even static baseline HTML files should model secure defaults to ensure agents/users copying them do not omit critical defense-in-depth protections against XSS.
**Prevention:** Include standard CSP rules (default-src 'self') in all boilerplate/example HTML files provided by the project.
