/* eslint-disable @next/next/no-img-element */
'use client'

import AnimatedText from '@/components/st/animated-text'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { motion, useInView } from 'framer-motion'
import { BarChart3, Check, ChevronRight, CloudLightning, Database, FileText, Globe, Shield, Users, Zap } from 'lucide-react'
import Image from 'next/image'
import { useRef } from 'react'

const features = [
  'Real-time collaboration',
  'Advanced database views',
  'Custom field types',
  'API integrations',
  'Role-based permissions',
  'Automated workflows',
  'Mobile responsive',
  'Offline sync',
  'Enterprise security',
  'Unlimited storage',
]

const cards = [
  {
    title: 'Database-First Design',
    description: 'Build powerful databases with flexible views, relationships, and automation.',
    icon: Database,
    image: 'https://chroniclehq.com/images/block-stats.png',
    features: [
      'Grid, Kanban, Calendar, and Gallery views',
      'Linked records and rollup fields',
      'Advanced filtering and sorting options',
      'Real-time collaboration with team members',
    ],
  },
  {
    title: 'Document Collaboration',
    description: 'Create rich documents with embedded databases, tables, and multimedia.',
    icon: FileText,
    image: 'https://chroniclehq.com/images/block-tickets.png',
    features: [
      'Rich text editor with database embeds',
      'Version history and comments',
      'Templates and reusable blocks',
      'Export to PDF, Word, and Markdown',
    ],
  },
  {
    title: 'Team Workspaces',
    description: 'Organize your work with teams, projects, and shared workspaces.',
    icon: Users,
    image: 'https://chroniclehq.com/images/block-poll.png',
    features: [
      'Team-based access control',
      'Project templates and workflows',
      'Activity feeds and notifications',
      'Cross-workspace data sharing',
    ],
  },
]

const overviewSections = [
  {
    title: 'Database Management',
    items: [
      'Create unlimited databases and tables',
      'Custom field types (text, number, date, select, etc.)',
      'Linked records and relationships',
      'Advanced formulas and calculations',
      'Bulk operations and data import',
      'Real-time sync across devices',
      'Backup and restore functionality',
      'Data validation and constraints',
      'Audit logs and change tracking',
    ],
  },
  {
    title: 'Document Creation',
    items: [
      'Rich text editor with formatting',
      'Database embeds and live data',
      'Tables, lists, and code blocks',
      'Media embedding (images, videos, files)',
      'Page templates and layouts',
      'Comments and mentions',
      'Version history and rollbacks',
      'Export and sharing options',
      'Full-text search capabilities',
    ],
  },
  {
    title: 'Collaboration Features',
    items: [
      'Real-time editing and presence',
      'Role-based permissions',
      'Team workspaces and projects',
      'Activity feeds and notifications',
      'Comment threads and discussions',
      'Approval workflows',
      'Guest access and sharing',
      'Mobile apps for iOS and Android',
      'Offline sync and editing',
    ],
  },
]

const testimonials = [
  {
    quote: 'VPBank has transformed how our team manages projects. The combination of databases and documents in one platform is game-changing.',
    author: 'Sarah Chen',
    role: 'Product Manager, TechFlow',
  },
  {
    quote: 'We switched from Airtable and Notion to VPBank and haven&apos;t looked back. The performance and flexibility are unmatched.',
    author: 'Marcus Rodriguez',
    role: 'CTO, StartupXYZ',
  },
  {
    quote: 'The real-time collaboration features make remote work seamless. Our team productivity has increased by 40%.',
    author: 'Emily Watson',
    role: 'Operations Director, GrowthCo',
  },
]

const utilities = [
  {
    title: 'Integrations',
    icon: Zap,
    description: 'Connect with your favorite tools. Slack, Google Workspace, Microsoft 365, and 100+ more integrations.',
  },
  {
    title: 'API Access',
    icon: Globe,
    description: 'Build custom integrations with our REST API. Webhooks, SDKs, and comprehensive documentation included.',
  },

  {
    title: 'Security',
    icon: Shield,
    description: 'Enterprise-grade security with SSO, 2FA, encryption, and compliance certifications.',
  },
]

const utilityCards = [
  {
    title: 'API & Webhooks',
    icon: Globe,
    image: 'https://chroniclehq.com/images/block-timeline.png',
    description: 'Build custom integrations with our comprehensive API. Webhooks, SDKs, and real-time data sync for your applications.',
  },
]

