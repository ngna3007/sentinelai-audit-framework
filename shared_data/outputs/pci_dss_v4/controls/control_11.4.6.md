PCI DSS 4_0_1 Requirement Control 11.4.6

Defined Approach Requirements:
Additional requirement for service_ _providers only:_ If segmentation is used to isolate the CDE from other networks, penetration tests are performed on segmentation controls as follows: At least once every six months and after any changes to segmentation controls/methods. Covering all segmentation controls/methods in use. According to the entity’s defined penetration testing methodology. Confirming that the segmentation controls/methods are operational and effective, and isolate the CDE from all out-of-scope systems. Confirming effectiveness of any use of isolation to separate systems with differing security levels (see Requirement 2.2.3). Performed by a qualified internal resource or qualified external third party. Organizational independence of the tester exists (not required to be a QSA or ASV).

Customized Approach Objective:
If segmentation is used, it is verified by technical testing to be continually effective, including after any changes, in isolating the CDE from out-of-scope systems.

Applicability Notes:
This requirement applies only when the entity being assessed is a service provider.

Testing Procedures:
Testing Procedure 11.4.6.a: **_Additional testing procedure for_** **_service provider assessments only:_
Testing Procedure 11.4.6.b: **_Additional testing procedure for_** **_service provider assessments only:_

Guidance:
Purpose: Service providers typically have access to greater volumes of cardholder data or can provide an entry point that can be exploited to then compromise multiple other entities. service providers also typically have larger and more complex networks that are subject to more frequent change. the probability of segmentation controls failing in complex and dynamic networks is greater in service-provider environments. validating segmentation controls more frequently is likely to discover such failings before they can be exploited by an attacker attempting to pivot laterally from an out-of-scope untrusted network to the cde. Good Practice: Although the requirement specifies that this scope validation is carried out at least once every six months and after significant change, this exercise should be performed as frequently as possible to ensure it remains effective at isolating the cde from other networks.