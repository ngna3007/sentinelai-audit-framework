"use client"

import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { motion } from "framer-motion"
import { Check, ChevronDown } from "lucide-react"

const pricingPlans = [
    {
        name: "Free",
        price: 0,
        description: "For personal use only with limited features and support",
        features: [
            "Live Collaboration",
            "1 GB Storage",
            "2 Projects",
            "Basic Support",
            "Limited Customization",
            "Limited Integration",
            "Limited API Access",
        ],
        buttonText: "Get Started",
        buttonVariant: "outline" as const,
        highlighted: false,
    },
    {
        name: "Pro",
        price: 29,
        monthlyPrice: 34,
        description: "For small businesses with all the features and support",
        features: [
            "2 Team Members",
            "10 GB Storage",
            "10 Projects",
            "Priority Support",
            "Full Customization",
            "Full Integration",
            "Full API Access",
        ],
        buttonText: "Try for free",
        buttonVariant: "default" as const,
        highlighted: true,
        additionalText: "or purchase now",
    },
    {
        name: "Premium",
        price: 59,
        monthlyPrice: 69,
        description: "For teams and organizations with advanced features and support",
        features: [
            "5 Team Members",
            "50 GB Storage",
            "50 Projects",
            "Dedicated Support",
            "Advanced Customization",
            "Analytics",
            "Reports",
        ],
        buttonText: "Try for free",
        buttonVariant: "outline" as const,
        highlighted: false,
        additionalText: "or purchase now",
    },
    {
        name: "Enterprise",
        price: null,
        description: "For large companies with custom features and support and a dedicated account manager",
        features: [
            "10+ Team Members",
            "100+ GB Storage",
            "100+ Projects",
            "Dedicated Account Manager",
            "Custom Features",
            "Custom Support",
            "Custom Integration",
        ],
        buttonText: "Contact sales",
        buttonVariant: "outline" as const,
        highlighted: false,
    },
]

export default function Pricing() {
    return (
        <main className="w-full flex items-center flex-col">
            <section className="py-32 mx-auto">
                <div className="container">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        className="mx-auto mb-20 max-w-screen-lg text-center"
                    >
                        <h2 className="mb-3 text-pretty text-4xl font-bold lg:text-6xl">Pricing</h2>
                        <p className="text-muted-foreground lg:text-xl">
                            Check out our affordable pricing plans below and choose the one that suits you best. If you need a custom
                            plan, please contact us.
                        </p>
                    </motion.div>

                    <div className="mx-auto grid max-w-screen-sm gap-4 lg:max-w-none lg:grid-cols-4">
                        {pricingPlans.map((plan, index) => (
                            <motion.div
                                key={plan.name}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.5, delay: index * 0.1 }}
                                whileHover={{ y: -5 }}
                                className="h-full"
                            >
                                <Card className={`h-full flex flex-col ${plan.highlighted ? "border-primary shadow-lg" : ""}`}>
                                    <CardHeader className="text-center">
                                        <CardTitle className="text-3xl font-semibold">{plan.name}</CardTitle>
                                        <CardDescription className="text-balance">{plan.description}</CardDescription>
                                    </CardHeader>

                                    <CardContent className="flex-1 flex flex-col">
                                        <div className="mb-6 text-center">
                                            {plan.price !== null ? (
                                                <>
                                                    <div className="flex justify-center items-baseline">
                                                        <span className="text-lg font-semibold">$</span>
                                                        <span className="text-6xl font-semibold">{plan.price}</span>
                                                    </div>
                                                    {plan.monthlyPrice && (
                                                        <p className="text-sm text-muted-foreground mt-2">
                                                            Per user, per month billed annually <br />${plan.monthlyPrice} billed monthly
                                                        </p>
                                                    )}
                                                </>
                                            ) : (
                                                <div className="text-lg font-semibold text-muted-foreground">Custom</div>
                                            )}
                                        </div>

                                        <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} className="mb-6">
                                            <Button variant={plan.buttonVariant} className="w-full">
                                                {plan.buttonText}
                                            </Button>
                                            {plan.additionalText && (
                                                <p className="mt-4 text-muted-foreground text-sm">
                                                    or{" "}
                                                    <Link href="#" className="text-foreground hover:underline">
                                                        {plan.additionalText}
                                                    </Link>
                                                </p>
                                            )}
                                        </motion.div>

                                        <div className="flex-1">
                                            <div className="hidden lg:block">
                                                <p className="mb-2 text-lg font-semibold">
                                                    {index > 0 ? `Everything in ${pricingPlans[index - 1].name}, and:` : "Features"}
                                                </p>
                                                <ul className="space-y-4">
                                                    {plan.features.map((feature, featureIndex) => (
                                                        <motion.li
                                                            key={feature}
                                                            initial={{ opacity: 0, x: -10 }}
                                                            animate={{ opacity: 1, x: 0 }}
                                                            transition={{ duration: 0.3, delay: featureIndex * 0.05 }}
                                                            className="flex items-center gap-2"
                                                        >
                                                            <Check className="h-4 w-4 text-primary" />
                                                            <span>{feature}</span>
                                                        </motion.li>
                                                    ))}
                                                </ul>
                                            </div>

                                            <div className="lg:hidden">
                                                <Collapsible>
                                                    <CollapsibleTrigger className="flex flex-1 items-center justify-between py-4 font-medium transition-all hover:underline [&[data-state=open]>svg]:rotate-180">
                                                        See what&apos;s included
                                                        <ChevronDown className="h-4 w-4 shrink-0 transition-transform duration-200" />
                                                    </CollapsibleTrigger>
                                                    <CollapsibleContent>
                                                        <ul className="space-y-2">
                                                            {plan.features.map((feature) => (
                                                                <li key={feature} className="flex items-center gap-2">
                                                                    <Check className="h-4 w-4 text-primary" />
                                                                    <span className="text-sm">{feature}</span>
                                                                </li>
                                                            ))}
                                                        </ul>
                                                    </CollapsibleContent>
                                                </Collapsible>
                                            </div>

                                            <Link href="#" className="hover:underline text-sm text-muted-foreground mt-4 block">
                                                Learn more
                                            </Link>
                                        </div>
                                    </CardContent>
                                </Card>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>
        </main>
    )
}
