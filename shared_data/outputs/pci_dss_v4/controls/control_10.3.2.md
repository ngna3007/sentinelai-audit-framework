PCI DSS 4_0_1 Requirement Control 10.3.2

Defined Approach Requirements:
Audit log files are protected to prevent modifications by individuals.

Customized Approach Objective:
Stored activity records cannot be modified by personnel.

Testing Procedures:
Testing Procedure 10.3.2: Examine system configurations and privileges and interview system administrators to verify that current audit log files are protected from modifications by individuals via access control mechanisms, physical segregation, and/or network segregation.

Guidance:
Purpose: Promptly backing up the logs to a centralized log server or media that is difficult to alter keeps the logs protected, even if the system generating the logs becomes compromised. writing logs from external-facing technologies such as wireless, network security controls, dns, and mail servers, reduces the risk of those logs being lost or altered. Good Practice: Each entity determines the best way to back up log files, whether via one or more centralized log servers or other secure media. logs may be written directly, offloaded, or copied from external systems to the secure internal system or media.