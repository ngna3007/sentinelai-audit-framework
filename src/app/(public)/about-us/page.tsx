'use client'

import AnimatedText from '@/components/st/animated-text'
import { FloatingPathsBackground } from '@/components/st/bgr'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { motion } from 'framer-motion'
import { Check, ChevronRight, Dribbble, Github, Heart, Lightbulb, Linkedin, Target, TrendingUp } from 'lucide-react'
import Image from 'next/image'

const values = [
    'Innovation at the core',
    'Customer-first approach',
    'Transparency and trust',
    'Continuous improvement',
    'Diversity and inclusion',
    'Environmental responsibility',
    'Data privacy protection',
    'Community building',
    'Accessibility for all',
    'Sustainable growth',
]

const team = [
    {
        name: 'Sarah Chen',
        role: 'CEO & Co-founder',
        image: 'https://chroniclehq.com/images/block-jessica.png',
        bio: 'Former product leader at Google and Notion. Passionate about building tools that empower teams.',
    },
    {
        name: 'Marcus Rodriguez',
        role: 'CTO & Co-founder',
        image: 'https://chroniclehq.com/images/block-timeline.png',
        bio: 'Ex-engineering lead at Stripe and Airbnb. Expert in scalable architecture and real-time systems.',
    },
]

const milestones = [
    {
        year: '2024',
        title: 'Series A Funding',
        description: 'Raised $25M to accelerate product development and team growth.',
    },
    {
        year: '2023',
        title: 'Product Launch',
        description: 'Launched VPBank to the public with overwhelming positive response.',
    },
    {
        year: '2022',
        title: 'Company Founded',
        description: 'Started with a vision to unify databases and documents in one platform.',
    },
]

const stats = [
    {
        number: '10,000+',
        label: 'Active users',
    },
    {
        number: '500+',
        label: 'Organizations',
    },
    {
        number: '99.9%',
        label: 'Uptime',
    },
    {
        number: '24/7',
        label: 'Support',
    },
]

const missionFeatures = [
    {
        icon: Target,
        title: 'Clear Vision',
        description: 'We envision a world where teams can focus on their work, not their tools.',
    },
    {
        icon: Heart,
        title: 'User-First',
        description: 'Every feature we build is designed with our users\' needs in mind.',
    },
    {
        icon: Lightbulb,
        title: 'Innovation',
        description: 'We\'re constantly pushing the boundaries of what\'s possible.',
    },
]

const teamMembers = [
    {
        name: 'Name',
        role: 'Role',
        bio: 'Elig doloremque mollitia fugiat omnis! Porro facilis quo animi consequatur. Explicabo.',
        image: '/placeholder.svg',
    },
    {
        name: 'Name',
        role: 'Role',
        bio: 'Elig doloremque mollitia fugiat omnis!',
        image: '/placeholder.svg',
    },
    {
        name: 'Name',
        role: 'Role',
        bio: 'Elig doloremque mollitia fugiat omnis! Porro facilis quo animi consequatur. Explicabo.',
        image: '/placeholder.svg',
    },
    {
        name: 'Name',
        role: 'Role',
        bio: 'Elig doloremque mollitia fugiat omnis! Porro facilis quo animi consequatur. Explicabo.',
        image: '/placeholder.svg',
    },
    {
        name: 'Name',
        role: 'Role',
        bio: 'Elig doloremque mollitia fugiat omnis! Porro facilis quo animi consequatur. Explicabo.',
        image: '/placeholder.svg',
    },
    {
        name: 'Name',
        role: 'Role',
        bio: 'Elig doloremque mollitia fugiat omnis! Porro facilis quo animi consequatur. Explicabo.',
        image: '/placeholder.svg',
    },
]

const socialLinks = [
    { icon: Github, href: '#' },
    { icon: Linkedin, href: '#' },
    { icon: Dribbble, href: '#' },
]

const testimonials = [
    {
        quote: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Atque eveniet suscipit corporis sequi usdam alias fugiat iusto perspiciatis.',
        author: 'John Doe',
        role: 'CEO, Company Name',
    },
    {
        quote: 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Ipsa, eveniet inventore! Omnis incidunt vel iste.',
        author: 'John Doe',
        role: 'CEO, Company Name',
    },
    {
        quote: 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Ipsa, eveniet inventore! Omnis incidunt vel iste.',
        author: 'John Doe',
        role: 'CEO, Company Name',
    },
]

