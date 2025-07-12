PCI DSS 4_0_1 Requirement Control 5.3.5

Defined Approach Requirements:
Anti-malware mechanisms cannot be disabled or altered by users, unless specifically documented, and authorized by management on a case-by-case basis for a limited time period.

Applicability Notes:
Anti-malware solutions may be temporarily disabled only if there is a legitimate technical need, as authorized by management on a case-by-case basis. If anti-malware protection needs to be disabled for a specific purpose, it must be formally authorized. Additional security measures may also need to be implemented for the period during which anti-malware protection is not active.

Testing Procedures:
Testing Procedure 5.3.5.a: Examine anti-malware configurations, to verify that the anti-malware mechanisms cannot be disabled or altered by users.
Testing Procedure 5.3.5.b: Interview responsible personnel and observe processes to verify that any requests to disable or alter anti-malware mechanisms are specifically documented and authorized by management on a case-by-case basis for a limited time period.

Guidance:
Purpose: It is important that defensive mechanisms are always running so that malware is detected in real time. ad-hoc starting and stopping of anti-malware solutions could allow malware to propagate unchecked and undetected. Examples: Additional security measures that may need to be implemented for the period during which anti- malware protection is not active include disconnecting the unprotected system from the internet while the anti-malware protection is disabled and running a full scan once it is re- enabled. Good Practice: Where there is a legitimate need to temporarily disable a system’s anti-malware protection—for example, to support a specific maintenance activity or investigation of a technical problem—the reason for taking such action should be understood and approved by an appropriate management representative. any disabling or altering of anti- malware mechanisms, including on administrators’ own devices, should be performed by authorized personnel. it is recognized that administrators have privileges that may allow them to disable anti- malware on their own computers, but there should be alerting mechanisms in place when such software is disabled and then follow up that occurs to ensure correct processes were followed.