PCI DSS 4_0_1 Requirement Control 8.4.3

Defined Approach Requirements:
MFA is implemented for all remote access originating from outside the entity’s network that could access or impact the CDE.

Customized Approach Objective:
Remote access to the entity’s network cannot be obtained by using a single authentication factor.

Testing Procedures:
Testing Procedure 8.4.3.a: Examine network and/or system configurations for remote access servers and systems to verify MFA is required in accordance with all elements specified in this requirement.
Testing Procedure 8.4.3.b: Observe personnel (for example, users and administrators) and third parties connecting remotely to the network and verify that multi-factor authentication is required.

Guidance:
Purpose: Requiring more than one type of authentication factor reduces the probability that an attacker can gain access to a system by masquerading as a legitimate user, because the attacker would need to compromise multiple authentication factors. this is especially true in environments where traditionally the single authentication factor employed was something a user knows, such as a password or passphrase. Definitions: Multi-factor authentication (mfa) requires an individual to present a minimum of two of the three authentication factors specified in requirement 8.3.1 before access is granted. using one factor twice (for example, using two separate passwords) is not considered multi- factor authentication. _(continued on next page)_.