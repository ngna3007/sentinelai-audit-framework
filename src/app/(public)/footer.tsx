'use client'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Separator } from '@/components/ui/separator'
import { AnimatePresence, motion } from 'framer-motion'
import { ArrowRight, Check, Github, Linkedin, Mail, Twitter } from 'lucide-react'
import Image from 'next/image'
import Link from 'next/link'
import { useState } from 'react'

const footerSections = [
    {
        title: 'Product',
        links: [
            { name: 'Why VPBank', href: '/why' },
            { name: 'Pricing', href: '/pricing' },
            { name: 'Features', href: '/#features' },
            { name: 'Integrations', href: '/#integrations' },
            { name: 'Security', href: '/security' },
        ],
    },
    {
        title: 'Company',
        links: [
            { name: 'About Us', href: '/about-us' },
            { name: 'Blog', href: '/blog' },
            { name: 'Contact Sales', href: '/contact-sales' },
            { name: 'Careers', href: '/careers' },
            { name: 'Privacy', href: '/privacy' },
        ],
    },
    {
        title: 'Resources',
        links: [
            { name: 'Help Center', href: '/help' },
            { name: 'API Docs', href: '/docs' },
            { name: 'Community', href: '/community' },
            { name: 'Status', href: '/status' },
            { name: 'Support', href: '/support' },
        ],
    },
]

const socialLinks = [
    { icon: Twitter, href: '#', label: 'Twitter', color: 'hover:text-blue-400' },
    { icon: Github, href: '#', label: 'GitHub', color: 'hover:text-gray-400' },
    { icon: Linkedin, href: '#', label: 'LinkedIn', color: 'hover:text-blue-600' },
    { icon: Mail, href: '#', label: 'Email', color: 'hover:text-red-400' },
]

