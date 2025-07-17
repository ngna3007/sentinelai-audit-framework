'use client'

import { Button } from '@/components/ui/button'
import { AnimatePresence, motion } from 'framer-motion'
import { Menu, Shield, Activity, X } from 'lucide-react'
import Link from 'next/link'
import React, { useState } from 'react'

const navItems = [
    { href: '/features', label: 'Features' },
    { href: '/pricing', label: 'Pricing' },
    { href: '/security', label: 'Security' },
    { href: '/about-us', label: 'About' },
    { href: '/contact', label: 'Contact' },
]

export default function Header() {
    const [isMenuOpen, setIsMenuOpen] = useState(false)

    return (
        <motion.header
            className="bg-background/80 backdrop-blur-md border-b border-border/50 fixed top-0 left-0 right-0 z-50 transition-all duration-300"
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
        >
            <div className="flex h-16 lg:h-20 items-center justify-between px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
                {/* Logo */}
                <Link href="/" className="flex items-center space-x-3 group">
                    <motion.div
                        whileHover={{ scale: 1.05, rotate: 5 }}
                        transition={{ duration: 0.2 }}
                        className="p-2 bg-primary/10 rounded-xl group-hover:bg-primary/20 transition-colors"
                    >
                        <Shield className="h-6 w-6 lg:h-7 lg:w-7 text-primary" />
                    </motion.div>
                    <span className="font-bold text-xl lg:text-2xl bg-gradient-to-r from-primary to-primary/80 bg-clip-text text-transparent">
                        SentinelAI
                    </span>
                </Link>

                {/* Desktop Navigation */}
                <nav className="hidden lg:flex items-center space-x-8">
                    {navItems.map((item) => (
                        <Link
                            key={item.href}
                            href={item.href}
                            className="relative text-sm font-medium text-muted-foreground hover:text-foreground transition-colors duration-300 py-2 px-3 rounded-lg hover:bg-muted/50 group"
                        >
                            {item.label}
                            <motion.div
                                className="absolute bottom-0 left-1/2 w-0 h-0.5 bg-primary rounded-full group-hover:w-full group-hover:left-0 transition-all duration-300"
                                initial={false}
                            />
                        </Link>
                    ))}
                </nav>

                {/* Desktop Actions */}
                <div className="hidden lg:flex items-center space-x-4">
                    <Button 
                        variant="outline" 
                        size="sm"
                        className="flex items-center gap-2 hover:bg-muted/80 transition-colors"
                        disabled
                        title="Dashboard - Coming Soon"
                    >
                        <Activity className="h-4 w-4" />
                        <span className="hidden xl:inline">Dashboard</span>
                    </Button>
                    <Button size="sm" className="px-6 py-2 font-semibold bg-gradient-to-r from-primary to-primary/90 hover:from-primary/90 hover:to-primary">
                        Start Trial
                    </Button>
                </div>

                {/* Mobile Menu Button */}
                <Button
                    variant="ghost"
                    size="sm"
                    className="lg:hidden p-2"
                    onClick={() => setIsMenuOpen(!isMenuOpen)}
                >
                    <AnimatePresence mode="wait">
                        {isMenuOpen ? (
                            <motion.div
                                key="close"
                                initial={{ rotate: -90, opacity: 0 }}
                                animate={{ rotate: 0, opacity: 1 }}
                                exit={{ rotate: 90, opacity: 0 }}
                                transition={{ duration: 0.2 }}
                            >
                                <X className="h-5 w-5" />
                            </motion.div>
                        ) : (
                            <motion.div
                                key="menu"
                                initial={{ rotate: 90, opacity: 0 }}
                                animate={{ rotate: 0, opacity: 1 }}
                                exit={{ rotate: -90, opacity: 0 }}
                                transition={{ duration: 0.2 }}
                            >
                                <Menu className="h-5 w-5" />
                            </motion.div>
                        )}
                    </AnimatePresence>
                </Button>
            </div>

            {/* Mobile Navigation */}
            <AnimatePresence>
                {isMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3, ease: 'easeInOut' }}
                        className="lg:hidden border-t border-border/50 bg-background/95 backdrop-blur-md"
                    >
                        <div className="px-4 py-6 space-y-4">
                            {navItems.map((item, index) => (
                                <motion.div
                                    key={item.href}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ duration: 0.3, delay: index * 0.1 }}
                                >
                                    <Link
                                        href={item.href}
                                        className="block text-sm font-medium text-muted-foreground hover:text-foreground transition-colors py-3 px-4 rounded-lg hover:bg-muted/50"
                                        onClick={() => setIsMenuOpen(false)}
                                    >
                                        {item.label}
                                    </Link>
                                </motion.div>
                            ))}
                            <motion.div 
                                className="pt-4 border-t border-border/50 space-y-3"
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.3, delay: 0.4 }}
                            >
                                <Button 
                                    variant="outline" 
                                    size="sm" 
                                    className="w-full flex items-center gap-2 justify-center"
                                    disabled
                                    title="Dashboard - Coming Soon"
                                >
                                    <Activity className="h-4 w-4" />
                                    Dashboard
                                </Button>
                                <Button size="sm" className="w-full font-semibold bg-gradient-to-r from-primary to-primary/90">
                                    Start Trial
                                </Button>
                            </motion.div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.header>
    )
}
