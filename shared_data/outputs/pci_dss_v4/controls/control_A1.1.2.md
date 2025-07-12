PCI DSS 4_0_1 Requirement Control A1.1.2

Defined Approach Requirements:
Controls are implemented such that each customer only has permission to access its own cardholder data and CDE.

Customized Approach Objective:
Customers cannot access other customers’ environments.

Testing Procedures:
Testing Procedure A1.1.2.a: Examine documentation to verify controls are defined such that each customer only has permission to access its own cardholder data and CDE.
Testing Procedure A1.1.2.b: Examine system configurations to verify that customers have privileges established to only access their own account data and CDE.

Guidance:
Purpose: To prevent any inadvertent or intentional impact to other customers’ environments or account data, it is important that each customer can access only resources allocated to that customer. Examples: In a cloud-based infrastructure, such as an infrastructure as a service (iaas) offering, the customers’ cde may include virtual network devices and virtual servers that are configured and managed by the customers, including operating systems, files, memory, etc.