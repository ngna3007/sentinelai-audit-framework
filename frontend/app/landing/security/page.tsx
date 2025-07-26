
'use client'

import AnimatedText from '@/components/st/animated-text'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { motion } from 'framer-motion'
import { Bell, Check, ChevronRight, LayoutTemplate, Play } from 'lucide-react'
import Image from 'next/image'

const securityFeatures = [
    'End-to-end encryption',
    'Two-factor authentication',
    'Single sign-on (SSO)',
    'Role-based access control',
    'Audit logs and monitoring',
    'Data backup and recovery',
    'GDPR compliance',
    'SOC 2 Type II certified',
    'Regular security audits',
    'Penetration testing',
]


const websiteFeatures = [
    'Responsive Design and Layout',
    'Clean and Modern Design',
    'Easy to Customize',
    'Cross Browser Compatible',
    'SEO Friendly',
    'High Performance and Speed',
    'Clean Code and Well Documented',
    'Fast Loading and Free Updates',
    '24/7 Support',
    'Lifetime Access and Updates',
]

const blockCards = [
    {
        title: 'Copy and paste Blocks',
        description: 'Easly copy and paste any block you like and use it in your project.',
        image: '/images/placeholders/minima/placeholder-1.jpg',
        features: [
            'Responsive design and layout with clean and modern design',
            'Easy to customize with cross browser compatibility',
            'SEO friendly with high performance and speed for improved laod times',
        ],
    },
    {
        title: 'Easy to Customize Blocks',
        description: 'Easly customize any block you like and use it in your project.',
        image: '/images/placeholders/minima/placeholder-2.jpg',
        features: [
            'The blocks are clean and modern with easy to customize features',
            'All blocks are SEO friendly with cross browser compatibility',
            'Each block is responsive with high performance and speed',
        ],
    },
    {
        title: 'Readymade Blocks for you to use',
        description: 'Easly use any block you like and use it in your project.',
        image: '/images/placeholders/minima/placeholder-3.jpg',
        features: [
            'Prebuilt blocks built with shadcn/ui & TailwindCSS',
            'Synced with your project theme and design with easy to customize features',
            'Various blocks to choose from with high performance and speed',
        ],
    },
]

