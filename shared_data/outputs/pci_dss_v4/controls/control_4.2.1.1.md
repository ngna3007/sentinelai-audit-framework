PCI DSS 4_0_1 Requirement Control 4.2.1.1

Defined Approach Requirements:
An inventory of the entity’s trusted keys and certificates used to protect PAN during transmission is maintained.

Customized Approach Objective:
All keys and certificates used to protect PAN during transmission are identified and confirmed as trusted.

Applicability Notes:
_This requirement is a best practice until 31 March_ _2025, after which it will be required and must be_ _fully considered during a PCI DSS assessment._

Testing Procedures:
Testing Procedure 4.2.1.1.a: Examine documented policies and procedures to verify processes are defined for the entity to maintain an inventory of its trusted keys and certificates.
Testing Procedure 4.2.1.1.b: Examine the inventory of trusted keys and certificates to verify it is kept up to date.

Guidance:
Purpose: The inventory of trusted keys helps the entity keep track of the algorithms, protocols, key strength, key custodians, and key expiry dates. this enables the entity to respond quickly to vulnerabilities discovered in encryption software, certificates, and cryptographic algorithms. Good Practice: For certificates, the inventory should include the issuing ca and certification expiration date.