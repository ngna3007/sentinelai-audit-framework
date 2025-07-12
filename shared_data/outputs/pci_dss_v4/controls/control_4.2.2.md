PCI DSS 4_0_1 Requirement Control 4.2.2

Defined Approach Requirements:
PAN is secured with strong cryptography whenever it is sent via end-user messaging technologies.

Customized Approach Objective:
Cleartext PAN cannot be read or intercepted from transmissions using end-user messaging technologies.

Applicability Notes:
This requirement also applies if a customer, or other third party, requests that PAN is sent to them via end-user messaging technologies. There could be occurrences where an entity receives unsolicited cardholder data via an insecure communication channel that was not intended for transmissions of sensitive data. In this situation, the entity can choose to either include the channel in the scope of their CDE and secure it according to PCI DSS or delete the cardholder data and implement measures to prevent the channel from being used for cardholder data.

Testing Procedures:
Testing Procedure 4.2.2.a: Examine documented policies and procedures to verify that processes are defined to secure PAN with strong cryptography whenever sent over end-user messaging technologies.
Testing Procedure 4.2.2.b: Examine system configurations and vendor documentation to verify that PAN is secured with strong cryptography whenever it is sent via end- user messaging technologies.

Guidance:
Purpose: End-user messaging technologies typically can be easily intercepted by packet-sniffing during delivery across internal and public networks. Examples: E-mail, instant messaging, sms, and chat are examples of the type of end-user messaging technology that this requirement refers to. Good Practice: The use of end-user messaging technology to send pan should only be considered where there is a defined business need and should be controlled through the acceptable use policies for end-user technologies defined by the entity according to requirement 12.2.1.