PCI DSS 4_0_1 Requirement Control 1.3.2

Defined Approach Requirements:
Outbound traffic from the CDE is restricted as follows: To only traffic that is necessary. All other traffic is specifically denied.

Customized Approach Objective:
Unauthorized traffic cannot leave the CDE.

Testing Procedures:
Testing Procedure 1.3.2.a: Examine configuration standards for NSCs to verify that they define restricting outbound traffic from the CDE in accordance with all elements specified in this requirement.
Testing Procedure 1.3.2.b: Examine configurations of NSCs to verify that outbound traffic from the CDE is restricted in accordance with all elements specified in this requirement.

Guidance:
Purpose: This requirement aims to prevent malicious individuals and compromised system components within the entity’s network from communicating with an untrusted external host. Examples: Implementing a rule that denies all inbound and outbound traffic that is not specifically needed— for example, by using an explicit “deny all” or implicit deny after allow statement—helps to prevent inadvertent holes that would allow unintended and potentially harmful traffic. Good Practice: All traffic outbound from the cde, regardless of the destination, should be evaluated to ensure it follows established, authorized rules. connections should be inspected to restrict traffic to only authorized communications—for example, by restricting source/destination addresses and ports, and blocking of content.