PCI DSS 4_0_1 Requirement Control 9.4.6

Defined Approach Requirements:
Hard-copy materials with cardholder data are destroyed when no longer needed for business or legal reasons, as follows: Materials are cross-cut shredded, incinerated, or pulped so that cardholder data cannot be reconstructed. Materials are stored in secure storage containers prior to destruction.

Customized Approach Objective:
Cardholder data cannot be recovered from media that has been destroyed or which is pending destruction.

Applicability Notes:
These requirements for media destruction when that media is no longer needed for business or legal reasons are separate and distinct from PCI DSS Requirement 3.2.1, which is for securely deleting cardholder data when no longer needed per the entity’s cardholder data retention policies.

Testing Procedures:
Testing Procedure 9.4.6.a: Examine the media destruction policy to verify that procedures are defined to destroy hard- copy media with cardholder data when no longer needed for business or legal reasons in accordance with all elements specified in this requirement.
Testing Procedure 9.4.6.b: Observe processes and interview personnel to verify that hard-copy materials are cross-cut shredded, incinerated, or pulped such that cardholder data cannot be reconstructed.
Testing Procedure 9.4.6.c: Observe storage containers used for materials that contain information to be destroyed to verify that the containers are secure.

Guidance:
Purpose: If steps are not taken to destroy information contained on hard-copy media before disposal, malicious individuals may retrieve information from the disposed media, leading to a data compromise. for example, malicious individuals may use a technique known as “dumpster diving,” where they search through trashcans and recycle bins looking for hard-copy materials with information they can use to launch an attack. securing storage containers used for materials that are going to be destroyed prevents sensitive information from being captured while the materials are being collected. Good Practice: Consider “to-be-shredded” containers with a lock that prevents access to its contents or that physically prevent access to the inside of the container. Further Information: See_nist special publication 800-88, revision 1:_ _guidelines for media sanitization_.