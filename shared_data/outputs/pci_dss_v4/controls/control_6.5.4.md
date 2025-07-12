PCI DSS 4_0_1 Requirement Control 6.5.4

Defined Approach Requirements:
Roles and functions are separated between production and pre-production environments to provide accountability such that only reviewed and approved changes are deployed.

Customized Approach Objective:
Job roles and accountability that differentiate between pre-production and production activities are defined and managed to minimize the risk of unauthorized, unintentional, or inappropriate actions.

Applicability Notes:
In environments with limited personnel where individuals perform multiple roles or functions, this same goal can be achieved with additional procedural controls that provide accountability. For example, a developer may also be an administrator that uses an administrator-level account with elevated privileges in the development environment and, for their developer role, they use a separate account with user-level access to the production environment.

Testing Procedures:
Testing Procedure 6.5.4.a: Examine policies and procedures to verify that processes are defined for separating roles and functions to provide accountability such that only reviewed and approved changes are deployed.
Testing Procedure 6.5.4.b: Observe processes and interview personnel to verify implemented controls separate roles and functions and provide accountability such that only reviewed and approved changes are deployed.

Guidance:
Purpose: Use of live pans outside of protected cdes provides malicious individuals with the opportunity to gain unauthorized access to cardholder data. Definitions: Live pans refer to valid pans (not test pans) issued by, or on behalf of, a payment brand. additionally, when payment cards expire, the same pan is often reused with a different expiry date. all pans must be verified as being unable to conduct payment transactions or pose fraud risk to the payment system before they are excluded from pci dss scope. it is the responsibility of the entity to confirm that pans are not live.