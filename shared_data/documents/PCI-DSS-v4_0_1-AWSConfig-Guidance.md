**AWS Config Developer Guide**
## **Template**
[The template is available on GitHub: Operational Best Practices for PCI DSS 4.0 (Excluding global](https://github.com/awslabs/aws-config-rules/blob/master/aws-config-conformance-packs/Operational-Best-Practices-for-PCI-DSS-v4.0-excluding-global-resourcetypes.yaml)
[resource types).](https://github.com/awslabs/aws-config-rules/blob/master/aws-config-conformance-packs/Operational-Best-Practices-for-PCI-DSS-v4.0-excluding-global-resourcetypes.yaml)
# **Operational Best Practices for PCI DSS 4.0 (Including global resource** **types)**
Conformance packs provide a general-purpose compliance framework designed to enable you
to create security, operational or cost-optimization governance checks using managed or custom
**AWS Config rules and AWS Config remediation actions. Conformance Packs, as sample templates,**
are not designed to fully ensure compliance with a specific governance or compliance standard.
You are responsible for making your own assessment of whether your use of the Services meets
applicable legal and regulatory requirements.
The following provides a sample mapping between the Payment Card Industry Data Security
**Standard (PCI DSS) 4.0 (Excluding global resource types) and AWS managed Config rules. Each AWS**
**Config rule applies to a specific AWS resource, and relates to one or more PCI DSS controls. A PCI**
**DSS control can be related to multiple Config rules. Refer to the table below for more detail and**
guidance related to these mappings.
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.2.5|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|cloudfront-security-<br>policy-check|Ensure that Amazon<br>CloudFront distribut<br>ions are using a<br>minimum security<br>policy and cipher<br>suite of TLSv1.2 or<br>greater for viewer<br>connections. This<br>rule is NON_COMPL<br>IANT for a CloudFron<br>t distribution if<br>the minimumPr<br>otocolVersion is<br>below TLSv1.2_2018.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13907
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.2.5|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|cloudfront-sni-ena <br>bled|Ensure that Amazon<br>CloudFront distribut<br>ions are using a<br>custom SSL certiﬁca<br>te and are conﬁgure<br>d to use SNI to serve<br>HTTPS requests. The<br>rule is NON_COMPL<br>IANT if a custom<br>SSL certiﬁcate is<br>associated but the<br>SSL support method<br>is a dedicated IP<br>address.|
|1.2.5|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|transfer-family-se <br>rver-no-ftp|Ensure that a<br>server created<br>with AWS Transfer<br>Family does not use<br>FTP for endpoint<br>connection. The<br>rule is NON_COMPL<br>IANT if the server<br>protocol for endpoint<br>connection is FTP-<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13908
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.2.5|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|cloudfront-no-depr <br>ecated-ssl-protocols|Ensure that<br>CloudFront distribut<br>ions are not using<br>deprecated SSL<br>protocols for HTTPS<br>communication<br>between CloudFron<br>t edge locations and<br>custom origins. This<br>rule is NON_COMPL<br>IANT for a CloudFron<br>t distribution if<br>any'OriginSslProto<br>cols' includes'SSLv3'.|
|1.2.5|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|cloudfront-traﬃc-to-<br>origin-encrypted|Ensure that Amazon<br>CloudFront distribut<br>ions are encryptin<br>g traﬃc to custom<br>origins. The rule is<br>NON_COMPLIANT<br>if'OriginProtocolP<br>olicy' is'http-only' or<br>if'OriginProtocolP<br>olicy' is'match-viewer'<br>and'ViewerProtocol<br>Policy' is'allow-all'.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13909
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.2.5|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|cloudfront-viewer- <br>policy-https|Ensure that your<br>Amazon CloudFron<br>t distributions use<br>HTTPS (directly or<br>via a redirection). The<br>rule is NON_COMPL<br>IANT if the value of<br>ViewerProtocolPoli<br>cy is set to 'allow-al<br>l' for the DefaultCa<br>cheBehavior or for<br>the CacheBehaviors.|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|api-gw-endpoint-ty <br>pe-check|Ensure that Amazon<br>API Gateway APIs are<br>of the type speciﬁed<br>in the rule parameter<br>'endpointConﬁgura<br>tionType'. The rule<br>returns NON_COMPL<br>IANT if the REST<br>API does not match<br>the endpoint type<br>conﬁgured in the rule<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13910
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|cloudfront-associa <br>ted-with-waf|Ensure that Amazon<br>CloudFront distribut<br>ions are associate<br>d with either web<br>application ﬁrewall<br>(WAF) or WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion is not associated<br>with a WAF web ACL.|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13911
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|netfw-policy-defau <br>lt-action-fragment-<br>packets|Ensure that an AWS<br>Network Firewall<br>policy is conﬁgured<br>with a user deﬁned<br>stateless default<br>action for fragmente<br>d packets. The rule<br>is NON_COMPLIANT<br>if stateless default<br>action for fragmente<br>d packets does not<br>match with user<br>deﬁned default<br>action.|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|rds-db-security-gr <br>oup-not-allowed|Ensure that the<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) DB<br>security groups is the<br>default one. The rule<br>is NON_COMPLIANT<br>if there are any DB<br>security groups that<br>are not the default<br>DB security group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13912
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|ec2-transit-gatewa <br>y-auto-vpc-attach- <br>disabled|Ensure that Amazon<br>Elastic Compute<br>Cloud (Amazon EC2)<br>Transit Gateways do<br>not have 'AutoAcce<br>ptSharedAttachment<br>s' enabled. The rule is<br>NON_COMPLIANT for<br>a Transit Gateway if<br>'AutoAcceptSharedA<br>ttachments' is set to<br>'enable'.|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|eks-endpoint-no-pu <br>blic-access|Ensure that the<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS)<br>endpoint is not<br>publicly accessibl<br>e. The rule is<br>NON_COMPLIANT<br>if the endpoint is<br>publicly accessible.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13913
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|restricted-ssh|Note: For this rule,<br>the rule identiﬁe<br>r (INCOMING<br>_SSH_DISABLED)<br>and rule name<br>(restricted-ssh) are<br>diﬀerent. Ensure<br>that the incoming<br>SSH traﬃc for the<br>security groups is<br>accessible. The rule<br>is COMPLIANT if the<br>IP addresses of the<br>incoming SSH traﬃc<br>in the security groups<br>are restricted (CIDR<br>other than 0.0.0.0/0<br>or ::/0). Otherwise,<br>NON_COMPLIANT.|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|appsync-associated-<br>with-waf|Ensure that AWS<br>AppSync APIs are<br>associated with<br>AWS WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT for<br>an AWS AppSync API<br>if it is not associated<br>with a web ACL.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13914
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|docdb-cluster-snap <br>shot-public-prohib <br>ited|Ensure that Amazon<br>DocumentDB manual<br>cluster snapshots<br>are not public. The<br>rule is NON_COMPL<br>IANT if any Amazon<br>DocumentDB manual<br>cluster snapshots are<br>public.|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|codebuild-project- <br>source-repo-url-check|Ensure that the<br>Bitbucket source<br>repository URL<br>DOES NOT contain<br>sign-in credentials<br>or not. The rule is<br>NON_COMPLIANT if<br>the URL contains any<br>sign-in information<br>and COMPLIANT if it<br>doesn't.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13915
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|emr-block-public-a <br>ccess|Ensure that an<br>account with Amazon<br>EMR has block public<br>access settings<br>enabled. The rule is<br>NON_COMPLIANT if<br>BlockPublicSecurit<br>yGroupRules is false,<br>or if true, ports other<br>than Port 22 are<br>listed in Permitted<br>PublicSecurityGrou<br>pRuleRanges.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13916
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|nacl-no-unrestricted-<br>ssh-rdp|Ensure that default<br>ports for SSH/RDP<br>ingress traﬃc for<br>network access<br>control lists (NACLs)<br>are restricted. The<br>rule is NON_COMPL<br>IANT if a NACL<br>inbound entry allows<br>a source TCP or UDP<br>CIDR block for ports<br>22 or 3389.|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|waf-global-webacl- <br>not-empty|Ensure that a WAF<br>Global Web ACL<br>contains some<br>WAF rules or rule<br>groups. This rule is<br>NON_COMPLIANT if<br>a Web ACL does not<br>contain any WAF rule<br>or rule group.|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|waf-global-rulegro <br>up-not-empty|Ensure that an AWS<br>WAF Classic rule<br>group contains some<br>rules. The rule is<br>NON_COMPLIANT<br>if there are no rules<br>present within a rule<br>group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13917
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|waf-global-rule-not-<br>empty|Ensure that an<br>AWS WAF global<br>rule contains some<br>conditions. The rule<br>is NON_COMPLIANT<br>if no conditions are<br>present within the<br>WAF global rule.|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|ec2-client-vpn-not-<br>authorize-all|Ensure that the<br>AWS Client VPN<br>authorization rules<br>does not authorize<br>connection access for<br>all clients. The rule is<br>NON_COMPLIANT if<br>'AccessAll' is present<br>and set to true.|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|internet-gateway-a <br>uthorized-vpc-only|Ensure that internet<br>gateways are<br>attached to an<br>authorized virtual<br>private cloud<br>(Amazon VPC). The<br>rule is NON_COMPL<br>IANT if internet<br>gateways are<br>attached to an<br>unauthorized VPC.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13918
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|s3-access-point-pu <br>blic-access-blocks|Ensure that Amazon<br>S3 access points have<br>block public access<br>settings enabled. The<br>rule is NON_COMPL<br>IANT if block public<br>access settings are<br>not enabled for S3<br>access points.|
|1.2.8|Network security<br>controls (NSCs)<br>are conﬁgured and<br>maintained. (PCI-<br>DSS-v4.0)|s3-account-level-p <br>ublic-access-blocks|Ensure that the<br>required public<br>access block settings<br>are conﬁgured<br>from account level.<br>The rule is only<br>NON_COMPLIANT<br>when the ﬁelds set<br>below do not match<br>the corresponding<br>ﬁelds in the conﬁgura<br>tion item.|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|api-gw-endpoint-ty <br>pe-check|Ensure that Amazon<br>API Gateway APIs are<br>of the type speciﬁed<br>in the rule parameter<br>'endpointConﬁgura<br>tionType'. The rule<br>returns NON_COMPL<br>IANT if the REST<br>API does not match<br>the endpoint type<br>conﬁgured in the rule<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13919
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|cloudfront-associa <br>ted-with-waf|Ensure that Amazon<br>CloudFront distribut<br>ions are associate<br>d with either web<br>application ﬁrewall<br>(WAF) or WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion is not associated<br>with a WAF web ACL.|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13920
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|netfw-policy-defau <br>lt-action-fragment-<br>packets|Ensure that an AWS<br>Network Firewall<br>policy is conﬁgured<br>with a user deﬁned<br>stateless default<br>action for fragmente<br>d packets. The rule<br>is NON_COMPLIANT<br>if stateless default<br>action for fragmente<br>d packets does not<br>match with user<br>deﬁned default<br>action.|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|rds-db-security-gr <br>oup-not-allowed|Ensure that the<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) DB<br>security groups is the<br>default one. The rule<br>is NON_COMPLIANT<br>if there are any DB<br>security groups that<br>are not the default<br>DB security group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13921
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|redshift-enhanced- <br>vpc-routing-enabled|Ensure that Amazon<br>Redshift clusters have<br>'enhancedVpcRoutin<br>g' enabled. The rule is<br>NON_COMPLIANT if<br>'enhancedVpcRoutin<br>g' is not enabled<br>or if the conﬁgura<br>tion.enhancedVpcRo<br>uting ﬁeld is 'false'.|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|ec2-transit-gatewa <br>y-auto-vpc-attach- <br>disabled|Ensure that Amazon<br>Elastic Compute<br>Cloud (Amazon EC2)<br>Transit Gateways do<br>not have 'AutoAcce<br>ptSharedAttachment<br>s' enabled. The rule is<br>NON_COMPLIANT for<br>a Transit Gateway if<br>'AutoAcceptSharedA<br>ttachments' is set to<br>'enable'.|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|eks-endpoint-no-pu <br>blic-access|Ensure that the<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS)<br>endpoint is not<br>publicly accessibl<br>e. The rule is<br>NON_COMPLIANT<br>if the endpoint is<br>publicly accessible.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13922
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|restricted-ssh|Note: For this rule,<br>the rule identiﬁe<br>r (INCOMING<br>_SSH_DISABLED)<br>and rule name<br>(restricted-ssh) are<br>diﬀerent. Ensure<br>that the incoming<br>SSH traﬃc for the<br>security groups is<br>accessible. The rule<br>is COMPLIANT if the<br>IP addresses of the<br>incoming SSH traﬃc<br>in the security groups<br>are restricted (CIDR<br>other than 0.0.0.0/0<br>or ::/0). Otherwise,<br>NON_COMPLIANT.|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|appsync-associated-<br>with-waf|Ensure that AWS<br>AppSync APIs are<br>associated with<br>AWS WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT for<br>an AWS AppSync API<br>if it is not associated<br>with a web ACL.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13923
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|docdb-cluster-snap <br>shot-public-prohib <br>ited|Ensure that Amazon<br>DocumentDB manual<br>cluster snapshots<br>are not public. The<br>rule is NON_COMPL<br>IANT if any Amazon<br>DocumentDB manual<br>cluster snapshots are<br>public.|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|codebuild-project- <br>source-repo-url-check|Ensure that the<br>Bitbucket source<br>repository URL<br>DOES NOT contain<br>sign-in credentials<br>or not. The rule is<br>NON_COMPLIANT if<br>the URL contains any<br>sign-in information<br>and COMPLIANT if it<br>doesn't.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13924
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|emr-block-public-a <br>ccess|Ensure that an<br>account with Amazon<br>EMR has block public<br>access settings<br>enabled. The rule is<br>NON_COMPLIANT if<br>BlockPublicSecurit<br>yGroupRules is false,<br>or if true, ports other<br>than Port 22 are<br>listed in Permitted<br>PublicSecurityGrou<br>pRuleRanges.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13925
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|nacl-no-unrestricted-<br>ssh-rdp|Ensure that default<br>ports for SSH/RDP<br>ingress traﬃc for<br>network access<br>control lists (NACLs)<br>are restricted. The<br>rule is NON_COMPL<br>IANT if a NACL<br>inbound entry allows<br>a source TCP or UDP<br>CIDR block for ports<br>22 or 3389.|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|waf-global-webacl- <br>not-empty|Ensure that a WAF<br>Global Web ACL<br>contains some<br>WAF rules or rule<br>groups. This rule is<br>NON_COMPLIANT if<br>a Web ACL does not<br>contain any WAF rule<br>or rule group.|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|waf-global-rulegro <br>up-not-empty|Ensure that an AWS<br>WAF Classic rule<br>group contains some<br>rules. The rule is<br>NON_COMPLIANT<br>if there are no rules<br>present within a rule<br>group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13926
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|waf-global-rule-not-<br>empty|Ensure that an<br>AWS WAF global<br>rule contains some<br>conditions. The rule<br>is NON_COMPLIANT<br>if no conditions are<br>present within the<br>WAF global rule.|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|ec2-client-vpn-not-<br>authorize-all|Ensure that the<br>AWS Client VPN<br>authorization rules<br>does not authorize<br>connection access for<br>all clients. The rule is<br>NON_COMPLIANT if<br>'AccessAll' is present<br>and set to true.|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|internet-gateway-a <br>uthorized-vpc-only|Ensure that internet<br>gateways are<br>attached to an<br>authorized virtual<br>private cloud<br>(Amazon VPC). The<br>rule is NON_COMPL<br>IANT if internet<br>gateways are<br>attached to an<br>unauthorized VPC.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13927
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|s3-access-point-pu <br>blic-access-blocks|Ensure that Amazon<br>S3 access points have<br>block public access<br>settings enabled. The<br>rule is NON_COMPL<br>IANT if block public<br>access settings are<br>not enabled for S3<br>access points.|
|1.3.1|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|s3-account-level-p <br>ublic-access-blocks|Ensure that the<br>required public<br>access block settings<br>are conﬁgured<br>from account level.<br>The rule is only<br>NON_COMPLIANT<br>when the ﬁelds set<br>below do not match<br>the corresponding<br>ﬁelds in the conﬁgura<br>tion item.|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|api-gw-endpoint-ty <br>pe-check|Ensure that Amazon<br>API Gateway APIs are<br>of the type speciﬁed<br>in the rule parameter<br>'endpointConﬁgura<br>tionType'. The rule<br>returns NON_COMPL<br>IANT if the REST<br>API does not match<br>the endpoint type<br>conﬁgured in the rule<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13928
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|cloudfront-associa <br>ted-with-waf|Ensure that Amazon<br>CloudFront distribut<br>ions are associate<br>d with either web<br>application ﬁrewall<br>(WAF) or WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion is not associated<br>with a WAF web ACL.|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13929
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|netfw-policy-defau <br>lt-action-fragment-<br>packets|Ensure that an AWS<br>Network Firewall<br>policy is conﬁgured<br>with a user deﬁned<br>stateless default<br>action for fragmente<br>d packets. The rule<br>is NON_COMPLIANT<br>if stateless default<br>action for fragmente<br>d packets does not<br>match with user<br>deﬁned default<br>action.|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|rds-db-security-gr <br>oup-not-allowed|Ensure that the<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) DB<br>security groups is the<br>default one. The rule<br>is NON_COMPLIANT<br>if there are any DB<br>security groups that<br>are not the default<br>DB security group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13930
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|redshift-enhanced- <br>vpc-routing-enabled|Ensure that Amazon<br>Redshift clusters have<br>'enhancedVpcRoutin<br>g' enabled. The rule is<br>NON_COMPLIANT if<br>'enhancedVpcRoutin<br>g' is not enabled<br>or if the conﬁgura<br>tion.enhancedVpcRo<br>uting ﬁeld is 'false'.|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|ec2-transit-gatewa <br>y-auto-vpc-attach- <br>disabled|Ensure that Amazon<br>Elastic Compute<br>Cloud (Amazon EC2)<br>Transit Gateways do<br>not have 'AutoAcce<br>ptSharedAttachment<br>s' enabled. The rule is<br>NON_COMPLIANT for<br>a Transit Gateway if<br>'AutoAcceptSharedA<br>ttachments' is set to<br>'enable'.|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|eks-endpoint-no-pu <br>blic-access|Ensure that the<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS)<br>endpoint is not<br>publicly accessibl<br>e. The rule is<br>NON_COMPLIANT<br>if the endpoint is<br>publicly accessible.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13931
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|restricted-ssh|Note: For this rule,<br>the rule identiﬁe<br>r (INCOMING<br>_SSH_DISABLED)<br>and rule name<br>(restricted-ssh) are<br>diﬀerent. Ensure<br>that the incoming<br>SSH traﬃc for the<br>security groups is<br>accessible. The rule<br>is COMPLIANT if the<br>IP addresses of the<br>incoming SSH traﬃc<br>in the security groups<br>are restricted (CIDR<br>other than 0.0.0.0/0<br>or ::/0). Otherwise,<br>NON_COMPLIANT.|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|appsync-associated-<br>with-waf|Ensure that AWS<br>AppSync APIs are<br>associated with<br>AWS WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT for<br>an AWS AppSync API<br>if it is not associated<br>with a web ACL.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13932
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|docdb-cluster-snap <br>shot-public-prohib <br>ited|Ensure that Amazon<br>DocumentDB manual<br>cluster snapshots<br>are not public. The<br>rule is NON_COMPL<br>IANT if any Amazon<br>DocumentDB manual<br>cluster snapshots are<br>public.|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|codebuild-project- <br>source-repo-url-check|Ensure that the<br>Bitbucket source<br>repository URL<br>DOES NOT contain<br>sign-in credentials<br>or not. The rule is<br>NON_COMPLIANT if<br>the URL contains any<br>sign-in information<br>and COMPLIANT if it<br>doesn't.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13933
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|emr-block-public-a <br>ccess|Ensure that an<br>account with Amazon<br>EMR has block public<br>access settings<br>enabled. The rule is<br>NON_COMPLIANT if<br>BlockPublicSecurit<br>yGroupRules is false,<br>or if true, ports other<br>than Port 22 are<br>listed in Permitted<br>PublicSecurityGrou<br>pRuleRanges.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13934
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|nacl-no-unrestricted-<br>ssh-rdp|Ensure that default<br>ports for SSH/RDP<br>ingress traﬃc for<br>network access<br>control lists (NACLs)<br>are restricted. The<br>rule is NON_COMPL<br>IANT if a NACL<br>inbound entry allows<br>a source TCP or UDP<br>CIDR block for ports<br>22 or 3389.|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|waf-global-webacl- <br>not-empty|Ensure that a WAF<br>Global Web ACL<br>contains some<br>WAF rules or rule<br>groups. This rule is<br>NON_COMPLIANT if<br>a Web ACL does not<br>contain any WAF rule<br>or rule group.|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|waf-global-rulegro <br>up-not-empty|Ensure that an AWS<br>WAF Classic rule<br>group contains some<br>rules. The rule is<br>NON_COMPLIANT<br>if there are no rules<br>present within a rule<br>group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13935
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|waf-global-rule-not-<br>empty|Ensure that an<br>AWS WAF global<br>rule contains some<br>conditions. The rule<br>is NON_COMPLIANT<br>if no conditions are<br>present within the<br>WAF global rule.|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|ec2-client-vpn-not-<br>authorize-all|Ensure that the<br>AWS Client VPN<br>authorization rules<br>does not authorize<br>connection access for<br>all clients. The rule is<br>NON_COMPLIANT if<br>'AccessAll' is present<br>and set to true.|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|internet-gateway-a <br>uthorized-vpc-only|Ensure that internet<br>gateways are<br>attached to an<br>authorized virtual<br>private cloud<br>(Amazon VPC). The<br>rule is NON_COMPL<br>IANT if internet<br>gateways are<br>attached to an<br>unauthorized VPC.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13936
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|s3-access-point-pu <br>blic-access-blocks|Ensure that Amazon<br>S3 access points have<br>block public access<br>settings enabled. The<br>rule is NON_COMPL<br>IANT if block public<br>access settings are<br>not enabled for S3<br>access points.|
|1.3.2|Network access<br>to and from the<br>cardholder data<br>environment is<br>restricted. (PCI-DSS-<br>v4.0)|s3-account-level-p <br>ublic-access-blocks|Ensure that the<br>required public<br>access block settings<br>are conﬁgured<br>from account level.<br>The rule is only<br>NON_COMPLIANT<br>when the ﬁelds set<br>below do not match<br>the corresponding<br>ﬁelds in the conﬁgura<br>tion item.|
|1.4.1|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|api-gw-endpoint-ty <br>pe-check|Ensure that Amazon<br>API Gateway APIs are<br>of the type speciﬁed<br>in the rule parameter<br>'endpointConﬁgura<br>tionType'. The rule<br>returns NON_COMPL<br>IANT if the REST<br>API does not match<br>the endpoint type<br>conﬁgured in the rule<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13937
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.1|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|redshift-enhanced- <br>vpc-routing-enabled|Ensure that Amazon<br>Redshift clusters have<br>'enhancedVpcRoutin<br>g' enabled. The rule is<br>NON_COMPLIANT if<br>'enhancedVpcRoutin<br>g' is not enabled<br>or if the conﬁgura<br>tion.enhancedVpcRo<br>uting ﬁeld is 'false'.|
|1.4.1|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|internet-gateway-a <br>uthorized-vpc-only|Ensure that internet<br>gateways are<br>attached to an<br>authorized virtual<br>private cloud<br>(Amazon VPC). The<br>rule is NON_COMPL<br>IANT if internet<br>gateways are<br>attached to an<br>unauthorized VPC.|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|api-gw-endpoint-ty <br>pe-check|Ensure that Amazon<br>API Gateway APIs are<br>of the type speciﬁed<br>in the rule parameter<br>'endpointConﬁgura<br>tionType'. The rule<br>returns NON_COMPL<br>IANT if the REST<br>API does not match<br>the endpoint type<br>conﬁgured in the rule<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13938
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|cloudfront-associa <br>ted-with-waf|Ensure that Amazon<br>CloudFront distribut<br>ions are associate<br>d with either web<br>application ﬁrewall<br>(WAF) or WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion is not associated<br>with a WAF web ACL.|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13939
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|netfw-policy-defau <br>lt-action-fragment-<br>packets|Ensure that an AWS<br>Network Firewall<br>policy is conﬁgured<br>with a user deﬁned<br>stateless default<br>action for fragmente<br>d packets. The rule<br>is NON_COMPLIANT<br>if stateless default<br>action for fragmente<br>d packets does not<br>match with user<br>deﬁned default<br>action.|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|rds-db-security-gr <br>oup-not-allowed|Ensure that the<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) DB<br>security groups is the<br>default one. The rule<br>is NON_COMPLIANT<br>if there are any DB<br>security groups that<br>are not the default<br>DB security group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13940
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|redshift-enhanced- <br>vpc-routing-enabled|Ensure that Amazon<br>Redshift clusters have<br>'enhancedVpcRoutin<br>g' enabled. The rule is<br>NON_COMPLIANT if<br>'enhancedVpcRoutin<br>g' is not enabled<br>or if the conﬁgura<br>tion.enhancedVpcRo<br>uting ﬁeld is 'false'.|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|ec2-transit-gatewa <br>y-auto-vpc-attach- <br>disabled|Ensure that Amazon<br>Elastic Compute<br>Cloud (Amazon EC2)<br>Transit Gateways do<br>not have 'AutoAcce<br>ptSharedAttachment<br>s' enabled. The rule is<br>NON_COMPLIANT for<br>a Transit Gateway if<br>'AutoAcceptSharedA<br>ttachments' is set to<br>'enable'.|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|eks-endpoint-no-pu <br>blic-access|Ensure that the<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS)<br>endpoint is not<br>publicly accessibl<br>e. The rule is<br>NON_COMPLIANT<br>if the endpoint is<br>publicly accessible.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13941
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|restricted-ssh|Note: For this rule,<br>the rule identiﬁe<br>r (INCOMING<br>_SSH_DISABLED)<br>and rule name<br>(restricted-ssh) are<br>diﬀerent. Ensure<br>that the incoming<br>SSH traﬃc for the<br>security groups is<br>accessible. The rule<br>is COMPLIANT if the<br>IP addresses of the<br>incoming SSH traﬃc<br>in the security groups<br>are restricted (CIDR<br>other than 0.0.0.0/0<br>or ::/0). Otherwise,<br>NON_COMPLIANT.|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|appsync-associated-<br>with-waf|Ensure that AWS<br>AppSync APIs are<br>associated with<br>AWS WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT for<br>an AWS AppSync API<br>if it is not associated<br>with a web ACL.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13942
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|docdb-cluster-snap <br>shot-public-prohib <br>ited|Ensure that Amazon<br>DocumentDB manual<br>cluster snapshots<br>are not public. The<br>rule is NON_COMPL<br>IANT if any Amazon<br>DocumentDB manual<br>cluster snapshots are<br>public.|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|codebuild-project- <br>source-repo-url-check|Ensure that the<br>Bitbucket source<br>repository URL<br>DOES NOT contain<br>sign-in credentials<br>or not. The rule is<br>NON_COMPLIANT if<br>the URL contains any<br>sign-in information<br>and COMPLIANT if it<br>doesn't.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13943
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|emr-block-public-a <br>ccess|Ensure that an<br>account with Amazon<br>EMR has block public<br>access settings<br>enabled. The rule is<br>NON_COMPLIANT if<br>BlockPublicSecurit<br>yGroupRules is false,<br>or if true, ports other<br>than Port 22 are<br>listed in Permitted<br>PublicSecurityGrou<br>pRuleRanges.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13944
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|nacl-no-unrestricted-<br>ssh-rdp|Ensure that default<br>ports for SSH/RDP<br>ingress traﬃc for<br>network access<br>control lists (NACLs)<br>are restricted. The<br>rule is NON_COMPL<br>IANT if a NACL<br>inbound entry allows<br>a source TCP or UDP<br>CIDR block for ports<br>22 or 3389.|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|waf-global-webacl- <br>not-empty|Ensure that a WAF<br>Global Web ACL<br>contains some<br>WAF rules or rule<br>groups. This rule is<br>NON_COMPLIANT if<br>a Web ACL does not<br>contain any WAF rule<br>or rule group.|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|waf-global-rulegro <br>up-not-empty|Ensure that an AWS<br>WAF Classic rule<br>group contains some<br>rules. The rule is<br>NON_COMPLIANT<br>if there are no rules<br>present within a rule<br>group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13945
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|waf-global-rule-not-<br>empty|Ensure that an<br>AWS WAF global<br>rule contains some<br>conditions. The rule<br>is NON_COMPLIANT<br>if no conditions are<br>present within the<br>WAF global rule.|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|ec2-client-vpn-not-<br>authorize-all|Ensure that the<br>AWS Client VPN<br>authorization rules<br>does not authorize<br>connection access for<br>all clients. The rule is<br>NON_COMPLIANT if<br>'AccessAll' is present<br>and set to true.|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|internet-gateway-a <br>uthorized-vpc-only|Ensure that internet<br>gateways are<br>attached to an<br>authorized virtual<br>private cloud<br>(Amazon VPC). The<br>rule is NON_COMPL<br>IANT if internet<br>gateways are<br>attached to an<br>unauthorized VPC.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13946
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|s3-access-point-pu <br>blic-access-blocks|Ensure that Amazon<br>S3 access points have<br>block public access<br>settings enabled. The<br>rule is NON_COMPL<br>IANT if block public<br>access settings are<br>not enabled for S3<br>access points.|
|1.4.2|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|s3-account-level-p <br>ublic-access-blocks|Ensure that the<br>required public<br>access block settings<br>are conﬁgured<br>from account level.<br>The rule is only<br>NON_COMPLIANT<br>when the ﬁelds set<br>below do not match<br>the corresponding<br>ﬁelds in the conﬁgura<br>tion item.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13947
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.3|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|netfw-policy-defau <br>lt-action-fragment-<br>packets|Ensure that an AWS<br>Network Firewall<br>policy is conﬁgured<br>with a user deﬁned<br>stateless default<br>action for fragmente<br>d packets. The rule<br>is NON_COMPLIANT<br>if stateless default<br>action for fragmente<br>d packets does not<br>match with user<br>deﬁned default<br>action.|
|1.4.3|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|netfw-policy-defau <br>lt-action-fragment-<br>packets|Ensure that an AWS<br>Network Firewall<br>policy is conﬁgured<br>with a user deﬁned<br>stateless default<br>action for fragmente<br>d packets. The rule<br>is NON_COMPLIANT<br>if stateless default<br>action for fragmente<br>d packets does not<br>match with user<br>deﬁned default<br>action.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13948
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.3|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|netfw-policy-default-<br>action-full-packets|Ensure that an AWS<br>Network Firewall<br>policy is conﬁgured<br>with a user deﬁned<br>default stateless<br>action for full<br>packets. This rule is<br>NON_COMPLIANT<br>if default stateless<br>action for full packets<br>does not match with<br>user deﬁned default<br>stateless action.|
|1.4.4|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|api-gw-endpoint-ty <br>pe-check|Ensure that Amazon<br>API Gateway APIs are<br>of the type speciﬁed<br>in the rule parameter<br>'endpointConﬁgura<br>tionType'. The rule<br>returns NON_COMPL<br>IANT if the REST<br>API does not match<br>the endpoint type<br>conﬁgured in the rule<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13949
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.4|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|redshift-enhanced- <br>vpc-routing-enabled|Ensure that Amazon<br>Redshift clusters have<br>'enhancedVpcRoutin<br>g' enabled. The rule is<br>NON_COMPLIANT if<br>'enhancedVpcRoutin<br>g' is not enabled<br>or if the conﬁgura<br>tion.enhancedVpcRo<br>uting ﬁeld is 'false'.|
|1.4.4|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|internet-gateway-a <br>uthorized-vpc-only|Ensure that internet<br>gateways are<br>attached to an<br>authorized virtual<br>private cloud<br>(Amazon VPC). The<br>rule is NON_COMPL<br>IANT if internet<br>gateways are<br>attached to an<br>unauthorized VPC.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13950
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.4.5|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|ecs-task-deﬁnition-<br>pid-mode-check|Ensure that<br>ECSTaskDeﬁnitions<br>are conﬁgured<br>to share a host's<br>process namespace<br>with its Amazon<br>Elastic Container<br>Service (Amazon<br>ECS) containers. The<br>rule is NON_COMPL<br>IANT if the pidMode<br>parameter is set<br>to'host'.|
|1.4.5|Network connections<br>between trusted and<br>untrusted networks<br>are controlled. (PCI-<br>DSS-v4.0)|ec2-launch-template-<br>public-ip-disabled|Ensure that Amazon<br>EC2 Launch<br>Templates are not set<br>to assign public IP<br>addresses to Network<br>Interfaces. The rule<br>is NON_COMPL<br>IANT if the default<br>version of an EC2<br>Launch Template has<br>at least 1 Network<br>Interface with<br>'AssociatePublicIp<br>Address' set to 'true'.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13951
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|api-gw-endpoint-ty <br>pe-check|Ensure that Amazon<br>API Gateway APIs are<br>of the type speciﬁed<br>in the rule parameter<br>'endpointConﬁgura<br>tionType'. The rule<br>returns NON_COMPL<br>IANT if the REST<br>API does not match<br>the endpoint type<br>conﬁgured in the rule<br>parameter.|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|cloudfront-associa <br>ted-with-waf|Ensure that Amazon<br>CloudFront distribut<br>ions are associate<br>d with either web<br>application ﬁrewall<br>(WAF) or WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion is not associated<br>with a WAF web ACL.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13952
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|netfw-policy-defau <br>lt-action-fragment-<br>packets|Ensure that an AWS<br>Network Firewall<br>policy is conﬁgured<br>with a user deﬁned<br>stateless default<br>action for fragmente<br>d packets. The rule<br>is NON_COMPLIANT<br>if stateless default<br>action for fragmente<br>d packets does not<br>match with user<br>deﬁned default<br>action.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13953
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|rds-db-security-gr <br>oup-not-allowed|Ensure that the<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) DB<br>security groups is the<br>default one. The rule<br>is NON_COMPLIANT<br>if there are any DB<br>security groups that<br>are not the default<br>DB security group.|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|ec2-transit-gatewa <br>y-auto-vpc-attach- <br>disabled|Ensure that Amazon<br>Elastic Compute<br>Cloud (Amazon EC2)<br>Transit Gateways do<br>not have 'AutoAcce<br>ptSharedAttachment<br>s' enabled. The rule is<br>NON_COMPLIANT for<br>a Transit Gateway if<br>'AutoAcceptSharedA<br>ttachments' is set to<br>'enable'.|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|eks-endpoint-no-pu <br>blic-access|Ensure that the<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS)<br>endpoint is not<br>publicly accessibl<br>e. The rule is<br>NON_COMPLIANT<br>if the endpoint is<br>publicly accessible.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13954
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|restricted-ssh|Note: For this rule,<br>the rule identiﬁe<br>r (INCOMING<br>_SSH_DISABLED)<br>and rule name<br>(restricted-ssh) are<br>diﬀerent. Ensure<br>that the incoming<br>SSH traﬃc for the<br>security groups is<br>accessible. The rule<br>is COMPLIANT if the<br>IP addresses of the<br>incoming SSH traﬃc<br>in the security groups<br>are restricted (CIDR<br>other than 0.0.0.0/0<br>or ::/0). Otherwise,<br>NON_COMPLIANT.|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|appsync-associated-<br>with-waf|Ensure that AWS<br>AppSync APIs are<br>associated with<br>AWS WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT for<br>an AWS AppSync API<br>if it is not associated<br>with a web ACL.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13955
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|docdb-cluster-snap <br>shot-public-prohib <br>ited|Ensure that Amazon<br>DocumentDB manual<br>cluster snapshots<br>are not public. The<br>rule is NON_COMPL<br>IANT if any Amazon<br>DocumentDB manual<br>cluster snapshots are<br>public.|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|codebuild-project- <br>source-repo-url-check|Ensure that the<br>Bitbucket source<br>repository URL<br>DOES NOT contain<br>sign-in credentials<br>or not. The rule is<br>NON_COMPLIANT if<br>the URL contains any<br>sign-in information<br>and COMPLIANT if it<br>doesn't.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13956
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|emr-block-public-a <br>ccess|Ensure that an<br>account with Amazon<br>EMR has block public<br>access settings<br>enabled. The rule is<br>NON_COMPLIANT if<br>BlockPublicSecurit<br>yGroupRules is false,<br>or if true, ports other<br>than Port 22 are<br>listed in Permitted<br>PublicSecurityGrou<br>pRuleRanges.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13957
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|nacl-no-unrestricted-<br>ssh-rdp|Ensure that default<br>ports for SSH/RDP<br>ingress traﬃc for<br>network access<br>control lists (NACLs)<br>are restricted. The<br>rule is NON_COMPL<br>IANT if a NACL<br>inbound entry allows<br>a source TCP or UDP<br>CIDR block for ports<br>22 or 3389.|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|waf-global-webacl- <br>not-empty|Ensure that a WAF<br>Global Web ACL<br>contains some<br>WAF rules or rule<br>groups. This rule is<br>NON_COMPLIANT if<br>a Web ACL does not<br>contain any WAF rule<br>or rule group.|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|waf-global-rulegro <br>up-not-empty|Ensure that an AWS<br>WAF Classic rule<br>group contains some<br>rules. The rule is<br>NON_COMPLIANT<br>if there are no rules<br>present within a rule<br>group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13958
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|waf-global-rule-not-<br>empty|Ensure that an<br>AWS WAF global<br>rule contains some<br>conditions. The rule<br>is NON_COMPLIANT<br>if no conditions are<br>present within the<br>WAF global rule.|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|ec2-client-vpn-not-<br>authorize-all|Ensure that the<br>AWS Client VPN<br>authorization rules<br>does not authorize<br>connection access for<br>all clients. The rule is<br>NON_COMPLIANT if<br>'AccessAll' is present<br>and set to true.|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|internet-gateway-a <br>uthorized-vpc-only|Ensure that internet<br>gateways are<br>attached to an<br>authorized virtual<br>private cloud<br>(Amazon VPC). The<br>rule is NON_COMPL<br>IANT if internet<br>gateways are<br>attached to an<br>unauthorized VPC.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13959
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|s3-access-point-pu <br>blic-access-blocks|Ensure that Amazon<br>S3 access points have<br>block public access<br>settings enabled. The<br>rule is NON_COMPL<br>IANT if block public<br>access settings are<br>not enabled for S3<br>access points.|
|1.5.1|Risks to the CDE<br>from computing<br>devices that are able<br>to connect to both<br>untrusted networks<br>and the CDE are<br>mitigated. (PCI-DSS-<br>v4.0)|s3-account-level-p <br>ublic-access-blocks|Ensure that the<br>required public<br>access block settings<br>are conﬁgured<br>from account level.<br>The rule is only<br>NON_COMPLIANT<br>when the ﬁelds set<br>below do not match<br>the corresponding<br>ﬁelds in the conﬁgura<br>tion item.|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gwv2-access-lo <br>gs-enabled|Ensure that Amazon<br>API Gateway V2<br>stages have access<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if 'accessLo<br>gSettings' is not<br>present in Stage<br>conﬁguration.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13960
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudfront-accessl <br>ogs-enabled|Ensure that Amazon<br>CloudFront distribut<br>ions are conﬁgure<br>d to deliver access<br>logs to an Amazon<br>S3 bucket. The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion does not have<br>logging conﬁgured.|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|neptune-cluster-cl <br>oudwatch-log-expor <br>t-enabled|Ensure that an<br>Amazon Neptune<br>cluster has<br>CloudWatch log<br>export enabled for<br>audit logs. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have CloudWatc<br>h log export enabled<br>for audit logs.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13961
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|ecs-task-deﬁnition-<br>log-conﬁguration|Ensure that logConﬁg<br>uration is set on<br>active ECS Task<br>Deﬁnitions. This<br>rule is NON_COMPL<br>IANT if an active<br>ECSTaskDeﬁnition<br>does not have the<br>logConﬁguration<br>resource deﬁned<br>or the value for<br>logConﬁguration is<br>null in at least one<br>container deﬁnition.|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudtrail-enabled|Note: For this rule,<br>the rule identiﬁe<br>r (CLOUD_TR<br>AIL_ENABLED) and<br>rule name (cloudtrail-<br>enabled) are diﬀerent<br>. Ensure that an AWS<br>CloudTrail trail is<br>enabled in your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>a trail is not enabled.<br>Optionally, the rule<br>checks a speciﬁc<br>S3 bucket, Amazon<br>Simple Notiﬁcation<br>Service (Amazon SNS)<br>topic, and CloudWatc<br>h log group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13962
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|multi-region-cloud <br>trail-enabled|Note: for this rule,<br>the rule identiﬁe<br>r (MULTI_RE<br>GION_CLOU<br>D_TRAIL_ENABLED)<br>and rule name<br>(multi-region-clou<br>dtrail-enabled) are<br>diﬀerent. Ensure<br>that there is at least<br>one multi-region<br>AWS CloudTrail. The<br>rule is NON_COMPL<br>IANT if the trails<br>do not match input<br>parameters. The rule<br>is NON_COMPLIANT<br>if the ExcludeMa<br>nagementEventSourc<br>es ﬁeld is not empty<br>or if AWS CloudTrai<br>l is conﬁgured to<br>exclude managemen<br>t events such as<br>AWS KMS events or<br>Amazon RDS Data<br>API events.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13963
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|appsync-logging-en <br>abled|Ensure that an AWS<br>AppSync API has<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging is not<br>enabled, or 'ﬁeldLog<br>Level' is neither<br>ERROR nor ALL.|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|waf-classic-logging-<br>enabled|Ensure that logging is<br>enabled on AWS WAF<br>classic global web<br>access control lists<br>(web ACLs). The rule<br>is NON_COMPLIANT<br>for a global web ACL,<br>if it does not have<br>logging enabled.|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-logging-enabled|Ensure that Amazon<br>MQ brokers have<br>Amazon CloudWatc<br>h audit logging<br>enabled. The rule is<br>NON_COMPLIANT<br>if a broker does not<br>have audit logging<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13964
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-log-enabled|Ensure that an<br>Amazon MQ broker<br>has CloudWatch audit<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if the broker<br>does not have audit<br>logging enabled.|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|eks-cluster-logging-<br>enabled|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS) cluster<br>is conﬁgured with<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging for<br>Amazon EKS clusters<br>is not enabled for all<br>log types.|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|elastic-beanstalk- <br>logs-to-cloudwatch|Ensure that AWS<br>Elastic Beanstalk<br>environments<br>are conﬁgured<br>to send logs to<br>Amazon CloudWatc<br>h Logs. The rule<br>is NON_COMPL<br>IANT if the value<br>of `StreamLogs` is<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13965
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|step-functions-sta <br>te-machine-logging-<br>enabled|Ensure that AWS<br>Step Functions<br>machine has logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a state machine does<br>not have logging<br>enabled or the<br>logging conﬁgura<br>tion is not at the<br>minimum level<br>provided.|
|10.2.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|netfw-logging-enab <br>led|Ensure that AWS<br>Network Firewall<br>ﬁrewalls have logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a logging type is not<br>conﬁgured. You can<br>specify which logging<br>type you want the<br>rule to check.|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gwv2-access-lo <br>gs-enabled|Ensure that Amazon<br>API Gateway V2<br>stages have access<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if 'accessLo<br>gSettings' is not<br>present in Stage<br>conﬁguration.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13966
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudfront-accessl <br>ogs-enabled|Ensure that Amazon<br>CloudFront distribut<br>ions are conﬁgure<br>d to deliver access<br>logs to an Amazon<br>S3 bucket. The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion does not have<br>logging conﬁgured.|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|neptune-cluster-cl <br>oudwatch-log-expor <br>t-enabled|Ensure that an<br>Amazon Neptune<br>cluster has<br>CloudWatch log<br>export enabled for<br>audit logs. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have CloudWatc<br>h log export enabled<br>for audit logs.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13967
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|ec2-instance-detai <br>led-monitoring-ena <br>bled|Ensure that detailed<br>monitoring is<br>enabled for EC2<br>instances. The rule is<br>NON_COMPLIANT if<br>detailed monitoring<br>is not enabled.|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|ecs-task-deﬁnition-<br>log-conﬁguration|Ensure that logConﬁg<br>uration is set on<br>active ECS Task<br>Deﬁnitions. This<br>rule is NON_COMPL<br>IANT if an active<br>ECSTaskDeﬁnition<br>does not have the<br>logConﬁguration<br>resource deﬁned<br>or the value for<br>logConﬁguration is<br>null in at least one<br>container deﬁnition.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13968
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13969
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-r <br>esource-check|Ensure that a<br>resource type has a<br>CloudWatch alarm<br>for the named metric.<br>For resource type,<br>you can specify<br>EBS volumes, EC2<br>instances, Amazon<br>RDS clusters, or S3<br>buckets. The rule is<br>COMPLIANT if the<br>named metric has<br>a resource ID and<br>CloudWatch alarm.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13970
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudtrail-enabled|Note: For this rule,<br>the rule identiﬁe<br>r (CLOUD_TR<br>AIL_ENABLED) and<br>rule name (cloudtrail-<br>enabled) are diﬀerent<br>. Ensure that an AWS<br>CloudTrail trail is<br>enabled in your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>a trail is not enabled.<br>Optionally, the rule<br>checks a speciﬁc<br>S3 bucket, Amazon<br>Simple Notiﬁcation<br>Service (Amazon SNS)<br>topic, and CloudWatc<br>h log group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13971
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|multi-region-cloud <br>trail-enabled|Note: for this rule,<br>the rule identiﬁe<br>r (MULTI_RE<br>GION_CLOU<br>D_TRAIL_ENABLED)<br>and rule name<br>(multi-region-clou<br>dtrail-enabled) are<br>diﬀerent. Ensure<br>that there is at least<br>one multi-region<br>AWS CloudTrail. The<br>rule is NON_COMPL<br>IANT if the trails<br>do not match input<br>parameters. The rule<br>is NON_COMPLIANT<br>if the ExcludeMa<br>nagementEventSourc<br>es ﬁeld is not empty<br>or if AWS CloudTrai<br>l is conﬁgured to<br>exclude managemen<br>t events such as<br>AWS KMS events or<br>Amazon RDS Data<br>API events.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13972
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|appsync-logging-en <br>abled|Ensure that an AWS<br>AppSync API has<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging is not<br>enabled, or 'ﬁeldLog<br>Level' is neither<br>ERROR nor ALL.|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|waf-classic-logging-<br>enabled|Ensure that logging is<br>enabled on AWS WAF<br>classic global web<br>access control lists<br>(web ACLs). The rule<br>is NON_COMPLIANT<br>for a global web ACL,<br>if it does not have<br>logging enabled.|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-logging-enabled|Ensure that Amazon<br>MQ brokers have<br>Amazon CloudWatc<br>h audit logging<br>enabled. The rule is<br>NON_COMPLIANT<br>if a broker does not<br>have audit logging<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13973
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-log-enabled|Ensure that an<br>Amazon MQ broker<br>has CloudWatch audit<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if the broker<br>does not have audit<br>logging enabled.|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|eks-cluster-logging-<br>enabled|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS) cluster<br>is conﬁgured with<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging for<br>Amazon EKS clusters<br>is not enabled for all<br>log types.|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|elastic-beanstalk- <br>logs-to-cloudwatch|Ensure that AWS<br>Elastic Beanstalk<br>environments<br>are conﬁgured<br>to send logs to<br>Amazon CloudWatc<br>h Logs. The rule<br>is NON_COMPL<br>IANT if the value<br>of `StreamLogs` is<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13974
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|wafv2-rulegroup-lo <br>gging-enabled|Ensure that Amazon<br>CloudWatch security<br>metrics collectio<br>n on AWS WAFv2<br>rule groups is<br>enabled. The rule is<br>NON_COMPLIANT if<br>the 'VisibilityConﬁg.<br>CloudWatchMetricsE<br>nabled' ﬁeld is set to<br>false.|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|sns-topic-message- <br>delivery-notiﬁcation-<br>enabled|Ensure that Amazon<br>Simple Notiﬁcation<br>Service (SNS) logging<br>is enabled for the<br>delivery status of<br>notiﬁcation messages<br>sent to a topic for<br>the endpoints. The<br>rule is NON_COMPL<br>IANT if the delivery<br>status notiﬁcation<br>for messages is not<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13975
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|step-functions-sta <br>te-machine-logging-<br>enabled|Ensure that AWS<br>Step Functions<br>machine has logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a state machine does<br>not have logging<br>enabled or the<br>logging conﬁgura<br>tion is not at the<br>minimum level<br>provided.|
|10.2.1.1|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|netfw-logging-enab <br>led|Ensure that AWS<br>Network Firewall<br>ﬁrewalls have logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a logging type is not<br>conﬁgured. You can<br>specify which logging<br>type you want the<br>rule to check.|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gwv2-access-lo <br>gs-enabled|Ensure that Amazon<br>API Gateway V2<br>stages have access<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if 'accessLo<br>gSettings' is not<br>present in Stage<br>conﬁguration.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13976
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudfront-accessl <br>ogs-enabled|Ensure that Amazon<br>CloudFront distribut<br>ions are conﬁgure<br>d to deliver access<br>logs to an Amazon<br>S3 bucket. The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion does not have<br>logging conﬁgured.|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|neptune-cluster-cl <br>oudwatch-log-expor <br>t-enabled|Ensure that an<br>Amazon Neptune<br>cluster has<br>CloudWatch log<br>export enabled for<br>audit logs. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have CloudWatc<br>h log export enabled<br>for audit logs.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13977
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|ecs-task-deﬁnition-<br>log-conﬁguration|Ensure that logConﬁg<br>uration is set on<br>active ECS Task<br>Deﬁnitions. This<br>rule is NON_COMPL<br>IANT if an active<br>ECSTaskDeﬁnition<br>does not have the<br>logConﬁguration<br>resource deﬁned<br>or the value for<br>logConﬁguration is<br>null in at least one<br>container deﬁnition.|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudtrail-enabled|Note: For this rule,<br>the rule identiﬁe<br>r (CLOUD_TR<br>AIL_ENABLED) and<br>rule name (cloudtrail-<br>enabled) are diﬀerent<br>. Ensure that an AWS<br>CloudTrail trail is<br>enabled in your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>a trail is not enabled.<br>Optionally, the rule<br>checks a speciﬁc<br>S3 bucket, Amazon<br>Simple Notiﬁcation<br>Service (Amazon SNS)<br>topic, and CloudWatc<br>h log group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13978
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|multi-region-cloud <br>trail-enabled|Note: for this rule,<br>the rule identiﬁe<br>r (MULTI_RE<br>GION_CLOU<br>D_TRAIL_ENABLED)<br>and rule name<br>(multi-region-clou<br>dtrail-enabled) are<br>diﬀerent. Ensure<br>that there is at least<br>one multi-region<br>AWS CloudTrail. The<br>rule is NON_COMPL<br>IANT if the trails<br>do not match input<br>parameters. The rule<br>is NON_COMPLIANT<br>if the ExcludeMa<br>nagementEventSourc<br>es ﬁeld is not empty<br>or if AWS CloudTrai<br>l is conﬁgured to<br>exclude managemen<br>t events such as<br>AWS KMS events or<br>Amazon RDS Data<br>API events.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13979
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|appsync-logging-en <br>abled|Ensure that an AWS<br>AppSync API has<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging is not<br>enabled, or 'ﬁeldLog<br>Level' is neither<br>ERROR nor ALL.|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|waf-classic-logging-<br>enabled|Ensure that logging is<br>enabled on AWS WAF<br>classic global web<br>access control lists<br>(web ACLs). The rule<br>is NON_COMPLIANT<br>for a global web ACL,<br>if it does not have<br>logging enabled.|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-logging-enabled|Ensure that Amazon<br>MQ brokers have<br>Amazon CloudWatc<br>h audit logging<br>enabled. The rule is<br>NON_COMPLIANT<br>if a broker does not<br>have audit logging<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13980
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-log-enabled|Ensure that an<br>Amazon MQ broker<br>has CloudWatch audit<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if the broker<br>does not have audit<br>logging enabled.|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|eks-cluster-logging-<br>enabled|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS) cluster<br>is conﬁgured with<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging for<br>Amazon EKS clusters<br>is not enabled for all<br>log types.|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|elastic-beanstalk- <br>logs-to-cloudwatch|Ensure that AWS<br>Elastic Beanstalk<br>environments<br>are conﬁgured<br>to send logs to<br>Amazon CloudWatc<br>h Logs. The rule<br>is NON_COMPL<br>IANT if the value<br>of `StreamLogs` is<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13981
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|step-functions-sta <br>te-machine-logging-<br>enabled|Ensure that AWS<br>Step Functions<br>machine has logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a state machine does<br>not have logging<br>enabled or the<br>logging conﬁgura<br>tion is not at the<br>minimum level<br>provided.|
|10.2.1.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|netfw-logging-enab <br>led|Ensure that AWS<br>Network Firewall<br>ﬁrewalls have logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a logging type is not<br>conﬁgured. You can<br>specify which logging<br>type you want the<br>rule to check.|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gwv2-access-lo <br>gs-enabled|Ensure that Amazon<br>API Gateway V2<br>stages have access<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if 'accessLo<br>gSettings' is not<br>present in Stage<br>conﬁguration.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13982
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudfront-accessl <br>ogs-enabled|Ensure that Amazon<br>CloudFront distribut<br>ions are conﬁgure<br>d to deliver access<br>logs to an Amazon<br>S3 bucket. The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion does not have<br>logging conﬁgured.|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|neptune-cluster-cl <br>oudwatch-log-expor <br>t-enabled|Ensure that an<br>Amazon Neptune<br>cluster has<br>CloudWatch log<br>export enabled for<br>audit logs. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have CloudWatc<br>h log export enabled<br>for audit logs.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13983
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|ecs-task-deﬁnition-<br>log-conﬁguration|Ensure that logConﬁg<br>uration is set on<br>active ECS Task<br>Deﬁnitions. This<br>rule is NON_COMPL<br>IANT if an active<br>ECSTaskDeﬁnition<br>does not have the<br>logConﬁguration<br>resource deﬁned<br>or the value for<br>logConﬁguration is<br>null in at least one<br>container deﬁnition.|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudtrail-enabled|Note: For this rule,<br>the rule identiﬁe<br>r (CLOUD_TR<br>AIL_ENABLED) and<br>rule name (cloudtrail-<br>enabled) are diﬀerent<br>. Ensure that an AWS<br>CloudTrail trail is<br>enabled in your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>a trail is not enabled.<br>Optionally, the rule<br>checks a speciﬁc<br>S3 bucket, Amazon<br>Simple Notiﬁcation<br>Service (Amazon SNS)<br>topic, and CloudWatc<br>h log group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13984
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|multi-region-cloud <br>trail-enabled|Note: for this rule,<br>the rule identiﬁe<br>r (MULTI_RE<br>GION_CLOU<br>D_TRAIL_ENABLED)<br>and rule name<br>(multi-region-clou<br>dtrail-enabled) are<br>diﬀerent. Ensure<br>that there is at least<br>one multi-region<br>AWS CloudTrail. The<br>rule is NON_COMPL<br>IANT if the trails<br>do not match input<br>parameters. The rule<br>is NON_COMPLIANT<br>if the ExcludeMa<br>nagementEventSourc<br>es ﬁeld is not empty<br>or if AWS CloudTrai<br>l is conﬁgured to<br>exclude managemen<br>t events such as<br>AWS KMS events or<br>Amazon RDS Data<br>API events.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13985
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|appsync-logging-en <br>abled|Ensure that an AWS<br>AppSync API has<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging is not<br>enabled, or 'ﬁeldLog<br>Level' is neither<br>ERROR nor ALL.|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|waf-classic-logging-<br>enabled|Ensure that logging is<br>enabled on AWS WAF<br>classic global web<br>access control lists<br>(web ACLs). The rule<br>is NON_COMPLIANT<br>for a global web ACL,<br>if it does not have<br>logging enabled.|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-logging-enabled|Ensure that Amazon<br>MQ brokers have<br>Amazon CloudWatc<br>h audit logging<br>enabled. The rule is<br>NON_COMPLIANT<br>if a broker does not<br>have audit logging<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13986
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-log-enabled|Ensure that an<br>Amazon MQ broker<br>has CloudWatch audit<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if the broker<br>does not have audit<br>logging enabled.|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|eks-cluster-logging-<br>enabled|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS) cluster<br>is conﬁgured with<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging for<br>Amazon EKS clusters<br>is not enabled for all<br>log types.|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|elastic-beanstalk- <br>logs-to-cloudwatch|Ensure that AWS<br>Elastic Beanstalk<br>environments<br>are conﬁgured<br>to send logs to<br>Amazon CloudWatc<br>h Logs. The rule<br>is NON_COMPL<br>IANT if the value<br>of `StreamLogs` is<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13987
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|step-functions-sta <br>te-machine-logging-<br>enabled|Ensure that AWS<br>Step Functions<br>machine has logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a state machine does<br>not have logging<br>enabled or the<br>logging conﬁgura<br>tion is not at the<br>minimum level<br>provided.|
|10.2.1.3|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|netfw-logging-enab <br>led|Ensure that AWS<br>Network Firewall<br>ﬁrewalls have logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a logging type is not<br>conﬁgured. You can<br>specify which logging<br>type you want the<br>rule to check.|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gwv2-access-lo <br>gs-enabled|Ensure that Amazon<br>API Gateway V2<br>stages have access<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if 'accessLo<br>gSettings' is not<br>present in Stage<br>conﬁguration.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13988
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudfront-accessl <br>ogs-enabled|Ensure that Amazon<br>CloudFront distribut<br>ions are conﬁgure<br>d to deliver access<br>logs to an Amazon<br>S3 bucket. The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion does not have<br>logging conﬁgured.|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|neptune-cluster-cl <br>oudwatch-log-expor <br>t-enabled|Ensure that an<br>Amazon Neptune<br>cluster has<br>CloudWatch log<br>export enabled for<br>audit logs. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have CloudWatc<br>h log export enabled<br>for audit logs.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13989
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|ecs-task-deﬁnition-<br>log-conﬁguration|Ensure that logConﬁg<br>uration is set on<br>active ECS Task<br>Deﬁnitions. This<br>rule is NON_COMPL<br>IANT if an active<br>ECSTaskDeﬁnition<br>does not have the<br>logConﬁguration<br>resource deﬁned<br>or the value for<br>logConﬁguration is<br>null in at least one<br>container deﬁnition.|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudtrail-enabled|Note: For this rule,<br>the rule identiﬁe<br>r (CLOUD_TR<br>AIL_ENABLED) and<br>rule name (cloudtrail-<br>enabled) are diﬀerent<br>. Ensure that an AWS<br>CloudTrail trail is<br>enabled in your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>a trail is not enabled.<br>Optionally, the rule<br>checks a speciﬁc<br>S3 bucket, Amazon<br>Simple Notiﬁcation<br>Service (Amazon SNS)<br>topic, and CloudWatc<br>h log group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13990
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|multi-region-cloud <br>trail-enabled|Note: for this rule,<br>the rule identiﬁe<br>r (MULTI_RE<br>GION_CLOU<br>D_TRAIL_ENABLED)<br>and rule name<br>(multi-region-clou<br>dtrail-enabled) are<br>diﬀerent. Ensure<br>that there is at least<br>one multi-region<br>AWS CloudTrail. The<br>rule is NON_COMPL<br>IANT if the trails<br>do not match input<br>parameters. The rule<br>is NON_COMPLIANT<br>if the ExcludeMa<br>nagementEventSourc<br>es ﬁeld is not empty<br>or if AWS CloudTrai<br>l is conﬁgured to<br>exclude managemen<br>t events such as<br>AWS KMS events or<br>Amazon RDS Data<br>API events.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13991
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|appsync-logging-en <br>abled|Ensure that an AWS<br>AppSync API has<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging is not<br>enabled, or 'ﬁeldLog<br>Level' is neither<br>ERROR nor ALL.|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|waf-classic-logging-<br>enabled|Ensure that logging is<br>enabled on AWS WAF<br>classic global web<br>access control lists<br>(web ACLs). The rule<br>is NON_COMPLIANT<br>for a global web ACL,<br>if it does not have<br>logging enabled.|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-logging-enabled|Ensure that Amazon<br>MQ brokers have<br>Amazon CloudWatc<br>h audit logging<br>enabled. The rule is<br>NON_COMPLIANT<br>if a broker does not<br>have audit logging<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13992
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-log-enabled|Ensure that an<br>Amazon MQ broker<br>has CloudWatch audit<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if the broker<br>does not have audit<br>logging enabled.|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|eks-cluster-logging-<br>enabled|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS) cluster<br>is conﬁgured with<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging for<br>Amazon EKS clusters<br>is not enabled for all<br>log types.|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|elastic-beanstalk- <br>logs-to-cloudwatch|Ensure that AWS<br>Elastic Beanstalk<br>environments<br>are conﬁgured<br>to send logs to<br>Amazon CloudWatc<br>h Logs. The rule<br>is NON_COMPL<br>IANT if the value<br>of `StreamLogs` is<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13993
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|step-functions-sta <br>te-machine-logging-<br>enabled|Ensure that AWS<br>Step Functions<br>machine has logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a state machine does<br>not have logging<br>enabled or the<br>logging conﬁgura<br>tion is not at the<br>minimum level<br>provided.|
|10.2.1.4|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|netfw-logging-enab <br>led|Ensure that AWS<br>Network Firewall<br>ﬁrewalls have logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a logging type is not<br>conﬁgured. You can<br>specify which logging<br>type you want the<br>rule to check.|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gwv2-access-lo <br>gs-enabled|Ensure that Amazon<br>API Gateway V2<br>stages have access<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if 'accessLo<br>gSettings' is not<br>present in Stage<br>conﬁguration.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13994
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudfront-accessl <br>ogs-enabled|Ensure that Amazon<br>CloudFront distribut<br>ions are conﬁgure<br>d to deliver access<br>logs to an Amazon<br>S3 bucket. The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion does not have<br>logging conﬁgured.|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|neptune-cluster-cl <br>oudwatch-log-expor <br>t-enabled|Ensure that an<br>Amazon Neptune<br>cluster has<br>CloudWatch log<br>export enabled for<br>audit logs. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have CloudWatc<br>h log export enabled<br>for audit logs.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13995
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|ecs-task-deﬁnition-<br>log-conﬁguration|Ensure that logConﬁg<br>uration is set on<br>active ECS Task<br>Deﬁnitions. This<br>rule is NON_COMPL<br>IANT if an active<br>ECSTaskDeﬁnition<br>does not have the<br>logConﬁguration<br>resource deﬁned<br>or the value for<br>logConﬁguration is<br>null in at least one<br>container deﬁnition.|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudtrail-enabled|Note: For this rule,<br>the rule identiﬁe<br>r (CLOUD_TR<br>AIL_ENABLED) and<br>rule name (cloudtrail-<br>enabled) are diﬀerent<br>. Ensure that an AWS<br>CloudTrail trail is<br>enabled in your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>a trail is not enabled.<br>Optionally, the rule<br>checks a speciﬁc<br>S3 bucket, Amazon<br>Simple Notiﬁcation<br>Service (Amazon SNS)<br>topic, and CloudWatc<br>h log group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13996
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|multi-region-cloud <br>trail-enabled|Note: for this rule,<br>the rule identiﬁe<br>r (MULTI_RE<br>GION_CLOU<br>D_TRAIL_ENABLED)<br>and rule name<br>(multi-region-clou<br>dtrail-enabled) are<br>diﬀerent. Ensure<br>that there is at least<br>one multi-region<br>AWS CloudTrail. The<br>rule is NON_COMPL<br>IANT if the trails<br>do not match input<br>parameters. The rule<br>is NON_COMPLIANT<br>if the ExcludeMa<br>nagementEventSourc<br>es ﬁeld is not empty<br>or if AWS CloudTrai<br>l is conﬁgured to<br>exclude managemen<br>t events such as<br>AWS KMS events or<br>Amazon RDS Data<br>API events.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13997
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|appsync-logging-en <br>abled|Ensure that an AWS<br>AppSync API has<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging is not<br>enabled, or 'ﬁeldLog<br>Level' is neither<br>ERROR nor ALL.|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|waf-classic-logging-<br>enabled|Ensure that logging is<br>enabled on AWS WAF<br>classic global web<br>access control lists<br>(web ACLs). The rule<br>is NON_COMPLIANT<br>for a global web ACL,<br>if it does not have<br>logging enabled.|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-logging-enabled|Ensure that Amazon<br>MQ brokers have<br>Amazon CloudWatc<br>h audit logging<br>enabled. The rule is<br>NON_COMPLIANT<br>if a broker does not<br>have audit logging<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13998
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-log-enabled|Ensure that an<br>Amazon MQ broker<br>has CloudWatch audit<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if the broker<br>does not have audit<br>logging enabled.|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|eks-cluster-logging-<br>enabled|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS) cluster<br>is conﬁgured with<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging for<br>Amazon EKS clusters<br>is not enabled for all<br>log types.|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|elastic-beanstalk- <br>logs-to-cloudwatch|Ensure that AWS<br>Elastic Beanstalk<br>environments<br>are conﬁgured<br>to send logs to<br>Amazon CloudWatc<br>h Logs. The rule<br>is NON_COMPL<br>IANT if the value<br>of `StreamLogs` is<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 13999
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|step-functions-sta <br>te-machine-logging-<br>enabled|Ensure that AWS<br>Step Functions<br>machine has logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a state machine does<br>not have logging<br>enabled or the<br>logging conﬁgura<br>tion is not at the<br>minimum level<br>provided.|
|10.2.1.5|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|netfw-logging-enab <br>led|Ensure that AWS<br>Network Firewall<br>ﬁrewalls have logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a logging type is not<br>conﬁgured. You can<br>specify which logging<br>type you want the<br>rule to check.|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gwv2-access-lo <br>gs-enabled|Ensure that Amazon<br>API Gateway V2<br>stages have access<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if 'accessLo<br>gSettings' is not<br>present in Stage<br>conﬁguration.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14000
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudfront-accessl <br>ogs-enabled|Ensure that Amazon<br>CloudFront distribut<br>ions are conﬁgure<br>d to deliver access<br>logs to an Amazon<br>S3 bucket. The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion does not have<br>logging conﬁgured.|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|neptune-cluster-cl <br>oudwatch-log-expor <br>t-enabled|Ensure that an<br>Amazon Neptune<br>cluster has<br>CloudWatch log<br>export enabled for<br>audit logs. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have CloudWatc<br>h log export enabled<br>for audit logs.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14001
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|ecs-task-deﬁnition-<br>log-conﬁguration|Ensure that logConﬁg<br>uration is set on<br>active ECS Task<br>Deﬁnitions. This<br>rule is NON_COMPL<br>IANT if an active<br>ECSTaskDeﬁnition<br>does not have the<br>logConﬁguration<br>resource deﬁned<br>or the value for<br>logConﬁguration is<br>null in at least one<br>container deﬁnition.|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudtrail-enabled|Note: For this rule,<br>the rule identiﬁe<br>r (CLOUD_TR<br>AIL_ENABLED) and<br>rule name (cloudtrail-<br>enabled) are diﬀerent<br>. Ensure that an AWS<br>CloudTrail trail is<br>enabled in your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>a trail is not enabled.<br>Optionally, the rule<br>checks a speciﬁc<br>S3 bucket, Amazon<br>Simple Notiﬁcation<br>Service (Amazon SNS)<br>topic, and CloudWatc<br>h log group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14002
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|multi-region-cloud <br>trail-enabled|Note: for this rule,<br>the rule identiﬁe<br>r (MULTI_RE<br>GION_CLOU<br>D_TRAIL_ENABLED)<br>and rule name<br>(multi-region-clou<br>dtrail-enabled) are<br>diﬀerent. Ensure<br>that there is at least<br>one multi-region<br>AWS CloudTrail. The<br>rule is NON_COMPL<br>IANT if the trails<br>do not match input<br>parameters. The rule<br>is NON_COMPLIANT<br>if the ExcludeMa<br>nagementEventSourc<br>es ﬁeld is not empty<br>or if AWS CloudTrai<br>l is conﬁgured to<br>exclude managemen<br>t events such as<br>AWS KMS events or<br>Amazon RDS Data<br>API events.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14003
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|appsync-logging-en <br>abled|Ensure that an AWS<br>AppSync API has<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging is not<br>enabled, or 'ﬁeldLog<br>Level' is neither<br>ERROR nor ALL.|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|waf-classic-logging-<br>enabled|Ensure that logging is<br>enabled on AWS WAF<br>classic global web<br>access control lists<br>(web ACLs). The rule<br>is NON_COMPLIANT<br>for a global web ACL,<br>if it does not have<br>logging enabled.|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-logging-enabled|Ensure that Amazon<br>MQ brokers have<br>Amazon CloudWatc<br>h audit logging<br>enabled. The rule is<br>NON_COMPLIANT<br>if a broker does not<br>have audit logging<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14004
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-log-enabled|Ensure that an<br>Amazon MQ broker<br>has CloudWatch audit<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if the broker<br>does not have audit<br>logging enabled.|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|eks-cluster-logging-<br>enabled|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS) cluster<br>is conﬁgured with<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging for<br>Amazon EKS clusters<br>is not enabled for all<br>log types.|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|elastic-beanstalk- <br>logs-to-cloudwatch|Ensure that AWS<br>Elastic Beanstalk<br>environments<br>are conﬁgured<br>to send logs to<br>Amazon CloudWatc<br>h Logs. The rule<br>is NON_COMPL<br>IANT if the value<br>of `StreamLogs` is<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14005
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|step-functions-sta <br>te-machine-logging-<br>enabled|Ensure that AWS<br>Step Functions<br>machine has logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a state machine does<br>not have logging<br>enabled or the<br>logging conﬁgura<br>tion is not at the<br>minimum level<br>provided.|
|10.2.1.6|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|netfw-logging-enab <br>led|Ensure that AWS<br>Network Firewall<br>ﬁrewalls have logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a logging type is not<br>conﬁgured. You can<br>specify which logging<br>type you want the<br>rule to check.|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gwv2-access-lo <br>gs-enabled|Ensure that Amazon<br>API Gateway V2<br>stages have access<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if 'accessLo<br>gSettings' is not<br>present in Stage<br>conﬁguration.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14006
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudfront-accessl <br>ogs-enabled|Ensure that Amazon<br>CloudFront distribut<br>ions are conﬁgure<br>d to deliver access<br>logs to an Amazon<br>S3 bucket. The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion does not have<br>logging conﬁgured.|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|neptune-cluster-cl <br>oudwatch-log-expor <br>t-enabled|Ensure that an<br>Amazon Neptune<br>cluster has<br>CloudWatch log<br>export enabled for<br>audit logs. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have CloudWatc<br>h log export enabled<br>for audit logs.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14007
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|ecs-task-deﬁnition-<br>log-conﬁguration|Ensure that logConﬁg<br>uration is set on<br>active ECS Task<br>Deﬁnitions. This<br>rule is NON_COMPL<br>IANT if an active<br>ECSTaskDeﬁnition<br>does not have the<br>logConﬁguration<br>resource deﬁned<br>or the value for<br>logConﬁguration is<br>null in at least one<br>container deﬁnition.|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudtrail-enabled|Note: For this rule,<br>the rule identiﬁe<br>r (CLOUD_TR<br>AIL_ENABLED) and<br>rule name (cloudtrail-<br>enabled) are diﬀerent<br>. Ensure that an AWS<br>CloudTrail trail is<br>enabled in your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>a trail is not enabled.<br>Optionally, the rule<br>checks a speciﬁc<br>S3 bucket, Amazon<br>Simple Notiﬁcation<br>Service (Amazon SNS)<br>topic, and CloudWatc<br>h log group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14008
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|multi-region-cloud <br>trail-enabled|Note: for this rule,<br>the rule identiﬁe<br>r (MULTI_RE<br>GION_CLOU<br>D_TRAIL_ENABLED)<br>and rule name<br>(multi-region-clou<br>dtrail-enabled) are<br>diﬀerent. Ensure<br>that there is at least<br>one multi-region<br>AWS CloudTrail. The<br>rule is NON_COMPL<br>IANT if the trails<br>do not match input<br>parameters. The rule<br>is NON_COMPLIANT<br>if the ExcludeMa<br>nagementEventSourc<br>es ﬁeld is not empty<br>or if AWS CloudTrai<br>l is conﬁgured to<br>exclude managemen<br>t events such as<br>AWS KMS events or<br>Amazon RDS Data<br>API events.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14009
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|appsync-logging-en <br>abled|Ensure that an AWS<br>AppSync API has<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging is not<br>enabled, or 'ﬁeldLog<br>Level' is neither<br>ERROR nor ALL.|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|waf-classic-logging-<br>enabled|Ensure that logging is<br>enabled on AWS WAF<br>classic global web<br>access control lists<br>(web ACLs). The rule<br>is NON_COMPLIANT<br>for a global web ACL,<br>if it does not have<br>logging enabled.|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-logging-enabled|Ensure that Amazon<br>MQ brokers have<br>Amazon CloudWatc<br>h audit logging<br>enabled. The rule is<br>NON_COMPLIANT<br>if a broker does not<br>have audit logging<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14010
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-log-enabled|Ensure that an<br>Amazon MQ broker<br>has CloudWatch audit<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if the broker<br>does not have audit<br>logging enabled.|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|eks-cluster-logging-<br>enabled|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS) cluster<br>is conﬁgured with<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging for<br>Amazon EKS clusters<br>is not enabled for all<br>log types.|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|elastic-beanstalk- <br>logs-to-cloudwatch|Ensure that AWS<br>Elastic Beanstalk<br>environments<br>are conﬁgured<br>to send logs to<br>Amazon CloudWatc<br>h Logs. The rule<br>is NON_COMPL<br>IANT if the value<br>of `StreamLogs` is<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14011
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|step-functions-sta <br>te-machine-logging-<br>enabled|Ensure that AWS<br>Step Functions<br>machine has logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a state machine does<br>not have logging<br>enabled or the<br>logging conﬁgura<br>tion is not at the<br>minimum level<br>provided.|
|10.2.1.7|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|netfw-logging-enab <br>led|Ensure that AWS<br>Network Firewall<br>ﬁrewalls have logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a logging type is not<br>conﬁgured. You can<br>specify which logging<br>type you want the<br>rule to check.|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gwv2-access-lo <br>gs-enabled|Ensure that Amazon<br>API Gateway V2<br>stages have access<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if 'accessLo<br>gSettings' is not<br>present in Stage<br>conﬁguration.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14012
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudfront-accessl <br>ogs-enabled|Ensure that Amazon<br>CloudFront distribut<br>ions are conﬁgure<br>d to deliver access<br>logs to an Amazon<br>S3 bucket. The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion does not have<br>logging conﬁgured.|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|neptune-cluster-cl <br>oudwatch-log-expor <br>t-enabled|Ensure that an<br>Amazon Neptune<br>cluster has<br>CloudWatch log<br>export enabled for<br>audit logs. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have CloudWatc<br>h log export enabled<br>for audit logs.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14013
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|ecs-task-deﬁnition-<br>log-conﬁguration|Ensure that logConﬁg<br>uration is set on<br>active ECS Task<br>Deﬁnitions. This<br>rule is NON_COMPL<br>IANT if an active<br>ECSTaskDeﬁnition<br>does not have the<br>logConﬁguration<br>resource deﬁned<br>or the value for<br>logConﬁguration is<br>null in at least one<br>container deﬁnition.|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|cloudtrail-enabled|Note: For this rule,<br>the rule identiﬁe<br>r (CLOUD_TR<br>AIL_ENABLED) and<br>rule name (cloudtrail-<br>enabled) are diﬀerent<br>. Ensure that an AWS<br>CloudTrail trail is<br>enabled in your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>a trail is not enabled.<br>Optionally, the rule<br>checks a speciﬁc<br>S3 bucket, Amazon<br>Simple Notiﬁcation<br>Service (Amazon SNS)<br>topic, and CloudWatc<br>h log group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14014
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|multi-region-cloud <br>trail-enabled|Note: for this rule,<br>the rule identiﬁe<br>r (MULTI_RE<br>GION_CLOU<br>D_TRAIL_ENABLED)<br>and rule name<br>(multi-region-clou<br>dtrail-enabled) are<br>diﬀerent. Ensure<br>that there is at least<br>one multi-region<br>AWS CloudTrail. The<br>rule is NON_COMPL<br>IANT if the trails<br>do not match input<br>parameters. The rule<br>is NON_COMPLIANT<br>if the ExcludeMa<br>nagementEventSourc<br>es ﬁeld is not empty<br>or if AWS CloudTrai<br>l is conﬁgured to<br>exclude managemen<br>t events such as<br>AWS KMS events or<br>Amazon RDS Data<br>API events.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14015
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|appsync-logging-en <br>abled|Ensure that an AWS<br>AppSync API has<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging is not<br>enabled, or 'ﬁeldLog<br>Level' is neither<br>ERROR nor ALL.|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|waf-classic-logging-<br>enabled|Ensure that logging is<br>enabled on AWS WAF<br>classic global web<br>access control lists<br>(web ACLs). The rule<br>is NON_COMPLIANT<br>for a global web ACL,<br>if it does not have<br>logging enabled.|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-logging-enabled|Ensure that Amazon<br>MQ brokers have<br>Amazon CloudWatc<br>h audit logging<br>enabled. The rule is<br>NON_COMPLIANT<br>if a broker does not<br>have audit logging<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14016
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|mq-cloudwatch-audi <br>t-log-enabled|Ensure that an<br>Amazon MQ broker<br>has CloudWatch audit<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if the broker<br>does not have audit<br>logging enabled.|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|eks-cluster-logging-<br>enabled|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS) cluster<br>is conﬁgured with<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging for<br>Amazon EKS clusters<br>is not enabled for all<br>log types.|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|elastic-beanstalk- <br>logs-to-cloudwatch|Ensure that AWS<br>Elastic Beanstalk<br>environments<br>are conﬁgured<br>to send logs to<br>Amazon CloudWatc<br>h Logs. The rule<br>is NON_COMPL<br>IANT if the value<br>of `StreamLogs` is<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14017
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|step-functions-sta <br>te-machine-logging-<br>enabled|Ensure that AWS<br>Step Functions<br>machine has logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a state machine does<br>not have logging<br>enabled or the<br>logging conﬁgura<br>tion is not at the<br>minimum level<br>provided.|
|10.2.2|Audit logs are<br>implemented to<br>support the detection<br>of anomalies and<br>suspicious activity,<br>and the forensic<br>analysis of events.<br>(PCI-DSS-v4.0)|netfw-logging-enab <br>led|Ensure that AWS<br>Network Firewall<br>ﬁrewalls have logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a logging type is not<br>conﬁgured. You can<br>specify which logging<br>type you want the<br>rule to check.|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|api-gwv2-access-lo <br>gs-enabled|Ensure that Amazon<br>API Gateway V2<br>stages have access<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if 'accessLo<br>gSettings' is not<br>present in Stage<br>conﬁguration.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14018
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|cloudfront-accessl <br>ogs-enabled|Ensure that Amazon<br>CloudFront distribut<br>ions are conﬁgure<br>d to deliver access<br>logs to an Amazon<br>S3 bucket. The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion does not have<br>logging conﬁgured.|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|neptune-cluster-cl <br>oudwatch-log-expor <br>t-enabled|Ensure that an<br>Amazon Neptune<br>cluster has<br>CloudWatch log<br>export enabled for<br>audit logs. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have CloudWatc<br>h log export enabled<br>for audit logs.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14019
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|ecs-task-deﬁnition-<br>log-conﬁguration|Ensure that logConﬁg<br>uration is set on<br>active ECS Task<br>Deﬁnitions. This<br>rule is NON_COMPL<br>IANT if an active<br>ECSTaskDeﬁnition<br>does not have the<br>logConﬁguration<br>resource deﬁned<br>or the value for<br>logConﬁguration is<br>null in at least one<br>container deﬁnition.|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|cloudtrail-enabled|Note: For this rule,<br>the rule identiﬁe<br>r (CLOUD_TR<br>AIL_ENABLED) and<br>rule name (cloudtrail-<br>enabled) are diﬀerent<br>. Ensure that an AWS<br>CloudTrail trail is<br>enabled in your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>a trail is not enabled.<br>Optionally, the rule<br>checks a speciﬁc<br>S3 bucket, Amazon<br>Simple Notiﬁcation<br>Service (Amazon SNS)<br>topic, and CloudWatc<br>h log group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14020
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|multi-region-cloud <br>trail-enabled|Note: for this rule,<br>the rule identiﬁe<br>r (MULTI_RE<br>GION_CLOU<br>D_TRAIL_ENABLED)<br>and rule name<br>(multi-region-clou<br>dtrail-enabled) are<br>diﬀerent. Ensure<br>that there is at least<br>one multi-region<br>AWS CloudTrail. The<br>rule is NON_COMPL<br>IANT if the trails<br>do not match input<br>parameters. The rule<br>is NON_COMPLIANT<br>if the ExcludeMa<br>nagementEventSourc<br>es ﬁeld is not empty<br>or if AWS CloudTrai<br>l is conﬁgured to<br>exclude managemen<br>t events such as<br>AWS KMS events or<br>Amazon RDS Data<br>API events.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14021
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|appsync-logging-en <br>abled|Ensure that an AWS<br>AppSync API has<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging is not<br>enabled, or 'ﬁeldLog<br>Level' is neither<br>ERROR nor ALL.|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|waf-classic-logging-<br>enabled|Ensure that logging is<br>enabled on AWS WAF<br>classic global web<br>access control lists<br>(web ACLs). The rule<br>is NON_COMPLIANT<br>for a global web ACL,<br>if it does not have<br>logging enabled.|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|mq-cloudwatch-audi <br>t-logging-enabled|Ensure that Amazon<br>MQ brokers have<br>Amazon CloudWatc<br>h audit logging<br>enabled. The rule is<br>NON_COMPLIANT<br>if a broker does not<br>have audit logging<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14022
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|mq-cloudwatch-audi <br>t-log-enabled|Ensure that an<br>Amazon MQ broker<br>has CloudWatch audit<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if the broker<br>does not have audit<br>logging enabled.|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|eks-cluster-logging-<br>enabled|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS) cluster<br>is conﬁgured with<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging for<br>Amazon EKS clusters<br>is not enabled for all<br>log types.|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|elastic-beanstalk- <br>logs-to-cloudwatch|Ensure that AWS<br>Elastic Beanstalk<br>environments<br>are conﬁgured<br>to send logs to<br>Amazon CloudWatc<br>h Logs. The rule<br>is NON_COMPL<br>IANT if the value<br>of `StreamLogs` is<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14023
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|step-functions-sta <br>te-machine-logging-<br>enabled|Ensure that AWS<br>Step Functions<br>machine has logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a state machine does<br>not have logging<br>enabled or the<br>logging conﬁgura<br>tion is not at the<br>minimum level<br>provided.|
|10.3.1|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|netfw-logging-enab <br>led|Ensure that AWS<br>Network Firewall<br>ﬁrewalls have logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a logging type is not<br>conﬁgured. You can<br>specify which logging<br>type you want the<br>rule to check.|
|10.3.2|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|cloudtrail-security-<br>trail-enabled|Ensure that there<br>is at least one AWS<br>CloudTrail trail<br>deﬁned with security<br>best practices. This<br>rule is COMPLIANT if<br>there is at least one<br>trail that meets all of<br>the following:|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14024
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.2|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|neptune-cluster-sn <br>apshot-public-proh <br>ibited|Ensure that an<br>Amazon Neptune<br>manual DB cluster<br>snapshot is not<br>public. The rule is<br>NON_COMPLIANT<br>if any existing and<br>new Neptune cluster<br>snapshot is public.|
|10.3.2|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|docdb-cluster-snap <br>shot-public-prohib <br>ited|Ensure that Amazon<br>DocumentDB manual<br>cluster snapshots<br>are not public. The<br>rule is NON_COMPL<br>IANT if any Amazon<br>DocumentDB manual<br>cluster snapshots are<br>public.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14025
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.2|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|backup-recovery-po <br>int-manual-deletion-<br>disabled|Ensure that a backup<br>vault has an attached<br>resource-based<br>policy which prevents<br>deletion of recovery<br>points. The rule<br>is NON_COMPL<br>IANT if the Backup<br>Vault does not<br>have resource-<br>based policies or<br>has policies without<br>a suitable 'Deny'<br>statement (statemen<br>t with backup:De<br>leteRecoveryPoint,<br>backup:UpdateRecov<br>eryPointLifecycle,<br>and backup:Pu<br>tBackupVaultAccess<br>Policy permissions).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14026
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.2|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|emr-block-public-a <br>ccess|Ensure that an<br>account with Amazon<br>EMR has block public<br>access settings<br>enabled. The rule is<br>NON_COMPLIANT if<br>BlockPublicSecurit<br>yGroupRules is false,<br>or if true, ports other<br>than Port 22 are<br>listed in Permitted<br>PublicSecurityGrou<br>pRuleRanges.|
|10.3.2|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|s3-access-point-pu <br>blic-access-blocks|Ensure that Amazon<br>S3 access points have<br>block public access<br>settings enabled. The<br>rule is NON_COMPL<br>IANT if block public<br>access settings are<br>not enabled for S3<br>access points.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14027
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.2|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|s3-account-level-p <br>ublic-access-blocks|Ensure that the<br>required public<br>access block settings<br>are conﬁgured<br>from account level.<br>The rule is only<br>NON_COMPLIANT<br>when the ﬁelds set<br>below do not match<br>the corresponding<br>ﬁelds in the conﬁgura<br>tion item.|
|10.3.2|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|s3-bucket-mfa-dele <br>te-enabled|Ensure that MFA<br>Delete is enabled in<br>the Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>versioning conﬁgura<br>tion. The rule is<br>NON_COMPLIANT<br>if MFA Delete is not<br>enabled.|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|aurora-resources-p <br>rotected-by-backup-<br>plan|Ensure that Amazon<br>Aurora DB clusters<br>are protected by a<br>backup plan. The<br>rule is NON_COMPL<br>IANT if the Amazon<br>Relational Database<br>Service (Amazon RDS)<br>Database Cluster is<br>not protected by a<br>backup plan.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14028
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|db-instance-backup-<br>enabled|Ensure that RDS<br>DB instances have<br>backups enabled.<br>Optionally, the rule<br>checks the backup<br>retention period and<br>the backup window.|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|dynamodb-in-backup <br>-plan|Ensure that Amazon<br>DynamoDB tables<br>are present in AWS<br>Backup Plans. The<br>rule is NON_COMPL<br>IANT if Amazon<br>DynamoDB tables are<br>not present in any<br>AWS Backup plan.|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|dynamodb-resources-<br>protected-by-backup-<br>plan|Ensure that Amazon<br>DynamoDB tables<br>are protected by a<br>backup plan. The rule<br>is NON_COMPLIANT<br>if the DynamoDB<br>Table is not covered<br>by a backup plan.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14029
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|ebs-in-backup-plan|Ensure that Amazon<br>Elastic Block Store<br>(Amazon EBS)<br>volumes are added in<br>backup plans of AWS<br>Backup. The rule is<br>NON_COMPLIANT if<br>Amazon EBS volumes<br>are not included in<br>backup plans.|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|ebs-resources-prot <br>ected-by-backup-pl <br>an|Ensure that Amazon<br>Elastic Block<br>Store (Amazon<br>EBS) volumes are<br>protected by a<br>backup plan. The rule<br>is NON_COMPLIANT<br>if the Amazon EBS<br>volume is not covered<br>by a backup plan.|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|ec2-resources-prot <br>ected-by-backup-pl <br>an|Ensure that Amazon<br>Elastic Compute<br>Cloud (Amazon<br>EC2) instances are<br>protected by a<br>backup plan. The<br>rule is NON_COMPL<br>IANT if the Amazon<br>EC2 instance is not<br>covered by a backup<br>plan.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14030
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|efs-in-backup-plan|Ensure that Amazon<br>Elastic File System<br>(Amazon EFS) ﬁle<br>systems are added in<br>the backup plans of<br>AWS Backup. The rule<br>is NON_COMPLIANT<br>if EFS ﬁle systems are<br>not included in the<br>backup plans.|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|efs-resources-prot <br>ected-by-backup-pl <br>an|Ensure that Amazon<br>Elastic File System<br>(Amazon EFS)<br>ﬁle systems are<br>protected by a<br>backup plan. The rule<br>is NON_COMPLIANT<br>if the EFS File System<br>is not covered by a<br>backup plan.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14031
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|elasticache-redis- <br>cluster-automatic- <br>backup-check|Check if the Amazon<br>ElastiCache Redis<br>clusters have<br>automatic backup<br>turned on. The rule<br>is NON_COMPLIANT<br>if the SnapshotR<br>etentionLimit for<br>Redis cluster is less<br>than the SnapshotR<br>etentionPeriod<br>parameter. For<br>example: If the<br>parameter is 15 then<br>the rule is non-compl<br>iant if the snapshotR<br>etentionPeriod is<br>between 0-15.|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|fsx-resources-prot <br>ected-by-backup-pl <br>an|Ensure that Amazon<br>FSx File Systems<br>are protected by a<br>backup plan. The rule<br>is NON_COMPLIANT<br>if the Amazon FSx<br>File System is not<br>covered by a backup<br>plan.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14032
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|neptune-cluster-ba <br>ckup-retention-check|Ensure that an<br>Amazon Neptune<br>DB cluster retention<br>period is set to<br>speciﬁc number of<br>days. The rule is<br>NON_COMPLIANT if<br>the retention period<br>is less than the value<br>speciﬁed by the<br>parameter.|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|rds-in-backup-plan|Ensure that Amazon<br>Relational Database<br>Service (Amazon<br>RDS) databases<br>are present in AWS<br>Backup plans. The<br>rule is NON_COMPL<br>IANT if Amazon RDS<br>databases are not<br>included in any AWS<br>Backup plan.|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|rds-resources-prot <br>ected-by-backup-pl <br>an|Ensure that Amazon<br>Relational Database<br>Service (Amazon<br>RDS) instances<br>are protected by a<br>backup plan. The rule<br>is NON_COMPLIANT<br>if the Amazon RDS<br>Database instance<br>is not covered by a<br>backup plan.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14033
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|redshift-backup-en <br>abled|Ensure that<br>Amazon Redshift<br>automated snapshots<br>are enabled for<br>clusters. The rule<br>is NON_COMPL<br>IANT if the value<br>for automated<br>SnapshotRetentionP<br>eriod is greater<br>than MaxRetent<br>ionPeriod or less than<br>MinRetentionPeriod<br>or the value is 0.|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|s3-resources-prote <br>cted-by-backup-plan|Ensure that Amazon<br>Simple Storage<br>Service (Amazon S3)<br>buckets are protected<br>by a backup plan. The<br>rule is NON_COMPL<br>IANT if the Amazon<br>S3 bucket is not<br>covered by a backup<br>plan.|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|cloudtrail-security-<br>trail-enabled|Ensure that there<br>is at least one AWS<br>CloudTrail trail<br>deﬁned with security<br>best practices. This<br>rule is COMPLIANT if<br>there is at least one<br>trail that meets all of<br>the following:|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14034
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|db-instance-backup-<br>enabled|Ensure that RDS<br>DB instances have<br>backups enabled.<br>Optionally, the rule<br>checks the backup<br>retention period and<br>the backup window.|
|10.3.3|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|dynamodb-pitr-enab <br>led|Ensure that point-<br>in-time recovery<br>(PITR) is enabled for<br>Amazon DynamoDB<br>tables. The rule is<br>NON_COMPLIANT if<br>PITR is not enabled<br>for DynamoDB tables.|
|10.3.4|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|cloudfront-origin- <br>access-identity-en <br>abled|Ensure that<br>CloudFront distribut<br>ion with Amazon<br>S3 Origin type has<br>origin access identity<br>(OAI) conﬁgured. The<br>rule is NON_COMPL<br>IANT if the CloudFron<br>t distribution is<br>backed by S3 and any<br>origin type is not OAI<br>conﬁgured, or the<br>origin is not an S3<br>bucket.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14035
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.4|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|cloudfront-s3-orig <br>in-access-control- <br>enabled|Ensure that an<br>Amazon CloudFron<br>t distribution with<br>an Amazon Simple<br>Storage Service<br>(Amazon S3) Origin<br>type has origin<br>access control (OAC)<br>enabled. The rule is<br>NON_COMPLIANT for<br>CloudFront distribut<br>ions with Amazon<br>S3 origins that don't<br>have OAC enabled.|
|10.3.4|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|s3-bucket-default- <br>lock-enabled|Ensure that the<br>S3 bucket has<br>lock enabled, by<br>default. The rule is<br>NON_COMPLIANT<br>if the lock is not<br>enabled.|
|10.3.4|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|s3-bucket-versioning-<br>enabled|Ensure that versionin<br>g is enabled for your<br>S3 buckets. Optionall<br>y, the rule checks if<br>MFA delete is enabled<br>for your S3 buckets.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14036
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.3.4|Audit logs are<br>protected from<br>destruction and<br>unauthorized<br>modiﬁcations. (PCI-<br>DSS-v4.0)|cloudtrail-security-<br>trail-enabled|Ensure that there<br>is at least one AWS<br>CloudTrail trail<br>deﬁned with security<br>best practices. This<br>rule is COMPLIANT if<br>there is at least one<br>trail that meets all of<br>the following:|
|10.4.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|10.4.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|ec2-instance-detai <br>led-monitoring-ena <br>bled|Ensure that detailed<br>monitoring is<br>enabled for EC2<br>instances. The rule is<br>NON_COMPLIANT if<br>detailed monitoring<br>is not enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14037
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.4.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|10.4.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14038
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.4.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|10.4.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-r <br>esource-check|Ensure that a<br>resource type has a<br>CloudWatch alarm<br>for the named metric.<br>For resource type,<br>you can specify<br>EBS volumes, EC2<br>instances, Amazon<br>RDS clusters, or S3<br>buckets. The rule is<br>COMPLIANT if the<br>named metric has<br>a resource ID and<br>CloudWatch alarm.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14039
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.4.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|wafv2-rulegroup-lo <br>gging-enabled|Ensure that Amazon<br>CloudWatch security<br>metrics collectio<br>n on AWS WAFv2<br>rule groups is<br>enabled. The rule is<br>NON_COMPLIANT if<br>the 'VisibilityConﬁg.<br>CloudWatchMetricsE<br>nabled' ﬁeld is set to<br>false.|
|10.4.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|sns-topic-message- <br>delivery-notiﬁcation-<br>enabled|Ensure that Amazon<br>Simple Notiﬁcation<br>Service (SNS) logging<br>is enabled for the<br>delivery status of<br>notiﬁcation messages<br>sent to a topic for<br>the endpoints. The<br>rule is NON_COMPL<br>IANT if the delivery<br>status notiﬁcation<br>for messages is not<br>enabled.|
|10.4.1.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14040
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.4.1.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|ec2-instance-detai <br>led-monitoring-ena <br>bled|Ensure that detailed<br>monitoring is<br>enabled for EC2<br>instances. The rule is<br>NON_COMPLIANT if<br>detailed monitoring<br>is not enabled.|
|10.4.1.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14041
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.4.1.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|10.4.1.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14042
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.4.1.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-r <br>esource-check|Ensure that a<br>resource type has a<br>CloudWatch alarm<br>for the named metric.<br>For resource type,<br>you can specify<br>EBS volumes, EC2<br>instances, Amazon<br>RDS clusters, or S3<br>buckets. The rule is<br>COMPLIANT if the<br>named metric has<br>a resource ID and<br>CloudWatch alarm.|
|10.4.1.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|wafv2-rulegroup-lo <br>gging-enabled|Ensure that Amazon<br>CloudWatch security<br>metrics collectio<br>n on AWS WAFv2<br>rule groups is<br>enabled. The rule is<br>NON_COMPLIANT if<br>the 'VisibilityConﬁg.<br>CloudWatchMetricsE<br>nabled' ﬁeld is set to<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14043
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.4.1.1|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|sns-topic-message- <br>delivery-notiﬁcation-<br>enabled|Ensure that Amazon<br>Simple Notiﬁcation<br>Service (SNS) logging<br>is enabled for the<br>delivery status of<br>notiﬁcation messages<br>sent to a topic for<br>the endpoints. The<br>rule is NON_COMPL<br>IANT if the delivery<br>status notiﬁcation<br>for messages is not<br>enabled.|
|10.4.2|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|10.4.2|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|ec2-instance-detai <br>led-monitoring-ena <br>bled|Ensure that detailed<br>monitoring is<br>enabled for EC2<br>instances. The rule is<br>NON_COMPLIANT if<br>detailed monitoring<br>is not enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14044
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.4.2|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|10.4.2|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14045
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.4.2|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|10.4.2|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-r <br>esource-check|Ensure that a<br>resource type has a<br>CloudWatch alarm<br>for the named metric.<br>For resource type,<br>you can specify<br>EBS volumes, EC2<br>instances, Amazon<br>RDS clusters, or S3<br>buckets. The rule is<br>COMPLIANT if the<br>named metric has<br>a resource ID and<br>CloudWatch alarm.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14046
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.4.2|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|wafv2-rulegroup-lo <br>gging-enabled|Ensure that Amazon<br>CloudWatch security<br>metrics collectio<br>n on AWS WAFv2<br>rule groups is<br>enabled. The rule is<br>NON_COMPLIANT if<br>the 'VisibilityConﬁg.<br>CloudWatchMetricsE<br>nabled' ﬁeld is set to<br>false.|
|10.4.2|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|sns-topic-message- <br>delivery-notiﬁcation-<br>enabled|Ensure that Amazon<br>Simple Notiﬁcation<br>Service (SNS) logging<br>is enabled for the<br>delivery status of<br>notiﬁcation messages<br>sent to a topic for<br>the endpoints. The<br>rule is NON_COMPL<br>IANT if the delivery<br>status notiﬁcation<br>for messages is not<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14047
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.4.3|Audit logs are<br>reviewed to identify<br>anomalies or<br>suspicious activity.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|10.5.1|Audit log history<br>is retained and<br>available for analysis.<br>(PCI-DSS-v4.0)|cloudtrail-security-<br>trail-enabled|Ensure that there<br>is at least one AWS<br>CloudTrail trail<br>deﬁned with security<br>best practices. This<br>rule is COMPLIANT if<br>there is at least one<br>trail that meets all of<br>the following:|
|10.5.1|Audit log history<br>is retained and<br>available for analysis.<br>(PCI-DSS-v4.0)|ec2-volume-inuse-c <br>heck|Ensure that EBS<br>volumes are attached<br>to EC2 instances.<br>Optionally ensure<br>that EBS volumes are<br>marked for deletion<br>when an instance is<br>terminated.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14048
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.5.1|Audit log history<br>is retained and<br>available for analysis.<br>(PCI-DSS-v4.0)|ecr-private-lifecycle-<br>policy-conﬁgured|Ensure that a private<br>Amazon Elastic<br>Container Registry<br>(ECR) repository<br>has at least one<br>lifecycle policy<br>conﬁgured. The rule<br>is NON_COMPLIANT<br>if no lifecycle policy<br>is conﬁgured for the<br>ECR private repositor<br>y.|
|10.5.1|Audit log history<br>is retained and<br>available for analysis.<br>(PCI-DSS-v4.0)|dynamodb-pitr-enab <br>led|Ensure that point-<br>in-time recovery<br>(PITR) is enabled for<br>Amazon DynamoDB<br>tables. The rule is<br>NON_COMPLIANT if<br>PITR is not enabled<br>for DynamoDB tables.|
|10.5.1|Audit log history<br>is retained and<br>available for analysis.<br>(PCI-DSS-v4.0)|cw-loggroup-retent <br>ion-period-check|Ensure that an<br>Amazon CloudWatch<br>LogGroup retention<br>period is set to<br>greater than 365 days<br>or else a speciﬁed<br>retention period. The<br>rule is NON_COMPL<br>IANT if the retention<br>period is less than<br>MinRetentionTime, if<br>speciﬁed, or else 365<br>days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14049
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|api-gwv2-access-lo <br>gs-enabled|Ensure that Amazon<br>API Gateway V2<br>stages have access<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if 'accessLo<br>gSettings' is not<br>present in Stage<br>conﬁguration.|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|cloudfront-accessl <br>ogs-enabled|Ensure that Amazon<br>CloudFront distribut<br>ions are conﬁgure<br>d to deliver access<br>logs to an Amazon<br>S3 bucket. The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion does not have<br>logging conﬁgured.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14050
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|s3-bucket-blacklis <br>ted-actions-prohib <br>ited|Ensure that an<br>Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>policy does not allow<br>blocklisted bucket-le<br>vel and object-level<br>actions on resources<br>in the bucket for<br>principals from other<br>AWS accounts. For<br>example, the rule<br>checks that the<br>Amazon S3 bucket<br>policy does not allow<br>another AWS account<br>to perform any<br>s3:GetBucket* actions<br>and s3:DeleteObject<br>on any object in the<br>bucket. The rule is<br>NON_COMPLIANT<br>if any blocklisted<br>actions are allowed<br>by the Amazon S3<br>bucket policy.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14051
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|s3-bucket-policy-not-<br>more-permissive|Ensure that your<br>Amazon Simple<br>Storage Service (S3)<br>bucket policies do<br>not allow other inter-<br>account permissio<br>ns than the control<br>Amazon S3 bucket<br>policy that you<br>provide.|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|neptune-cluster-cl <br>oudwatch-log-expor <br>t-enabled|Ensure that an<br>Amazon Neptune<br>cluster has<br>CloudWatch log<br>export enabled for<br>audit logs. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have CloudWatc<br>h log export enabled<br>for audit logs.|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|ec2-instance-detai <br>led-monitoring-ena <br>bled|Ensure that detailed<br>monitoring is<br>enabled for EC2<br>instances. The rule is<br>NON_COMPLIANT if<br>detailed monitoring<br>is not enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14052
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|ecs-task-deﬁnition-<br>log-conﬁguration|Ensure that logConﬁg<br>uration is set on<br>active ECS Task<br>Deﬁnitions. This<br>rule is NON_COMPL<br>IANT if an active<br>ECSTaskDeﬁnition<br>does not have the<br>logConﬁguration<br>resource deﬁned<br>or the value for<br>logConﬁguration is<br>null in at least one<br>container deﬁnition.|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14053
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14054
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|cloudwatch-alarm-r <br>esource-check|Ensure that a<br>resource type has a<br>CloudWatch alarm<br>for the named metric.<br>For resource type,<br>you can specify<br>EBS volumes, EC2<br>instances, Amazon<br>RDS clusters, or S3<br>buckets. The rule is<br>COMPLIANT if the<br>named metric has<br>a resource ID and<br>CloudWatch alarm.|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|cloudtrail-enabled|Note: For this rule,<br>the rule identiﬁe<br>r (CLOUD_TR<br>AIL_ENABLED) and<br>rule name (cloudtrail-<br>enabled) are diﬀerent<br>. Ensure that an AWS<br>CloudTrail trail is<br>enabled in your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>a trail is not enabled.<br>Optionally, the rule<br>checks a speciﬁc<br>S3 bucket, Amazon<br>Simple Notiﬁcation<br>Service (Amazon SNS)<br>topic, and CloudWatc<br>h log group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14055
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|multi-region-cloud <br>trail-enabled|Note: for this rule,<br>the rule identiﬁe<br>r (MULTI_RE<br>GION_CLOU<br>D_TRAIL_ENABLED)<br>and rule name<br>(multi-region-clou<br>dtrail-enabled) are<br>diﬀerent. Ensure<br>that there is at least<br>one multi-region<br>AWS CloudTrail. The<br>rule is NON_COMPL<br>IANT if the trails<br>do not match input<br>parameters. The rule<br>is NON_COMPLIANT<br>if the ExcludeMa<br>nagementEventSourc<br>es ﬁeld is not empty<br>or if AWS CloudTrai<br>l is conﬁgured to<br>exclude managemen<br>t events such as<br>AWS KMS events or<br>Amazon RDS Data<br>API events.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14056
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|appsync-logging-en <br>abled|Ensure that an AWS<br>AppSync API has<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging is not<br>enabled, or 'ﬁeldLog<br>Level' is neither<br>ERROR nor ALL.|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|waf-classic-logging-<br>enabled|Ensure that logging is<br>enabled on AWS WAF<br>classic global web<br>access control lists<br>(web ACLs). The rule<br>is NON_COMPLIANT<br>for a global web ACL,<br>if it does not have<br>logging enabled.|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|mq-cloudwatch-audi <br>t-logging-enabled|Ensure that Amazon<br>MQ brokers have<br>Amazon CloudWatc<br>h audit logging<br>enabled. The rule is<br>NON_COMPLIANT<br>if a broker does not<br>have audit logging<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14057
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|mq-cloudwatch-audi <br>t-log-enabled|Ensure that an<br>Amazon MQ broker<br>has CloudWatch audit<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if the broker<br>does not have audit<br>logging enabled.|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|eks-cluster-logging-<br>enabled|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS) cluster<br>is conﬁgured with<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging for<br>Amazon EKS clusters<br>is not enabled for all<br>log types.|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|elastic-beanstalk- <br>logs-to-cloudwatch|Ensure that AWS<br>Elastic Beanstalk<br>environments<br>are conﬁgured<br>to send logs to<br>Amazon CloudWatc<br>h Logs. The rule<br>is NON_COMPL<br>IANT if the value<br>of `StreamLogs` is<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14058
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|wafv2-rulegroup-lo <br>gging-enabled|Ensure that Amazon<br>CloudWatch security<br>metrics collectio<br>n on AWS WAFv2<br>rule groups is<br>enabled. The rule is<br>NON_COMPLIANT if<br>the 'VisibilityConﬁg.<br>CloudWatchMetricsE<br>nabled' ﬁeld is set to<br>false.|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|sns-topic-message- <br>delivery-notiﬁcation-<br>enabled|Ensure that Amazon<br>Simple Notiﬁcation<br>Service (SNS) logging<br>is enabled for the<br>delivery status of<br>notiﬁcation messages<br>sent to a topic for<br>the endpoints. The<br>rule is NON_COMPL<br>IANT if the delivery<br>status notiﬁcation<br>for messages is not<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14059
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|step-functions-sta <br>te-machine-logging-<br>enabled|Ensure that AWS<br>Step Functions<br>machine has logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a state machine does<br>not have logging<br>enabled or the<br>logging conﬁgura<br>tion is not at the<br>minimum level<br>provided.|
|10.6.3|Time-synchronizati<br>on mechanisms<br>support consistent<br>time settings across<br>all systems. (PCI-DSS-<br>v4.0)|netfw-logging-enab <br>led|Ensure that AWS<br>Network Firewall<br>ﬁrewalls have logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a logging type is not<br>conﬁgured. You can<br>specify which logging<br>type you want the<br>rule to check.|
|10.7.1|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14060
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.7.1|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|cloudformation-sta <br>ck-notiﬁcation-check|Ensure that your<br>CloudFormation<br>stacks send event<br>notiﬁcations to<br>an Amazon SNS<br>topic. Optionally<br>ensure that speciﬁed<br>Amazon SNS topics<br>are used. The rule is<br>NON_COMPLIANT<br>if CloudFormation<br>stacks do not send<br>notiﬁcations.|
|10.7.1|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|ec2-instance-detai <br>led-monitoring-ena <br>bled|Ensure that detailed<br>monitoring is<br>enabled for EC2<br>instances. The rule is<br>NON_COMPLIANT if<br>detailed monitoring<br>is not enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14061
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.7.1|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|10.7.1|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14062
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.7.1|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|10.7.1|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|cloudwatch-alarm-r <br>esource-check|Ensure that a<br>resource type has a<br>CloudWatch alarm<br>for the named metric.<br>For resource type,<br>you can specify<br>EBS volumes, EC2<br>instances, Amazon<br>RDS clusters, or S3<br>buckets. The rule is<br>COMPLIANT if the<br>named metric has<br>a resource ID and<br>CloudWatch alarm.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14063
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.7.1|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|wafv2-rulegroup-lo <br>gging-enabled|Ensure that Amazon<br>CloudWatch security<br>metrics collectio<br>n on AWS WAFv2<br>rule groups is<br>enabled. The rule is<br>NON_COMPLIANT if<br>the 'VisibilityConﬁg.<br>CloudWatchMetricsE<br>nabled' ﬁeld is set to<br>false.|
|10.7.1|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|sns-topic-message- <br>delivery-notiﬁcation-<br>enabled|Ensure that Amazon<br>Simple Notiﬁcation<br>Service (SNS) logging<br>is enabled for the<br>delivery status of<br>notiﬁcation messages<br>sent to a topic for<br>the endpoints. The<br>rule is NON_COMPL<br>IANT if the delivery<br>status notiﬁcation<br>for messages is not<br>enabled.|
|10.7.2|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14064
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.7.2|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|cloudformation-sta <br>ck-notiﬁcation-check|Ensure that your<br>CloudFormation<br>stacks send event<br>notiﬁcations to<br>an Amazon SNS<br>topic. Optionally<br>ensure that speciﬁed<br>Amazon SNS topics<br>are used. The rule is<br>NON_COMPLIANT<br>if CloudFormation<br>stacks do not send<br>notiﬁcations.|
|10.7.2|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|ec2-instance-detai <br>led-monitoring-ena <br>bled|Ensure that detailed<br>monitoring is<br>enabled for EC2<br>instances. The rule is<br>NON_COMPLIANT if<br>detailed monitoring<br>is not enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14065
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.7.2|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|10.7.2|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14066
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.7.2|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|10.7.2|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|cloudwatch-alarm-r <br>esource-check|Ensure that a<br>resource type has a<br>CloudWatch alarm<br>for the named metric.<br>For resource type,<br>you can specify<br>EBS volumes, EC2<br>instances, Amazon<br>RDS clusters, or S3<br>buckets. The rule is<br>COMPLIANT if the<br>named metric has<br>a resource ID and<br>CloudWatch alarm.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14067
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|10.7.2|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|wafv2-rulegroup-lo <br>gging-enabled|Ensure that Amazon<br>CloudWatch security<br>metrics collectio<br>n on AWS WAFv2<br>rule groups is<br>enabled. The rule is<br>NON_COMPLIANT if<br>the 'VisibilityConﬁg.<br>CloudWatchMetricsE<br>nabled' ﬁeld is set to<br>false.|
|10.7.2|Failures of critical<br>security control<br>systems are detected,<br>reported, and<br>responded to<br>promptly. (PCI-DSS-<br>v4.0)|sns-topic-message- <br>delivery-notiﬁcation-<br>enabled|Ensure that Amazon<br>Simple Notiﬁcation<br>Service (SNS) logging<br>is enabled for the<br>delivery status of<br>notiﬁcation messages<br>sent to a topic for<br>the endpoints. The<br>rule is NON_COMPL<br>IANT if the delivery<br>status notiﬁcation<br>for messages is not<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14068
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|11.5.2|Network intrusions<br>and unexpected ﬁle<br>changes are detected<br>and responded to.<br>(PCI-DSS-v4.0)|cloudformation-sta <br>ck-notiﬁcation-check|Ensure that your<br>CloudFormation<br>stacks send event<br>notiﬁcations to<br>an Amazon SNS<br>topic. Optionally<br>ensure that speciﬁed<br>Amazon SNS topics<br>are used. The rule is<br>NON_COMPLIANT<br>if CloudFormation<br>stacks do not send<br>notiﬁcations.|
|11.5.2|Network intrusions<br>and unexpected ﬁle<br>changes are detected<br>and responded to.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14069
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|11.5.2|Network intrusions<br>and unexpected ﬁle<br>changes are detected<br>and responded to.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|11.5.2|Network intrusions<br>and unexpected ﬁle<br>changes are detected<br>and responded to.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-s <br>ettings-check|Ensure that<br>CloudWatch alarms<br>with the given metric<br>name have the<br>speciﬁed settings.|
|11.5.2|Network intrusions<br>and unexpected ﬁle<br>changes are detected<br>and responded to.<br>(PCI-DSS-v4.0)|sns-topic-message- <br>delivery-notiﬁcation-<br>enabled|Ensure that Amazon<br>Simple Notiﬁcation<br>Service (SNS) logging<br>is enabled for the<br>delivery status of<br>notiﬁcation messages<br>sent to a topic for<br>the endpoints. The<br>rule is NON_COMPL<br>IANT if the delivery<br>status notiﬁcation<br>for messages is not<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14070
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|11.6.1|Unauthorized<br>changes on payment<br>pages are detected<br>and responded to.<br>(PCI-DSS-v4.0)|cloudformation-sta <br>ck-notiﬁcation-check|Ensure that your<br>CloudFormation<br>stacks send event<br>notiﬁcations to<br>an Amazon SNS<br>topic. Optionally<br>ensure that speciﬁed<br>Amazon SNS topics<br>are used. The rule is<br>NON_COMPLIANT<br>if CloudFormation<br>stacks do not send<br>notiﬁcations.|
|11.6.1|Unauthorized<br>changes on payment<br>pages are detected<br>and responded to.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14071
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|11.6.1|Unauthorized<br>changes on payment<br>pages are detected<br>and responded to.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|11.6.1|Unauthorized<br>changes on payment<br>pages are detected<br>and responded to.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-s <br>ettings-check|Ensure that<br>CloudWatch alarms<br>with the given metric<br>name have the<br>speciﬁed settings.|
|11.6.1|Unauthorized<br>changes on payment<br>pages are detected<br>and responded to.<br>(PCI-DSS-v4.0)|sns-topic-message- <br>delivery-notiﬁcation-<br>enabled|Ensure that Amazon<br>Simple Notiﬁcation<br>Service (SNS) logging<br>is enabled for the<br>delivery status of<br>notiﬁcation messages<br>sent to a topic for<br>the endpoints. The<br>rule is NON_COMPL<br>IANT if the delivery<br>status notiﬁcation<br>for messages is not<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14072
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|12.10.5|Suspected and<br>conﬁrmed security<br>incidents that could<br>impact the CDE<br>are responded to<br>immediately. (PCI-<br>DSS-v4.0)|cloudformation-sta <br>ck-notiﬁcation-check|Ensure that your<br>CloudFormation<br>stacks send event<br>notiﬁcations to<br>an Amazon SNS<br>topic. Optionally<br>ensure that speciﬁed<br>Amazon SNS topics<br>are used. The rule is<br>NON_COMPLIANT<br>if CloudFormation<br>stacks do not send<br>notiﬁcations.|
|12.10.5|Suspected and<br>conﬁrmed security<br>incidents that could<br>impact the CDE<br>are responded to<br>immediately. (PCI-<br>DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14073
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|12.10.5|Suspected and<br>conﬁrmed security<br>incidents that could<br>impact the CDE<br>are responded to<br>immediately. (PCI-<br>DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|12.10.5|Suspected and<br>conﬁrmed security<br>incidents that could<br>impact the CDE<br>are responded to<br>immediately. (PCI-<br>DSS-v4.0)|cloudwatch-alarm-s <br>ettings-check|Ensure that<br>CloudWatch alarms<br>with the given metric<br>name have the<br>speciﬁed settings.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14074
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|12.10.5|Suspected and<br>conﬁrmed security<br>incidents that could<br>impact the CDE<br>are responded to<br>immediately. (PCI-<br>DSS-v4.0)|sns-topic-message- <br>delivery-notiﬁcation-<br>enabled|Ensure that Amazon<br>Simple Notiﬁcation<br>Service (SNS) logging<br>is enabled for the<br>delivery status of<br>notiﬁcation messages<br>sent to a topic for<br>the endpoints. The<br>rule is NON_COMPL<br>IANT if the delivery<br>status notiﬁcation<br>for messages is not<br>enabled.|
|12.4.2.1|PCI DSS compliance is<br>managed. (PCI-DSS-<br>v4.0)|service-catalog-sh <br>ared-within-organi <br>zation|Ensure that AWS<br>Service Catalog<br>shares portfolios to<br>an organization (a<br>collection of AWS<br>accounts treated as<br>a single unit) when<br>integration is enabled<br>with AWS Organizat<br>ions. The rule is<br>NON_COMPLIANT if<br>the `Type` value of a<br>share is `ACCOUNT`.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14075
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|2.2.5|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|cloudfront-security-<br>policy-check|Ensure that Amazon<br>CloudFront distribut<br>ions are using a<br>minimum security<br>policy and cipher<br>suite of TLSv1.2 or<br>greater for viewer<br>connections. This<br>rule is NON_COMPL<br>IANT for a CloudFron<br>t distribution if<br>the minimumPr<br>otocolVersion is<br>below TLSv1.2_2018.|
|2.2.5|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|cloudfront-sni-ena <br>bled|Ensure that Amazon<br>CloudFront distribut<br>ions are using a<br>custom SSL certiﬁca<br>te and are conﬁgure<br>d to use SNI to serve<br>HTTPS requests. The<br>rule is NON_COMPL<br>IANT if a custom<br>SSL certiﬁcate is<br>associated but the<br>SSL support method<br>is a dedicated IP<br>address.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14076
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|2.2.5|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|transfer-family-se <br>rver-no-ftp|Ensure that a<br>server created<br>with AWS Transfer<br>Family does not use<br>FTP for endpoint<br>connection. The<br>rule is NON_COMPL<br>IANT if the server<br>protocol for endpoint<br>connection is FTP-<br>enabled.|
|2.2.5|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|cloudfront-no-depr <br>ecated-ssl-protocols|Ensure that<br>CloudFront distribut<br>ions are not using<br>deprecated SSL<br>protocols for HTTPS<br>communication<br>between CloudFron<br>t edge locations and<br>custom origins. This<br>rule is NON_COMPL<br>IANT for a CloudFron<br>t distribution if<br>any'OriginSslProto<br>cols' includes'SSLv3'.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14077
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|2.2.5|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|cloudfront-traﬃc-to-<br>origin-encrypted|Ensure that Amazon<br>CloudFront distribut<br>ions are encryptin<br>g traﬃc to custom<br>origins. The rule is<br>NON_COMPLIANT<br>if'OriginProtocolP<br>olicy' is'http-only' or<br>if'OriginProtocolP<br>olicy' is'match-viewer'<br>and'ViewerProtocol<br>Policy' is'allow-all'.|
|2.2.5|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|cloudfront-viewer- <br>policy-https|Ensure that your<br>Amazon CloudFron<br>t distributions use<br>HTTPS (directly or<br>via a redirection). The<br>rule is NON_COMPL<br>IANT if the value of<br>ViewerProtocolPoli<br>cy is set to 'allow-al<br>l' for the DefaultCa<br>cheBehavior or for<br>the CacheBehaviors.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14078
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|2.2.7|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|dms-redis-tls-enab <br>led|Ensure that AWS<br>Database Migration<br>Service (AWS DMS)<br>endpoints for Redis<br>data stores are<br>enabled for TLS/SSL<br>encryption of data<br>communicated with<br>other endpoints. The<br>rule is NON_COMPL<br>IANT if TLS/SSL<br>encryption is not<br>enabled.|
|2.2.7|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|cloudfront-no-depr <br>ecated-ssl-protocols|Ensure that<br>CloudFront distribut<br>ions are not using<br>deprecated SSL<br>protocols for HTTPS<br>communication<br>between CloudFron<br>t edge locations and<br>custom origins. This<br>rule is NON_COMPL<br>IANT for a CloudFron<br>t distribution if<br>any'OriginSslProto<br>cols' includes'SSLv3'.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14079
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|2.2.7|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|cloudfront-traﬃc-to-<br>origin-encrypted|Ensure that Amazon<br>CloudFront distribut<br>ions are encryptin<br>g traﬃc to custom<br>origins. The rule is<br>NON_COMPLIANT<br>if'OriginProtocolP<br>olicy' is'http-only' or<br>if'OriginProtocolP<br>olicy' is'match-viewer'<br>and'ViewerProtocol<br>Policy' is'allow-all'.|
|2.2.7|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|cloudfront-viewer- <br>policy-https|Ensure that your<br>Amazon CloudFron<br>t distributions use<br>HTTPS (directly or<br>via a redirection). The<br>rule is NON_COMPL<br>IANT if the value of<br>ViewerProtocolPoli<br>cy is set to 'allow-al<br>l' for the DefaultCa<br>cheBehavior or for<br>the CacheBehaviors.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14080
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|2.2.7|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|2.2.7|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|dax-tls-endpoint-e <br>ncryption|Ensure that your<br>Amazon DynamoDB<br>Accelerator (DAX)<br>cluster has ClusterEn<br>dpointEncryptionTy<br>pe set to TLS. The<br>rule is NON_COMPL<br>IANT if a DAX cluster<br>is not encrypted<br>by transport layer<br>security (TLS).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14081
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|2.2.7|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|msk-in-cluster-node-<br>require-tls|Ensure that an<br>Amazon MSK cluster<br>enforces encryptio<br>n in transit using<br>HTTPS (TLS) with the<br>broker nodes of the<br>cluster. The rule is<br>NON_COMPLIANT if<br>plain text communica<br>tion is enabled for in-<br>cluster broker node<br>connections.|
|2.2.7|System component<br>s are conﬁgured and<br>managed securely.<br>(PCI-DSS-v4.0)|dms-endpoint-ssl-c <br>onﬁgured|Ensure that AWS<br>Database Migration<br>Service (AWS DMS)<br>endpoints are<br>conﬁgured with an<br>SSL connection. The<br>rule is NON_COMPL<br>IANT if AWS DMS<br>does not have an SSL<br>connection conﬁgure<br>d.|
|3.2.1|Storage of account<br>data is kept to a<br>minimum. (PCI-DSS-<br>v4.0)|ec2-volume-inuse-c <br>heck|Ensure that EBS<br>volumes are attached<br>to EC2 instances.<br>Optionally ensure<br>that EBS volumes are<br>marked for deletion<br>when an instance is<br>terminated.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14082
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.2.1|Storage of account<br>data is kept to a<br>minimum. (PCI-DSS-<br>v4.0)|ecr-private-lifecycle-<br>policy-conﬁgured|Ensure that a private<br>Amazon Elastic<br>Container Registry<br>(ECR) repository<br>has at least one<br>lifecycle policy<br>conﬁgured. The rule<br>is NON_COMPLIANT<br>if no lifecycle policy<br>is conﬁgured for the<br>ECR private repositor<br>y.|
|3.2.1|Storage of account<br>data is kept to a<br>minimum. (PCI-DSS-<br>v4.0)|dynamodb-pitr-enab <br>led|Ensure that point-<br>in-time recovery<br>(PITR) is enabled for<br>Amazon DynamoDB<br>tables. The rule is<br>NON_COMPLIANT if<br>PITR is not enabled<br>for DynamoDB tables.|
|3.2.1|Storage of account<br>data is kept to a<br>minimum. (PCI-DSS-<br>v4.0)|cw-loggroup-retent <br>ion-period-check|Ensure that an<br>Amazon CloudWatch<br>LogGroup retention<br>period is set to<br>greater than 365 days<br>or else a speciﬁed<br>retention period. The<br>rule is NON_COMPL<br>IANT if the retention<br>period is less than<br>MinRetentionTime, if<br>speciﬁed, or else 365<br>days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14083
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.3.1.1|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|ec2-volume-inuse-c <br>heck|Ensure that EBS<br>volumes are attached<br>to EC2 instances.<br>Optionally ensure<br>that EBS volumes are<br>marked for deletion<br>when an instance is<br>terminated.|
|3.3.1.1|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|ecr-private-lifecycle-<br>policy-conﬁgured|Ensure that a private<br>Amazon Elastic<br>Container Registry<br>(ECR) repository<br>has at least one<br>lifecycle policy<br>conﬁgured. The rule<br>is NON_COMPLIANT<br>if no lifecycle policy<br>is conﬁgured for the<br>ECR private repositor<br>y.|
|3.3.1.1|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|dynamodb-pitr-enab <br>led|Ensure that point-<br>in-time recovery<br>(PITR) is enabled for<br>Amazon DynamoDB<br>tables. The rule is<br>NON_COMPLIANT if<br>PITR is not enabled<br>for DynamoDB tables.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14084
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.3.1.1|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|cw-loggroup-retent <br>ion-period-check|Ensure that an<br>Amazon CloudWatch<br>LogGroup retention<br>period is set to<br>greater than 365 days<br>or else a speciﬁed<br>retention period. The<br>rule is NON_COMPL<br>IANT if the retention<br>period is less than<br>MinRetentionTime, if<br>speciﬁed, or else 365<br>days.|
|3.3.1.3|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|ec2-volume-inuse-c <br>heck|Ensure that EBS<br>volumes are attached<br>to EC2 instances.<br>Optionally ensure<br>that EBS volumes are<br>marked for deletion<br>when an instance is<br>terminated.|
|3.3.1.3|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|ecr-private-lifecycle-<br>policy-conﬁgured|Ensure that a private<br>Amazon Elastic<br>Container Registry<br>(ECR) repository<br>has at least one<br>lifecycle policy<br>conﬁgured. The rule<br>is NON_COMPLIANT<br>if no lifecycle policy<br>is conﬁgured for the<br>ECR private repositor<br>y.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14085
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.3.1.3|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|dynamodb-pitr-enab <br>led|Ensure that point-<br>in-time recovery<br>(PITR) is enabled for<br>Amazon DynamoDB<br>tables. The rule is<br>NON_COMPLIANT if<br>PITR is not enabled<br>for DynamoDB tables.|
|3.3.1.3|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|cw-loggroup-retent <br>ion-period-check|Ensure that an<br>Amazon CloudWatch<br>LogGroup retention<br>period is set to<br>greater than 365 days<br>or else a speciﬁed<br>retention period. The<br>rule is NON_COMPL<br>IANT if the retention<br>period is less than<br>MinRetentionTime, if<br>speciﬁed, or else 365<br>days.|
|3.3.2|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|ec2-volume-inuse-c <br>heck|Ensure that EBS<br>volumes are attached<br>to EC2 instances.<br>Optionally ensure<br>that EBS volumes are<br>marked for deletion<br>when an instance is<br>terminated.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14086
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.3.2|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|ecr-private-lifecycle-<br>policy-conﬁgured|Ensure that a private<br>Amazon Elastic<br>Container Registry<br>(ECR) repository<br>has at least one<br>lifecycle policy<br>conﬁgured. The rule<br>is NON_COMPLIANT<br>if no lifecycle policy<br>is conﬁgured for the<br>ECR private repositor<br>y.|
|3.3.2|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|dynamodb-pitr-enab <br>led|Ensure that point-<br>in-time recovery<br>(PITR) is enabled for<br>Amazon DynamoDB<br>tables. The rule is<br>NON_COMPLIANT if<br>PITR is not enabled<br>for DynamoDB tables.|
|3.3.2|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|cw-loggroup-retent <br>ion-period-check|Ensure that an<br>Amazon CloudWatch<br>LogGroup retention<br>period is set to<br>greater than 365 days<br>or else a speciﬁed<br>retention period. The<br>rule is NON_COMPL<br>IANT if the retention<br>period is less than<br>MinRetentionTime, if<br>speciﬁed, or else 365<br>days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14087
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.3.3|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|ec2-volume-inuse-c <br>heck|Ensure that EBS<br>volumes are attached<br>to EC2 instances.<br>Optionally ensure<br>that EBS volumes are<br>marked for deletion<br>when an instance is<br>terminated.|
|3.3.3|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|ecr-private-lifecycle-<br>policy-conﬁgured|Ensure that a private<br>Amazon Elastic<br>Container Registry<br>(ECR) repository<br>has at least one<br>lifecycle policy<br>conﬁgured. The rule<br>is NON_COMPLIANT<br>if no lifecycle policy<br>is conﬁgured for the<br>ECR private repositor<br>y.|
|3.3.3|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|dynamodb-pitr-enab <br>led|Ensure that point-<br>in-time recovery<br>(PITR) is enabled for<br>Amazon DynamoDB<br>tables. The rule is<br>NON_COMPLIANT if<br>PITR is not enabled<br>for DynamoDB tables.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14088
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.3.3|Sensitive authentic<br>ation data (SAD)<br>is not stored after<br>authorization. (PCI-<br>DSS-v4.0)|cw-loggroup-retent <br>ion-period-check|Ensure that an<br>Amazon CloudWatch<br>LogGroup retention<br>period is set to<br>greater than 365 days<br>or else a speciﬁed<br>retention period. The<br>rule is NON_COMPL<br>IANT if the retention<br>period is less than<br>MinRetentionTime, if<br>speciﬁed, or else 365<br>days.|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|athena-workgroup-e <br>ncrypted-at-rest|Ensure that an<br>Amazon Athena<br>workgroup is<br>encrypted at rest. The<br>rule is NON_COMPL<br>IANT if encryptio<br>n of data at rest is<br>not enabled for an<br>Athena workgroup.|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|neptune-cluster-sn <br>apshot-encrypted|Ensure that an<br>Amazon Neptune DB<br>cluster has snapshots<br>encrypted. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have snapshots<br>encrypted.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14089
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|redshift-cluster-kms-<br>enabled|Ensure that Amazon<br>Redshift clusters are<br>using a speciﬁed AWS<br>Key Management<br>Service (AWS KMS)<br>key for encryptio<br>n. The rule is<br>COMPLIANT if<br>encryption is enabled<br>and the cluster is<br>encrypted with<br>the key provided<br>in the kmsKeyArn<br>parameter. The rule<br>is NON_COMPL<br>IANT if the cluster<br>is not encrypted<br>or encrypted with<br>another key.|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|codebuild-project- <br>artifact-encryption|Ensure that an AWS<br>CodeBuild project<br>has encryption<br>enabled for all of its<br>artifacts. The rule is<br>NON_COMPLIANT if<br>'encryptionDisabled'<br>is set to 'true' for any<br>primary or secondary<br>(if present) artifact<br>conﬁgurations.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14090
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|codebuild-project-s3-<br>logs-encrypted|Ensure that an AWS<br>CodeBuild project<br>conﬁgured with<br>Amazon S3 Logs has<br>encryption enabled<br>for its logs. The rule<br>is NON_COMPLIANT<br>if'encryptionDisab<br>led' is set to'true' in<br>a S3LogsConﬁg of a<br>CodeBuild project.|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|dax-encryption-ena <br>bled|Ensure that Amazon<br>DynamoDB Accelerat<br>or (DAX) clusters are<br>encrypted. The rule<br>is NON_COMPLIANT<br>if a DAX cluster is not<br>encrypted.|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|eks-secrets-encryp <br>ted|Ensure that Amazon<br>Elastic Kubernetes<br>Service clusters are<br>conﬁgured to have<br>Kubernetes secrets<br>encrypted using AWS<br>Key Management<br>Service (KMS) keys.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14091
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|api-gw-cache-enabl <br>ed-and-encrypted|Ensure that all<br>methods in Amazon<br>API Gateway<br>stages have cache<br>enabled and cache<br>encrypted. The rule<br>is NON_COMPL<br>IANT if any method<br>in an Amazon API<br>Gateway stage is not<br>conﬁgured to cache<br>or the cache is not<br>encrypted.|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|docdb-cluster-encr <br>ypted|Ensure that storage<br>encryption is enabled<br>for your Amazon<br>DocumentDB (with<br>MongoDB compatibi<br>lity) clusters. The rule<br>is NON_COMPLIANT<br>if storage encryption<br>is not enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14092
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|dynamodb-table-enc <br>rypted-kms|Ensure that Amazon<br>DynamoDB table is<br>encrypted with AWS<br>Key Management<br>Service (KMS). The<br>rule is NON_COMPL<br>IANT if Amazon<br>DynamoDB table is<br>not encrypted with<br>AWS KMS. The rule<br>is also NON_COMPL<br>IANT if the encrypted<br>AWS KMS key is not<br>present in kmsKeyArn<br>s input parameter.|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|dynamodb-table-enc <br>ryption-enabled|Ensure that the<br>Amazon DynamoDB<br>tables are encrypted<br>and checks their<br>status. The rule is<br>COMPLIANT if the<br>status is enabled or<br>enabling.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14093
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|codebuild-project- <br>envvar-awscred-che <br>ck|Ensure that the<br>project DOES NOT<br>contain environment<br>variables AWS_ACCES<br>S_KEY_ID and<br>AWS_SECRE<br>T_ACCESS_KEY. The<br>rule is NON_COMPL<br>IANT when the<br>project environme<br>nt variables contains<br>plaintext credentials.|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|eks-cluster-secrets-<br>encrypted|Ensure that Amazon<br>EKS clusters are not<br>conﬁgured to have<br>Kubernetes secrets<br>encrypted using<br>AWS KMS. The rule is<br>NON_COMPLIANT if<br>an EKS cluster does<br>not have an encryptio<br>nConﬁg resource or<br>if encryptionConﬁg<br>does not name<br>secrets as a resource.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14094
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|kinesis-stream-enc <br>rypted|Ensure that Amazon<br>Kinesis streams are<br>encrypted at rest<br>with server-side<br>encryption. The rule<br>is NON_COMPLIANT<br>for a Kinesis stream if<br>'StreamEncryption' is<br>not present.|
|3.5.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|neptune-cluster-en <br>crypted|Ensure that storage<br>encryption is<br>enabled for your<br>Amazon Neptune DB<br>clusters. The rule is<br>NON_COMPLIANT if<br>storage encryption is<br>not enabled.|
|3.5.1.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|acm-pca-root-ca-di <br>sabled|Ensure that AWS<br>Private Certiﬁca<br>te Authority (AWS<br>Private CA) has<br>a root CA that is<br>disabled. The rule is<br>NON_COMPLIANT for<br>root CAs with status<br>that is not DISABLED.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14095
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.5.1.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
|3.5.1.1|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14096
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.5.1.3|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|acm-pca-root-ca-di <br>sabled|Ensure that AWS<br>Private Certiﬁca<br>te Authority (AWS<br>Private CA) has<br>a root CA that is<br>disabled. The rule is<br>NON_COMPLIANT for<br>root CAs with status<br>that is not DISABLED.|
|3.5.1.3|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
|3.5.1.3|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|neptune-cluster-sn <br>apshot-public-proh <br>ibited|Ensure that an<br>Amazon Neptune<br>manual DB cluster<br>snapshot is not<br>public. The rule is<br>NON_COMPLIANT<br>if any existing and<br>new Neptune cluster<br>snapshot is public.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14097
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.5.1.3|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|docdb-cluster-snap <br>shot-public-prohib <br>ited|Ensure that Amazon<br>DocumentDB manual<br>cluster snapshots<br>are not public. The<br>rule is NON_COMPL<br>IANT if any Amazon<br>DocumentDB manual<br>cluster snapshots are<br>public.|
|3.5.1.3|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|backup-recovery-po <br>int-manual-deletion-<br>disabled|Ensure that a backup<br>vault has an attached<br>resource-based<br>policy which prevents<br>deletion of recovery<br>points. The rule<br>is NON_COMPL<br>IANT if the Backup<br>Vault does not<br>have resource-<br>based policies or<br>has policies without<br>a suitable 'Deny'<br>statement (statemen<br>t with backup:De<br>leteRecoveryPoint,<br>backup:UpdateRecov<br>eryPointLifecycle,<br>and backup:Pu<br>tBackupVaultAccess<br>Policy permissions).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14098
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.5.1.3|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|3.5.1.3|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|emr-block-public-a <br>ccess|Ensure that an<br>account with Amazon<br>EMR has block public<br>access settings<br>enabled. The rule is<br>NON_COMPLIANT if<br>BlockPublicSecurit<br>yGroupRules is false,<br>or if true, ports other<br>than Port 22 are<br>listed in Permitted<br>PublicSecurityGrou<br>pRuleRanges.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14099
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.5.1.3|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|s3-access-point-pu <br>blic-access-blocks|Ensure that Amazon<br>S3 access points have<br>block public access<br>settings enabled. The<br>rule is NON_COMPL<br>IANT if block public<br>access settings are<br>not enabled for S3<br>access points.|
|3.5.1.3|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|s3-account-level-p <br>ublic-access-blocks|Ensure that the<br>required public<br>access block settings<br>are conﬁgured<br>from account level.<br>The rule is only<br>NON_COMPLIANT<br>when the ﬁelds set<br>below do not match<br>the corresponding<br>ﬁelds in the conﬁgura<br>tion item.|
|3.5.1.3|Primary account<br>number (PAN) is<br>secured wherever it<br>is stored. (PCI-DSS-<br>v4.0)|s3-bucket-mfa-dele <br>te-enabled|Ensure that MFA<br>Delete is enabled in<br>the Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>versioning conﬁgura<br>tion. The rule is<br>NON_COMPLIANT<br>if MFA Delete is not<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14100
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.6.1|Cryptographic keys<br>used to protect<br>stored account data<br>are secured. (PCI-<br>DSS-v4.0)|acm-pca-root-ca-di <br>sabled|Ensure that AWS<br>Private Certiﬁca<br>te Authority (AWS<br>Private CA) has<br>a root CA that is<br>disabled. The rule is<br>NON_COMPLIANT for<br>root CAs with status<br>that is not DISABLED.|
|3.6.1|Cryptographic keys<br>used to protect<br>stored account data<br>are secured. (PCI-<br>DSS-v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14101
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.6.1|Cryptographic keys<br>used to protect<br>stored account data<br>are secured. (PCI-<br>DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|3.6.1.2|Cryptographic keys<br>used to protect<br>stored account data<br>are secured. (PCI-<br>DSS-v4.0)|acm-pca-root-ca-di <br>sabled|Ensure that AWS<br>Private Certiﬁca<br>te Authority (AWS<br>Private CA) has<br>a root CA that is<br>disabled. The rule is<br>NON_COMPLIANT for<br>root CAs with status<br>that is not DISABLED.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14102
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.6.1.2|Cryptographic keys<br>used to protect<br>stored account data<br>are secured. (PCI-<br>DSS-v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
|3.6.1.2|Cryptographic keys<br>used to protect<br>stored account data<br>are secured. (PCI-<br>DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14103
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.6.1.3|Cryptographic keys<br>used to protect<br>stored account data<br>are secured. (PCI-<br>DSS-v4.0)|acm-pca-root-ca-di <br>sabled|Ensure that AWS<br>Private Certiﬁca<br>te Authority (AWS<br>Private CA) has<br>a root CA that is<br>disabled. The rule is<br>NON_COMPLIANT for<br>root CAs with status<br>that is not DISABLED.|
|3.6.1.3|Cryptographic keys<br>used to protect<br>stored account data<br>are secured. (PCI-<br>DSS-v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14104
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.6.1.3|Cryptographic keys<br>used to protect<br>stored account data<br>are secured. (PCI-<br>DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|3.6.1.4|Cryptographic keys<br>used to protect<br>stored account data<br>are secured. (PCI-<br>DSS-v4.0)|acm-pca-root-ca-di <br>sabled|Ensure that AWS<br>Private Certiﬁca<br>te Authority (AWS<br>Private CA) has<br>a root CA that is<br>disabled. The rule is<br>NON_COMPLIANT for<br>root CAs with status<br>that is not DISABLED.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14105
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.6.1.4|Cryptographic keys<br>used to protect<br>stored account data<br>are secured. (PCI-<br>DSS-v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
|3.6.1.4|Cryptographic keys<br>used to protect<br>stored account data<br>are secured. (PCI-<br>DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14106
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.7.1|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|acm-certiﬁcate-rsa-<br>check|Ensure that RSA<br>certiﬁcates managed<br>by AWS Certiﬁcate<br>Manager (ACM) have<br>a key length of at<br>least '2048' bits.The<br>rule is NON_COMPL<br>IANT if the minimum<br>key length is less<br>than 2048 bits.|
|3.7.1|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|acm-pca-root-ca-di <br>sabled|Ensure that AWS<br>Private Certiﬁca<br>te Authority (AWS<br>Private CA) has<br>a root CA that is<br>disabled. The rule is<br>NON_COMPLIANT for<br>root CAs with status<br>that is not DISABLED.|
|3.7.1|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14107
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.7.1|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|3.7.2|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|acm-pca-root-ca-di <br>sabled|Ensure that AWS<br>Private Certiﬁca<br>te Authority (AWS<br>Private CA) has<br>a root CA that is<br>disabled. The rule is<br>NON_COMPLIANT for<br>root CAs with status<br>that is not DISABLED.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14108
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.7.2|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
|3.7.2|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14109
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.7.4|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|acm-pca-root-ca-di <br>sabled|Ensure that AWS<br>Private Certiﬁca<br>te Authority (AWS<br>Private CA) has<br>a root CA that is<br>disabled. The rule is<br>NON_COMPLIANT for<br>root CAs with status<br>that is not DISABLED.|
|3.7.4|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14110
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.7.4|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|3.7.6|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|acm-pca-root-ca-di <br>sabled|Ensure that AWS<br>Private Certiﬁca<br>te Authority (AWS<br>Private CA) has<br>a root CA that is<br>disabled. The rule is<br>NON_COMPLIANT for<br>root CAs with status<br>that is not DISABLED.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14111
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.7.6|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
|3.7.6|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14112
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.7.7|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|acm-pca-root-ca-di <br>sabled|Ensure that AWS<br>Private Certiﬁca<br>te Authority (AWS<br>Private CA) has<br>a root CA that is<br>disabled. The rule is<br>NON_COMPLIANT for<br>root CAs with status<br>that is not DISABLED.|
|3.7.7|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14113
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|3.7.7|Where cryptography<br>is used to protect<br>stored account data,<br>key managemen<br>t processes and<br>procedures covering<br>all aspects of the key<br>lifecycle are deﬁned<br>and implemented.<br>(PCI-DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|4.2.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|dms-redis-tls-enab <br>led|Ensure that AWS<br>Database Migration<br>Service (AWS DMS)<br>endpoints for Redis<br>data stores are<br>enabled for TLS/SSL<br>encryption of data<br>communicated with<br>other endpoints. The<br>rule is NON_COMPL<br>IANT if TLS/SSL<br>encryption is not<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14114
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|4.2.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|cloudfront-no-depr <br>ecated-ssl-protocols|Ensure that<br>CloudFront distribut<br>ions are not using<br>deprecated SSL<br>protocols for HTTPS<br>communication<br>between CloudFron<br>t edge locations and<br>custom origins. This<br>rule is NON_COMPL<br>IANT for a CloudFron<br>t distribution if<br>any'OriginSslProto<br>cols' includes'SSLv3'.|
|4.2.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|cloudfront-traﬃc-to-<br>origin-encrypted|Ensure that Amazon<br>CloudFront distribut<br>ions are encryptin<br>g traﬃc to custom<br>origins. The rule is<br>NON_COMPLIANT<br>if'OriginProtocolP<br>olicy' is'http-only' or<br>if'OriginProtocolP<br>olicy' is'match-viewer'<br>and'ViewerProtocol<br>Policy' is'allow-all'.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14115
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|4.2.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|cloudfront-viewer- <br>policy-https|Ensure that your<br>Amazon CloudFron<br>t distributions use<br>HTTPS (directly or<br>via a redirection). The<br>rule is NON_COMPL<br>IANT if the value of<br>ViewerProtocolPoli<br>cy is set to 'allow-al<br>l' for the DefaultCa<br>cheBehavior or for<br>the CacheBehaviors.|
|4.2.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14116
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|4.2.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|dax-tls-endpoint-e <br>ncryption|Ensure that your<br>Amazon DynamoDB<br>Accelerator (DAX)<br>cluster has ClusterEn<br>dpointEncryptionTy<br>pe set to TLS. The<br>rule is NON_COMPL<br>IANT if a DAX cluster<br>is not encrypted<br>by transport layer<br>security (TLS).|
|4.2.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|msk-in-cluster-node-<br>require-tls|Ensure that an<br>Amazon MSK cluster<br>enforces encryptio<br>n in transit using<br>HTTPS (TLS) with the<br>broker nodes of the<br>cluster. The rule is<br>NON_COMPLIANT if<br>plain text communica<br>tion is enabled for in-<br>cluster broker node<br>connections.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14117
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|4.2.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|dms-endpoint-ssl-c <br>onﬁgured|Ensure that AWS<br>Database Migration<br>Service (AWS DMS)<br>endpoints are<br>conﬁgured with an<br>SSL connection. The<br>rule is NON_COMPL<br>IANT if AWS DMS<br>does not have an SSL<br>connection conﬁgure<br>d.|
|4.2.1.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|acm-pca-root-ca-di <br>sabled|Ensure that AWS<br>Private Certiﬁca<br>te Authority (AWS<br>Private CA) has<br>a root CA that is<br>disabled. The rule is<br>NON_COMPLIANT for<br>root CAs with status<br>that is not DISABLED.|
|4.2.1.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14118
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|4.2.1.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|dms-redis-tls-enab <br>led|Ensure that AWS<br>Database Migration<br>Service (AWS DMS)<br>endpoints for Redis<br>data stores are<br>enabled for TLS/SSL<br>encryption of data<br>communicated with<br>other endpoints. The<br>rule is NON_COMPL<br>IANT if TLS/SSL<br>encryption is not<br>enabled.|
|4.2.1.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|cloudfront-no-depr <br>ecated-ssl-protocols|Ensure that<br>CloudFront distribut<br>ions are not using<br>deprecated SSL<br>protocols for HTTPS<br>communication<br>between CloudFron<br>t edge locations and<br>custom origins. This<br>rule is NON_COMPL<br>IANT for a CloudFron<br>t distribution if<br>any'OriginSslProto<br>cols' includes'SSLv3'.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14119
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|4.2.1.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|cloudfront-traﬃc-to-<br>origin-encrypted|Ensure that Amazon<br>CloudFront distribut<br>ions are encryptin<br>g traﬃc to custom<br>origins. The rule is<br>NON_COMPLIANT<br>if'OriginProtocolP<br>olicy' is'http-only' or<br>if'OriginProtocolP<br>olicy' is'match-viewer'<br>and'ViewerProtocol<br>Policy' is'allow-all'.|
|4.2.1.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|cloudfront-viewer- <br>policy-https|Ensure that your<br>Amazon CloudFron<br>t distributions use<br>HTTPS (directly or<br>via a redirection). The<br>rule is NON_COMPL<br>IANT if the value of<br>ViewerProtocolPoli<br>cy is set to 'allow-al<br>l' for the DefaultCa<br>cheBehavior or for<br>the CacheBehaviors.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14120
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|4.2.1.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|4.2.1.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|dax-tls-endpoint-e <br>ncryption|Ensure that your<br>Amazon DynamoDB<br>Accelerator (DAX)<br>cluster has ClusterEn<br>dpointEncryptionTy<br>pe set to TLS. The<br>rule is NON_COMPL<br>IANT if a DAX cluster<br>is not encrypted<br>by transport layer<br>security (TLS).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14121
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|4.2.1.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|msk-in-cluster-node-<br>require-tls|Ensure that an<br>Amazon MSK cluster<br>enforces encryptio<br>n in transit using<br>HTTPS (TLS) with the<br>broker nodes of the<br>cluster. The rule is<br>NON_COMPLIANT if<br>plain text communica<br>tion is enabled for in-<br>cluster broker node<br>connections.|
|4.2.1.1|PAN is protected with<br>strong cryptography<br>during transmission.<br>(PCI-DSS-v4.0)|dms-endpoint-ssl-c <br>onﬁgured|Ensure that AWS<br>Database Migration<br>Service (AWS DMS)<br>endpoints are<br>conﬁgured with an<br>SSL connection. The<br>rule is NON_COMPL<br>IANT if AWS DMS<br>does not have an SSL<br>connection conﬁgure<br>d.|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|api-gwv2-access-lo <br>gs-enabled|Ensure that Amazon<br>API Gateway V2<br>stages have access<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if 'accessLo<br>gSettings' is not<br>present in Stage<br>conﬁguration.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14122
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|cloudfront-accessl <br>ogs-enabled|Ensure that Amazon<br>CloudFront distribut<br>ions are conﬁgure<br>d to deliver access<br>logs to an Amazon<br>S3 bucket. The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion does not have<br>logging conﬁgured.|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|cloudtrail-security-<br>trail-enabled|Ensure that there<br>is at least one AWS<br>CloudTrail trail<br>deﬁned with security<br>best practices. This<br>rule is COMPLIANT if<br>there is at least one<br>trail that meets all of<br>the following:|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14123
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|neptune-cluster-cl <br>oudwatch-log-expor <br>t-enabled|Ensure that an<br>Amazon Neptune<br>cluster has<br>CloudWatch log<br>export enabled for<br>audit logs. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have CloudWatc<br>h log export enabled<br>for audit logs.|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|ecs-task-deﬁnition-<br>log-conﬁguration|Ensure that logConﬁg<br>uration is set on<br>active ECS Task<br>Deﬁnitions. This<br>rule is NON_COMPL<br>IANT if an active<br>ECSTaskDeﬁnition<br>does not have the<br>logConﬁguration<br>resource deﬁned<br>or the value for<br>logConﬁguration is<br>null in at least one<br>container deﬁnition.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14124
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|cloudtrail-enabled|Note: For this rule,<br>the rule identiﬁe<br>r (CLOUD_TR<br>AIL_ENABLED) and<br>rule name (cloudtrail-<br>enabled) are diﬀerent<br>. Ensure that an AWS<br>CloudTrail trail is<br>enabled in your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>a trail is not enabled.<br>Optionally, the rule<br>checks a speciﬁc<br>S3 bucket, Amazon<br>Simple Notiﬁcation<br>Service (Amazon SNS)<br>topic, and CloudWatc<br>h log group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14125
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|multi-region-cloud <br>trail-enabled|Note: for this rule,<br>the rule identiﬁe<br>r (MULTI_RE<br>GION_CLOU<br>D_TRAIL_ENABLED)<br>and rule name<br>(multi-region-clou<br>dtrail-enabled) are<br>diﬀerent. Ensure<br>that there is at least<br>one multi-region<br>AWS CloudTrail. The<br>rule is NON_COMPL<br>IANT if the trails<br>do not match input<br>parameters. The rule<br>is NON_COMPLIANT<br>if the ExcludeMa<br>nagementEventSourc<br>es ﬁeld is not empty<br>or if AWS CloudTrai<br>l is conﬁgured to<br>exclude managemen<br>t events such as<br>AWS KMS events or<br>Amazon RDS Data<br>API events.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14126
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|appsync-logging-en <br>abled|Ensure that an AWS<br>AppSync API has<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging is not<br>enabled, or 'ﬁeldLog<br>Level' is neither<br>ERROR nor ALL.|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|waf-classic-logging-<br>enabled|Ensure that logging is<br>enabled on AWS WAF<br>classic global web<br>access control lists<br>(web ACLs). The rule<br>is NON_COMPLIANT<br>for a global web ACL,<br>if it does not have<br>logging enabled.|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|mq-cloudwatch-audi <br>t-logging-enabled|Ensure that Amazon<br>MQ brokers have<br>Amazon CloudWatc<br>h audit logging<br>enabled. The rule is<br>NON_COMPLIANT<br>if a broker does not<br>have audit logging<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14127
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|mq-cloudwatch-audi <br>t-log-enabled|Ensure that an<br>Amazon MQ broker<br>has CloudWatch audit<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if the broker<br>does not have audit<br>logging enabled.|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|eks-cluster-logging-<br>enabled|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS) cluster<br>is conﬁgured with<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging for<br>Amazon EKS clusters<br>is not enabled for all<br>log types.|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|elastic-beanstalk- <br>logs-to-cloudwatch|Ensure that AWS<br>Elastic Beanstalk<br>environments<br>are conﬁgured<br>to send logs to<br>Amazon CloudWatc<br>h Logs. The rule<br>is NON_COMPL<br>IANT if the value<br>of `StreamLogs` is<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14128
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|step-functions-sta <br>te-machine-logging-<br>enabled|Ensure that AWS<br>Step Functions<br>machine has logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a state machine does<br>not have logging<br>enabled or the<br>logging conﬁgura<br>tion is not at the<br>minimum level<br>provided.|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|netfw-logging-enab <br>led|Ensure that AWS<br>Network Firewall<br>ﬁrewalls have logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a logging type is not<br>conﬁgured. You can<br>specify which logging<br>type you want the<br>rule to check.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14129
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|5.3.4|Anti-malware<br>mechanisms and<br>processes are active,<br>maintained, and<br>monitored. (PCI-DSS-<br>v4.0)|cw-loggroup-retent <br>ion-period-check|Ensure that an<br>Amazon CloudWatch<br>LogGroup retention<br>period is set to<br>greater than 365 days<br>or else a speciﬁed<br>retention period. The<br>rule is NON_COMPL<br>IANT if the retention<br>period is less than<br>MinRetentionTime, if<br>speciﬁed, or else 365<br>days.|
|6.3.3|Security vulnerabi<br>lities are identiﬁed<br>and addressed. (PCI-<br>DSS-v4.0)|lambda-function-se <br>ttings-check|Ensure that the AWS<br>Lambda function<br>settings for runtime,<br>role, timeout, and<br>memory size match<br>the expected values.<br>The rule ignores<br>functions with the<br>'Image' package type<br>and functions with<br>runtime set to 'OS-<br>only Runtime'. The<br>rule is NON_COMPL<br>IANT if the Lambda<br>function settings<br>do not match the<br>expected values.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14130
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|6.3.3|Security vulnerabi<br>lities are identiﬁed<br>and addressed. (PCI-<br>DSS-v4.0)|eks-cluster-oldest-<br>supported-version|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(EKS) cluster is<br>not running the<br>oldest supported<br>version. The rule<br>is NON_COMPL<br>IANT if an EKS<br>cluster is running<br>oldest supported<br>version (equal to the<br>parameter 'oldestVe<br>rsionSupported').|
|6.4.1|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|cloudfront-associa <br>ted-with-waf|Ensure that Amazon<br>CloudFront distribut<br>ions are associate<br>d with either web<br>application ﬁrewall<br>(WAF) or WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion is not associated<br>with a WAF web ACL.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14131
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|6.4.1|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|appsync-associated-<br>with-waf|Ensure that AWS<br>AppSync APIs are<br>associated with<br>AWS WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT for<br>an AWS AppSync API<br>if it is not associated<br>with a web ACL.|
|6.4.1|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|wafv2-webacl-not-e <br>mpty|Ensure that a WAFv2<br>Web ACL contains<br>any WAF rules or WAF<br>rule groups. This rule<br>is NON_COMPLIANT<br>if a Web ACL does<br>not contain any WAF<br>rules or WAF rule<br>groups.|
|6.4.1|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|wafv2-rulegroup-not-<br>empty|Ensure that WAFv2<br>Rule Groups contain<br>rules. The rule is<br>NON_COMPLIANT if<br>there are no rules in a<br>WAFv2 Rule Group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14132
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|6.4.1|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|waf-global-webacl- <br>not-empty|Ensure that a WAF<br>Global Web ACL<br>contains some<br>WAF rules or rule<br>groups. This rule is<br>NON_COMPLIANT if<br>a Web ACL does not<br>contain any WAF rule<br>or rule group.|
|6.4.1|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|waf-global-rulegro <br>up-not-empty|Ensure that an AWS<br>WAF Classic rule<br>group contains some<br>rules. The rule is<br>NON_COMPLIANT<br>if there are no rules<br>present within a rule<br>group.|
|6.4.1|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|waf-global-rulegro <br>up-not-empty|Ensure that an AWS<br>WAF Classic rule<br>group contains some<br>rules. The rule is<br>NON_COMPLIANT<br>if there are no rules<br>present within a rule<br>group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14133
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|6.4.1|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|waf-global-rule-not-<br>empty|Ensure that an<br>AWS WAF global<br>rule contains some<br>conditions. The rule<br>is NON_COMPLIANT<br>if no conditions are<br>present within the<br>WAF global rule.|
|6.4.2|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|cloudfront-associa <br>ted-with-waf|Ensure that Amazon<br>CloudFront distribut<br>ions are associate<br>d with either web<br>application ﬁrewall<br>(WAF) or WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion is not associated<br>with a WAF web ACL.|
|6.4.2|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|appsync-associated-<br>with-waf|Ensure that AWS<br>AppSync APIs are<br>associated with<br>AWS WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT for<br>an AWS AppSync API<br>if it is not associated<br>with a web ACL.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14134
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|6.4.2|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|wafv2-webacl-not-e <br>mpty|Ensure that a WAFv2<br>Web ACL contains<br>any WAF rules or WAF<br>rule groups. This rule<br>is NON_COMPLIANT<br>if a Web ACL does<br>not contain any WAF<br>rules or WAF rule<br>groups.|
|6.4.2|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|wafv2-rulegroup-not-<br>empty|Ensure that WAFv2<br>Rule Groups contain<br>rules. The rule is<br>NON_COMPLIANT if<br>there are no rules in a<br>WAFv2 Rule Group.|
|6.4.2|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|waf-global-webacl- <br>not-empty|Ensure that a WAF<br>Global Web ACL<br>contains some<br>WAF rules or rule<br>groups. This rule is<br>NON_COMPLIANT if<br>a Web ACL does not<br>contain any WAF rule<br>or rule group.|
|6.4.2|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|waf-global-rulegro <br>up-not-empty|Ensure that an AWS<br>WAF Classic rule<br>group contains some<br>rules. The rule is<br>NON_COMPLIANT<br>if there are no rules<br>present within a rule<br>group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14135
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|6.4.2|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|waf-global-rulegro <br>up-not-empty|Ensure that an AWS<br>WAF Classic rule<br>group contains some<br>rules. The rule is<br>NON_COMPLIANT<br>if there are no rules<br>present within a rule<br>group.|
|6.4.2|Public-facing web<br>applications are<br>protected against<br>attacks. (PCI-DSS-<br>v4.0)|waf-global-rule-not-<br>empty|Ensure that an<br>AWS WAF global<br>rule contains some<br>conditions. The rule<br>is NON_COMPLIANT<br>if no conditions are<br>present within the<br>WAF global rule.|
|6.5.5|Changes to all system<br>components are<br>managed securely.<br>(PCI-DSS-v4.0)|codedeploy-lambda- <br>allatonce-traﬃc- <br>shift-disabled|Ensure that the<br>deployment<br>group for Lambda<br>Compute Platform<br>is not using the<br>default deploymen<br>t conﬁguration. The<br>rule is NON_COMPL<br>IANT if the<br>deployment group is<br>using the deploymen<br>t conﬁguration<br>'CodeDeployDefault<br>.LambdaAllAtOnce'.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14136
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|6.5.5|Changes to all system<br>components are<br>managed securely.<br>(PCI-DSS-v4.0)|codepipeline-deplo <br>yment-count-check|Ensure that the ﬁrst<br>deployment stage of<br>AWS CodePipeline<br>performs at least one<br>deployment. This is<br>to monitor continuou<br>s deployment<br>activity, ensuring<br>regular updates and<br>identifying inactive<br>or underutilized<br>pipelines, which<br>can signal issues<br>in the developme<br>nt or deployment<br>process. Optionall<br>y ensure that each<br>of the subsequen<br>t remaining stages<br>deploy to more than<br>the speciﬁed number<br>of deployments<br>(deploymentLimit).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14137
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|6.5.6|Changes to all system<br>components are<br>managed securely.<br>(PCI-DSS-v4.0)|codedeploy-lambda- <br>allatonce-traﬃc- <br>shift-disabled|Ensure that the<br>deployment<br>group for Lambda<br>Compute Platform<br>is not using the<br>default deploymen<br>t conﬁguration. The<br>rule is NON_COMPL<br>IANT if the<br>deployment group is<br>using the deploymen<br>t conﬁguration<br>'CodeDeployDefault<br>.LambdaAllAtOnce'.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14138
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|6.5.6|Changes to all system<br>components are<br>managed securely.<br>(PCI-DSS-v4.0)|codepipeline-deplo <br>yment-count-check|Ensure that the ﬁrst<br>deployment stage of<br>AWS CodePipeline<br>performs at least one<br>deployment. This is<br>to monitor continuou<br>s deployment<br>activity, ensuring<br>regular updates and<br>identifying inactive<br>or underutilized<br>pipelines, which<br>can signal issues<br>in the developme<br>nt or deployment<br>process. Optionall<br>y ensure that each<br>of the subsequen<br>t remaining stages<br>deploy to more than<br>the speciﬁed number<br>of deployments<br>(deploymentLimit).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14139
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.1|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|s3-bucket-blacklis <br>ted-actions-prohib <br>ited|Ensure that an<br>Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>policy does not allow<br>blocklisted bucket-le<br>vel and object-level<br>actions on resources<br>in the bucket for<br>principals from other<br>AWS accounts. For<br>example, the rule<br>checks that the<br>Amazon S3 bucket<br>policy does not allow<br>another AWS account<br>to perform any<br>s3:GetBucket* actions<br>and s3:DeleteObject<br>on any object in the<br>bucket. The rule is<br>NON_COMPLIANT<br>if any blocklisted<br>actions are allowed<br>by the Amazon S3<br>bucket policy.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14140
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.1|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|s3-bucket-policy-not-<br>more-permissive|Ensure that your<br>Amazon Simple<br>Storage Service (S3)<br>bucket policies do<br>not allow other inter-<br>account permissio<br>ns than the control<br>Amazon S3 bucket<br>policy that you<br>provide.|
|7.2.1|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|shield-drt-access|Ensure that the<br>Shield Response<br>Team (SRT) can<br>access your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>AWS Shield Advanced<br>is enabled but the<br>role for SRT access is<br>not conﬁgured.|
|7.2.1|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14141
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.1|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|neptune-cluster-ia <br>m-database-authent <br>ication|Ensure that an<br>Amazon Neptune<br>cluster has AWS<br>Identity and Access<br>Management (IAM)<br>database authentic<br>ation enabled. The<br>rule is NON_COMPL<br>IANT if an Amazon<br>Neptune cluster<br>does not have IAM<br>database authentic<br>ation enabled.|
|7.2.1|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|rds-cluster-iam-au <br>thentication-enabled|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) cluster<br>has AWS Identity and<br>Access Management<br>(IAM) authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>Cluster does not have<br>IAM authentication<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14142
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.1|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|ec2-instance-proﬁle-<br>attached|Ensure that an EC2<br>instance has an AWS<br>Identity and Access<br>Management (IAM)<br>proﬁle attached<br>to it. The rule is<br>NON_COMPLIANT<br>if no IAM proﬁle is<br>attached to the EC2<br>instance.|
|7.2.1|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|backup-recovery-po <br>int-manual-deletion-<br>disabled|Ensure that a backup<br>vault has an attached<br>resource-based<br>policy which prevents<br>deletion of recovery<br>points. The rule<br>is NON_COMPL<br>IANT if the Backup<br>Vault does not<br>have resource-<br>based policies or<br>has policies without<br>a suitable 'Deny'<br>statement (statemen<br>t with backup:De<br>leteRecoveryPoint,<br>backup:UpdateRecov<br>eryPointLifecycle,<br>and backup:Pu<br>tBackupVaultAccess<br>Policy permissions).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14143
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.1|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|rds-instance-iam-a <br>uthentication-enab <br>led|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS)<br>instance has AWS<br>Identity and Access<br>Management (IAM)<br>authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>instance does not<br>have IAM authentic<br>ation enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14144
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.2|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|s3-bucket-blacklis <br>ted-actions-prohib <br>ited|Ensure that an<br>Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>policy does not allow<br>blocklisted bucket-le<br>vel and object-level<br>actions on resources<br>in the bucket for<br>principals from other<br>AWS accounts. For<br>example, the rule<br>checks that the<br>Amazon S3 bucket<br>policy does not allow<br>another AWS account<br>to perform any<br>s3:GetBucket* actions<br>and s3:DeleteObject<br>on any object in the<br>bucket. The rule is<br>NON_COMPLIANT<br>if any blocklisted<br>actions are allowed<br>by the Amazon S3<br>bucket policy.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14145
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.2|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|s3-bucket-policy-not-<br>more-permissive|Ensure that your<br>Amazon Simple<br>Storage Service (S3)<br>bucket policies do<br>not allow other inter-<br>account permissio<br>ns than the control<br>Amazon S3 bucket<br>policy that you<br>provide.|
|7.2.2|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|shield-drt-access|Ensure that the<br>Shield Response<br>Team (SRT) can<br>access your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>AWS Shield Advanced<br>is enabled but the<br>role for SRT access is<br>not conﬁgured.|
|7.2.2|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14146
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.2|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|neptune-cluster-ia <br>m-database-authent <br>ication|Ensure that an<br>Amazon Neptune<br>cluster has AWS<br>Identity and Access<br>Management (IAM)<br>database authentic<br>ation enabled. The<br>rule is NON_COMPL<br>IANT if an Amazon<br>Neptune cluster<br>does not have IAM<br>database authentic<br>ation enabled.|
|7.2.2|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|rds-cluster-iam-au <br>thentication-enabled|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) cluster<br>has AWS Identity and<br>Access Management<br>(IAM) authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>Cluster does not have<br>IAM authentication<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14147
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.2|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|ec2-instance-proﬁle-<br>attached|Ensure that an EC2<br>instance has an AWS<br>Identity and Access<br>Management (IAM)<br>proﬁle attached<br>to it. The rule is<br>NON_COMPLIANT<br>if no IAM proﬁle is<br>attached to the EC2<br>instance.|
|7.2.2|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|backup-recovery-po <br>int-manual-deletion-<br>disabled|Ensure that a backup<br>vault has an attached<br>resource-based<br>policy which prevents<br>deletion of recovery<br>points. The rule<br>is NON_COMPL<br>IANT if the Backup<br>Vault does not<br>have resource-<br>based policies or<br>has policies without<br>a suitable 'Deny'<br>statement (statemen<br>t with backup:De<br>leteRecoveryPoint,<br>backup:UpdateRecov<br>eryPointLifecycle,<br>and backup:Pu<br>tBackupVaultAccess<br>Policy permissions).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14148
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.2|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|rds-instance-iam-a <br>uthentication-enab <br>led|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS)<br>instance has AWS<br>Identity and Access<br>Management (IAM)<br>authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>instance does not<br>have IAM authentic<br>ation enabled.|
|7.2.4|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|secretsmanager-sec <br>ret-unused|Ensure that AWS<br>Secrets Manager<br>secrets have been<br>accessed within a<br>speciﬁed number<br>of days. The rule is<br>NON_COMPLIANT if<br>a secret has not been<br>accessed in 'unusedFo<br>rDays' number of<br>days. The default<br>value is 90 days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14149
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.5|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|s3-bucket-blacklis <br>ted-actions-prohib <br>ited|Ensure that an<br>Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>policy does not allow<br>blocklisted bucket-le<br>vel and object-level<br>actions on resources<br>in the bucket for<br>principals from other<br>AWS accounts. For<br>example, the rule<br>checks that the<br>Amazon S3 bucket<br>policy does not allow<br>another AWS account<br>to perform any<br>s3:GetBucket* actions<br>and s3:DeleteObject<br>on any object in the<br>bucket. The rule is<br>NON_COMPLIANT<br>if any blocklisted<br>actions are allowed<br>by the Amazon S3<br>bucket policy.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14150
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.5|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|s3-bucket-policy-not-<br>more-permissive|Ensure that your<br>Amazon Simple<br>Storage Service (S3)<br>bucket policies do<br>not allow other inter-<br>account permissio<br>ns than the control<br>Amazon S3 bucket<br>policy that you<br>provide.|
|7.2.5|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|shield-drt-access|Ensure that the<br>Shield Response<br>Team (SRT) can<br>access your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>AWS Shield Advanced<br>is enabled but the<br>role for SRT access is<br>not conﬁgured.|
|7.2.5|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14151
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.5|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|neptune-cluster-ia <br>m-database-authent <br>ication|Ensure that an<br>Amazon Neptune<br>cluster has AWS<br>Identity and Access<br>Management (IAM)<br>database authentic<br>ation enabled. The<br>rule is NON_COMPL<br>IANT if an Amazon<br>Neptune cluster<br>does not have IAM<br>database authentic<br>ation enabled.|
|7.2.5|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|rds-cluster-iam-au <br>thentication-enabled|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) cluster<br>has AWS Identity and<br>Access Management<br>(IAM) authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>Cluster does not have<br>IAM authentication<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14152
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.5|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|ec2-instance-proﬁle-<br>attached|Ensure that an EC2<br>instance has an AWS<br>Identity and Access<br>Management (IAM)<br>proﬁle attached<br>to it. The rule is<br>NON_COMPLIANT<br>if no IAM proﬁle is<br>attached to the EC2<br>instance.|
|7.2.5|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|backup-recovery-po <br>int-manual-deletion-<br>disabled|Ensure that a backup<br>vault has an attached<br>resource-based<br>policy which prevents<br>deletion of recovery<br>points. The rule<br>is NON_COMPL<br>IANT if the Backup<br>Vault does not<br>have resource-<br>based policies or<br>has policies without<br>a suitable 'Deny'<br>statement (statemen<br>t with backup:De<br>leteRecoveryPoint,<br>backup:UpdateRecov<br>eryPointLifecycle,<br>and backup:Pu<br>tBackupVaultAccess<br>Policy permissions).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14153
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.5|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|rds-instance-iam-a <br>uthentication-enab <br>led|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS)<br>instance has AWS<br>Identity and Access<br>Management (IAM)<br>authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>instance does not<br>have IAM authentic<br>ation enabled.|
|7.2.5.1|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|secretsmanager-sec <br>ret-unused|Ensure that AWS<br>Secrets Manager<br>secrets have been<br>accessed within a<br>speciﬁed number<br>of days. The rule is<br>NON_COMPLIANT if<br>a secret has not been<br>accessed in 'unusedFo<br>rDays' number of<br>days. The default<br>value is 90 days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14154
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.6|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|s3-bucket-blacklis <br>ted-actions-prohib <br>ited|Ensure that an<br>Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>policy does not allow<br>blocklisted bucket-le<br>vel and object-level<br>actions on resources<br>in the bucket for<br>principals from other<br>AWS accounts. For<br>example, the rule<br>checks that the<br>Amazon S3 bucket<br>policy does not allow<br>another AWS account<br>to perform any<br>s3:GetBucket* actions<br>and s3:DeleteObject<br>on any object in the<br>bucket. The rule is<br>NON_COMPLIANT<br>if any blocklisted<br>actions are allowed<br>by the Amazon S3<br>bucket policy.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14155
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.2.6|Access to system<br>components and<br>data is appropriately<br>deﬁned and assigned.<br>(PCI-DSS-v4.0)|s3-bucket-policy-not-<br>more-permissive|Ensure that your<br>Amazon Simple<br>Storage Service (S3)<br>bucket policies do<br>not allow other inter-<br>account permissio<br>ns than the control<br>Amazon S3 bucket<br>policy that you<br>provide.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14156
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.1|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|s3-bucket-blacklis <br>ted-actions-prohib <br>ited|Ensure that an<br>Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>policy does not allow<br>blocklisted bucket-le<br>vel and object-level<br>actions on resources<br>in the bucket for<br>principals from other<br>AWS accounts. For<br>example, the rule<br>checks that the<br>Amazon S3 bucket<br>policy does not allow<br>another AWS account<br>to perform any<br>s3:GetBucket* actions<br>and s3:DeleteObject<br>on any object in the<br>bucket. The rule is<br>NON_COMPLIANT<br>if any blocklisted<br>actions are allowed<br>by the Amazon S3<br>bucket policy.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14157
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.1|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|s3-bucket-policy-not-<br>more-permissive|Ensure that your<br>Amazon Simple<br>Storage Service (S3)<br>bucket policies do<br>not allow other inter-<br>account permissio<br>ns than the control<br>Amazon S3 bucket<br>policy that you<br>provide.|
|7.3.1|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|shield-drt-access|Ensure that the<br>Shield Response<br>Team (SRT) can<br>access your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>AWS Shield Advanced<br>is enabled but the<br>role for SRT access is<br>not conﬁgured.|
|7.3.1|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14158
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.1|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|neptune-cluster-ia <br>m-database-authent <br>ication|Ensure that an<br>Amazon Neptune<br>cluster has AWS<br>Identity and Access<br>Management (IAM)<br>database authentic<br>ation enabled. The<br>rule is NON_COMPL<br>IANT if an Amazon<br>Neptune cluster<br>does not have IAM<br>database authentic<br>ation enabled.|
|7.3.1|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|rds-cluster-iam-au <br>thentication-enabled|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) cluster<br>has AWS Identity and<br>Access Management<br>(IAM) authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>Cluster does not have<br>IAM authentication<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14159
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.1|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|ec2-instance-proﬁle-<br>attached|Ensure that an EC2<br>instance has an AWS<br>Identity and Access<br>Management (IAM)<br>proﬁle attached<br>to it. The rule is<br>NON_COMPLIANT<br>if no IAM proﬁle is<br>attached to the EC2<br>instance.|
|7.3.1|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|backup-recovery-po <br>int-manual-deletion-<br>disabled|Ensure that a backup<br>vault has an attached<br>resource-based<br>policy which prevents<br>deletion of recovery<br>points. The rule<br>is NON_COMPL<br>IANT if the Backup<br>Vault does not<br>have resource-<br>based policies or<br>has policies without<br>a suitable 'Deny'<br>statement (statemen<br>t with backup:De<br>leteRecoveryPoint,<br>backup:UpdateRecov<br>eryPointLifecycle,<br>and backup:Pu<br>tBackupVaultAccess<br>Policy permissions).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14160
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.1|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|rds-instance-iam-a <br>uthentication-enab <br>led|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS)<br>instance has AWS<br>Identity and Access<br>Management (IAM)<br>authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>instance does not<br>have IAM authentic<br>ation enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14161
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.2|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|s3-bucket-blacklis <br>ted-actions-prohib <br>ited|Ensure that an<br>Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>policy does not allow<br>blocklisted bucket-le<br>vel and object-level<br>actions on resources<br>in the bucket for<br>principals from other<br>AWS accounts. For<br>example, the rule<br>checks that the<br>Amazon S3 bucket<br>policy does not allow<br>another AWS account<br>to perform any<br>s3:GetBucket* actions<br>and s3:DeleteObject<br>on any object in the<br>bucket. The rule is<br>NON_COMPLIANT<br>if any blocklisted<br>actions are allowed<br>by the Amazon S3<br>bucket policy.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14162
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.2|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|s3-bucket-policy-not-<br>more-permissive|Ensure that your<br>Amazon Simple<br>Storage Service (S3)<br>bucket policies do<br>not allow other inter-<br>account permissio<br>ns than the control<br>Amazon S3 bucket<br>policy that you<br>provide.|
|7.3.2|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|shield-drt-access|Ensure that the<br>Shield Response<br>Team (SRT) can<br>access your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>AWS Shield Advanced<br>is enabled but the<br>role for SRT access is<br>not conﬁgured.|
|7.3.2|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14163
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.2|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|neptune-cluster-ia <br>m-database-authent <br>ication|Ensure that an<br>Amazon Neptune<br>cluster has AWS<br>Identity and Access<br>Management (IAM)<br>database authentic<br>ation enabled. The<br>rule is NON_COMPL<br>IANT if an Amazon<br>Neptune cluster<br>does not have IAM<br>database authentic<br>ation enabled.|
|7.3.2|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|rds-cluster-iam-au <br>thentication-enabled|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) cluster<br>has AWS Identity and<br>Access Management<br>(IAM) authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>Cluster does not have<br>IAM authentication<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14164
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.2|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|ec2-instance-proﬁle-<br>attached|Ensure that an EC2<br>instance has an AWS<br>Identity and Access<br>Management (IAM)<br>proﬁle attached<br>to it. The rule is<br>NON_COMPLIANT<br>if no IAM proﬁle is<br>attached to the EC2<br>instance.|
|7.3.2|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|backup-recovery-po <br>int-manual-deletion-<br>disabled|Ensure that a backup<br>vault has an attached<br>resource-based<br>policy which prevents<br>deletion of recovery<br>points. The rule<br>is NON_COMPL<br>IANT if the Backup<br>Vault does not<br>have resource-<br>based policies or<br>has policies without<br>a suitable 'Deny'<br>statement (statemen<br>t with backup:De<br>leteRecoveryPoint,<br>backup:UpdateRecov<br>eryPointLifecycle,<br>and backup:Pu<br>tBackupVaultAccess<br>Policy permissions).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14165
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.2|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|rds-instance-iam-a <br>uthentication-enab <br>led|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS)<br>instance has AWS<br>Identity and Access<br>Management (IAM)<br>authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>instance does not<br>have IAM authentic<br>ation enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14166
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.3|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|s3-bucket-blacklis <br>ted-actions-prohib <br>ited|Ensure that an<br>Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>policy does not allow<br>blocklisted bucket-le<br>vel and object-level<br>actions on resources<br>in the bucket for<br>principals from other<br>AWS accounts. For<br>example, the rule<br>checks that the<br>Amazon S3 bucket<br>policy does not allow<br>another AWS account<br>to perform any<br>s3:GetBucket* actions<br>and s3:DeleteObject<br>on any object in the<br>bucket. The rule is<br>NON_COMPLIANT<br>if any blocklisted<br>actions are allowed<br>by the Amazon S3<br>bucket policy.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14167
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.3|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|s3-bucket-policy-not-<br>more-permissive|Ensure that your<br>Amazon Simple<br>Storage Service (S3)<br>bucket policies do<br>not allow other inter-<br>account permissio<br>ns than the control<br>Amazon S3 bucket<br>policy that you<br>provide.|
|7.3.3|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|shield-drt-access|Ensure that the<br>Shield Response<br>Team (SRT) can<br>access your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>AWS Shield Advanced<br>is enabled but the<br>role for SRT access is<br>not conﬁgured.|
|7.3.3|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14168
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.3|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|neptune-cluster-ia <br>m-database-authent <br>ication|Ensure that an<br>Amazon Neptune<br>cluster has AWS<br>Identity and Access<br>Management (IAM)<br>database authentic<br>ation enabled. The<br>rule is NON_COMPL<br>IANT if an Amazon<br>Neptune cluster<br>does not have IAM<br>database authentic<br>ation enabled.|
|7.3.3|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|rds-cluster-iam-au <br>thentication-enabled|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) cluster<br>has AWS Identity and<br>Access Management<br>(IAM) authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>Cluster does not have<br>IAM authentication<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14169
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.3|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|ec2-instance-proﬁle-<br>attached|Ensure that an EC2<br>instance has an AWS<br>Identity and Access<br>Management (IAM)<br>proﬁle attached<br>to it. The rule is<br>NON_COMPLIANT<br>if no IAM proﬁle is<br>attached to the EC2<br>instance.|
|7.3.3|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|backup-recovery-po <br>int-manual-deletion-<br>disabled|Ensure that a backup<br>vault has an attached<br>resource-based<br>policy which prevents<br>deletion of recovery<br>points. The rule<br>is NON_COMPL<br>IANT if the Backup<br>Vault does not<br>have resource-<br>based policies or<br>has policies without<br>a suitable 'Deny'<br>statement (statemen<br>t with backup:De<br>leteRecoveryPoint,<br>backup:UpdateRecov<br>eryPointLifecycle,<br>and backup:Pu<br>tBackupVaultAccess<br>Policy permissions).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14170
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|7.3.3|Access to system<br>components and<br>data is managed via<br>an access control<br>system(s). (PCI-DSS-<br>v4.0)|rds-instance-iam-a <br>uthentication-enab <br>led|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS)<br>instance has AWS<br>Identity and Access<br>Management (IAM)<br>authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>instance does not<br>have IAM authentic<br>ation enabled.|
|8.2.1|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
|8.2.1|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|ec2-no-amazon-key- <br>pair|Ensure that running<br>Amazon Elastic<br>Compute Cloud<br>(EC2) instances<br>are not launched<br>using amazon key<br>pairs. The rule is<br>NON_COMPLIANT if a<br>running EC2 instance<br>is launched with a key<br>pair.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14171
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.2|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
|8.2.2|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|ec2-no-amazon-key- <br>pair|Ensure that running<br>Amazon Elastic<br>Compute Cloud<br>(EC2) instances<br>are not launched<br>using amazon key<br>pairs. The rule is<br>NON_COMPLIANT if a<br>running EC2 instance<br>is launched with a key<br>pair.|
|8.2.2|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|codebuild-project- <br>envvar-awscred-che <br>ck|Ensure that the<br>project DOES NOT<br>contain environment<br>variables AWS_ACCES<br>S_KEY_ID and<br>AWS_SECRE<br>T_ACCESS_KEY. The<br>rule is NON_COMPL<br>IANT when the<br>project environme<br>nt variables contains<br>plaintext credentials.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14172
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.2|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|secretsmanager-sch <br>eduled-rotation-su <br>ccess-check|Ensure that AWS<br>Secrets Manager<br>secrets rotated<br>successfully according<br>to the rotation<br>schedule. Secrets<br>Manager calculates<br>the date the rotation<br>should happen. The<br>rule is NON_COMPL<br>IANT if the date<br>passes and the secret<br>isn't rotated.|
|8.2.2|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|secretsmanager-sec <br>ret-periodic-rotation|Ensure that AWS<br>Secrets Manager<br>secrets have been<br>rotated in the past<br>speciﬁed number<br>of days. The rule is<br>NON_COMPLIANT if<br>a secret has not been<br>rotated for more than<br>maxDaysSinceRotati<br>on number of days.<br>The default value is<br>90 days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14173
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.2|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|secretsmanager-sec <br>ret-unused|Ensure that AWS<br>Secrets Manager<br>secrets have been<br>accessed within a<br>speciﬁed number<br>of days. The rule is<br>NON_COMPLIANT if<br>a secret has not been<br>accessed in 'unusedFo<br>rDays' number of<br>days. The default<br>value is 90 days.|
|8.2.4|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
|8.2.4|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|ec2-no-amazon-key- <br>pair|Ensure that running<br>Amazon Elastic<br>Compute Cloud<br>(EC2) instances<br>are not launched<br>using amazon key<br>pairs. The rule is<br>NON_COMPLIANT if a<br>running EC2 instance<br>is launched with a key<br>pair.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14174
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.5|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
|8.2.5|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|ec2-no-amazon-key- <br>pair|Ensure that running<br>Amazon Elastic<br>Compute Cloud<br>(EC2) instances<br>are not launched<br>using amazon key<br>pairs. The rule is<br>NON_COMPLIANT if a<br>running EC2 instance<br>is launched with a key<br>pair.|
|8.2.6|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|secretsmanager-sec <br>ret-unused|Ensure that AWS<br>Secrets Manager<br>secrets have been<br>accessed within a<br>speciﬁed number<br>of days. The rule is<br>NON_COMPLIANT if<br>a secret has not been<br>accessed in 'unusedFo<br>rDays' number of<br>days. The default<br>value is 90 days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14175
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.7|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|s3-bucket-blacklis <br>ted-actions-prohib <br>ited|Ensure that an<br>Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>policy does not allow<br>blocklisted bucket-le<br>vel and object-level<br>actions on resources<br>in the bucket for<br>principals from other<br>AWS accounts. For<br>example, the rule<br>checks that the<br>Amazon S3 bucket<br>policy does not allow<br>another AWS account<br>to perform any<br>s3:GetBucket* actions<br>and s3:DeleteObject<br>on any object in the<br>bucket. The rule is<br>NON_COMPLIANT<br>if any blocklisted<br>actions are allowed<br>by the Amazon S3<br>bucket policy.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14176
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.7|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|s3-bucket-policy-not-<br>more-permissive|Ensure that your<br>Amazon Simple<br>Storage Service (S3)<br>bucket policies do<br>not allow other inter-<br>account permissio<br>ns than the control<br>Amazon S3 bucket<br>policy that you<br>provide.|
|8.2.7|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|shield-drt-access|Ensure that the<br>Shield Response<br>Team (SRT) can<br>access your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>AWS Shield Advanced<br>is enabled but the<br>role for SRT access is<br>not conﬁgured.|
|8.2.7|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14177
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.7|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|neptune-cluster-ia <br>m-database-authent <br>ication|Ensure that an<br>Amazon Neptune<br>cluster has AWS<br>Identity and Access<br>Management (IAM)<br>database authentic<br>ation enabled. The<br>rule is NON_COMPL<br>IANT if an Amazon<br>Neptune cluster<br>does not have IAM<br>database authentic<br>ation enabled.|
|8.2.7|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|rds-cluster-iam-au <br>thentication-enabled|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) cluster<br>has AWS Identity and<br>Access Management<br>(IAM) authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>Cluster does not have<br>IAM authentication<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14178
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.7|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|ec2-instance-proﬁle-<br>attached|Ensure that an EC2<br>instance has an AWS<br>Identity and Access<br>Management (IAM)<br>proﬁle attached<br>to it. The rule is<br>NON_COMPLIANT<br>if no IAM proﬁle is<br>attached to the EC2<br>instance.|
|8.2.7|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|backup-recovery-po <br>int-manual-deletion-<br>disabled|Ensure that a backup<br>vault has an attached<br>resource-based<br>policy which prevents<br>deletion of recovery<br>points. The rule<br>is NON_COMPL<br>IANT if the Backup<br>Vault does not<br>have resource-<br>based policies or<br>has policies without<br>a suitable 'Deny'<br>statement (statemen<br>t with backup:De<br>leteRecoveryPoint,<br>backup:UpdateRecov<br>eryPointLifecycle,<br>and backup:Pu<br>tBackupVaultAccess<br>Policy permissions).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14179
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.7|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|rds-instance-iam-a <br>uthentication-enab <br>led|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS)<br>instance has AWS<br>Identity and Access<br>Management (IAM)<br>authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>instance does not<br>have IAM authentic<br>ation enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14180
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.8|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|s3-bucket-blacklis <br>ted-actions-prohib <br>ited|Ensure that an<br>Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>policy does not allow<br>blocklisted bucket-le<br>vel and object-level<br>actions on resources<br>in the bucket for<br>principals from other<br>AWS accounts. For<br>example, the rule<br>checks that the<br>Amazon S3 bucket<br>policy does not allow<br>another AWS account<br>to perform any<br>s3:GetBucket* actions<br>and s3:DeleteObject<br>on any object in the<br>bucket. The rule is<br>NON_COMPLIANT<br>if any blocklisted<br>actions are allowed<br>by the Amazon S3<br>bucket policy.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14181
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.8|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|s3-bucket-policy-not-<br>more-permissive|Ensure that your<br>Amazon Simple<br>Storage Service (S3)<br>bucket policies do<br>not allow other inter-<br>account permissio<br>ns than the control<br>Amazon S3 bucket<br>policy that you<br>provide.|
|8.2.8|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|shield-drt-access|Ensure that the<br>Shield Response<br>Team (SRT) can<br>access your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>AWS Shield Advanced<br>is enabled but the<br>role for SRT access is<br>not conﬁgured.|
|8.2.8|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14182
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.8|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|neptune-cluster-ia <br>m-database-authent <br>ication|Ensure that an<br>Amazon Neptune<br>cluster has AWS<br>Identity and Access<br>Management (IAM)<br>database authentic<br>ation enabled. The<br>rule is NON_COMPL<br>IANT if an Amazon<br>Neptune cluster<br>does not have IAM<br>database authentic<br>ation enabled.|
|8.2.8|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|rds-cluster-iam-au <br>thentication-enabled|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) cluster<br>has AWS Identity and<br>Access Management<br>(IAM) authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>Cluster does not have<br>IAM authentication<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14183
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.8|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|ec2-imdsv2-check|Ensure that<br>your Amazon<br>Elastic Compute<br>Cloud (Amazon<br>EC2) instance<br>metadata version<br>is conﬁgured with<br>Instance Metadata<br>Service Version 2<br>(IMDSv2). The rule is<br>NON_COMPLIANT if<br>the HttpTokens is set<br>to optional.|
|8.2.8|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|ec2-instance-proﬁle-<br>attached|Ensure that an EC2<br>instance has an AWS<br>Identity and Access<br>Management (IAM)<br>proﬁle attached<br>to it. The rule is<br>NON_COMPLIANT<br>if no IAM proﬁle is<br>attached to the EC2<br>instance.|
|8.2.8|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|autoscaling-launch <br>conﬁg-requires-im <br>dsv2|Ensure that<br>only IMDSv2 is<br>enabled. This rule is<br>NON_COMPLIANT if<br>the Metadata version<br>is not included in the<br>launch conﬁguration<br>or if both Metadata<br>V1 and V2 are<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14184
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.8|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|backup-recovery-po <br>int-manual-deletion-<br>disabled|Ensure that a backup<br>vault has an attached<br>resource-based<br>policy which prevents<br>deletion of recovery<br>points. The rule<br>is NON_COMPL<br>IANT if the Backup<br>Vault does not<br>have resource-<br>based policies or<br>has policies without<br>a suitable 'Deny'<br>statement (statemen<br>t with backup:De<br>leteRecoveryPoint,<br>backup:UpdateRecov<br>eryPointLifecycle,<br>and backup:Pu<br>tBackupVaultAccess<br>Policy permissions).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14185
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.2.8|User identiﬁc<br>ation and related<br>accounts for users<br>and administrators<br>are strictly managed<br>throughout an<br>accounts lifecycle.<br>(PCI-DSS-v4.0)|rds-instance-iam-a <br>uthentication-enab <br>led|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS)<br>instance has AWS<br>Identity and Access<br>Management (IAM)<br>authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>instance does not<br>have IAM authentic<br>ation enabled.|
|8.3.10.1|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|access-keys-rotated|Ensure that active<br>IAM access keys are<br>rotated (changed)<br>within the number<br>of days speciﬁed<br>in maxAccess<br>KeyAge. The rule is<br>NON_COMPLIANT if<br>access keys are not<br>rotated within the<br>speciﬁed time period.<br>The default value is<br>90 days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14186
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.10.1|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|secretsmanager-sch <br>eduled-rotation-su <br>ccess-check|Ensure that AWS<br>Secrets Manager<br>secrets rotated<br>successfully according<br>to the rotation<br>schedule. Secrets<br>Manager calculates<br>the date the rotation<br>should happen. The<br>rule is NON_COMPL<br>IANT if the date<br>passes and the secret<br>isn't rotated.|
|8.3.10.1|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|secretsmanager-sec <br>ret-periodic-rotation|Ensure that AWS<br>Secrets Manager<br>secrets have been<br>rotated in the past<br>speciﬁed number<br>of days. The rule is<br>NON_COMPLIANT if<br>a secret has not been<br>rotated for more than<br>maxDaysSinceRotati<br>on number of days.<br>The default value is<br>90 days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14187
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.11|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
|8.3.11|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|ec2-no-amazon-key- <br>pair|Ensure that running<br>Amazon Elastic<br>Compute Cloud<br>(EC2) instances<br>are not launched<br>using amazon key<br>pairs. The rule is<br>NON_COMPLIANT if a<br>running EC2 instance<br>is launched with a key<br>pair.|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|athena-workgroup-e <br>ncrypted-at-rest|Ensure that an<br>Amazon Athena<br>workgroup is<br>encrypted at rest. The<br>rule is NON_COMPL<br>IANT if encryptio<br>n of data at rest is<br>not enabled for an<br>Athena workgroup.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14188
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|neptune-cluster-sn <br>apshot-encrypted|Ensure that an<br>Amazon Neptune DB<br>cluster has snapshots<br>encrypted. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have snapshots<br>encrypted.|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|redshift-cluster-kms-<br>enabled|Ensure that Amazon<br>Redshift clusters are<br>using a speciﬁed AWS<br>Key Management<br>Service (AWS KMS)<br>key for encryptio<br>n. The rule is<br>COMPLIANT if<br>encryption is enabled<br>and the cluster is<br>encrypted with<br>the key provided<br>in the kmsKeyArn<br>parameter. The rule<br>is NON_COMPL<br>IANT if the cluster<br>is not encrypted<br>or encrypted with<br>another key.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14189
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|codebuild-project- <br>artifact-encryption|Ensure that an AWS<br>CodeBuild project<br>has encryption<br>enabled for all of its<br>artifacts. The rule is<br>NON_COMPLIANT if<br>'encryptionDisabled'<br>is set to 'true' for any<br>primary or secondary<br>(if present) artifact<br>conﬁgurations.|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|codebuild-project-s3-<br>logs-encrypted|Ensure that an AWS<br>CodeBuild project<br>conﬁgured with<br>Amazon S3 Logs has<br>encryption enabled<br>for its logs. The rule<br>is NON_COMPLIANT<br>if'encryptionDisab<br>led' is set to'true' in<br>a S3LogsConﬁg of a<br>CodeBuild project.|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|dax-encryption-ena <br>bled|Ensure that Amazon<br>DynamoDB Accelerat<br>or (DAX) clusters are<br>encrypted. The rule<br>is NON_COMPLIANT<br>if a DAX cluster is not<br>encrypted.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14190
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|dms-redis-tls-enab <br>led|Ensure that AWS<br>Database Migration<br>Service (AWS DMS)<br>endpoints for Redis<br>data stores are<br>enabled for TLS/SSL<br>encryption of data<br>communicated with<br>other endpoints. The<br>rule is NON_COMPL<br>IANT if TLS/SSL<br>encryption is not<br>enabled.|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|eks-secrets-encryp <br>ted|Ensure that Amazon<br>Elastic Kubernetes<br>Service clusters are<br>conﬁgured to have<br>Kubernetes secrets<br>encrypted using AWS<br>Key Management<br>Service (KMS) keys.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14191
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|api-gw-cache-enabl <br>ed-and-encrypted|Ensure that all<br>methods in Amazon<br>API Gateway<br>stages have cache<br>enabled and cache<br>encrypted. The rule<br>is NON_COMPL<br>IANT if any method<br>in an Amazon API<br>Gateway stage is not<br>conﬁgured to cache<br>or the cache is not<br>encrypted.|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|docdb-cluster-encr <br>ypted|Ensure that storage<br>encryption is enabled<br>for your Amazon<br>DocumentDB (with<br>MongoDB compatibi<br>lity) clusters. The rule<br>is NON_COMPLIANT<br>if storage encryption<br>is not enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14192
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|dynamodb-table-enc <br>rypted-kms|Ensure that Amazon<br>DynamoDB table is<br>encrypted with AWS<br>Key Management<br>Service (KMS). The<br>rule is NON_COMPL<br>IANT if Amazon<br>DynamoDB table is<br>not encrypted with<br>AWS KMS. The rule<br>is also NON_COMPL<br>IANT if the encrypted<br>AWS KMS key is not<br>present in kmsKeyArn<br>s input parameter.|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|dynamodb-table-enc <br>ryption-enabled|Ensure that the<br>Amazon DynamoDB<br>tables are encrypted<br>and checks their<br>status. The rule is<br>COMPLIANT if the<br>status is enabled or<br>enabling.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14193
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|cloudfront-no-depr <br>ecated-ssl-protocols|Ensure that<br>CloudFront distribut<br>ions are not using<br>deprecated SSL<br>protocols for HTTPS<br>communication<br>between CloudFron<br>t edge locations and<br>custom origins. This<br>rule is NON_COMPL<br>IANT for a CloudFron<br>t distribution if<br>any'OriginSslProto<br>cols' includes'SSLv3'.|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|cloudfront-traﬃc-to-<br>origin-encrypted|Ensure that Amazon<br>CloudFront distribut<br>ions are encryptin<br>g traﬃc to custom<br>origins. The rule is<br>NON_COMPLIANT<br>if'OriginProtocolP<br>olicy' is'http-only' or<br>if'OriginProtocolP<br>olicy' is'match-viewer'<br>and'ViewerProtocol<br>Policy' is'allow-all'.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14194
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|cloudfront-viewer- <br>policy-https|Ensure that your<br>Amazon CloudFron<br>t distributions use<br>HTTPS (directly or<br>via a redirection). The<br>rule is NON_COMPL<br>IANT if the value of<br>ViewerProtocolPoli<br>cy is set to 'allow-al<br>l' for the DefaultCa<br>cheBehavior or for<br>the CacheBehaviors.|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|codebuild-project- <br>envvar-awscred-che <br>ck|Ensure that the<br>project DOES NOT<br>contain environment<br>variables AWS_ACCES<br>S_KEY_ID and<br>AWS_SECRE<br>T_ACCESS_KEY. The<br>rule is NON_COMPL<br>IANT when the<br>project environme<br>nt variables contains<br>plaintext credentials.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14195
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|dax-tls-endpoint-e <br>ncryption|Ensure that your<br>Amazon DynamoDB<br>Accelerator (DAX)<br>cluster has ClusterEn<br>dpointEncryptionTy<br>pe set to TLS. The<br>rule is NON_COMPL<br>IANT if a DAX cluster<br>is not encrypted<br>by transport layer<br>security (TLS).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14196
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|eks-cluster-secrets-<br>encrypted|Ensure that Amazon<br>EKS clusters are not<br>conﬁgured to have<br>Kubernetes secrets<br>encrypted using<br>AWS KMS. The rule is<br>NON_COMPLIANT if<br>an EKS cluster does<br>not have an encryptio<br>nConﬁg resource or<br>if encryptionConﬁg<br>does not name<br>secrets as a resource.|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|kinesis-stream-enc <br>rypted|Ensure that Amazon<br>Kinesis streams are<br>encrypted at rest<br>with server-side<br>encryption. The rule<br>is NON_COMPLIANT<br>for a Kinesis stream if<br>'StreamEncryption' is<br>not present.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14197
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|msk-in-cluster-node-<br>require-tls|Ensure that an<br>Amazon MSK cluster<br>enforces encryptio<br>n in transit using<br>HTTPS (TLS) with the<br>broker nodes of the<br>cluster. The rule is<br>NON_COMPLIANT if<br>plain text communica<br>tion is enabled for in-<br>cluster broker node<br>connections.|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|neptune-cluster-en <br>crypted|Ensure that storage<br>encryption is<br>enabled for your<br>Amazon Neptune DB<br>clusters. The rule is<br>NON_COMPLIANT if<br>storage encryption is<br>not enabled.|
|8.3.2|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|dms-endpoint-ssl-c <br>onﬁgured|Ensure that AWS<br>Database Migration<br>Service (AWS DMS)<br>endpoints are<br>conﬁgured with an<br>SSL connection. The<br>rule is NON_COMPL<br>IANT if AWS DMS<br>does not have an SSL<br>connection conﬁgure<br>d.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14198
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.4|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|s3-bucket-blacklis <br>ted-actions-prohib <br>ited|Ensure that an<br>Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>policy does not allow<br>blocklisted bucket-le<br>vel and object-level<br>actions on resources<br>in the bucket for<br>principals from other<br>AWS accounts. For<br>example, the rule<br>checks that the<br>Amazon S3 bucket<br>policy does not allow<br>another AWS account<br>to perform any<br>s3:GetBucket* actions<br>and s3:DeleteObject<br>on any object in the<br>bucket. The rule is<br>NON_COMPLIANT<br>if any blocklisted<br>actions are allowed<br>by the Amazon S3<br>bucket policy.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14199
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.4|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|s3-bucket-policy-not-<br>more-permissive|Ensure that your<br>Amazon Simple<br>Storage Service (S3)<br>bucket policies do<br>not allow other inter-<br>account permissio<br>ns than the control<br>Amazon S3 bucket<br>policy that you<br>provide.|
|8.3.4|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|shield-drt-access|Ensure that the<br>Shield Response<br>Team (SRT) can<br>access your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>AWS Shield Advanced<br>is enabled but the<br>role for SRT access is<br>not conﬁgured.|
|8.3.4|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|iam-policy-in-use|Ensure that an<br>IAM policy ARN is<br>attached to an IAM<br>user, or a group with<br>one or more IAM<br>users, or an IAM role<br>with one or more<br>trusted entity.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14200
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.4|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|neptune-cluster-ia <br>m-database-authent <br>ication|Ensure that an<br>Amazon Neptune<br>cluster has AWS<br>Identity and Access<br>Management (IAM)<br>database authentic<br>ation enabled. The<br>rule is NON_COMPL<br>IANT if an Amazon<br>Neptune cluster<br>does not have IAM<br>database authentic<br>ation enabled.|
|8.3.4|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|rds-cluster-iam-au <br>thentication-enabled|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) cluster<br>has AWS Identity and<br>Access Management<br>(IAM) authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>Cluster does not have<br>IAM authentication<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14201
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.4|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|ec2-instance-proﬁle-<br>attached|Ensure that an EC2<br>instance has an AWS<br>Identity and Access<br>Management (IAM)<br>proﬁle attached<br>to it. The rule is<br>NON_COMPLIANT<br>if no IAM proﬁle is<br>attached to the EC2<br>instance.|
|8.3.4|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|backup-recovery-po <br>int-manual-deletion-<br>disabled|Ensure that a backup<br>vault has an attached<br>resource-based<br>policy which prevents<br>deletion of recovery<br>points. The rule<br>is NON_COMPL<br>IANT if the Backup<br>Vault does not<br>have resource-<br>based policies or<br>has policies without<br>a suitable 'Deny'<br>statement (statemen<br>t with backup:De<br>leteRecoveryPoint,<br>backup:UpdateRecov<br>eryPointLifecycle,<br>and backup:Pu<br>tBackupVaultAccess<br>Policy permissions).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14202
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.4|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|rds-instance-iam-a <br>uthentication-enab <br>led|Ensure that an<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS)<br>instance has AWS<br>Identity and Access<br>Management (IAM)<br>authentication<br>enabled. The rule is<br>NON_COMPLIANT<br>if an Amazon RDS<br>instance does not<br>have IAM authentic<br>ation enabled.|
|8.3.5|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|access-keys-rotated|Ensure that active<br>IAM access keys are<br>rotated (changed)<br>within the number<br>of days speciﬁed<br>in maxAccess<br>KeyAge. The rule is<br>NON_COMPLIANT if<br>access keys are not<br>rotated within the<br>speciﬁed time period.<br>The default value is<br>90 days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14203
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.5|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|secretsmanager-sch <br>eduled-rotation-su <br>ccess-check|Ensure that AWS<br>Secrets Manager<br>secrets rotated<br>successfully according<br>to the rotation<br>schedule. Secrets<br>Manager calculates<br>the date the rotation<br>should happen. The<br>rule is NON_COMPL<br>IANT if the date<br>passes and the secret<br>isn't rotated.|
|8.3.5|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|secretsmanager-sec <br>ret-periodic-rotation|Ensure that AWS<br>Secrets Manager<br>secrets have been<br>rotated in the past<br>speciﬁed number<br>of days. The rule is<br>NON_COMPLIANT if<br>a secret has not been<br>rotated for more than<br>maxDaysSinceRotati<br>on number of days.<br>The default value is<br>90 days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14204
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.7|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|access-keys-rotated|Ensure that active<br>IAM access keys are<br>rotated (changed)<br>within the number<br>of days speciﬁed<br>in maxAccess<br>KeyAge. The rule is<br>NON_COMPLIANT if<br>access keys are not<br>rotated within the<br>speciﬁed time period.<br>The default value is<br>90 days.|
|8.3.7|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|secretsmanager-sch <br>eduled-rotation-su <br>ccess-check|Ensure that AWS<br>Secrets Manager<br>secrets rotated<br>successfully according<br>to the rotation<br>schedule. Secrets<br>Manager calculates<br>the date the rotation<br>should happen. The<br>rule is NON_COMPL<br>IANT if the date<br>passes and the secret<br>isn't rotated.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14205
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.7|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|secretsmanager-sec <br>ret-periodic-rotation|Ensure that AWS<br>Secrets Manager<br>secrets have been<br>rotated in the past<br>speciﬁed number<br>of days. The rule is<br>NON_COMPLIANT if<br>a secret has not been<br>rotated for more than<br>maxDaysSinceRotati<br>on number of days.<br>The default value is<br>90 days.|
|8.3.9|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|access-keys-rotated|Ensure that active<br>IAM access keys are<br>rotated (changed)<br>within the number<br>of days speciﬁed<br>in maxAccess<br>KeyAge. The rule is<br>NON_COMPLIANT if<br>access keys are not<br>rotated within the<br>speciﬁed time period.<br>The default value is<br>90 days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14206
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.3.9|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|secretsmanager-sch <br>eduled-rotation-su <br>ccess-check|Ensure that AWS<br>Secrets Manager<br>secrets rotated<br>successfully according<br>to the rotation<br>schedule. Secrets<br>Manager calculates<br>the date the rotation<br>should happen. The<br>rule is NON_COMPL<br>IANT if the date<br>passes and the secret<br>isn't rotated.|
|8.3.9|Strong authentic<br>ation for users and<br>administrators is<br>established and<br>managed. (PCI-DSS-<br>v4.0)|secretsmanager-sec <br>ret-periodic-rotation|Ensure that AWS<br>Secrets Manager<br>secrets have been<br>rotated in the past<br>speciﬁed number<br>of days. The rule is<br>NON_COMPLIANT if<br>a secret has not been<br>rotated for more than<br>maxDaysSinceRotati<br>on number of days.<br>The default value is<br>90 days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14207
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.4.1|Multi-factor<br>authentication (MFA)<br>is implemented to<br>secure access into the<br>CDE. (PCI-DSS-v4.0)|s3-bucket-mfa-dele <br>te-enabled|Ensure that MFA<br>Delete is enabled in<br>the Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>versioning conﬁgura<br>tion. The rule is<br>NON_COMPLIANT<br>if MFA Delete is not<br>enabled.|
|8.4.2|Multi-factor<br>authentication (MFA)<br>is implemented to<br>secure access into the<br>CDE. (PCI-DSS-v4.0)|s3-bucket-mfa-dele <br>te-enabled|Ensure that MFA<br>Delete is enabled in<br>the Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>versioning conﬁgura<br>tion. The rule is<br>NON_COMPLIANT<br>if MFA Delete is not<br>enabled.|
|8.4.3|Multi-factor<br>authentication (MFA)<br>is implemented to<br>secure access into the<br>CDE. (PCI-DSS-v4.0)|s3-bucket-mfa-dele <br>te-enabled|Ensure that MFA<br>Delete is enabled in<br>the Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>versioning conﬁgura<br>tion. The rule is<br>NON_COMPLIANT<br>if MFA Delete is not<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14208
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.6.3|Use of application<br>and system accounts<br>and associated<br>authentication<br>factors is strictly<br>managed. (PCI-DSS-<br>v4.0)|access-keys-rotated|Ensure that active<br>IAM access keys are<br>rotated (changed)<br>within the number<br>of days speciﬁed<br>in maxAccess<br>KeyAge. The rule is<br>NON_COMPLIANT if<br>access keys are not<br>rotated within the<br>speciﬁed time period.<br>The default value is<br>90 days.|
|8.6.3|Use of application<br>and system accounts<br>and associated<br>authentication<br>factors is strictly<br>managed. (PCI-DSS-<br>v4.0)|secretsmanager-sch <br>eduled-rotation-su <br>ccess-check|Ensure that AWS<br>Secrets Manager<br>secrets rotated<br>successfully according<br>to the rotation<br>schedule. Secrets<br>Manager calculates<br>the date the rotation<br>should happen. The<br>rule is NON_COMPL<br>IANT if the date<br>passes and the secret<br>isn't rotated.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14209
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|8.6.3|Use of application<br>and system accounts<br>and associated<br>authentication<br>factors is strictly<br>managed. (PCI-DSS-<br>v4.0)|secretsmanager-sec <br>ret-periodic-rotation|Ensure that AWS<br>Secrets Manager<br>secrets have been<br>rotated in the past<br>speciﬁed number<br>of days. The rule is<br>NON_COMPLIANT if<br>a secret has not been<br>rotated for more than<br>maxDaysSinceRotati<br>on number of days.<br>The default value is<br>90 days.|
|A1.1.2|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|neptune-cluster-sn <br>apshot-public-proh <br>ibited|Ensure that an<br>Amazon Neptune<br>manual DB cluster<br>snapshot is not<br>public. The rule is<br>NON_COMPLIANT<br>if any existing and<br>new Neptune cluster<br>snapshot is public.|
|A1.1.2|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|docdb-cluster-snap <br>shot-public-prohib <br>ited|Ensure that Amazon<br>DocumentDB manual<br>cluster snapshots<br>are not public. The<br>rule is NON_COMPL<br>IANT if any Amazon<br>DocumentDB manual<br>cluster snapshots are<br>public.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14210
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.1.2|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|backup-recovery-po <br>int-manual-deletion-<br>disabled|Ensure that a backup<br>vault has an attached<br>resource-based<br>policy which prevents<br>deletion of recovery<br>points. The rule<br>is NON_COMPL<br>IANT if the Backup<br>Vault does not<br>have resource-<br>based policies or<br>has policies without<br>a suitable 'Deny'<br>statement (statemen<br>t with backup:De<br>leteRecoveryPoint,<br>backup:UpdateRecov<br>eryPointLifecycle,<br>and backup:Pu<br>tBackupVaultAccess<br>Policy permissions).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14211
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.1.2|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|emr-block-public-a <br>ccess|Ensure that an<br>account with Amazon<br>EMR has block public<br>access settings<br>enabled. The rule is<br>NON_COMPLIANT if<br>BlockPublicSecurit<br>yGroupRules is false,<br>or if true, ports other<br>than Port 22 are<br>listed in Permitted<br>PublicSecurityGrou<br>pRuleRanges.|
|A1.1.2|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|s3-access-point-pu <br>blic-access-blocks|Ensure that Amazon<br>S3 access points have<br>block public access<br>settings enabled. The<br>rule is NON_COMPL<br>IANT if block public<br>access settings are<br>not enabled for S3<br>access points.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14212
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.1.2|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|s3-account-level-p <br>ublic-access-blocks|Ensure that the<br>required public<br>access block settings<br>are conﬁgured<br>from account level.<br>The rule is only<br>NON_COMPLIANT<br>when the ﬁelds set<br>below do not match<br>the corresponding<br>ﬁelds in the conﬁgura<br>tion item.|
|A1.1.2|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|s3-bucket-mfa-dele <br>te-enabled|Ensure that MFA<br>Delete is enabled in<br>the Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>versioning conﬁgura<br>tion. The rule is<br>NON_COMPLIANT<br>if MFA Delete is not<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14213
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|api-gw-endpoint-ty <br>pe-check|Ensure that Amazon<br>API Gateway APIs are<br>of the type speciﬁed<br>in the rule parameter<br>'endpointConﬁgura<br>tionType'. The rule<br>returns NON_COMPL<br>IANT if the REST<br>API does not match<br>the endpoint type<br>conﬁgured in the rule<br>parameter.|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|cloudfront-associa <br>ted-with-waf|Ensure that Amazon<br>CloudFront distribut<br>ions are associate<br>d with either web<br>application ﬁrewall<br>(WAF) or WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion is not associated<br>with a WAF web ACL.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14214
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|cloudfront-custom- <br>ssl-certiﬁcate|Ensure that the<br>certiﬁcate associate<br>d with an Amazon<br>CloudFront distribut<br>ion is not the default<br>SSL certiﬁcate. The<br>rule is NON_COMPL<br>IANT if a CloudFront<br>distribution uses the<br>default SSL certiﬁca<br>te.|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|netfw-policy-defau <br>lt-action-fragment-<br>packets|Ensure that an AWS<br>Network Firewall<br>policy is conﬁgured<br>with a user deﬁned<br>stateless default<br>action for fragmente<br>d packets. The rule<br>is NON_COMPLIANT<br>if stateless default<br>action for fragmente<br>d packets does not<br>match with user<br>deﬁned default<br>action.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14215
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|rds-db-security-gr <br>oup-not-allowed|Ensure that the<br>Amazon Relationa<br>l Database Service<br>(Amazon RDS) DB<br>security groups is the<br>default one. The rule<br>is NON_COMPLIANT<br>if there are any DB<br>security groups that<br>are not the default<br>DB security group.|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|ec2-transit-gatewa <br>y-auto-vpc-attach- <br>disabled|Ensure that Amazon<br>Elastic Compute<br>Cloud (Amazon EC2)<br>Transit Gateways do<br>not have 'AutoAcce<br>ptSharedAttachment<br>s' enabled. The rule is<br>NON_COMPLIANT for<br>a Transit Gateway if<br>'AutoAcceptSharedA<br>ttachments' is set to<br>'enable'.|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|eks-endpoint-no-pu <br>blic-access|Ensure that the<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS)<br>endpoint is not<br>publicly accessibl<br>e. The rule is<br>NON_COMPLIANT<br>if the endpoint is<br>publicly accessible.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14216
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|restricted-ssh|Note: For this rule,<br>the rule identiﬁe<br>r (INCOMING<br>_SSH_DISABLED)<br>and rule name<br>(restricted-ssh) are<br>diﬀerent. Ensure<br>that the incoming<br>SSH traﬃc for the<br>security groups is<br>accessible. The rule<br>is COMPLIANT if the<br>IP addresses of the<br>incoming SSH traﬃc<br>in the security groups<br>are restricted (CIDR<br>other than 0.0.0.0/0<br>or ::/0). Otherwise,<br>NON_COMPLIANT.|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|appsync-associated-<br>with-waf|Ensure that AWS<br>AppSync APIs are<br>associated with<br>AWS WAFv2 web<br>access control lists<br>(ACLs). The rule is<br>NON_COMPLIANT for<br>an AWS AppSync API<br>if it is not associated<br>with a web ACL.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14217
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|docdb-cluster-snap <br>shot-public-prohib <br>ited|Ensure that Amazon<br>DocumentDB manual<br>cluster snapshots<br>are not public. The<br>rule is NON_COMPL<br>IANT if any Amazon<br>DocumentDB manual<br>cluster snapshots are<br>public.|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|codebuild-project- <br>source-repo-url-check|Ensure that the<br>Bitbucket source<br>repository URL<br>DOES NOT contain<br>sign-in credentials<br>or not. The rule is<br>NON_COMPLIANT if<br>the URL contains any<br>sign-in information<br>and COMPLIANT if it<br>doesn't.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14218
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|elb-acm-certiﬁcate-<br>required|Ensure that the<br>Classic Load<br>Balancers use SSL<br>certiﬁcates provided<br>by AWS Certiﬁca<br>te Manager. To use<br>this rule, use an SSL<br>or HTTPS listener<br>with your Classic<br>Load Balancer. Note<br>- this rule is only<br>applicable to Classic<br>Load Balancers.<br>This rule does not<br>check Applicati<br>on Load Balancers<br>and Network Load<br>Balancers.|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|emr-block-public-a <br>ccess|Ensure that an<br>account with Amazon<br>EMR has block public<br>access settings<br>enabled. The rule is<br>NON_COMPLIANT if<br>BlockPublicSecurit<br>yGroupRules is false,<br>or if true, ports other<br>than Port 22 are<br>listed in Permitted<br>PublicSecurityGrou<br>pRuleRanges.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14219
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|nacl-no-unrestricted-<br>ssh-rdp|Ensure that default<br>ports for SSH/RDP<br>ingress traﬃc for<br>network access<br>control lists (NACLs)<br>are restricted. The<br>rule is NON_COMPL<br>IANT if a NACL<br>inbound entry allows<br>a source TCP or UDP<br>CIDR block for ports<br>22 or 3389.|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|waf-global-webacl- <br>not-empty|Ensure that a WAF<br>Global Web ACL<br>contains some<br>WAF rules or rule<br>groups. This rule is<br>NON_COMPLIANT if<br>a Web ACL does not<br>contain any WAF rule<br>or rule group.|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|waf-global-rulegro <br>up-not-empty|Ensure that an AWS<br>WAF Classic rule<br>group contains some<br>rules. The rule is<br>NON_COMPLIANT<br>if there are no rules<br>present within a rule<br>group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14220
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|waf-global-rule-not-<br>empty|Ensure that an<br>AWS WAF global<br>rule contains some<br>conditions. The rule<br>is NON_COMPLIANT<br>if no conditions are<br>present within the<br>WAF global rule.|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|ec2-client-vpn-not-<br>authorize-all|Ensure that the<br>AWS Client VPN<br>authorization rules<br>does not authorize<br>connection access for<br>all clients. The rule is<br>NON_COMPLIANT if<br>'AccessAll' is present<br>and set to true.|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|internet-gateway-a <br>uthorized-vpc-only|Ensure that internet<br>gateways are<br>attached to an<br>authorized virtual<br>private cloud<br>(Amazon VPC). The<br>rule is NON_COMPL<br>IANT if internet<br>gateways are<br>attached to an<br>unauthorized VPC.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14221
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|s3-access-point-pu <br>blic-access-blocks|Ensure that Amazon<br>S3 access points have<br>block public access<br>settings enabled. The<br>rule is NON_COMPL<br>IANT if block public<br>access settings are<br>not enabled for S3<br>access points.|
|A1.1.3|Multi-tenant service<br>providers protect and<br>separate all customer<br>environments and<br>data. (PCI-DSS-v4.0)|s3-account-level-p <br>ublic-access-blocks|Ensure that the<br>required public<br>access block settings<br>are conﬁgured<br>from account level.<br>The rule is only<br>NON_COMPLIANT<br>when the ﬁelds set<br>below do not match<br>the corresponding<br>ﬁelds in the conﬁgura<br>tion item.|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|api-gwv2-access-lo <br>gs-enabled|Ensure that Amazon<br>API Gateway V2<br>stages have access<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if 'accessLo<br>gSettings' is not<br>present in Stage<br>conﬁguration.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14222
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|cloudfront-accessl <br>ogs-enabled|Ensure that Amazon<br>CloudFront distribut<br>ions are conﬁgure<br>d to deliver access<br>logs to an Amazon<br>S3 bucket. The rule is<br>NON_COMPLIANT if a<br>CloudFront distribut<br>ion does not have<br>logging conﬁgured.|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|cloudtrail-security-<br>trail-enabled|Ensure that there<br>is at least one AWS<br>CloudTrail trail<br>deﬁned with security<br>best practices. This<br>rule is COMPLIANT if<br>there is at least one<br>trail that meets all of<br>the following:|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14223
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|neptune-cluster-cl <br>oudwatch-log-expor <br>t-enabled|Ensure that an<br>Amazon Neptune<br>cluster has<br>CloudWatch log<br>export enabled for<br>audit logs. The rule is<br>NON_COMPLIANT if a<br>Neptune cluster does<br>not have CloudWatc<br>h log export enabled<br>for audit logs.|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|ecs-task-deﬁnition-<br>log-conﬁguration|Ensure that logConﬁg<br>uration is set on<br>active ECS Task<br>Deﬁnitions. This<br>rule is NON_COMPL<br>IANT if an active<br>ECSTaskDeﬁnition<br>does not have the<br>logConﬁguration<br>resource deﬁned<br>or the value for<br>logConﬁguration is<br>null in at least one<br>container deﬁnition.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14224
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|cloudtrail-enabled|Note: For this rule,<br>the rule identiﬁe<br>r (CLOUD_TR<br>AIL_ENABLED) and<br>rule name (cloudtrail-<br>enabled) are diﬀerent<br>. Ensure that an AWS<br>CloudTrail trail is<br>enabled in your AWS<br>account. The rule is<br>NON_COMPLIANT if<br>a trail is not enabled.<br>Optionally, the rule<br>checks a speciﬁc<br>S3 bucket, Amazon<br>Simple Notiﬁcation<br>Service (Amazon SNS)<br>topic, and CloudWatc<br>h log group.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14225
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|multi-region-cloud <br>trail-enabled|Note: for this rule,<br>the rule identiﬁe<br>r (MULTI_RE<br>GION_CLOU<br>D_TRAIL_ENABLED)<br>and rule name<br>(multi-region-clou<br>dtrail-enabled) are<br>diﬀerent. Ensure<br>that there is at least<br>one multi-region<br>AWS CloudTrail. The<br>rule is NON_COMPL<br>IANT if the trails<br>do not match input<br>parameters. The rule<br>is NON_COMPLIANT<br>if the ExcludeMa<br>nagementEventSourc<br>es ﬁeld is not empty<br>or if AWS CloudTrai<br>l is conﬁgured to<br>exclude managemen<br>t events such as<br>AWS KMS events or<br>Amazon RDS Data<br>API events.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14226
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|appsync-logging-en <br>abled|Ensure that an AWS<br>AppSync API has<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging is not<br>enabled, or 'ﬁeldLog<br>Level' is neither<br>ERROR nor ALL.|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|waf-classic-logging-<br>enabled|Ensure that logging is<br>enabled on AWS WAF<br>classic global web<br>access control lists<br>(web ACLs). The rule<br>is NON_COMPLIANT<br>for a global web ACL,<br>if it does not have<br>logging enabled.|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|mq-cloudwatch-audi <br>t-logging-enabled|Ensure that Amazon<br>MQ brokers have<br>Amazon CloudWatc<br>h audit logging<br>enabled. The rule is<br>NON_COMPLIANT<br>if a broker does not<br>have audit logging<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14227
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|mq-cloudwatch-audi <br>t-log-enabled|Ensure that an<br>Amazon MQ broker<br>has CloudWatch audit<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if the broker<br>does not have audit<br>logging enabled.|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|eks-cluster-logging-<br>enabled|Ensure that an<br>Amazon Elastic<br>Kubernetes Service<br>(Amazon EKS) cluster<br>is conﬁgured with<br>logging enabled. The<br>rule is NON_COMPL<br>IANT if logging for<br>Amazon EKS clusters<br>is not enabled for all<br>log types.|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|elastic-beanstalk- <br>logs-to-cloudwatch|Ensure that AWS<br>Elastic Beanstalk<br>environments<br>are conﬁgured<br>to send logs to<br>Amazon CloudWatc<br>h Logs. The rule<br>is NON_COMPL<br>IANT if the value<br>of `StreamLogs` is<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14228
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|step-functions-sta <br>te-machine-logging-<br>enabled|Ensure that AWS<br>Step Functions<br>machine has logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a state machine does<br>not have logging<br>enabled or the<br>logging conﬁgura<br>tion is not at the<br>minimum level<br>provided.|
|A1.2.1|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|netfw-logging-enab <br>led|Ensure that AWS<br>Network Firewall<br>ﬁrewalls have logging<br>enabled. The rule is<br>NON_COMPLIANT if<br>a logging type is not<br>conﬁgured. You can<br>specify which logging<br>type you want the<br>rule to check.|
|A1.2.3|Multi-tenant service<br>providers facilitate<br>logging and incident<br>response for all<br>customers. (PCI-DSS-<br>v4.0)|security-account-i <br>nformation-provided|Ensure that you have<br>provided security<br>contact information<br>for your AWS account<br>contacts. The rule is<br>NON_COMPLIANT<br>if security contact<br>information within<br>the account is not<br>provided.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14229
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.2.5.1|PCI DSS scope is<br>documented and<br>validated. (PCI-DSS-<br>v4.0)|macie-auto-sensitive-<br>data-discovery-check|Ensure that<br>automated sensitive<br>data discovery is<br>enabled for Amazon<br>Macie. The rule is<br>NON_COMPLIANT if<br>automated sensitive<br>data discovery<br>is disabled. The<br>rule is APPLICABL<br>E for administr<br>ator accounts and<br>NOT_APPLICABLE for<br>member accounts.|
|A3.2.5.1|PCI DSS scope is<br>documented and<br>validated. (PCI-DSS-<br>v4.0)|macie-status-check|Ensure that Amazon<br>Macie is enabled in<br>your account per<br>region. The rule<br>is NON_COMPL<br>IANT if the 'status'<br>attribute is not set to<br>'ENABLED'.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14230
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.2.5.2|PCI DSS scope is<br>documented and<br>validated. (PCI-DSS-<br>v4.0)|macie-auto-sensitive-<br>data-discovery-check|Ensure that<br>automated sensitive<br>data discovery is<br>enabled for Amazon<br>Macie. The rule is<br>NON_COMPLIANT if<br>automated sensitive<br>data discovery<br>is disabled. The<br>rule is APPLICABL<br>E for administr<br>ator accounts and<br>NOT_APPLICABLE for<br>member accounts.|
|A3.2.5.2|PCI DSS scope is<br>documented and<br>validated. (PCI-DSS-<br>v4.0)|macie-status-check|Ensure that Amazon<br>Macie is enabled in<br>your account per<br>region. The rule<br>is NON_COMPL<br>IANT if the 'status'<br>attribute is not set to<br>'ENABLED'.|
|A3.3.1|PCI DSS is incorpora<br>ted into business-as-<br>usual (BAU) activities.<br>(PCI-DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14231
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.3.1|PCI DSS is incorpora<br>ted into business-as-<br>usual (BAU) activities.<br>(PCI-DSS-v4.0)|cloudformation-sta <br>ck-notiﬁcation-check|Ensure that your<br>CloudFormation<br>stacks send event<br>notiﬁcations to<br>an Amazon SNS<br>topic. Optionally<br>ensure that speciﬁed<br>Amazon SNS topics<br>are used. The rule is<br>NON_COMPLIANT<br>if CloudFormation<br>stacks do not send<br>notiﬁcations.|
|A3.3.1|PCI DSS is incorpora<br>ted into business-as-<br>usual (BAU) activities.<br>(PCI-DSS-v4.0)|ec2-instance-detai <br>led-monitoring-ena <br>bled|Ensure that detailed<br>monitoring is<br>enabled for EC2<br>instances. The rule is<br>NON_COMPLIANT if<br>detailed monitoring<br>is not enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14232
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.3.1|PCI DSS is incorpora<br>ted into business-as-<br>usual (BAU) activities.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|A3.3.1|PCI DSS is incorpora<br>ted into business-as-<br>usual (BAU) activities.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14233
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.3.1|PCI DSS is incorpora<br>ted into business-as-<br>usual (BAU) activities.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|A3.3.1|PCI DSS is incorpora<br>ted into business-as-<br>usual (BAU) activities.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14234
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.3.1|PCI DSS is incorpora<br>ted into business-as-<br>usual (BAU) activities.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-r <br>esource-check|Ensure that a<br>resource type has a<br>CloudWatch alarm<br>for the named metric.<br>For resource type,<br>you can specify<br>EBS volumes, EC2<br>instances, Amazon<br>RDS clusters, or S3<br>buckets. The rule is<br>COMPLIANT if the<br>named metric has<br>a resource ID and<br>CloudWatch alarm.|
|A3.3.1|PCI DSS is incorpora<br>ted into business-as-<br>usual (BAU) activities.<br>(PCI-DSS-v4.0)|cloudwatch-alarm-s <br>ettings-check|Ensure that<br>CloudWatch alarms<br>with the given metric<br>name have the<br>speciﬁed settings.|
|A3.3.1|PCI DSS is incorpora<br>ted into business-as-<br>usual (BAU) activities.<br>(PCI-DSS-v4.0)|wafv2-rulegroup-lo <br>gging-enabled|Ensure that Amazon<br>CloudWatch security<br>metrics collectio<br>n on AWS WAFv2<br>rule groups is<br>enabled. The rule is<br>NON_COMPLIANT if<br>the 'VisibilityConﬁg.<br>CloudWatchMetricsE<br>nabled' ﬁeld is set to<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14235
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.3.1|PCI DSS is incorpora<br>ted into business-as-<br>usual (BAU) activities.<br>(PCI-DSS-v4.0)|sns-topic-message- <br>delivery-notiﬁcation-<br>enabled|Ensure that Amazon<br>Simple Notiﬁcation<br>Service (SNS) logging<br>is enabled for the<br>delivery status of<br>notiﬁcation messages<br>sent to a topic for<br>the endpoints. The<br>rule is NON_COMPL<br>IANT if the delivery<br>status notiﬁcation<br>for messages is not<br>enabled.|
|A3.4.1|Logical access to<br>the cardholder<br>data environment<br>is controlled and<br>managed. (PCI-DSS-<br>v4.0)|neptune-cluster-sn <br>apshot-public-proh <br>ibited|Ensure that an<br>Amazon Neptune<br>manual DB cluster<br>snapshot is not<br>public. The rule is<br>NON_COMPLIANT<br>if any existing and<br>new Neptune cluster<br>snapshot is public.|
|A3.4.1|Logical access to<br>the cardholder<br>data environment<br>is controlled and<br>managed. (PCI-DSS-<br>v4.0)|docdb-cluster-snap <br>shot-public-prohib <br>ited|Ensure that Amazon<br>DocumentDB manual<br>cluster snapshots<br>are not public. The<br>rule is NON_COMPL<br>IANT if any Amazon<br>DocumentDB manual<br>cluster snapshots are<br>public.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14236
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.4.1|Logical access to<br>the cardholder<br>data environment<br>is controlled and<br>managed. (PCI-DSS-<br>v4.0)|backup-recovery-po <br>int-manual-deletion-<br>disabled|Ensure that a backup<br>vault has an attached<br>resource-based<br>policy which prevents<br>deletion of recovery<br>points. The rule<br>is NON_COMPL<br>IANT if the Backup<br>Vault does not<br>have resource-<br>based policies or<br>has policies without<br>a suitable 'Deny'<br>statement (statemen<br>t with backup:De<br>leteRecoveryPoint,<br>backup:UpdateRecov<br>eryPointLifecycle,<br>and backup:Pu<br>tBackupVaultAccess<br>Policy permissions).|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14237
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.4.1|Logical access to<br>the cardholder<br>data environment<br>is controlled and<br>managed. (PCI-DSS-<br>v4.0)|emr-block-public-a <br>ccess|Ensure that an<br>account with Amazon<br>EMR has block public<br>access settings<br>enabled. The rule is<br>NON_COMPLIANT if<br>BlockPublicSecurit<br>yGroupRules is false,<br>or if true, ports other<br>than Port 22 are<br>listed in Permitted<br>PublicSecurityGrou<br>pRuleRanges.|
|A3.4.1|Logical access to<br>the cardholder<br>data environment<br>is controlled and<br>managed. (PCI-DSS-<br>v4.0)|secretsmanager-sec <br>ret-unused|Ensure that AWS<br>Secrets Manager<br>secrets have been<br>accessed within a<br>speciﬁed number<br>of days. The rule is<br>NON_COMPLIANT if<br>a secret has not been<br>accessed in 'unusedFo<br>rDays' number of<br>days. The default<br>value is 90 days.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14238
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.4.1|Logical access to<br>the cardholder<br>data environment<br>is controlled and<br>managed. (PCI-DSS-<br>v4.0)|s3-access-point-pu <br>blic-access-blocks|Ensure that Amazon<br>S3 access points have<br>block public access<br>settings enabled. The<br>rule is NON_COMPL<br>IANT if block public<br>access settings are<br>not enabled for S3<br>access points.|
|A3.4.1|Logical access to<br>the cardholder<br>data environment<br>is controlled and<br>managed. (PCI-DSS-<br>v4.0)|s3-account-level-p <br>ublic-access-blocks|Ensure that the<br>required public<br>access block settings<br>are conﬁgured<br>from account level.<br>The rule is only<br>NON_COMPLIANT<br>when the ﬁelds set<br>below do not match<br>the corresponding<br>ﬁelds in the conﬁgura<br>tion item.|
|A3.4.1|Logical access to<br>the cardholder<br>data environment<br>is controlled and<br>managed. (PCI-DSS-<br>v4.0)|s3-bucket-mfa-dele <br>te-enabled|Ensure that MFA<br>Delete is enabled in<br>the Amazon Simple<br>Storage Service<br>(Amazon S3) bucket<br>versioning conﬁgura<br>tion. The rule is<br>NON_COMPLIANT<br>if MFA Delete is not<br>enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14239
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.5.1|Suspicious events<br>are identiﬁed and<br>responded to. (PCI-<br>DSS-v4.0)|api-gw-xray-enabled|Ensure that AWS<br>X-Ray tracing is<br>enabled on Amazon<br>API Gateway REST<br>APIs. The rule is<br>COMPLIANT if X-Ray<br>tracing is enabled<br>and NON_COMPL<br>IANT otherwise.|
|A3.5.1|Suspicious events<br>are identiﬁed and<br>responded to. (PCI-<br>DSS-v4.0)|cloudformation-sta <br>ck-notiﬁcation-check|Ensure that your<br>CloudFormation<br>stacks send event<br>notiﬁcations to<br>an Amazon SNS<br>topic. Optionally<br>ensure that speciﬁed<br>Amazon SNS topics<br>are used. The rule is<br>NON_COMPLIANT<br>if CloudFormation<br>stacks do not send<br>notiﬁcations.|
|A3.5.1|Suspicious events<br>are identiﬁed and<br>responded to. (PCI-<br>DSS-v4.0)|ec2-instance-detai <br>led-monitoring-ena <br>bled|Ensure that detailed<br>monitoring is<br>enabled for EC2<br>instances. The rule is<br>NON_COMPLIANT if<br>detailed monitoring<br>is not enabled.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14240
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.5.1|Suspicious events<br>are identiﬁed and<br>responded to. (PCI-<br>DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|A3.5.1|Suspicious events<br>are identiﬁed and<br>responded to. (PCI-<br>DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14241
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.5.1|Suspicious events<br>are identiﬁed and<br>responded to. (PCI-<br>DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
|A3.5.1|Suspicious events<br>are identiﬁed and<br>responded to. (PCI-<br>DSS-v4.0)|cloudwatch-alarm-a <br>ction-check|Ensure that<br>CloudWatch alarms<br>have an action<br>conﬁgured for the<br>ALARM, INSUFFICI<br>ENT_DATA, or OK<br>state. Optionall<br>y ensure that any<br>actions match a<br>named ARN. The<br>rule is NON_COMPL<br>IANT if there is no<br>action speciﬁed for<br>the alarm or optional<br>parameter.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14242
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.5.1|Suspicious events<br>are identiﬁed and<br>responded to. (PCI-<br>DSS-v4.0)|cloudwatch-alarm-r <br>esource-check|Ensure that a<br>resource type has a<br>CloudWatch alarm<br>for the named metric.<br>For resource type,<br>you can specify<br>EBS volumes, EC2<br>instances, Amazon<br>RDS clusters, or S3<br>buckets. The rule is<br>COMPLIANT if the<br>named metric has<br>a resource ID and<br>CloudWatch alarm.|
|A3.5.1|Suspicious events<br>are identiﬁed and<br>responded to. (PCI-<br>DSS-v4.0)|cloudwatch-alarm-s <br>ettings-check|Ensure that<br>CloudWatch alarms<br>with the given metric<br>name have the<br>speciﬁed settings.|
|A3.5.1|Suspicious events<br>are identiﬁed and<br>responded to. (PCI-<br>DSS-v4.0)|wafv2-rulegroup-lo <br>gging-enabled|Ensure that Amazon<br>CloudWatch security<br>metrics collectio<br>n on AWS WAFv2<br>rule groups is<br>enabled. The rule is<br>NON_COMPLIANT if<br>the 'VisibilityConﬁg.<br>CloudWatchMetricsE<br>nabled' ﬁeld is set to<br>false.|
Operational Best Practices for PCI DSS 4.0 (Including global resource types) 14243
**AWS Config Developer Guide**
**|Control ID|Control Description|AWS Config Rule|Guidance|**
|---|---|---|---|
|A3.5.1|Suspicious events<br>are identiﬁed and<br>responded to. (PCI-<br>DSS-v4.0)|sns-topic-message- <br>delivery-notiﬁcation-<br>enabled|Ensure that Amazon<br>Simple Notiﬁcation<br>Service (SNS) logging<br>is enabled for the<br>delivery status of<br>notiﬁcation messages<br>sent to a topic for<br>the endpoints. The<br>rule is NON_COMPL<br>IANT if the delivery<br>status notiﬁcation<br>for messages is not<br>enabled.|
## **Template**
[The template is available on GitHub: Operational Best Practices for PCI DSS 4.0 (Including global](https://github.com/awslabs/aws-config-rules/blob/master/aws-config-conformance-packs/Operational-Best-Practices-for-PCI-DSS-v4.0-including-global-resourcetypes.yaml)
[resource types).](https://github.com/awslabs/aws-config-rules/blob/master/aws-config-conformance-packs/Operational-Best-Practices-for-PCI-DSS-v4.0-including-global-resourcetypes.yaml)
# **Operational Best Practices for Publicly Accessible Resources**
This conformance pack helps identify resources that may be publicly accessible.
s.
**[For a list of all managed rules supported by AWS Config, see List of AWS Config Managed Rule](https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html)**
See the `Parameters` section in the following template for the names and descriptions of the
required parameters.
[The template is available on GitHub: Operational Best Practices for Publicly Accessible Resources.](https://github.com/awslabs/aws-config-rules/blob/master/aws-config-conformance-packs/Operational-Best-Practices-for-Publicly-Accessible-Resources.yaml)
# **Operational Best Practices for RBI Cyber Security Framework for UCBs**
Conformance packs provide a general-purpose compliance framework designed to enable you
to create security, operational or cost-optimization governance checks using managed or custom
**AWS Config rules and AWS Config remediation actions. Conformance Packs, as sample templates,**
are not designed to fully ensure compliance with a specific governance or compliance standard.
Operational Best Practices for Publicly Accessible Resources 14244