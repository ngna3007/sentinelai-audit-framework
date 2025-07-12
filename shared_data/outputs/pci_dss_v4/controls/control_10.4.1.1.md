PCI DSS 4_0_1 Requirement Control 10.4.1.1

Defined Approach Requirements:
Automated mechanisms are used to perform audit log reviews.

Customized Approach Objective:
Potentially suspicious or anomalous activities are identified via a repeatable and consistent mechanism.

Applicability Notes:
_This requirement is a best practice until 31 March_ _2025, after which it will be required and must be_ _fully considered during a PCI DSS assessment._

Testing Procedures:
Testing Procedure 10.4.1.1: Examine log review mechanisms and interview personnel to verify that automated mechanisms are used to perform log reviews.

Guidance:
Purpose: Manual log reviews are difficult to perform, even for one or two systems, due to the amount of log data that is generated. however, using log harvesting, parsing, and alerting tools, centralized log management systems, event log analyzers, and security information and event management (siem) solutions can help facilitate the process by identifying log events that need to be reviewed. Good Practice: Establishing a baseline of normal audit activity patterns is critical to the effectiveness of an automated log review mechanism. the analysis of new audit activity against the established baseline can significantly improve the identification of suspicious or anomalous activities. the entity should keep logging tools aligned with any changes in their environment by periodically reviewing tool settings and updating settings to reflect any changes. Further Information: Refer to the information supplement:_effective_ _daily log monitoring_ for additional guidance.