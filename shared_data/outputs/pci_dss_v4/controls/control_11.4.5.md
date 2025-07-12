PCI DSS 4_0_1 Requirement Control 11.4.5

Defined Approach Requirements:
If segmentation is used to isolate the CDE from other networks, penetration tests are performed on segmentation controls as follows: At least once every 12 months and after any changes to segmentation controls/methods Covering all segmentation controls/methods in use. According to the entity’s defined penetration testing methodology. Confirming that the segmentation controls/methods are operational and effective, and isolate the CDE from all out-of-scope systems. Confirming effectiveness of any use of isolation to separate systems with differing security levels (see Requirement 2.2.3). Performed by a qualified internal resource or qualified external third party. Organizational independence of the tester exists (not required to be a QSA or ASV).

Customized Approach Objective:
If segmentation is used, it is verified periodically by technical testing to be continually effective, including after any changes, in isolating the CDE from all out- of-scope systems.

Testing Procedures:
Testing Procedure 11.4.5.a: Examine segmentation controls and review penetration-testing methodology to verify that penetration-testing procedures are defined to test all segmentation methods in accordance with all elements specified in this requirement.
Testing Procedure 11.4.5.b: Examine the results from the most recent penetration test to verify the penetration test covers and addresses all elements specified in this requirement.
Testing Procedure 11.4.5.c: Interview personnel to verify that the test was performed by a qualified internal resource or qualified external third party and that organizational independence of the tester exists (not required to be a QSA or ASV).

Guidance:
Purpose: When an entity uses segmentation controls to isolate the cde from internal untrusted networks, the security of the cde is dependent on that segmentation functioning. many attacks have involved the attacker moving laterally from what an entity deemed an isolated network into the cde. using penetration testing tools and techniques to validate that an untrusted network is indeed isolated from the cde can alert the entity to a failure or misconfiguration of the segmentation controls, which can then be rectified. Good Practice: Techniques such as host discovery and port scanning can be used to verify out-of-scope segments have no access to the cde.