export default function Footer() {
    const [email, setEmail] = useState('')
    const [isSubscribed, setIsSubscribed] = useState(false)
    const [isLoading, setIsLoading] = useState(false)

    const handleSubscribe = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!email) return

        setIsLoading(true)
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        setIsSubscribed(true)
        setIsLoading(false)
        setEmail('')
    }

    return (
        <motion.footer
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8 }}
            className="relative bg-gradient-to-b from-background to-background/95 border-t border-border/50"
        >
            {/* Background Pattern */}
            <div className="absolute inset-0 bg-grid-white/[0.02] bg-[size:50px_50px]" />

            <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
                <div className="py-20 lg:py-32">
                    {/* Main Footer Content */}
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16">
                        {/* Brand Section */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.1 }}
                            className="lg:col-span-4"
                        >
                            <div className="flex flex-col space-y-6">
                                {/* Logo */}
                                <motion.div
                                    whileHover={{ scale: 1.02 }}
                                    transition={{ duration: 0.2 }}
                                    className="flex items-center gap-3"
                                >
                                    <div className="relative">
                                        <Image
                                            src="/logo-light.svg"
                                            alt="VPBank"
                                            width={28}
                                            height={28}
                                            className="dark:hidden"
                                        />
                                        <Image
                                            src="/logo-dark.svg"
                                            alt="VPBank"
                                            width={28}
                                            height={28}
                                            className="hidden dark:block"
                                        />
                                    </div>
                                    <span className="text-2xl font-bold bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent">
                                        VPBank
                                    </span>
                                </motion.div>

                                {/* Description */}
                                <p className="text-muted-foreground leading-relaxed max-w-md">
                                    The all-in-one platform that combines the power of databases and documents
                                    in one seamless workspace. Build, collaborate, and scale faster than ever before.
                                </p>

                                {/* Social Links */}
                                <div className="flex items-center space-x-4">
                                    {socialLinks.map((social, index) => (
                                        <motion.a
                                            key={social.label}
                                            href={social.href}
                                            initial={{ opacity: 0, scale: 0 }}
                                            animate={{ opacity: 1, scale: 1 }}
                                            transition={{ duration: 0.3, delay: 0.2 + index * 0.1 }}
                                            whileHover={{ scale: 1.1, y: -2 }}
                                            whileTap={{ scale: 0.95 }}
                                            className={`p-2 rounded-lg bg-accent/50 hover:bg-accent transition-all duration-300 ${social.color}`}
                                        >
                                            <social.icon className="w-5 h-5" />
                                            <span className="sr-only">{social.label}</span>
                                        </motion.a>
                                    ))}
                                </div>
                            </div>
                        </motion.div>

                        {/* Navigation Sections */}
                        <div className="lg:col-span-8">
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                                {footerSections.map((section, sectionIndex) => (
                                    <motion.div
                                        key={section.title}
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ duration: 0.6, delay: 0.2 + sectionIndex * 0.1 }}
                                    >
                                        <h3 className="text-lg font-semibold mb-6 text-foreground">
                                            {section.title}
                                        </h3>
                                        <ul className="space-y-4">
                                            {section.links.map((link, linkIndex) => (
                                                <motion.li
                                                    key={link.name}
                                                    initial={{ opacity: 0, x: -10 }}
                                                    animate={{ opacity: 1, x: 0 }}
                                                    transition={{ duration: 0.3, delay: 0.3 + sectionIndex * 0.1 + linkIndex * 0.05 }}
                                                >
                                                    <Link
                                                        href={link.href}
                                                        className="text-muted-foreground hover:text-primary transition-colors duration-300 group flex items-center"
                                                    >
                                                        <span className="group-hover:translate-x-1 transition-transform duration-300">
                                                            {link.name}
                                                        </span>
                                                    </Link>
                                                </motion.li>
                                            ))}
                                        </ul>
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    </div>

                    <Separator className="my-16" />

                    {/* Newsletter Section */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.4 }}
                        className="max-w-7xl mx-auto text-center"
                    >
                        <div className="bg-gradient-to-r from-primary/5 to-primary/10 rounded-2xl p-8 lg:p-12 border border-primary/20">
                            <motion.div
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ duration: 0.6, delay: 0.5 }}
                                className="flex items-center justify-center mb-4"
                            >
                                <div className="p-3 rounded-full bg-primary/10 aspect-square">
                                    <Image
                                        src="/logo-light.svg"
                                        alt="VPBank"
                                        width={28}
                                        height={28}
                                        className="dark:hidden"
                                    />
                                    <Image
                                        src="/logo-dark.svg"
                                        alt="VPBank"
                                        width={28}
                                        height={28}
                                        className="hidden dark:block"
                                    />
                                </div>
                            </motion.div>

                            <h2 className="text-3xl lg:text-4xl font-bold mb-4">
                                Stay ahead of the curve
                            </h2>
                            <p className="text-muted-foreground text-lg mb-8 max-w-2xl mx-auto">
                                Get exclusive insights, product updates, and early access to new features.
                                Join thousands of teams already using VPBank.
                            </p>

                            <AnimatePresence mode="wait">
                                {!isSubscribed ? (
                                    <motion.form
                                        key="form"
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        exit={{ opacity: 0, y: -20 }}
                                        transition={{ duration: 0.3 }}
                                        onSubmit={handleSubscribe}
                                        className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto"
                                    >
                                        <div className="flex-1 relative">
                                            <Input
                                                type="email"
                                                placeholder="Enter your email"
                                                value={email}
                                                onChange={(e) => setEmail(e.target.value)}
                                                className="h-12 px-4 pr-12 rounded-full border-primary/20 focus:border-primary/40"
                                                required
                                            />
                                            <motion.div
                                                className="absolute right-3 top-1/2 -translate-y-1/2"
                                                animate={{ scale: isLoading ? [1, 1.2, 1] : 1 }}
                                                transition={{ duration: 0.5, repeat: isLoading ? Infinity : 0 }}
                                            >
                                                <Mail className="w-5 h-5 text-muted-foreground" />
                                            </motion.div>
                                        </div>
                                        <Button
                                            type="submit"
                                            disabled={isLoading || !email}
                                            className="h-12 px-8 rounded-full bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 disabled:opacity-50"
                                        >
                                            <AnimatePresence mode="wait">
                                                {isLoading ? (
                                                    <motion.div
                                                        key="loading"
                                                        initial={{ opacity: 0 }}
                                                        animate={{ opacity: 1 }}
                                                        exit={{ opacity: 0 }}
                                                        className="flex items-center"
                                                    >
                                                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2" />
                                                        Subscribing...
                                                    </motion.div>
                                                ) : (
                                                    <motion.div
                                                        key="subscribe"
                                                        initial={{ opacity: 0 }}
                                                        animate={{ opacity: 1 }}
                                                        exit={{ opacity: 0 }}
                                                        className="flex items-center"
                                                    >
                                                        Subscribe
                                                        <ArrowRight className="w-4 h-4 ml-2" />
                                                    </motion.div>
                                                )}
                                            </AnimatePresence>
                                        </Button>
                                    </motion.form>
                                ) : (
                                    <motion.div
                                        key="success"
                                        initial={{ opacity: 0, scale: 0.8 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        transition={{ duration: 0.5 }}
                                        className="flex items-center justify-center space-x-3 text-primary"
                                    >
                                        <Check className="w-6 h-6" />
                                        <span className="text-lg font-medium">Successfully subscribed!</span>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </div>
                    </motion.div>

                    <Separator className="my-16" />

                    {/* Bottom Section */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.6, delay: 0.6 }}
                        className="flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-muted-foreground"
                    >
                        <div className="flex items-center space-x-4">
                            <span>© 2024 VPBank. All rights reserved.</span>
                            <span className="hidden md:inline">•</span>
                            <Link href="/terms" className="hover:text-primary transition-colors">
                                Terms of Service
                            </Link>
                            <span className="hidden md:inline">•</span>
                            <Link href="/privacy" className="hover:text-primary transition-colors">
                                Privacy Policy
                            </Link>
                        </div>

                        <div className="flex items-center space-x-2 text-xs">
                            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                            <span>All systems operational</span>
                        </div>
                    </motion.div>
                </div>
            </div>
        </motion.footer>
    )
}
