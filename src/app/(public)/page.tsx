/* eslint-disable @next/next/no-img-element */
'use client'

import AnimatedText from '@/components/st/animated-text'
import { About } from '../../components/about'
import { Features } from '../../components/features'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { motion, useInView } from 'framer-motion'
import { BarChart3, Check, ChevronRight, CloudLightning, Database, Shield, Bot, Cpu, AlertTriangle, ArrowRight, Play } from 'lucide-react'
import React, { useRef } from 'react'

const features = [
  'Automated evidence collection',
  'AI-powered compliance analysis',
  'Real-time audit reporting',
  'Cross-account AWS monitoring',
  'PCI DSS v4.0 compliance',
  'Interactive audit chatbot',
  'Multi-format report export',
  'Cost optimization tracking',
  'Vulnerability assessment integration',
  'Continuous compliance monitoring',
]

const cards = [
  {
    title: 'Automated Evidence Collection',
    description: 'Automatically collect compliance evidence from 200+ AWS accounts using EventBridge and AWS Config.',
    icon: Database,
    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop&auto=format',
    alt: 'AWS cloud infrastructure dashboard showing automated data collection',
    features: [
      'AWS Config, CloudTrail, Security Hub integration',
      'Cross-account data aggregation',
      'Real-time evidence synchronization',
      'S3-based evidence vault with metadata tracking',
    ],
  },
  {
    title: 'AI-Powered Compliance Analysis',
    description: 'Leverage Amazon Bedrock Claude 3.5 for intelligent compliance evaluation and gap analysis.',
    icon: Bot,
    image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=400&fit=crop&auto=format',
    alt: 'AI artificial intelligence analyzing compliance data with neural networks',
    features: [
      'RAG-based compliance knowledge base',
      'Automated pass/fail determination',
      'Intelligent remediation recommendations',
      'Multi-framework support (PCI DSS, ISO 27001)',
    ],
  },
  {
    title: 'Enterprise Dashboard & Reporting',
    description: 'Comprehensive compliance visibility with executive reporting and audit trail management.',
    icon: BarChart3,
    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop&auto=format&overlay=color:0066CC:0.3',
    alt: 'Executive dashboard showing compliance metrics and audit reports',
    features: [
      'Real-time compliance status tracking',
      'PDF, Excel, JSON report generation',
      'Historical trend analysis',
      'Risk-based priority scoring',
    ],
  },
]

const beneficiaries = [
  {
    title: 'Internal Auditors',
    description: 'Eliminate manual evidence collection and get instant compliance answers with full explanations and supporting evidence.',
    benefits: [
      'Automated evidence aggregation',
      'Real-time compliance status',
      'AI-generated audit explanations',
      'One-click report generation'
    ]
  },
  {
    title: 'DevOps & Engineering Teams',
    description: 'Focus on core development while automated systems handle compliance data collection.',
    benefits: [
      'Zero manual audit interruptions',
      'Automated AWS configuration tracking',
      'Developer-friendly compliance interface',
      'Continuous integration support'
    ]
  },
  {
    title: 'Management & External Auditors',
    description: 'Get clear visibility into compliance posture without technical complexity.',
    benefits: [
      'Executive compliance dashboards',
      'Standardized audit packages',
      'Risk-based priority insights',
      'Regulatory compliance tracking'
    ]
  }
]

const overviewSections = [
  {
    title: 'Compliance Automation',
    items: [
      'PCI DSS v4.0 automated compliance',
      'ISO 27001 and Vietnamese Decree 13 support',
      'AWS Config rule mapping and evaluation',
      'Real-time compliance status monitoring',
      'Cross-account evidence collection',
      'Automated remediation recommendations',
      'Compliance knowledge base with RAG',
      'Historical compliance trending',
      'Risk-based priority scoring',
    ],
  },
  {
    title: 'Evidence Management',
    items: [
      'Automated AWS service integration',
      'S3-based evidence vault',
      'PostgreSQL metadata indexing',
      'Real-time evidence synchronization',
      'Version control and audit trails',
      'Cross-reference compliance mapping',
      'Evidence reuse across frameworks',
      'Data retention policy management',
      'Secure evidence encryption',
    ],
  },
  {
    title: 'AI & Analytics',
    items: [
      'Amazon Bedrock Claude 3.5 integration',
      'Intelligent compliance gap analysis',
      'Natural language audit explanations',
      'Conversational audit assistant',
      'Predictive compliance risk scoring',
      'Automated remediation guidance',
      'Multi-framework requirement mapping',
      'Cost-benefit analysis reporting',
      'Performance optimization insights',
    ],
  },
]

