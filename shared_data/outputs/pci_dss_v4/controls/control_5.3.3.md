PCI DSS 4_0_1 Requirement Control 5.3.3

Defined Approach Requirements:
For removable electronic media, the anti- malware solution(s): Performs automatic scans of when the media is inserted, connected, or logically mounted, OR Performs continuous behavioral analysis of systems or processes when the media is inserted, connected, or logically mounted.

Customized Approach Objective:
Malware cannot be introduced to system components via external removable media.

Applicability Notes:
_This requirement is a best practice until 31 March_ _2025, after which it will be required and must be_ _fully considered during a PCI DSS assessment._

Testing Procedures:
Testing Procedure 5.3.3.a: Examine anti-malware solution(**s)** configurations to verify that, for removable electronic media, the solution is configured to perform at least one of the elements specified in this requirement.
Testing Procedure 5.3.3.b: Examine system components with removable electronic media connected to verify that the solution(s) is enabled in accordance with at least one of the elements as specified in this requirement.
Testing Procedure 5.3.3.c: Examine logs and scan results to verify that the solution(s) is enabled in accordance with at least one of the elements specified in this requirement.

Guidance:
Purpose: Portable media devices are often overlooked as an entry method for malware. attackers will often pre- load malware onto portable devices such as usb and flash drives; connecting an infected device to a computer then triggers the malware, introducing new threats within the environment.