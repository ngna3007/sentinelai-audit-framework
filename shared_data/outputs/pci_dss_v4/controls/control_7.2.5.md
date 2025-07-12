PCI DSS 4_0_1 Requirement Control 7.2.5

Defined Approach Requirements:
All application and system accounts and related access privileges are assigned and managed as follows: Based on the least privileges necessary for the operability of the system or application. Access is limited to the systems, applications, or processes that specifically require their use.

Customized Approach Objective:
Access rights granted to application and system accounts are limited to only the access needed for the operability of that application or system.

Applicability Notes:
_This requirement is a best practice until 31 March_ _2025, after which it will be required and must be_ _fully considered during a PCI DSS assessment._

Testing Procedures:
Testing Procedure 7.2.5.a: Examine policies and procedures to verify they define processes to manage and assign application and system accounts and related access privileges in accordance with all elements specified in this requirement.
Testing Procedure 7.2.5.b: Examine privileges associated with system and application accounts and interview responsible personnel to verify that application and system accounts and related access privileges are assigned and managed in accordance with all elements specified in this requirement.

Guidance:
Purpose: It is important to establish the appropriate access level for application or system accounts. if such accounts are compromised, malicious users will receive the same access level as that granted to the application or system. therefore, it is important to ensure limited access is granted to system and application accounts on the same basis as to user accounts. Good Practice: Entities may want to consider establishing a baseline when setting up these application and system accounts including the following as applicable to the organization: making sure that the account is not a member of a privileged group such as domain administrators, local administrators, or root. restricting which computers the account can be used on. restricting hours of use. removing any additional settings like vpn access and remote access.