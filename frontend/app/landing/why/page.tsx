'use client'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { motion } from 'framer-motion'
import { Check, ChevronRight, LayoutTemplate, Minus } from 'lucide-react'

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
    'Unlimited storage'
]

const featureCards = [
    {
        image: 'https://chroniclehq.com/images/block-poll.png',
        title: 'Database-First Design',
        description: 'Build powerful databases with flexible views, relationships, and automation.',
        features: [
            'Grid, Kanban, Calendar, and Gallery views',
            'Linked records and rollup fields',
            'Advanced filtering and sorting options'
        ]
    },
    {
        image: 'https://chroniclehq.com/images/block-jessica.png',
        title: 'Document Collaboration',
        description: 'Create rich documents with embedded databases, tables, and multimedia.',
        features: [
            'Rich text editor with database embeds',
            'Version history and comments',
            'Templates and reusable blocks'
        ]
    },
    {
        image: 'https://chroniclehq.com/images/block-tickets.png',
        title: 'Team Workspaces',
        description: 'Organize your work with teams, projects, and shared workspaces.',
        features: [
            'Team-based access control',
            'Project templates and workflows',
            'Activity feeds and notifications'
        ]
    }
]

const pricingPlans = [
    {
        name: 'Pro',
        description: 'Perfect for growing teams.',
        price: '$10',
        priceDescription: 'per user per month',
        buttonText: 'Get Started',
        variant: 'default' as const
    },
    {
        name: 'Enterprise',
        description: 'For large organizations.',
        price: 'Contact us',
        priceDescription: 'Get in touch with us',
        buttonText: 'Get Started',
        variant: 'outline' as const
    }
]

const pricingFeatures = [
    { feature: 'Projects', pro: 'Unlimited', enterprise: 'Unlimited' },
    { feature: 'Integrations', pro: 'Unlimited', enterprise: 'Unlimited' },
    { feature: 'Live Collaboration', pro: true, enterprise: true },
    { feature: 'Custom permissions', pro: true, enterprise: true },
    { feature: 'Team members', pro: '$5/month per member', enterprise: '$5/month per member' },
    { feature: 'Basic reports', pro: true, enterprise: true },
    { feature: 'Advanced reports', pro: false, enterprise: true },
    { feature: 'Export data', pro: false, enterprise: true }
]

