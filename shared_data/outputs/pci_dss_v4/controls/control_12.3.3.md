PCI DSS 4_0_1 Requirement Control 12.3.3

Defined Approach Requirements:
Cryptographic cipher suites and protocols in use are documented and reviewed at least once every 12 months, including at least the following: An up-to-date inventory of all cryptographic cipher suites and protocols in use, including purpose and where used. Active monitoring of industry trends regarding continued viability of all cryptographic cipher suites and protocols in use. Documentation of a plan, to respond to anticipated changes in cryptographic vulnerabilities.

Customized Approach Objective:
The entity is able to respond quickly to any vulnerabilities in cryptographic protocols or algorithms, where those vulnerabilities affect protection of cardholder data.

Applicability Notes:
The requirement applies to all cryptographic cipher suites and protocols used to meet PCI DSS requirements, including, but not limited to, those used to render PAN unreadable in storage and transmission, to protect passwords, and as part of authenticating access. _This requirement is a best practice until 31 March_ _2025, after which it will be required and must be_ _fully considered during a PCI DSS assessment._

Testing Procedures:
Testing Procedure 12.3.3: Examine documentation for cryptographic suites and protocols in use and interview personnel to verify the documentation and review is in accordance with all elements specified in this requirement.

Guidance:
Purpose: Protocols and encryption strengths may quickly change or be deprecated due to identification of vulnerabilities or design flaws. in order to support current and future data security needs, entities need to know where cryptography is used and understand how they would be able to respond rapidly to changes impacting the strength of their cryptographic implementations. Good Practice: Cryptographic agility is important to ensure an alternative to the original encryption method or cryptographic primitive is available, with plans to upgrade to the alternative without significant change to system infrastructure. for example, if the entity is aware of when protocols or algorithms will be deprecated by standards bodies, proactive plans will help the entity to upgrade before the deprecation is impactful to operations. Definitions: “cryptographic agility” refers to the ability to monitor and manage the encryption and related verification technologies deployed across an organization. Further Information: Refer to_nist_ _sp 800-131a,_ _transitioning the_ _use of cryptographic algorithms and key_ _lengths_.