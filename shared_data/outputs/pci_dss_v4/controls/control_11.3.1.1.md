PCI DSS 4_0_1 Requirement Control 11.3.1.1

Defined Approach Requirements:
All other applicable vulnerabilities (those not ranked as high-risk vulnerabilities or critical vulnerabilities according to the entity’s vulnerability risk rankings defined at Requirement 6.3.1) are managed as follows: Addressed based on the risk defined in the entity’s targeted risk analysis, which is performed according to all elements specified in Requirement 12.3.1. Rescans are conducted as needed.

Customized Approach Objective:
Lower ranked vulnerabilities (lower than high-risk or critical) are addressed at a frequency in accordance with the entity’s risk.

Applicability Notes:
The timeframe for addressing lower-risk vulnerabilities is subject to the results of a risk analysis per Requirement 12.3.1 that includes (minimally) identification of assets being protected, threats, and likelihood and/or impact of a threat being realized. _This requirement is a best practice until 31 March_ _2025, after which it will be required and must be_ _fully considered during a PCI DSS assessment._

Testing Procedures:
Testing Procedure 11.3.1.1.a: Examine the entity’s targeted risk analysis that defines the risk for addressing all other applicable vulnerabilities (those not ranked as high-risk vulnerabilities or critical vulnerabilities according to the entity’s vulnerability risk rankings at Requirement 6.3.1) to verify the risk analysis was performed in accordance with all elements specified at Requirement 12.3.1.
Testing Procedure 11.3.1.1.b: Interview responsible personnel and examine internal scan report results or other documentation to verify that all other applicable vulnerabilities (those not ranked as high-risk vulnerabilities or critical vulnerabilities according to the entity’s vulnerability risk rankings at Requirement 6.3.1) are addressed based on the risk defined in the entity’s targeted risk analysis, and that the scan process includes rescans as needed to confirm the vulnerabilities have been addressed.

Guidance:
Purpose: All vulnerabilities, regardless of criticality, provide a potential avenue of attack and must therefore be addressed periodically, with the vulnerabilities that expose the most risk addressed more quickly to limit the potential window of attack.