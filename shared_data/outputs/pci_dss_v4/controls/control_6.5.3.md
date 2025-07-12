PCI DSS 4_0_1 Requirement Control 6.5.3

Defined Approach Requirements:
Pre-production environments are separated from production environments and the separation is enforced with access controls.

Customized Approach Objective:
Pre-production environments cannot introduce risks and vulnerabilities into production environments.

Testing Procedures:
Testing Procedure 6.5.3.a: Examine policies and procedures to verify that processes are defined for separating the pre- production environment from the production environment via access controls that enforce the separation.
Testing Procedure 6.5.3.b: Examine network documentation and configurations of network security controls to verify that the pre-production environment is separate from the production environment(s).
Testing Procedure 6.5.3.c: Examine access control settings to verify that access controls are in place to enforce separation between the pre-production and production environment(s).

Guidance:
Purpose: Due to the constantly changing state of pre- production environments, they are often less secure than the production environment. Good Practice: Organizations must clearly understand which environments are test environments or development environments and how these environments interact on the level of networks and applications. Definitions: Pre-production environments include development, testing, user acceptance testing (uat), etc. even where production infrastructure is used to facilitate testing or development, production environments still need to be separated (logically or physically) from pre-production functionality such that vulnerabilities introduced as a result of pre-production activities do not adversely affect production systems.