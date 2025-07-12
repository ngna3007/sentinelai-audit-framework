PCI DSS 4_0_1 Requirement Control A3.2.5.2

Defined Approach Requirements:
Response procedures are implemented to be initiated upon the detection of cleartext PAN outside the CDE to include: Determining what to do if cleartext PAN is discovered outside the CDE, including its retrieval, secure deletion, and/or migration into the currently defined CDE, as applicable. Determining how the data ended up outside the CDE. Remediating data leaks or process gaps that resulted in the data being outside the CDE. Identifying the source of the data. Identifying whether any track data is stored with the PANs.

Customized Approach Objective:
This requirement is not eligible for the customized approach.

Testing Procedures:
Testing Procedure A3.2.5.2.a: Examine documented response procedures to verify that procedures for responding to the detection of cleartext PAN outside the CDE are defined and include all elements specified in this requirement.
Testing Procedure A3.2.5.2.b: Interview personnel and examine records of response actions to verify that remediation activities are performed when cleartext PAN is detected outside the CDE.

Guidance:
Purpose: Having documented response procedures that are followed in the event cleartext pan is found outside the cde helps to identify the necessary remediation actions and prevent future leaks. Good Practice: If pan was found outside the cde, an analysis should be performed to 1) determine whether it was saved independently of other data or with sensitive authentication data, 2) to identify the source of the data, and 3) identify the control gaps that resulted in the data being outside the cde. entities should consider whether contributory factors, such as business processes, user behavior, improper system configurations, etc., caused the pan to be stored in an unexpected location. if such contributory factors are present, they should be addressed per this requirement to prevent a recurrence.