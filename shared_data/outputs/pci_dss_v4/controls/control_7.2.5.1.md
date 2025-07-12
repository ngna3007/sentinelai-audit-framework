PCI DSS 4_0_1 Requirement Control 7.2.5.1

Defined Approach Requirements:
All access by application and system accounts and related access privileges are reviewed as follows: Periodically (at the frequency defined in the entity’s targeted risk analysis, which is performed according to all elements specified in Requirement 12.3.1). The application/system access remains appropriate for the function being performed. Any inappropriate access is addressed. Management acknowledges that access remains appropriate.

Customized Approach Objective:
Application and system account privilege assignments are verified periodically by management as correct, and nonconformities are remediated.

Applicability Notes:
_This requirement is a best practice until 31 March_ _2025, after which it will be required and must be_ _fully considered during a PCI DSS assessment._

Testing Procedures:
Testing Procedure 7.2.5.1.a: Examine policies and procedures to verify they define processes to review all application and system accounts and related access privileges in accordance with all elements specified in this requirement.
Testing Procedure 7.2.5.1.b: Examine the entity’s targeted risk analysis for the frequency of periodic reviews of application and system accounts and related access privileges to verify the risk analysis was performed in accordance with all elements specified in Requirement 12.3.1.
Testing Procedure 7.2.5.1.c: Interview responsible personnel and examine documented results of periodic reviews of system and application accounts and related privileges to verify that the reviews occur in accordance with all elements specified in this requirement.

Guidance:
Purpose: Regular review of access rights helps to detect excessive access rights remaining after system functions change, or other application or system modifications occur. if excessive rights are not removed when no longer needed, they may be used by malicious users for unauthorized access.