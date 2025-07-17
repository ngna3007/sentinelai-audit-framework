'use client'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Separator } from '@/components/ui/separator'
import { AnimatePresence, motion } from 'framer-motion'
import { ArrowRight, Check, Github, Linkedin, Mail, Twitter, Shield } from 'lucide-react'
import Link from 'next/link'
import React, { useState } from 'react'

const footerSections = [
    {
        title: 'Product',
        links: [
            { name: 'Features', href: '/features' },
            { name: 'Pricing', href: '/pricing' },
            { name: 'Security', href: '/security' },
            { name: 'API Documentation', href: '/docs' },
            { name: 'Demo', href: '/demo' },
        ],
    },
    {
        title: 'Compliance',
        links: [
            { name: 'PCI DSS', href: '/compliance/pci-dss' },
            { name: 'ISO 27001', href: '/compliance/iso-27001' },
            { name: 'SOC 2', href: '/compliance/soc2' },
            { name: 'Vietnamese Decree 13', href: '/compliance/decree-13' },
            { name: 'AWS Security', href: '/compliance/aws' },
        ],
    },
    {
        title: 'Resources',
        links: [
            { name: 'Documentation', href: '/docs' },
            { name: 'Help Center', href: '/help' },
            { name: 'API Reference', href: '/api' },
            { name: 'Status', href: '/status' },
            { name: 'Support', href: '/support' },
        ],
    },
    {
        title: 'Company',
        links: [
            { name: 'About Us', href: '/about-us' },
            { name: 'Contact', href: '/contact' },
            { name: 'Privacy Policy', href: '/privacy' },
            { name: 'Terms of Service', href: '/terms' },
            { name: 'Careers', href: '/careers' },
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

    const handleSubscribe = (e: React.FormEvent) => {
        e.preventDefault()
        // Handle newsletter subscription
        setIsSubscribed(true)
        setTimeout(() => setIsSubscribed(false), 3000)
        setEmail('')
    }

    return (
        <footer className="bg-muted/30 border-t border-border/50">
            <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
                {/* Newsletter Section */}
                <div className="mb-16 text-center">
                    <h3 className="text-2xl font-bold mb-4">Stay Updated on Compliance Automation</h3>
                    <p className="text-muted-foreground mb-8 max-w-2xl mx-auto">
                        Get the latest updates on AI-powered audit frameworks, compliance best practices, and new features from SentinelAI.
                    </p>
                    <form onSubmit={handleSubscribe} className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
                        <Input
                            type="email"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="flex-1"
                        />
                        <Button type="submit" disabled={isSubscribed}>
                            <AnimatePresence mode="wait">
                                {isSubscribed ? (
                                    <motion.div
                                        key="success"
                                        initial={{ scale: 0 }}
                                        animate={{ scale: 1 }}
                                        exit={{ scale: 0 }}
                                        className="flex items-center gap-2"
                                    >
                                        <Check className="h-4 w-4" />
                                        Subscribed!
                                    </motion.div>
                                ) : (
                                    <motion.div
                                        key="subscribe"
                                        initial={{ scale: 0 }}
                                        animate={{ scale: 1 }}
                                        exit={{ scale: 0 }}
                                        className="flex items-center gap-2"
                                    >
                                        Subscribe
                                        <ArrowRight className="h-4 w-4" />
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </Button>
                    </form>
                </div>

                {/* Footer Links */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
                    {footerSections.map((section, index) => (
                        <div key={index}>
                            <h4 className="font-semibold mb-4">{section.title}</h4>
                            <ul className="space-y-3">
                                {section.links.map((link, linkIndex) => (
                                    <li key={linkIndex}>
                                        <Link
                                            href={link.href}
                                            className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                                        >
                                            {link.name}
                                        </Link>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>

                <Separator className="mb-8" />

                {/* Bottom Section */}
                <div className="flex flex-col md:flex-row justify-between items-center gap-6">
                    {/* Logo and Copyright */}
                    <div className="flex items-center gap-4">
                        <Link href="/" className="flex items-center space-x-2">
                            <Shield className="h-6 w-6 text-primary" />
                            <span className="font-bold text-xl">SentinelAI</span>
                        </Link>
                        <Separator orientation="vertical" className="h-6" />
                        <p className="text-sm text-muted-foreground">
                            © 2025 SentinelAI. All rights reserved.
                        </p>
                    </div>

                    {/* Social Links */}
                    <div className="flex items-center gap-4">
                        <span className="text-sm text-muted-foreground">Follow us:</span>
                        <div className="flex gap-3">
                            {socialLinks.map((social, index) => (
                                <Link
                                    key={index}
                                    href={social.href}
                                    className={`p-2 rounded-lg transition-colors hover:bg-accent ${social.color}`}
                                    aria-label={social.label}
                                >
                                    <social.icon className="h-4 w-4" />
                                </Link>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Legal Notice */}
                <div className="mt-8 pt-8 border-t border-border/50">
                    <p className="text-xs text-muted-foreground text-center">
                        SentinelAI helps organizations achieve PCI DSS compliance through AI-powered automation. 
                        This product is designed for VPBank&apos;s hackathon challenge and demonstrates advanced 
                        compliance automation capabilities for AWS environments.
                    </p>
                </div>
            </div>
        </footer>
    )
}