const testimonials = [
  {
    quote: 'SentinelAI transformed our audit process from weeks of manual work to hours of automated analysis. The AI explanations help our team understand compliance requirements clearly.',
    author: 'Internal Audit Manager',
    role: 'Enterprise Financial Institution',
  },
  {
    quote: 'Finally, a solution that lets our DevOps team focus on development while maintaining perfect compliance visibility. The cross-account monitoring is game-changing.',
    author: 'Cloud Infrastructure Lead',
    role: 'Digital Banking Platform',
  },
  {
    quote: 'The automated evidence collection and AI-powered analysis reduced our PCI DSS audit preparation time by 80%. External auditors love the comprehensive reporting.',
    author: 'CISO',
    role: 'Regional Bank',
  },
]

const utilities = [
  {
    title: 'AWS Integration',
    icon: CloudLightning,
    description: 'Native integration with AWS Config, CloudTrail, Security Hub, GuardDuty, and Inspector for comprehensive evidence collection.',
  },
  {
    title: 'API & Automation',
    icon: Cpu,
    description: 'RESTful APIs for integration with existing workflows, CI/CD pipelines, and third-party audit management systems.',
  },
  {
    title: 'Enterprise Security',
    icon: Shield,
    description: 'Bank-grade security with private infrastructure deployment, encryption at rest and in transit, and role-based access control.',
  },
]

const comingSoonFeatures = [
  {
    title: 'Risk-Based Account Prioritization',
    icon: Bot,
    description: 'AI Agent intelligently prioritizes "high-risk" accounts based on user roles, traffic logs, and activity patterns. Automatically identifies and flags accounts with elevated privileges such as root, admin, and service accounts for enhanced monitoring.',
  },
  {
    title: 'Cross-Framework Compliance Mapping',
    icon: AlertTriangle,
    description: 'Beyond PCI DSS, our AI compares and maps requirements across multiple compliance frameworks like ISO 27001. Automatically identify corresponding requirements (e.g., PCI DSS Req 1 = ISO 27001 Req 10) to enable evidence reuse and eliminate duplicate audit efforts.',
  },
  {
    title: 'Intelligent Evidence Adaptation',
    description: 'For requirements that don\'t exist in PCI DSS but are present in other compliance frameworks, our trained AI learns to provide appropriate evidence even without direct mapping. The system intelligently understands what evidence is needed for new compliance scenarios.',
  },
]

const stats = [
  { number: '200+', label: 'AWS Accounts Monitored' },
  { number: '80%', label: 'Faster Audit Preparation' },
  { number: '99.9%', label: 'Evidence Accuracy Rate' },
  { number: '<2hrs', label: 'Complete Audit Scan' },
]

