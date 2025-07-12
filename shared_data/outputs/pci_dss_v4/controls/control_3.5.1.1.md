PCI DSS 4_0_1 Requirement Control 3.5.1.1

Defined Approach Requirements:
Hashes used to render PAN unreadable (per the first bullet of Requirement 3.5.1) are keyed cryptographic hashes of the entire PAN, with associated key- management processes and procedures in accordance with Requirements 3.6 and 3.7.

Customized Approach Objective:
**3.5.1.1.b**Examine documentation about the key management procedures and processes associated with the keyed cryptographic hashes to verify keys are managed in accordance with Requirements 3.6 and 3.7.

Applicability Notes:
**Purpose** Disk-level and partition-level encryption typically encrypts the entire disk or partition using the same key, with all data automatically decrypted when the system runs or when an authorized user requests it. For this reason, disk-level encryption is not appropriate to protect stored PAN on computers, laptops, servers, storage arrays, or any other system that provides transparent decryption upon user authentication. **Further Information** Where available, following vendors’ hardening and industry best practice guidelines can assist in securing PAN on these devices.

Testing Procedures:
Testing Procedure 3.5.1.1.b: Examine documentation about the key management procedures and processes associated with the keyed cryptographic hashes to verify keys are managed in accordance with Requirements 3.6 and 3.7.
Testing Procedure 3.5.1.1.c: Examine data repositories to verify the PAN is rendered unreadable.
Testing Procedure 3.5.1.1.d: Examine audit logs, including payment application logs, to verify the PAN is rendered unreadable.

Guidance:
Purpose: Disk-level and partition-level encryption typically encrypts the entire disk or partition using the same key, with all data automatically decrypted when the system runs or when an authorized user requests it. for this reason, disk-level encryption is not appropriate to protect stored pan on computers, laptops, servers, storage arrays, or any other system that provides transparent decryption upon user authentication. Further Information: Where available, following vendors’ hardening and industry best practice guidelines can assist in securing pan on these devices.