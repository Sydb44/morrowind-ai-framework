# Security Policy

## Supported Versions

Currently supported versions of the Morrowind AI Framework:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Morrowind AI Framework seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Reporting Process

1. **Do Not** report security vulnerabilities through public GitHub issues.

2. Instead, please report them via email to [INSERT SECURITY EMAIL].

3. Include the following information in your report:
   - Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
   - Full paths of source file(s) related to the manifestation of the issue
   - The location of the affected source code (tag/branch/commit or direct URL)
   - Any special configuration required to reproduce the issue
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if possible)
   - Impact of the issue, including how an attacker might exploit it

### Response Process

1. You will receive an acknowledgment within 48 hours.
2. We will confirm the issue and determine its severity.
3. We will work on a fix and release timeline.
4. We will keep you informed of the progress.

## Security Best Practices

### API Keys and Secrets

- Never commit API keys, passwords, or other secrets to the repository
- Use environment variables for sensitive configuration
- Follow the provided `.env.example` template
- Regularly rotate API keys and access tokens

### Server Security

- Keep Python and all dependencies up to date
- Use HTTPS for all API communications
- Implement rate limiting for API endpoints
- Validate and sanitize all input data
- Monitor server logs for suspicious activity

### Client Security

- Validate all server responses
- Sanitize user input
- Use secure WebSocket connections
- Implement proper error handling
- Keep OpenMW and dependencies updated

## Known Security Risks

1. **API Key Exposure**
   - Risk: Exposure of LLM provider API keys
   - Mitigation: Use environment variables and secure key management

2. **Memory Content**
   - Risk: Sensitive information in NPC memories
   - Mitigation: Sanitize and filter memory content

3. **WebSocket Security**
   - Risk: Unauthorized WebSocket connections
   - Mitigation: Implement authentication and encryption

## Security Updates

Security updates will be released as soon as possible after a vulnerability is confirmed. Updates will be distributed through:

1. GitHub releases
2. Security advisories
3. Project documentation updates

## Secure Development

When contributing to the project:

1. Follow secure coding practices
2. Review code for security issues
3. Keep dependencies updated
4. Use static analysis tools
5. Write security-focused tests

## Compliance

The project aims to comply with:

- OWASP Security Guidelines
- Common security best practices
- Data protection regulations where applicable

## Contact

For security-related questions or concerns, please contact:
- Security Team: [INSERT SECURITY EMAIL]
- Project Lead: [INSERT LEAD EMAIL]

## Attribution

We appreciate the responsible disclosure of security issues and will acknowledge security researchers in our security advisories (unless they wish to remain anonymous).
