PCI DSS 4_0_1 Requirement Control 5.3.1

Defined Approach Requirements:
The anti-malware solution(s) is kept current via automatic updates.

Customized Approach Objective:
Anti-malware mechanisms can detect and address the latest malware threats.

Testing Procedures:
Testing Procedure 5.3.1.a: Examine anti-malware solution(s) configurations, including any master installation of the software, to verify the solution is configured to perform automatic updates.
Testing Procedure 5.3.1.b: Examine system components and logs, to verify that the anti-malware solution(s) and definitions are current and have been promptly deployed

Guidance:
Purpose: For an anti-malware solution to remain effective, it needs to have the latest security updates, signatures, threat analysis engines, and any other malware protections on which the solution relies. having an automated update process avoids burdening end users with responsibility for manually installing updates and provides greater assurance that anti-malware protection mechanisms are updated as quickly as possible after an update is released. Good Practice: Anti-malware mechanisms should be updated via a trusted source as soon as possible after an update is available. using a trusted common source to distribute updates to end-user systems helps ensure the integrity and consistency of the solution architecture. updates may be automatically downloaded to a central location—for example, to allow for testing— prior to being deployed to individual system components.