export default function WhyPage() {
    return (
        <motion.div
            className="w-full flex flex-col items-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6 }}
        >
            <section className="mb-16 md:mb-32 border-b pt-16 md:pt-32">
                <div className="container max-w-7xl px-4 md:px-6 lg:px-8">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between text-sm gap-4">
                        <div className="flex items-center gap-1 text-muted-foreground">
                            <LayoutTemplate className="size-5" />
                            <p>Platform Features</p>
                        </div>
                        <a href="#" className="hover:text-foreground hover:underline flex items-center">
                            Learn more<ChevronRight className="ml-2 inline-block size-4" />
                        </a>
                    </div>
                    <Separator className="mb-6 md:mb-8 mt-3" />
                    <div className="flex flex-col justify-between gap-6 md:flex-row">
                        <h2 className="text-2xl md:text-3xl font-medium md:w-1/2">
                            Why teams choose VPBank over traditional tools
                        </h2>
                        <p className="leading-7 text-muted-foreground md:w-1/2 text-sm md:text-base">
                            VPBank combines the best of databases and documents in one platform, eliminating the need for multiple tools and complex integrations.
                        </p>
                    </div>
                    <img
                        src="https://chroniclehq.com/images/block-roadmap.png"
                        alt="VPBank platform overview"
                        className="mt-12 md:mt-20 max-h-64 md:max-h-96 w-full rounded-t-lg object-cover"
                    />
                </div>
            </section>

            <section className="py-16 md:py-32">
                <div className="container max-w-7xl px-4 md:px-6 lg:px-8">
                    <div className="grid gap-6 md:gap-4 md:grid-cols-3 md:gap-16">
                        <h2 className="mb-4 text-2xl md:text-4xl font-medium md:mb-0">
                            Everything you need to build and scale
                        </h2>
                        <ul className="flex flex-col gap-3 md:gap-4 text-muted-foreground text-sm md:text-base">
                            {features.slice(0, 5).map((feature, index) => (
                                <li key={index} className="flex items-center gap-2">
                                    <Check className="size-4" />
                                    {feature}
                                </li>
                            ))}
                        </ul>
                        <ul className="flex flex-col gap-3 md:gap-4 text-muted-foreground text-sm md:text-base">
                            {features.slice(5).map((feature, index) => (
                                <li key={index} className="flex items-center gap-2">
                                    <Check className="size-4" />
                                    {feature}
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div className="mt-12 md:mt-20 grid gap-6 md:gap-4 md:grid-cols-3">
                        {featureCards.map((card, index) => (
                            <Card key={index}>
                                <div className="relative p-1">
                                    <img
                                        src={card.image}
                                        alt={card.title}
                                        className="max-h-48 md:max-h-96 w-full rounded-t-lg object-cover md:max-h-64"
                                    />
                                </div>
                                <CardHeader className="pb-3">
                                    <h3 className="font-medium text-sm md:text-base">{card.title}</h3>
                                    <p className="text-muted-foreground text-sm">{card.description}</p>
                                </CardHeader>
                                <CardContent className="pt-0">
                                    <ul className="text-muted-foreground text-sm">
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
                                    <a href="#" className="flex items-center gap-2 font-medium text-sm">
                                        Learn more<ChevronRight className="mt-0.5 size-4" />
                                    </a>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </section>

            <section className="py-16 md:py-32 w-full max-w-7xl px-4 md:px-6 lg:px-8">
                <div className="w-full">
                    <div className="flex flex-col items-center gap-4 text-center">
                        <h2 className="mb-2 text-2xl md:text-3xl font-semibold lg:text-5xl">Pricing</h2>
                        <p className="text-muted-foreground text-sm md:text-base lg:text-lg">
                            Simple, transparent pricing for teams of all sizes.
                        </p>
                    </div>

                    <div className="mt-8 md:mt-10 flex flex-col gap-6 lg:flex-row lg:gap-0">
                        {pricingPlans.map((plan, index) => (
                            <Card
                                key={index}
                                className={`flex w-full flex-col justify-between gap-6 md:gap-8 text-center ${index === 0 ? 'lg:rounded-r-none lg:border-r-0' : 'rounded-l-none border-l-0'
                                    }`}
                            >
                                <CardHeader className="flex flex-col space-y-1.5">
                                    <h3 className="text-xl md:text-2xl font-semibold leading-none tracking-tight">
                                        {plan.name}
                                    </h3>
                                    <p className="text-muted-foreground text-sm">{plan.description}</p>
                                </CardHeader>
                                <div className="px-4 md:px-6">
                                    <span className="text-3xl md:text-5xl font-bold">{plan.price}</span>
                                    <p className="mt-2 md:mt-3 text-muted-foreground text-sm">{plan.priceDescription}</p>
                                </div>
                                <div className="px-4 md:px-6">
                                    <Button variant={plan.variant} className="w-full">
                                        {plan.buttonText}
                                    </Button>
                                </div>
                            </Card>
                        ))}
                        <Separator orientation="vertical" className="hidden lg:block" />
                    </div>

                    <div className="relative w-full overflow-auto">
                        <Table className="mt-8 md:mt-10 min-w-[320px] md:min-w-[420px]">
                            <TableHeader>
                                <TableRow>
                                    <TableHead className="text-xs md:text-sm"></TableHead>
                                    <TableHead className="text-xs md:text-sm">Pro</TableHead>
                                    <TableHead className="text-xs md:text-sm">Enterprise</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {pricingFeatures.map((feature, index) => (
                                    <TableRow key={index}>
                                        <TableCell className="text-xs md:text-sm">{feature.feature}</TableCell>
                                        <TableCell className="text-xs md:text-sm">
                                            {typeof feature.pro === 'boolean' ? (
                                                feature.pro ? <Check className="size-4 md:size-6" /> : <Minus className="size-4 md:size-6" />
                                            ) : (
                                                feature.pro
                                            )}
                                        </TableCell>
                                        <TableCell className="text-xs md:text-sm">
                                            {typeof feature.enterprise === 'boolean' ? (
                                                feature.enterprise ? <Check className="size-4 md:size-6" /> : <Minus className="size-4 md:size-6" />
                                            ) : (
                                                feature.enterprise
                                            )}
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                </div>
            </section>
        </motion.div>
    )
}