const comingSoonFeatures = [
  {
    title: 'AI Assistant',
    description: 'AI-powered assistance for data analysis, content generation, and workflow optimization. Built right into your workspace.',
  },
  {
    title: 'Workflow Automation',
    icon: Zap,
    image: 'https://chroniclehq.com/images/block-jessica.png',
    description: 'Automate repetitive tasks with triggers, actions, and conditional logic. Connect your databases and documents with powerful automation rules.',
  },
  {
    title: 'Analytics',
    icon: BarChart3,
    description: 'Track usage, performance, and insights with built-in analytics and reporting tools.',
  },
]

export default function Home() {
  // Refs for scroll animations
  const featuresRef = useRef(null)
  const cardsRef = useRef(null)
  const overviewRef = useRef(null)
  const testimonialsRef = useRef(null)
  const utilitiesRef = useRef(null)

  // InView hooks
  const isFeaturesInView = useInView(featuresRef, { once: true, margin: '-100px' })
  const isCardsInView = useInView(cardsRef, { once: true, margin: '-100px' })
  const isOverviewInView = useInView(overviewRef, { once: true, margin: '-100px' })
  const isTestimonialsInView = useInView(testimonialsRef, { once: true, margin: '-100px' })
  const isUtilitiesInView = useInView(utilitiesRef, { once: true, margin: '-100px' })

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
    <main className="w-screen flex flex-col items-center justify-center relative">
      {/* Hero Section */}
      <motion.section className="py-32 container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="overflow-hidden border-b z-10">
          <div className="mx-auto flex flex-col items-center">
            <div className="z-10 items-center text-center">
              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="mb-8 text-pretty text-4xl font-medium lg:text-8xl leading-[0.2]"
              >
                <AnimatedText
                  text="The all-in-one"
                  className="mb-8 text-pretty text-4xl font-bold lg:text-8xl"
                  animationType="letters"
                  staggerDelay={0.08}
                  duration={0.8}
                />
              </motion.h1>

              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="mx-auto max-w-screen-md text-muted-foreground lg:text-xl mt-8"
              >
                VPBank combines the power of databases and documents in one seamless platform.
                Build, collaborate, and scale faster than ever before.
              </motion.p>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.3 }}
                className="mt-12 flex w-full flex-col justify-center gap-2 sm:flex-row"
              >
                <Button size="lg" className='rounded-3xl'>
                  Start building for free
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
                <Button variant="outline" size="lg" className='rounded-3xl'>
                  Watch demo
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </motion.div>
            </div>
          </div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <Image
              src="/hero-dark.png"
              alt="VPBank workspace interface"
              width={1000}
              height={700}
              className="mx-auto mt-24 max-h-[700px] w-full rounded-3xl object-cover shadow-lg dark:hidden z-10 border border-[#454545] rounded-3xl overflow-hidden"
            />
            <Image
              src="/hero-light.png"
              alt="VPBank workspace interface"
              width={1000}
              height={700}
              className="mx-auto mt-24 max-h-[700px] w-full rounded-3xl object-cover shadow-lg hidden dark:block z-10 border border-[#454545] rounded-3xl overflow-hidden"
            />
          </motion.div>
        </div>
      </motion.section>

      {/* Features Section */}
      <motion.section
        ref={featuresRef}
        className="py-32 container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
        variants={containerVariants}
        initial="hidden"
        animate={isFeaturesInView ? "visible" : "hidden"}
      >
        <div className="grid gap-4 md:grid-cols-3 md:gap-16">
          <motion.div variants={itemVariants}>
            <AnimatedText
              text="Everything you need to build and scale"
              className="mb-4 text-4xl font-medium md:mb-0"
              animationType="letters"
              staggerDelay={0.08}
              duration={0.8}
            />
          </motion.div>
          <div className="flex flex-col gap-4 text-muted-foreground">
            {features.slice(0, 5).map((feature, index) => (
              <motion.div
                key={index}
                className="flex items-center gap-2"
                variants={itemVariants}
              >
                <Check className="h-4 w-4" />
                {feature}
              </motion.div>
            ))}
          </div>
          <div className="flex flex-col gap-4 text-muted-foreground">
            {features.slice(5).map((feature, index) => (
              <motion.div
                key={index}
                className="flex items-center gap-2"
                variants={itemVariants}
              >
                <Check className="h-4 w-4" />
                {feature}
              </motion.div>
            ))}
          </div>
        </div>

        {/* Cards Grid */}
        <motion.div
          ref={cardsRef}
          className="mt-20 grid gap-4 md:grid-cols-3"
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
              >
                <Card className="group h-full">
                  <div className="relative p-1">
                    <Image
                      src={card.image}
                      alt="VPBank feature preview"
                      width={400}
                      height={256}
                      className="max-h-96 w-full rounded-t-lg object-cover md:max-h-64 grayscale group-hover:grayscale-0 object-top hover:object-bottom transition-all duration-300"
                    />
                  </div>
                  <CardHeader>
                    <div className="flex items-center gap-2">
                      <IconComponent className="h-5 w-5 text-primary" />
                      <CardTitle className="text-lg">{card.title}</CardTitle>
                    </div>
                    <CardDescription>{card.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {card.features.map((feature, featureIndex) => (
                        <div key={featureIndex}>
                          <div className="flex items-start gap-2 text-muted-foreground">
                            <Check className="mt-1 h-4 w-4 shrink-0" />
                            {feature}
                          </div>
                          {featureIndex < card.features.length - 1 && <Separator className="mt-3" />}
                        </div>
                      ))}
                    </div>
                    <Separator className="my-4" />
                    <Button variant="link" className="p-0 h-auto font-medium">
                      Learn more
                      <ChevronRight className="ml-1 h-4 w-4" />
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            )
          })}
        </motion.div>
      </motion.section>

      {/* Overview Section */}
      <motion.section
        ref={overviewRef}
        className="pb-32 container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
        variants={containerVariants}
        initial="hidden"
        animate={isOverviewInView ? "visible" : "hidden"}
      >
        <div className="flex flex-col items-center justify-center">
          <div className="w-full max-w-96 lg:max-w-none">
            {overviewSections.map((section, sectionIndex) => (
              <div key={sectionIndex}>
                <Separator className="my-16" />
                <div className="mx-auto inline-block w-full gap-x-10 lg:grid lg:grid-cols-4">
                  <motion.h3
                    className="mb-4 text-lg font-semibold lg:text-3xl"
                    variants={itemVariants}
                  >
                    {section.title}
                  </motion.h3>
                  <div className="col-span-3 grid gap-x-10 gap-y-4 lg:grid-cols-3">
                    {section.items.map((item, itemIndex) => (
                      <motion.div
                        key={itemIndex}
                        className="flex gap-1 text-muted-foreground"
                        variants={itemVariants}
                      >
                        <Check className="mr-2 inline-block w-4 h-4 shrink-0" />
                        {item}
                      </motion.div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Testimonials Section */}
      <motion.section
        ref={testimonialsRef}
        className="py-32 container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
        variants={containerVariants}
        initial="hidden"
        animate={isTestimonialsInView ? "visible" : "hidden"}
      >
        <div className="flex flex-col gap-6">
          <div className="grid grid-cols-1 items-stretch gap-x-0 gap-y-4 lg:grid-cols-3 lg:gap-4">
            <motion.div variants={itemVariants}>
              <img
                src="https://chroniclehq.com/images/block-image-stack.png"
                alt="VPBank workspace"
                className="h-72 w-full rounded-md object-cover lg:h-auto"
              />
            </motion.div>
            <motion.div
              className="rounded-3xl border bg-card text-card-foreground shadow-sm col-span-2 flex items-center justify-center p-6"
              variants={cardVariants}
            >
              <div className="flex flex-col gap-4">
                <q className="text-xl font-medium lg:text-3xl">{testimonials[0].quote}</q>
                <div className="flex flex-col items-start">
                  <p className="font-medium">{testimonials[0].author}</p>
                  <p className="text-muted-foreground">{testimonials[0].role}</p>
                </div>
              </div>
            </motion.div>
          </div>
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
            {testimonials.slice(1).map((testimonial, index) => (
              <motion.div
                key={index}
                className="rounded-3xl border bg-card text-card-foreground shadow-sm"
                variants={cardVariants}
                whileHover={{
                  y: -5,
                  scale: 1.02,
                  transition: { duration: 0.3 }
                }}
              >
                <div className="p-6 px-6 pt-6 leading-7 text-muted-foreground">
                  <q>{testimonial.quote}</q>
                </div>
                <div className="flex items-center p-6 pt-0">
                  <div className="flex gap-4 leading-5">
                    <span className="relative flex shrink-0 overflow-hidden size-9 rounded-full ring-1 ring-input"></span>
                    <div className="text-sm">
                      <p className="font-medium">{testimonial.author}</p>
                      <p className="text-muted-foreground">{testimonial.role}</p>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Utilities Section */}
      <motion.section
        ref={utilitiesRef}
        className="py-32 container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
        variants={containerVariants}
        initial="hidden"
        animate={isUtilitiesInView ? "visible" : "hidden"}
      >
        <motion.div
          className="flex items-center gap-2 text-muted-foreground"
          variants={itemVariants}
        >
          <CloudLightning />
          <p className="text-sm">Platform Features</p>
        </motion.div>
        <Separator className="mb-8 mt-3" />
        <div className="flex flex-col justify-between gap-6 md:flex-row">
          <motion.h2
            className="text-3xl font-medium md:w-1/2"
            variants={itemVariants}
          >
            Built for teams that need more than just databases and documents.
          </motion.h2>
          <motion.p
            className="md:w-1/2 text-muted-foreground"
            variants={itemVariants}
          >
            From startups to enterprises, VPBank provides the tools you need to build, collaborate, and scale your operations.
          </motion.p>
        </div>
        <div className="mt-11 flex flex-col gap-6 md:flex-row">
          <div className="flex w-full flex-col gap-6">
            {utilities.slice(0, 2).map((utility, index) => {
              const IconComponent = utility.icon
              return (
                <motion.div
                  key={index}
                  className="rounded-3xl border bg-card text-card-foreground shadow-sm p-6"
                  variants={cardVariants}
                  whileHover={{
                    y: -5,
                    scale: 1.02,
                    transition: { duration: 0.3 }
                  }}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <IconComponent className="h-4 w-4" />
                    <p className="font-medium">{utility.title}</p>
                  </div>
                  <p className="text-muted-foreground">
                    {utility.description}
                  </p>
                </motion.div>
              )
            })}
            {utilityCards.map((card, index) => {
              const IconComponent = card.icon
              return (
                <motion.div
                  key={index}
                  className="rounded-3xl border bg-card text-card-foreground shadow-sm"
                  variants={cardVariants}
                  whileHover={{
                    y: -5,
                    scale: 1.02,
                    transition: { duration: 0.3 }
                  }}
                >
                  <img
                    src={card.image}
                    alt={`VPBank ${card.title.toLowerCase()}`}
                    className="aspect-video w-full object-cover object-top hover:object-bottom transition-all duration-300"
                  />
                  <div className="p-6">
                    <div className="flex items-center gap-2 mb-1">
                      <IconComponent className="h-4 w-4" />
                      <p className="font-medium">{card.title}</p>
                    </div>
                    <p className="text-muted-foreground">
                      {card.description}
                    </p>
                  </div>
                </motion.div>
              )
            })}
            {utilities.slice(2).map((utility, index) => {
              const IconComponent = utility.icon
              return (
                <motion.div
                  key={index}
                  className="rounded-3xl border bg-card text-card-foreground shadow-sm p-6"
                  variants={cardVariants}
                  whileHover={{
                    y: -5,
                    scale: 1.02,
                    transition: { duration: 0.3 }
                  }}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <IconComponent className="h-4 w-4" />
                    <p className="font-medium">{utility.title}</p>
                  </div>
                  <p className="text-muted-foreground">
                    {utility.description}
                  </p>
                </motion.div>
              )
            })}
          </div>
          <div className="flex w-full flex-col gap-6">
            {comingSoonFeatures.map((feature, index) => (
              <motion.div
                key={index}
                className="rounded-3xl border text-card-foreground border-dashed bg-transparent p-6 shadow-none"
                variants={cardVariants}
                whileHover={{
                  y: -5,
                  scale: 1.02,
                  transition: { duration: 0.3 }
                }}
              >
                {feature.image && (
                  <img
                    src={feature.image}
                    alt={`VPBank ${feature.title.toLowerCase()}`}
                    className="aspect-video w-full object-cover object-top hover:object-bottom transition-all duration-300"
                  />
                )}
                <div className="mb-1 flex items-center gap-2 font-medium">
                  {feature.title}
                  <div className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 text-foreground">
                    Coming soon
                  </div>
                </div>
                <p className="text-muted-foreground">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>
    </main>
  )
}
