PCI DSS 4_0_1 Requirement Control 6.2.3.1

Defined Approach Requirements:
If manual code reviews are performed for bespoke and custom software prior to release to production, code changes are: Reviewed by individuals other than the originating code author, and who are knowledgeable about code-review techniques and secure coding practices. Reviewed and approved by management prior to release.

Customized Approach Objective:
The manual code review process cannot be bypassed and is effective at discovering security vulnerabilities.

Applicability Notes:
Manual code reviews can be conducted by knowledgeable internal personnel or knowledgeable third-party personnel. An individual that has been formally granted accountability for release control and who is neither the original code author nor the code reviewer fulfills the criteria of being management.

Testing Procedures:
Testing Procedure 6.2.3.1.a: If manual code reviews are performed for bespoke and custom software prior to release to production, examine documented software development procedures and interview responsible personnel to verify that processes are defined for manual code reviews to be conducted in accordance with all elements specified in this requirement.
Testing Procedure 6.2.3.1.b: Examine evidence of changes to bespoke and custom software and interview personnel to verify that manual code reviews were conducted in accordance with all elements specified in this requirement.

Guidance:
Purpose: Having code reviewed by someone other than the original author, who is both experienced in code reviews and knowledgeable about secure coding practices, minimizes the possibility that code containing security or logic errors that could affect the security of cardholder data is released into a production environment. requiring management approval that the code was reviewed limits the ability for the process to be bypassed. Good Practice: Having a formal review methodology and review checklists has been found to improve the quality of the code review process. code review is a tiring process, and for this reason, it is most effective when reviewers only review small amounts of code at a time. to maintain the effectiveness of code reviews, it is beneficial to monitor the general workload of reviewers and to have them review applications they are familiar with. code reviews may be performed using either manual or automated processes, or a combination of both. entitles that rely solely on manual code review should ensure that reviewers maintain their skills through regular training as new vulnerabilities are found, and new secure coding methods are recommended. Further Information: See the_owasp code review guide_.