export default function AboutUs() {
    return (
        <main className="w-full min-h-screen flex flex-col items-center justify-center relative">
            {/* Hero Section */}
            <motion.section
                className="w-full py-16 md:py-24 lg:py-32"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <FloatingPathsBackground
                    className="flex aspect-16/9 items-center justify-center absolute top-0 left-0 -z-10"
                    position={0}
                >
                    <></>
                </FloatingPathsBackground>

                <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-12">
                        <motion.h1
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.1 }}
                            className="mb-8"
                        >
                            <AnimatedText
                                text="About VPBank"
                                className="text-4xl md:text-6xl lg:text-8xl font-bold"
                                animationType="letters"
                                staggerDelay={0.08}
                                duration={0.8}
                            />
                        </motion.h1>

                        <motion.p
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.2 }}
                            className="mx-auto max-w-3xl text-muted-foreground text-lg lg:text-xl"
                        >
                            We&apos;re building the future of work by combining the power of databases and documents in one seamless
                            platform.
                        </motion.p>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.3 }}
                            className="mt-8 flex flex-col sm:flex-row gap-4 justify-center"
                        >
                            <Button size="lg">
                                Join our team
                                <ChevronRight className="ml-2 h-4 w-4" />
                            </Button>
                            <Button variant="outline" size="lg">
                                Read our story
                                <ChevronRight className="ml-2 h-4 w-4" />
                            </Button>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.4 }}
                            className="mt-8 flex flex-col sm:flex-row gap-4 justify-center border border-[#454545] rounded-3xl overflow-hidden"
                        >
                            <Image
                                src="/about-us.jpg"
                                alt="VPBank team and culture"
                                width={1000}
                                height={700}
                                className="w-full rounded-3xl object-cover"
                            />
                        </motion.div>
                    </div>
                </div>
            </motion.section>

            {/* Kanban Board Grid Layout */}
            <section className="w-full py-16 md:py-24">
                <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-12">
                        {/* Column 1: Mission & Values */}
                        <div className="space-y-6">
                            {/* Mission Card */}
                            <Card className="h-fit">
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <Target className="h-5 w-5 text-primary" />
                                        Our Mission
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <p className="text-muted-foreground">
                                        To empower teams to work more efficiently by providing a unified platform that combines the
                                        flexibility of documents with the power of databases.
                                    </p>
                                    <div className="grid gap-4">
                                        {missionFeatures.map((feature, index) => {
                                            const IconComponent = feature.icon
                                            return (
                                                <div key={index} className="flex items-start gap-3">
                                                    <IconComponent className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                                                    <div>
                                                        <h4 className="font-medium">{feature.title}</h4>
                                                        <p className="text-sm text-muted-foreground">
                                                            {feature.description}
                                                        </p>
                                                    </div>
                                                </div>
                                            )
                                        })}
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Values Card */}
                            <Card className="h-fit">
                                <CardHeader>
                                    <CardTitle>Our Values</CardTitle>
                                    <CardDescription>Principles that guide everything we do</CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <div className="grid gap-3">
                                        {values.map((value, index) => (
                                            <div key={index} className="flex items-center gap-2">
                                                <Check className="h-4 w-4 text-primary flex-shrink-0" />
                                                <span className="text-sm">{value}</span>
                                            </div>
                                        ))}
                                    </div>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Column 2: Team & Stats */}
                        <div className="space-y-6">
                            {/* Stats Card */}
                            <Card className="h-fit">
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <TrendingUp className="h-5 w-5 text-primary" />
                                        By the Numbers
                                    </CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="grid grid-cols-2 gap-6">
                                        {stats.map((stat, index) => (
                                            <div key={index} className="text-center">
                                                <div className="text-2xl md:text-3xl font-bold text-primary mb-1">{stat.number}</div>
                                                <div className="text-sm text-muted-foreground">{stat.label}</div>
                                            </div>
                                        ))}
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Team Cards */}
                            {team.map((member, index) => (
                                <Card key={index} className="h-fit group">
                                    <div className="relative">
                                        <Image
                                            src={member.image}
                                            alt={member.name}
                                            width={400}
                                            height={200}
                                            className="w-full h-32 object-cover rounded-t-lg grayscale group-hover:grayscale-0 transition-all duration-300"
                                        />
                                    </div>
                                    <CardHeader className="pb-2">
                                        <CardTitle className="text-lg">{member.name}</CardTitle>
                                        <CardDescription className="font-medium text-primary">{member.role}</CardDescription>
                                    </CardHeader>
                                    <CardContent>
                                        <p className="text-sm text-muted-foreground">{member.bio}</p>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>

                        {/* Column 3: Journey & CTA */}
                        <div className="space-y-6">
                            {/* Timeline Cards */}
                            {milestones.map((milestone, index) => (
                                <Card key={index} className="h-fit">
                                    <CardHeader>
                                        <div className="flex items-center gap-3">
                                            <div className="text-2xl font-bold text-primary bg-primary/10 rounded-full w-12 h-12 flex items-center justify-center">
                                                {milestone.year.slice(-2)}
                                            </div>
                                            <div>
                                                <CardTitle className="text-lg">{milestone.title}</CardTitle>
                                                <CardDescription>{milestone.year}</CardDescription>
                                            </div>
                                        </div>
                                    </CardHeader>
                                    <CardContent>
                                        <p className="text-muted-foreground">{milestone.description}</p>
                                    </CardContent>
                                </Card>
                            ))}

                            {/* CTA Card */}
                            <Card className="h-fit bg-primary/5 border-primary/20">
                                <CardHeader>
                                    <CardTitle>Join Us in Building the Future</CardTitle>
                                    <CardDescription>We&apos;re always looking for talented people who share our vision.</CardDescription>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <p className="text-sm text-muted-foreground">Come help us transform how teams work together.</p>
                                    <div className="flex flex-col gap-3">
                                        <Button size="sm" className="w-full">
                                            View open positions
                                            <ChevronRight className="ml-2 h-4 w-4" />
                                        </Button>
                                        <Button variant="outline" size="sm" className="w-full bg-transparent">
                                            Contact us
                                            <ChevronRight className="ml-2 h-4 w-4" />
                                        </Button>
                                    </div>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                </div>
            </section>

            <section className="py-32 max-w-7xl mx-auto px-4 md:px-6 lg:px-8">
                <div className="container flex flex-col items-start text-left">
                    <p className="semibold">We&#x27;re hiring</p>
                    <h2 className="my-6 text-pretty text-2xl font-bold lg:text-4xl">Meet our team</h2>
                    <p className="mb-8 max-w-3xl text-muted-foreground lg:text-xl">
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Elig doloremque mollitia fugiat
                        omnis! Porro facilis quo animi consequatur. Explicabo.
                    </p>
                </div>
                <div className="container mt-16 grid gap-x-12 gap-y-8 lg:grid-cols-2">
                    {teamMembers.map((member, index) => (
                        <div key={index} className="flex flex-col sm:flex-row">
                            <div className="mb-4 aspect-square w-full shrink-0 overflow-clip  sm:mb-0 sm:mr-5 sm:size-48">
                                {/* <Image
                                    src={member.image}
                                    alt={member.name}
                                    width={192}
                                    height={192}
                                    className="w-full h-full object-cover"
                                /> */}
                                <Avatar
                                    className="w-full h-full object-cover">
                                    <AvatarImage src={member.image} alt={member.name} />
                                    <AvatarFallback>
                                        {member.name.charAt(0)}
                                    </AvatarFallback>
                                </Avatar>
                            </div>
                            <div className="flex flex-1 flex-col items-start">
                                <p className="w-full text-left font-medium">{member.name}</p>
                                <p className="w-full text-left text-muted-foreground">{member.role}</p>
                                <p className="w-full py-2 text-sm text-muted-foreground">
                                    {member.bio}
                                </p>
                                <div className="my-2 flex items-start gap-4">
                                    {socialLinks.map((social, socialIndex) => {
                                        const IconComponent = social.icon
                                        return (
                                            <a key={socialIndex} href={social.href}>
                                                <IconComponent className="size-4 text-muted-foreground" />
                                            </a>
                                        )
                                    })}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            <section className="py-32 max-w-7xl mx-auto px-4 md:px-6 lg:px-8">
                <div className="container">
                    <div className="flex flex-col gap-6">
                        <div className="grid grid-cols-1 items-stretch gap-x-0 gap-y-4 lg:grid-cols-3 lg:gap-4">
                            <Image
                                src="/images/placeholders/minima/placeholder-1.jpg"
                                alt="placeholder"
                                width={400}
                                height={288}
                                className="h-72 w-full rounded-md object-cover lg:h-auto"
                            />
                            <div className="rounded-lg border bg-card text-card-foreground shadow-sm col-span-2 flex items-center justify-center p-6">
                                <div className="flex flex-col gap-4">
                                    <q className="text-xl font-medium lg:text-3xl">{testimonials[0].quote}</q>
                                    <div className="flex flex-col items-start">
                                        <p>{testimonials[0].author}</p>
                                        <p className="text-muted-foreground">{testimonials[0].role}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
                            {testimonials.slice(1).map((testimonial, index) => (
                                <div key={index} className="rounded-lg border bg-card text-card-foreground shadow-sm">
                                    <div className="p-6 px-6 pt-6 leading-7 text-foreground/70">
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
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </section>
        </main>
    )
}
