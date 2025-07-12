PCI DSS 4_0_1 Requirement Control 7.2.2

Defined Approach Requirements:
Access is assigned to users, including privileged users, based on: Job classification and function. Least privileges necessary to perform job responsibilities.

Customized Approach Objective:
Access to systems and data is limited to only the access needed to perform job functions, as defined in the related access roles.

Testing Procedures:
Testing Procedure 7.2.2.a: Examine policies and procedures to verify they cover assigning access to users in accordance with all elements specified in this requirement.
Testing Procedure 7.2.2.b: Examine user access settings, including for privileged users, and interview responsible management personnel to verify that privileges assigned are in accordance with all elements specified in this requirement.
Testing Procedure 7.2.2.c: Interview personnel responsible for assigning access to verify that privileged user access is assigned in accordance with all elements specified in this requirement.

Guidance:
Purpose: Assigning least privileges helps prevent users without sufficient knowledge about the application from incorrectly or accidentally changing application configuration or altering its security settings. enforcing least privilege also helps to minimize the scope of damage if an unauthorized person gains access to a user id. Good Practice: Access rights are granted to a user by assignment to one or several functions. access is assigned depending on the specific user functions and with the minimum scope required for the job. when assigning privileged access, it is important to assign individuals only the privileges they need to perform their job (the “least privileges”). for example, the database administrator or backup administrator should not be assigned the same privileges as the overall systems administrator. once needs are defined for user functions (per pci dss requirement 7.2.1), it is easy to grant individuals access according to their job classification and function by using the already- created roles. entities may wish to consider use of privileged access management (pam), which is a method to grant access to privileged accounts only when those privileges are required, immediately revoking that access once they are no longer needed.