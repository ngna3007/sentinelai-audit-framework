PCI DSS 4_0_1 Requirement Control 10.7.2

Defined Approach Requirements:
Failures of critical security control systems are detected, alerted, and addressed promptly, including but not limited to failure of the following critical security control systems: Network security controls. IDS/IPS. Change-detection mechanisms. Anti-malware solutions. Physical access controls. Logical access controls. Audit logging mechanisms. Segmentation controls (if used). Audit log review mechanisms. Automated security testing tools (if used).

Customized Approach Objective:
Failures in critical security control systems are promptly identified and addressed.

Applicability Notes:
_This requirement applies to all entities, including_ _service providers, and will supersede Requirement_ _10.7.1 as of 31 March 2025. It includes two_ _additional critical security control systems not in_ _Requirement 10.7.1._ _This requirement is a best practice until 31 March_ _2025, after which it will be required and must be_ _fully considered during a PCI DSS assessment._

Testing Procedures:
Testing Procedure 10.7.2.a: Examine documentation to verify that processes are defined for the prompt detection and addressing of failures of critical security control systems, including but not limited to failure of all elements specified in this requirement.
Testing Procedure 10.7.2.b: Observe detection and alerting processes and interview personnel to verify that failures of critical security control systems are detected and reported, and that failure of a critical security control results in the generation of an alert.

Guidance:
Purpose: Without formal processes to detect and alert when critical security controls fail, failures may go undetected for extended periods and provide attackers ample time to compromise system components and steal account data from the cde. Good Practice: The specific types of failures may vary, depending on the function of the device system component and technology in use. however, typical failures include a system no longer performing its security function or not functioning in its intended manner—for example, a firewall erasing its rules or going offline.