PCI DSS 4_0_1 Requirement Control 12.10.7

Defined Approach Requirements:
Incident response procedures are in place, to be initiated upon the detection of stored PAN anywhere it is not expected, and include: Determining what to do if PAN is discovered outside the CDE, including its retrieval, secure deletion, and/or migration into the currently defined CDE, as applicable. Identifying whether sensitive authentication data is stored with PAN. Determining where the account data came from and how it ended up where it was not expected. Remediating data leaks or process gaps that resulted in the account data being where it was not expected.

Customized Approach Objective:
Processes are in place to quickly respond, analyze, and address situations in the event that cleartext PAN is detected where it is not expected.

Applicability Notes:
_This requirement is a best practice until 31 March_ _2025, after which it will be required and must be_ _fully considered during a PCI DSS assessment._

Testing Procedures:
Testing Procedure 12.10.7.a: Examine documented incident response procedures to verify that procedures for responding to the detection of stored PAN anywhere it is not expected to exist, ready to be initiated, and include all elements specified in this requirement.
Testing Procedure 12.10.7.b: Interview personnel and examine records of response actions to verify that incident response procedures are performed upon detection of stored PAN anywhere it is not expected.

Guidance:
Purpose: Having documented incident response procedures that are followed in the event that stored pan is found anywhere it is not expected to be, helps to identify the necessary remediation actions and prevent future leaks. Good Practice: If pan was found outside the cde, analysis should be performed to 1) determine whether it was saved independently of other data or with sensitive authentication data, 2) identify the source of the data, and 3) identify the control gaps that resulted in the data being outside the cde. entities should consider whether there are contributory factors, such as business processes, user behavior, improper system configurations, etc. that caused the pan to be stored in an unexpected location. if such contributory factors are present, they should be addressed per this requirement to prevent recurrence.