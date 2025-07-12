PCI DSS 4_0_1 Requirement Control 1.4.5

Defined Approach Requirements:
The disclosure of internal IP addresses and routing information is limited to only authorized parties.

Customized Approach Objective:
Internal network information is protected from unauthorized disclosure.

Testing Procedures:
Testing Procedure 1.4.5.a: Examine configurations of NSCs to verify that the disclosure of internal IP addresses and routing information is limited to only authorized parties.
Testing Procedure 1.4.5.b: Interview personnel and examine documentation to verify that controls are implemented such that any disclosure of internal IP addresses and routing information is limited to only authorized parties.

Guidance:
Purpose: Restricting the disclosure of internal, private, and local ip addresses is useful to prevent a hacker from obtaining knowledge of these ip addresses and using that information to access the network. Examples: Methods to obscure ip addressing may include, but are not limited to: ipv4 network address translation (nat). placing system components behind proxy servers/nscs. removal or filtering of route advertisements for internal networks that use registered addressing. internal use of rfc 1918 (ipv4) or use ipv6 privacy extension (rfc 4941) when initiating outgoing sessions to the internet. Good Practice: Methods used to meet the intent of this requirement may vary, depending on the specific networking technology being used. for example, the controls used to meet this requirement may be different for ipv4 networks than for ipv6 networks.