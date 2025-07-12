PCI DSS 4_0_1 Requirement Control 7.2.4

Defined Approach Requirements:
All user accounts and related access privileges, including third-party/vendor accounts, are reviewed as follows: At least once every six months. To ensure user accounts and access remain appropriate based on job function. Any inappropriate access is addressed. Management acknowledges that access remains appropriate.

Customized Approach Objective:
Account privilege assignments are verified periodically by management as correct, and nonconformities are remediated.

Applicability Notes:
This requirement applies to all user accounts and related access privileges, including those used by personnel and third parties/vendors, and accounts used to access third-party cloud services. See Requirements 7.2.5 and 7.2.5.1 and 8.6.1 through 8.6.3 for controls for application and system accounts. _This requirement is a best practice until 31 March_ _2025, after which it will be required and must be_ _fully considered during a PCI DSS assessment._

Testing Procedures:
Testing Procedure 7.2.4.a: Examine policies and procedures to verify they define processes to review all user accounts and related access privileges, including third- party/vendor accounts, in accordance with all elements specified in this requirement.
Testing Procedure 7.2.4.b: Interview responsible personnel and examine documented results of periodic reviews of user accounts to verify that all the results are in accordance with all elements specified in this requirement.

Guidance:
Purpose: Regular review of access rights helps to detect excessive access rights remaining after user job responsibilities change, system functions change, or other modifications. if excessive user rights are not revoked in due time, they may be used by malicious users for unauthorized access. this review provides another opportunity to ensure that accounts for all terminated users have been removed (if any were missed at the time of termination), as well as to ensure that any third parties that no longer need access have had their access terminated. Good Practice: When a user transfers into a new role or a new department, typically the privileges and access associated with their former role are no longer required. continued access to privileges or functions that are no longer required may introduce the risk of misuse or errors. therefore, when responsibilities change, processes that revalidate access help to ensure user access is appropriate for the user’s new responsibilities. entities can consider implementing a regular, repeatable process for conducting reviews of access rights, and assigning “data owners” that are responsible for managing and monitoring access to data related to their job function and that also ensure user access remains current and appropriate. as an example, a direct manager could review team access monthly, while the senior manager reviews their groups’ access quarterly, both making updates to access as needed. the intent of these best practices is to support and facilitate conducting the reviews at least once every 6 months.