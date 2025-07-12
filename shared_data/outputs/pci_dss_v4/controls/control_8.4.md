PCI DSS 4_0_1 Requirement Control 8.4

Defined Approach Requirements:
Multi-factor authentication (MFA) is implemented to secure access into the CDE.

Guidance:
Purpose: Requiring more than one type of authentication factor reduces the probability that an attacker can gain access to a system by masquerading as a legitimate user, because the attacker would need to compromise multiple authentication factors. this is especially true in environments where traditionally the single authentication factor employed was something a user knows such as a password or passphrase. Good Practice: Implementing mfa for non-console administrative access to in-scope system components that are not part of the cde will help prevent unauthorized users from using a single factor to gain access and compromise in-scope system components. Definitions: Using one factor twice (for example, using two separate passwords) is not considered multi- factor authentication.