export default function Security() {
    return (
        <motion.main
            className="w-screen flex flex-col items-center justify-center relative"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6 }}
        >
            {/* Hero Section */}
            <section className="py-32">
                <div className="container max-w-7xl px-4 md:px-6 lg:px-8 mx-auto">
                    <div className="inline-flex items-center rounded-full border px-2.5 py-0.5 transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 text-foreground mb-4 max-w-full text-sm font-normal lg:mb-10 lg:py-2 lg:pl-2 lg:pr-5">
                        <span className="mr-2 flex size-8 shrink-0 items-center justify-center rounded-full ">
                            <Bell className="size-4" />
                        </span>
                        <p className="truncate whitespace-nowrap">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Commodi eaque distinctio iusto
                            voluptas voluptatum sed!
                        </p>
                    </div>
                    <h1 className="mb-6 text-4xl font-bold leading-none tracking-tighter md:text-[7vw] lg:text-8xl">
                        Streamline your workflow experience.
                    </h1>
                    <p className="max-w-2xl text-muted-foreground md:text-[2vw] lg:text-xl">
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum dolor assumenda voluptatem
                        nemo magni a maiores aspernatur.
                    </p>
                    <div className="mt-6 flex flex-col gap-4 sm:flex-row lg:mt-10">
                        <Button className="w-full md:w-auto">
                            Get a demo
                        </Button>
                        <Button variant="outline" className="w-full md:w-auto">
                            <Play className="mr-2 size-4" />
                            Watch video
                        </Button>
                    </div>
                </div>
            </section>

            {/* Security Features Section */}
            <section className="py-16 md:py-32">
                <div className="container max-w-7xl px-4 md:px-6 lg:px-8">
                    <div className="grid gap-6 md:gap-4 md:grid-cols-3 md:gap-16">
                        <AnimatedText
                            text="Enterprise security features"
                            className="mb-4 text-2xl md:text-4xl font-medium md:mb-0"
                            animationType="letters"
                            staggerDelay={0.08}
                            duration={0.8}
                        />
                        <div className="flex flex-col gap-3 md:gap-4 text-muted-foreground text-sm md:text-base">
                            {securityFeatures.slice(0, 5).map((feature, index) => (
                                <div key={index} className="flex items-center gap-2">
                                    <Check className="h-4 w-4" />
                                    {feature}
                                </div>
                            ))}
                        </div>
                        <div className="flex flex-col gap-3 md:gap-4 text-muted-foreground text-sm md:text-base">
                            {securityFeatures.slice(5).map((feature, index) => (
                                <div key={index} className="flex items-center gap-2">
                                    <Check className="h-4 w-4" />
                                    {feature}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            <section className="py-32">
                <div className="container max-w-7xl px-4 md:px-6 lg:px-8 mx-auto">
                    <div className="grid gap-4 md:grid-cols-3 md:gap-16">
                        <h2 className="mb-4 text-4xl font-medium md:mb-0">Build any kind of Website with our Blocks</h2>
                        <ul className="flex flex-col gap-4 text-muted-foreground">
                            {websiteFeatures.slice(0, 5).map((feature, index) => (
                                <li key={index} className="flex items-center gap-2">
                                    <Check className="size-4" />
                                    {feature}
                                </li>
                            ))}
                        </ul>
                        <ul className="flex flex-col gap-4 text-muted-foreground">
                            {websiteFeatures.slice(5).map((feature, index) => (
                                <li key={index} className="flex items-center gap-2">
                                    <Check className="size-4" />
                                    {feature}
                                </li>
                            ))}
                        </ul>
                    </div>
                    <div className="mt-20 grid gap-4 md:grid-cols-3">
                        {blockCards.map((card, index) => (
                            <Card key={index} className='rounded-3xl'>
                                <div className="relative p-1">
                                    <Image
                                        src={card.image}
                                        alt={card.title}
                                        width={400}
                                        height={256}
                                        className="max-h-96 w-full rounded-t-lg object-cover md:max-h-64"
                                    />
                                    <Badge className="absolute left-5 top-5 bg-zinc-900">
                                        Example
                                    </Badge>
                                </div>
                                <CardHeader className="pb-3">
                                    <CardTitle className="text-lg">{card.title}</CardTitle>
                                    <p className="text-muted-foreground">{card.description}</p>
                                </CardHeader>
                                <CardContent className="pt-0">
                                    <ul className="text-muted-foreground">
                                        {card.features.map((feature, featureIndex) => (
                                            <li key={featureIndex}>
                                                <div className="flex items-start gap-2 py-3">
                                                    <Check className="mt-1 size-4 shrink-0" />
                                                    {feature}
                                                </div>
                                                {featureIndex < card.features.length - 1 && <Separator />}
                                            </li>
                                        ))}
                                    </ul>
                                    <Separator className="my-4" />
                                    <Button variant="link" className="p-0 h-auto font-medium">
                                        Read more
                                        <ChevronRight className="ml-1 size-4" />
                                    </Button>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </section>

            <section className="mb-32 border-b pt-32">
                <div className="container max-w-7xl px-4 md:px-6 lg:px-8">
                    <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-1 text-muted-foreground">
                            <LayoutTemplate className="size-5" />
                            <p>UI Components</p>
                        </div>
                        <a href="#" className="hover:text-gray-800 hover:underline flex items-center">
                            Learn more
                            <ChevronRight className="ml-2 inline-block size-4" />
                        </a>
                    </div>
                    <Separator className="mb-8 mt-3" />
                    <div className="flex flex-col justify-between gap-6 md:flex-row">
                        <h2 className="text-3xl font-medium md:w-1/2">
                            Use our UI components to build your website faster
                        </h2>
                        <p className="leading-7 text-muted-foreground md:w-1/2">
                            Lorem ipsum dolor sit, amet consectetur adipisicing elit. Molestiae praesent, ad ullam quis
                            cupiditate atque maxime alias eaque repellendus perferendis, nemo repudiandae.
                        </p>
                    </div>
                    <Image
                        src="/images/placeholders/minima/placeholder-wide-1.jpg"
                        alt="placeholder"
                        width={1200}
                        height={384}
                        className="mt-20 max-h-96 w-full rounded-t-lg object-cover"
                    />
                </div>
            </section>
        </motion.main>
    )
} 