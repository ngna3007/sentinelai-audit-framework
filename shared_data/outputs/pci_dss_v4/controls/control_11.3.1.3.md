PCI DSS 4_0_1 Requirement Control 11.3.1.3

Defined Approach Requirements:
Internal vulnerability scans are performed after any significant change as follows: Vulnerabilities that are either high-risk or critical (according to the entity’s vulnerability risk rankings defined at Requirement 6.3.1) are resolved. Rescans are conducted as needed. Scans are performed by qualified personnel and organizational independence of the tester exists (not required to be a QSA or ASV).

Customized Approach Objective:
The security posture of all system components is verified following significant changes to the network or systems, by using automated tools designed to detect vulnerabilities operating inside the network. Detected vulnerabilities are assessed and rectified based on a formal risk assessment framework.

Applicability Notes:
Authenticated internal vulnerability scanning per Requirement 11.3.1.2 is not required for scans performed after significant changes.

Testing Procedures:
Testing Procedure 11.3.1.3.a: Examine change control documentation and internal scan reports to verify that system components were scanned after any significant changes.
Testing Procedure 11.3.1.3.b: Interview personnel and examine internal scan and rescan reports to verify that internal scans were performed after significant changes and that all high-risk vulnerabilities and all critical vulnerabilities (defined in PCI DSS Requirement 6.3.1) were resolved.
Testing Procedure 11.3.1.3.c: Interview personnel to verify that internal scans are performed by a qualified internal resource(s) or qualified external third party and that organizational independence of the tester exists.

Guidance:
Purpose: Scanning an environment after any significant changes ensures that changes were completed appropriately such that the security of the environment was not compromised because of the change. Good Practice: Entities should perform scans after significant changes as part of the change process per requirement 6.5.2 and before considering the change complete. all system components affected by the change will need to be scanned.