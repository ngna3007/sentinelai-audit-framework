PCI DSS 4_0_1 Requirement Control 3.6.1.3

Defined Approach Requirements:
Access to cleartext cryptographic key components is restricted to the fewest number of custodians necessary.

Customized Approach Objective:
Access to cleartext cryptographic key components is restricted to necessary personnel.

Testing Procedures:
Testing Procedure 3.6.1.3: Examine user access lists to verify that access to cleartext cryptographic key components is restricted to the fewest number of custodians necessary.

Guidance:
Purpose: Restricting the number of people who have access to cleartext cryptographic key components reduces the risk of stored account data being retrieved or rendered visible by unauthorized parties. Good Practice: Only personnel with defined key custodian responsibilities (creating, altering, rotating, distributing, or otherwise maintaining encryption keys) should be granted access to key components. ideally this will be a very small number of people.