PCI DSS 4_0_1 Requirement Control 1.2.8

Defined Approach Requirements:
Configuration files for NSCs are: Secured from unauthorized access. Kept consistent with active network configurations.

Customized Approach Objective:
NSCs cannot be defined or modified using untrusted configuration objects (including files).

Applicability Notes:
Any file or setting used to configure or synchronize NSCs is considered to be a “configuration file.” This includes files, automated and system-based controls, scripts, settings, infrastructure as code, or other parameters that are backed up, archived, or stored remotely.

Testing Procedures:
Testing Procedure 1.2.8: Examine configuration files for NSCs to verify they are in accordance with all elements specified in this requirement.

Guidance:
Purpose: To prevent unauthorized configurations from being applied to the network, stored files with configurations for network controls need to be kept up to date and secured against unauthorized changes. keeping configuration information current and secure ensures that the correct settings for nscs are applied whenever the configuration is run. Examples: If the secure configuration for a router is stored in non-volatile memory, when that router is restarted or rebooted, these controls should ensure that its secure configuration is reinstated.