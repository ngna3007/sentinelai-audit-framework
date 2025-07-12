PCI DSS 4_0_1 Requirement Control 8.6.1

Defined Approach Requirements:
If accounts used by systems or applications can be used for interactive login, they are managed as follows: Interactive use is prevented unless needed for an exceptional circumstance. Interactive use is limited to the time needed for the exceptional circumstance. Business justification for interactive use is documented. Interactive use is explicitly approved by management. Individual user identity is confirmed before access to account is granted. Every action taken is attributable to an individual user.

Customized Approach Objective:
When used interactively, all actions with accounts designated as system or application accounts are authorized and attributable to an individual person.

Applicability Notes:
_This requirement is a best practice until 31 March_ _2025, after which it will be required and must be_ _fully considered during a PCI DSS assessment._

Testing Procedures:
Testing Procedure 8.6.1: Examine application and system accounts that can be used interactively and interview administrative personnel to verify that application and system accounts are managed in accordance with all elements specified in this requirement.