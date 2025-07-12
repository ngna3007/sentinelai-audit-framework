PCI DSS 4_0_1 Requirement Control 11.5.2

Defined Approach Requirements:
A change-detection mechanism (for example, file integrity monitoring tools) is deployed as follows: To alert personnel to unauthorized modification (including changes, additions, and deletions) of critical files. To perform critical file comparisons at least once weekly.

Customized Approach Objective:
Critical files cannot be modified by unauthorized personnel without an alert being generated. _(continued on next page)_

Testing Procedures:
Testing Procedure 11.5.2.a: Examine system settings, monitored files, and results from monitoring activities to verify the use of a change-detection mechanism.
Testing Procedure 11.5.2.b: Examine settings for the change-detection mechanism to verify it is configured in accordance with all elements specified in this requirement.

Guidance:
Purpose: Changes to critical system, configuration, or content files can be an indicator an attacker has accessed an organization’s system. such changes can allow an attacker to take additional malicious actions, access cardholder data, and/or conduct activities without detection or record. a change detection mechanism will detect and evaluate such changes to critical files and generate alerts that can be responded to following defined processes so that personnel can take appropriate actions. _(continued on next page)_. Examples: Change-detection solutions such as file integrity monitoring (fim) tools check for changes, additions, and deletions to critical files, and notify when such changes are detected. Good Practice: Examples of the types of files that should be monitored include, but are not limited to: system executables. application executables. configuration and parameter files. centrally stored, historical, or archived audit logs. additional critical files determined by entity (for example, through risk assessment or other means).