export default function Home() {
  // Refs for scroll animations
  const featuresRef = useRef(null)
  const cardsRef = useRef(null)
  const beneficiariesRef = useRef(null)
  const overviewRef = useRef(null)
  const testimonialsRef = useRef(null)
  const utilitiesRef = useRef(null)
  const statsRef = useRef(null)

  // InView hooks
  const isFeaturesInView = useInView(featuresRef, { once: true, margin: '-100px' })
  const isCardsInView = useInView(cardsRef, { once: true, margin: '-100px' })
  const isBeneficiariesInView = useInView(beneficiariesRef, { once: true, margin: '-100px' })
  const isOverviewInView = useInView(overviewRef, { once: true, margin: '-100px' })
  const isTestimonialsInView = useInView(testimonialsRef, { once: true, margin: '-100px' })
  const isUtilitiesInView = useInView(utilitiesRef, { once: true, margin: '-100px' })
  const isStatsInView = useInView(statsRef, { once: true, margin: '-100px' })

  // Simplified animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.8,
        staggerChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6 },
    },
  }

  const cardVariants = {
    hidden: { opacity: 0, y: 40 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.8 },
    },
  }

  return (
    <main className="w-full flex flex-col items-center justify-center relative overflow-x-hidden">
      {/* Hero Section */}
      <motion.section className="py-16 sm:py-24 lg:py-32 container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="border-b z-10">
          <div className="mx-auto flex flex-col items-center text-center">
            <div className="z-10 items-center">
              {/* Hero Badge */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="inline-flex items-center rounded-full border px-3 py-1.5 text-sm font-medium mb-8"
              >
                <Shield className="mr-2 h-4 w-4 text-primary" />
                PCI DSS v4.0 Certified • Enterprise AI-Powered
              </motion.div>

              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="mb-6 text-4xl sm:text-5xl lg:text-7xl xl:text-8xl font-bold leading-tight"
              >
                <AnimatedText
                  text="SentinelAI"
                  className="text-4xl sm:text-5xl lg:text-7xl xl:text-8xl font-bold bg-gradient-to-r from-primary via-primary to-primary/80 bg-clip-text text-transparent"
                  animationType="letters"
                  staggerDelay={0.08}
                  duration={0.8}
                />
              </motion.h1>

              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="mx-auto max-w-3xl text-lg sm:text-xl lg:text-2xl text-muted-foreground mb-8"
              >
                AI-powered automated audit framework for <span className="text-primary font-semibold">PCI DSS compliance</span>. 
                Eliminate manual evidence collection and accelerate your compliance journey with intelligent automation.
              </motion.p>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.4 }}
                className="flex flex-col sm:flex-row gap-4 justify-center mb-8"
              >
                <Button size="lg" className="px-8 py-6 text-lg font-semibold group">
                  Start Compliance Scan
                  <ChevronRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Button>
                <Button variant="outline" size="lg" className="px-8 py-6 text-lg font-semibold group">
                  <Play className="mr-2 h-5 w-5" />
                  Watch Demo
                </Button>
              </motion.div>

              {/* Hero Stats */}
              <motion.div
                ref={statsRef}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.6 }}
                className="grid grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8 mt-12 p-6 bg-muted/30 rounded-2xl border"
              >
                {stats.map((stat, index) => (
                  <motion.div
                    key={index}
                    variants={itemVariants}
                    initial="hidden"
                    animate={isStatsInView ? "visible" : "hidden"}
                    transition={{ delay: index * 0.1 }}
                    className="text-center"
                  >
                    <div className="text-2xl lg:text-3xl font-bold text-primary">{stat.number}</div>
                    <div className="text-sm lg:text-base text-muted-foreground">{stat.label}</div>
                  </motion.div>
                ))}
              </motion.div>
            </div>
          </div>

          {/* Hero Image */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.8 }}
            className="mt-16 lg:mt-24 relative"
          >
            <div className="relative rounded-2xl overflow-hidden border shadow-2xl bg-gradient-to-br from-primary/5 to-primary/10">
              <img
                src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=600&fit=crop&auto=format"
                alt="SentinelAI compliance dashboard showing AWS monitoring and audit reports"
                className="w-full h-[300px] sm:h-[400px] lg:h-[500px] object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-background/20 to-transparent" />
              <div className="absolute bottom-6 left-6 right-6">
                <div className="bg-background/90 backdrop-blur-sm rounded-lg p-4 border">
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                    <span>Live monitoring 247 AWS accounts • PCI DSS compliance: 96.8%</span>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </motion.section>

      {/* Features Section */}
      <motion.section
        ref={featuresRef}
        className="py-16 sm:py-24 lg:py-32 container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
        variants={containerVariants}
        initial="hidden"
        animate={isFeaturesInView ? "visible" : "hidden"}
      >
        <div className="grid gap-8 lg:grid-cols-3 lg:gap-16">
          <motion.div variants={itemVariants} className="lg:col-span-1">
            <AnimatedText
              text="Everything you need for automated compliance"
              className="text-3xl sm:text-4xl lg:text-5xl font-bold leading-tight"
              animationType="words"
              staggerDelay={0.08}
              duration={0.8}
            />
            <p className="mt-6 text-lg text-muted-foreground">
              From evidence collection to AI-powered analysis, SentinelAI streamlines every aspect of your compliance workflow.
            </p>
          </motion.div>
          
          <div className="lg:col-span-2 grid sm:grid-cols-2 gap-6">
            <div className="space-y-4">
              {features.slice(0, 5).map((feature, index) => (
                <motion.div
                  key={index}
                  className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted/50 transition-colors"
                  variants={itemVariants}
                >
                  <Check className="h-5 w-5 text-primary flex-shrink-0" />
                  <span className="text-sm lg:text-base">{feature}</span>
                </motion.div>
              ))}
            </div>
            <div className="space-y-4">
              {features.slice(5).map((feature, index) => (
                <motion.div
                  key={index}
                  className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted/50 transition-colors"
                  variants={itemVariants}
                >
                  <Check className="h-5 w-5 text-primary flex-shrink-0" />
                  <span className="text-sm lg:text-base">{feature}</span>
                </motion.div>
              ))}
            </div>
          </div>
        </div>

        {/* Core Features Cards */}
        <motion.div
          ref={cardsRef}
          className="mt-20 lg:mt-32 grid gap-8 lg:grid-cols-3"
          variants={containerVariants}
          initial="hidden"
          animate={isCardsInView ? "visible" : "hidden"}
        >
          {cards.map((card, index) => {
            const IconComponent = card.icon
            return (
              <motion.div
                key={index}
                variants={cardVariants}
                whileHover={{
                  y: -10,
                  scale: 1.02,
                  transition: { duration: 0.3 }
                }}
                className="group"
              >
                <Card className="h-full overflow-hidden border-0 shadow-lg hover:shadow-xl transition-all duration-300">
                  <div className="relative overflow-hidden">
                    <img
                      src={card.image}
                      alt={card.alt}
                      className="w-full h-48 lg:h-56 object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-background/60 to-transparent" />
                    <div className="absolute top-4 left-4">
                      <div className="p-2 bg-background/90 backdrop-blur-sm rounded-lg border">
                        <IconComponent className="h-6 w-6 text-primary" />
                      </div>
                    </div>
                  </div>
                  <CardHeader className="pb-4">
                    <CardTitle className="text-xl lg:text-2xl">{card.title}</CardTitle>
                    <CardDescription className="text-base">{card.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-3">
                      {card.features.map((feature, featureIndex) => (
                        <li key={featureIndex} className="flex items-start gap-2 text-sm">
                          <Check className="h-4 w-4 mt-0.5 text-primary flex-shrink-0" />
                          <span>{feature}</span>
                        </li>
                      ))}
                    </ul>
                    <Button 
                      variant="outline" 
                      className="w-full mt-6 group"
                    >
                      Learn More
                      <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            )
          })}
        </motion.div>
      </motion.section>

      {/* Who Benefits Section */}
      <motion.section
        ref={beneficiariesRef}
        className="py-16 sm:py-24 lg:py-32 bg-muted/30"
        variants={containerVariants}
        initial="hidden"
        animate={isBeneficiariesInView ? "visible" : "hidden"}
      >
        <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div className="text-center mb-16" variants={itemVariants}>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">Who Benefits from SentinelAI?</h2>
            <p className="text-lg lg:text-xl text-muted-foreground max-w-3xl mx-auto">
              Our AI-powered audit framework helps every stakeholder in your compliance journey, 
              from technical teams to executive leadership.
            </p>
          </motion.div>

          <div className="grid gap-8 lg:grid-cols-3">
            {beneficiaries.map((beneficiary, index) => (
              <motion.div key={index} variants={cardVariants}>
                <Card className="h-full hover:shadow-lg transition-shadow duration-300">
                  <CardHeader>
                    <CardTitle className="text-xl lg:text-2xl">{beneficiary.title}</CardTitle>
                    <CardDescription className="text-base">{beneficiary.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-4">
                      {beneficiary.benefits.map((benefit, benefitIndex) => (
                        <li key={benefitIndex} className="flex items-start gap-3">
                          <Check className="h-5 w-5 mt-0.5 text-green-600 flex-shrink-0" />
                          <span className="text-sm lg:text-base">{benefit}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Platform Overview */}
      <motion.section
        ref={overviewRef}
        className="py-16 sm:py-24 lg:py-32 container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
        variants={containerVariants}
        initial="hidden"
        animate={isOverviewInView ? "visible" : "hidden"}
      >
        <motion.div className="text-center mb-16" variants={itemVariants}>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">Comprehensive Compliance Platform</h2>
          <p className="text-lg lg:text-xl text-muted-foreground max-w-3xl mx-auto">
            From evidence collection to AI-powered analysis, SentinelAI covers every aspect of your audit workflow
          </p>
        </motion.div>

        <div className="grid gap-12 lg:grid-cols-3">
          {overviewSections.map((section, index) => (
            <motion.div key={index} variants={itemVariants}>
              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold mb-4">{section.title}</h3>
              </div>
              <ul className="space-y-4">
                {section.items.map((item, itemIndex) => (
                  <li key={itemIndex} className="flex items-start gap-3 p-3 rounded-lg hover:bg-muted/50 transition-colors">
                    <Check className="h-5 w-5 mt-0.5 text-primary flex-shrink-0" />
                    <span className="text-sm lg:text-base">{item}</span>
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* Testimonials */}
      <motion.section
        ref={testimonialsRef}
        className="py-16 sm:py-24 lg:py-32 bg-muted/30"
        variants={containerVariants}
        initial="hidden"
        animate={isTestimonialsInView ? "visible" : "hidden"}
      >
        <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div className="text-center mb-16" variants={itemVariants}>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">Trusted by Compliance Teams</h2>
            <p className="text-lg lg:text-xl text-muted-foreground">
              See how SentinelAI transforms audit workflows across organizations
            </p>
          </motion.div>

          <div className="grid gap-8 lg:grid-cols-3">
            {testimonials.map((testimonial, index) => (
              <motion.div key={index} variants={cardVariants}>
                <Card className="h-full hover:shadow-lg transition-shadow duration-300">
                  <CardContent className="pt-8">
                    <blockquote className="text-base lg:text-lg mb-6 leading-relaxed">&quot;{testimonial.quote}&quot;</blockquote>
                    <footer>
                      <div className="font-semibold text-base">{testimonial.author}</div>
                      <div className="text-sm text-muted-foreground">{testimonial.role}</div>
                    </footer>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Platform Integrations */}
      <motion.section
        ref={utilitiesRef}
        className="py-16 sm:py-24 lg:py-32 container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
        variants={containerVariants}
        initial="hidden"
        animate={isUtilitiesInView ? "visible" : "hidden"}
      >
        <motion.div
          className="flex items-center gap-2 text-muted-foreground mb-4"
          variants={itemVariants}
        >
          <CloudLightning className="h-5 w-5" />
          <p className="text-sm">Platform Integrations</p>
        </motion.div>
        <Separator className="mb-8" />
        
        <div className="grid gap-8 lg:grid-cols-2 lg:gap-16 mb-16">
          <motion.h2
            className="text-3xl sm:text-4xl lg:text-5xl font-bold leading-tight"
            variants={itemVariants}
          >
            Built for enterprise-scale compliance automation
          </motion.h2>
          <motion.p
            className="text-lg lg:text-xl text-muted-foreground"
            variants={itemVariants}
          >
            SentinelAI integrates natively with AWS services and provides secure, scalable infrastructure for continuous compliance monitoring.
          </motion.p>
        </div>

        <motion.div
          className="grid gap-8 lg:grid-cols-3"
          variants={containerVariants}
        >
          {utilities.map((utility, index) => {
            const IconComponent = utility.icon
            return (
              <motion.div key={index} variants={itemVariants}>
                <Card className="h-full hover:shadow-lg transition-shadow duration-300">
                  <CardHeader>
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-primary/10 rounded-lg">
                        <IconComponent className="h-6 w-6 text-primary" />
                      </div>
                      <CardTitle className="text-xl">{utility.title}</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-base text-muted-foreground leading-relaxed">{utility.description}</p>
                  </CardContent>
                </Card>
              </motion.div>
            )
          })}
        </motion.div>
      </motion.section>

      {/* Coming Soon */}
      <motion.section className="py-16 sm:py-24 lg:py-32 bg-muted/30">
        <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">What&apos;s Coming Next</h2>
            <p className="text-lg lg:text-xl text-muted-foreground">
              Advanced AI capabilities and expanded compliance coverage
            </p>
          </div>

          <div className="grid gap-8 lg:grid-cols-3">
            {comingSoonFeatures.map((feature, index) => (
              <Card key={index} className="h-full opacity-90 hover:opacity-100 transition-opacity duration-300">
                <CardHeader>
                  <div className="flex items-center gap-3">
                    {feature.icon && (
                      <div className="p-2 bg-primary/10 rounded-lg">
                        <feature.icon className="h-6 w-6 text-primary" />
                      </div>
                    )}
                    <div>
                      <CardTitle className="text-xl">{feature.title}</CardTitle>
                      <div className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors mt-2">
                        Coming Soon
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-base text-muted-foreground leading-relaxed">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Features Timeline Section */}
      <Features />

      {/* About Section */}
      <About />

      {/* CTA Section */}
      <motion.section className="py-16 sm:py-24 lg:py-32 container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center bg-gradient-to-br from-primary/5 to-primary/10 rounded-3xl p-8 lg:p-16 border border-primary/20">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">Ready to Automate Your Compliance?</h2>
          <p className="text-lg lg:text-xl text-muted-foreground mb-10 max-w-3xl mx-auto">
            Join leading organizations using SentinelAI to streamline their PCI DSS compliance and reduce audit preparation time by 80%.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="px-8 py-6 text-lg font-semibold group">
              Start Free Trial
              <ChevronRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button variant="outline" size="lg" className="px-8 py-6 text-lg font-semibold">
              Schedule Demo
            </Button>
          </div>
          <p className="mt-8 text-sm text-muted-foreground">
            No setup required • 30-day free trial • Enterprise support available
          </p>
        </div>
      </motion.section>
    </main>
  )
}
