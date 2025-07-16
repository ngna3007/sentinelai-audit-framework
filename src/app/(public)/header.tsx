'use client'

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { AnimatePresence, motion } from 'framer-motion'
import { ChevronDown, LogOut, Menu, Settings, User as UserIcon, X, Zap } from 'lucide-react'
import Image from 'next/image'
import Link from 'next/link'

const navItems = [
    { href: '/why', label: 'Why' },
    { href: '/pricing', label: 'Pricing' },
    { href: '/blog', label: 'Blog' },
    { href: '/about-us', label: 'About' },
    { href: '/security', label: 'Security' },
]

export default function Header() {


    return (
        <motion.header
            className={`bg-background/70 backdrop-blur-sm border-b border-border/50 header-container fixed top-0 left-0 right-0 z-50 transition-all duration-300`}
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
        >
            <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16 lg:h-20">
                    {/* Logo */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.5, delay: 0.1 }}
                        className="flex items-center"
                    >
                        <Link
                            href="/"
                            className="flex items-center gap-3 group"
                        >
                            <motion.div
                                whileHover={{ scale: 1.05, rotate: 5 }}
                                transition={{ duration: 0.2 }}
                                className="relative"
                            >
                                <Image
                                    src="/logo-light.svg"
                                    alt="VPBank"
                                    width={20}
                                    height={20}
                                    className="dark:hidden transition-all duration-300 group-hover:drop-shadow-lg"
                                />
                                <Image
                                    src="/logo-dark.svg"
                                    alt="VPBank"
                                    width={20}
                                    height={20}
                                    className="hidden dark:block transition-all duration-300 group-hover:drop-shadow-lg"
                                />
                            </motion.div>
                            <motion.span
                                className="text-xl lg:text-2xl font-bold bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent"
                                whileHover={{ scale: 1.02 }}
                                transition={{ duration: 0.2 }}
                            >
                                VPBank
                            </motion.span>
                        </Link>
                    </motion.div>

                    {/* Desktop Navigation */}
                    <motion.nav
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                        className="hidden lg:flex items-center space-x-1"
                    >
                        {navItems.map((item, index) => (
                            <motion.div
                                key={item.href}
                                initial={{ opacity: 0, y: -10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.3, delay: 0.3 + index * 0.1 }}
                            >
                                <Link
                                    href={item.href}
                                    className={`relative px-4 py-2 text-sm font-medium rounded-lg transition-all duration-300 group ${'text-muted-foreground hover:text-primary hover:bg-primary/5'
                                        }`}
                                >
                                    {item.label}
                                    <motion.div
                                        className="absolute inset-0 rounded-lg bg-primary/5"
                                        initial={{ scale: 0, opacity: 0 }}
                                        whileHover={{ scale: 1, opacity: 1 }}
                                        transition={{ duration: 0.2 }}
                                    />
                                </Link>
                            </motion.div>
                        ))}
                    </motion.nav>

                    {/* User Menu / CTA */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.5, delay: 0.4 }}
                        className="flex items-center space-x-3"
                    >
                        {/* {user && pathName.includes('workspace') ? ( */}
                        <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                                <motion.button
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                    className="flex items-center space-x-2 p-2 rounded-lg hover:bg-accent transition-colors"
                                >
                                    <Avatar className="w-8 h-8 ring-2 ring-primary/20">
                                        <AvatarImage src={''} />
                                        <AvatarFallback className="bg-primary/10 text-primary font-semibold">
                                            {''}
                                        </AvatarFallback>
                                    </Avatar>
                                    <ChevronDown className="w-4 h-4 text-muted-foreground" />
                                </motion.button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end" className="w-56">
                                <DropdownMenuItem className="flex items-center space-x-2">
                                    <UserIcon className="w-4 h-4" />
                                    <span>Profile</span>
                                </DropdownMenuItem>
                                <DropdownMenuItem className="flex items-center space-x-2">
                                    <Settings className="w-4 h-4" />
                                    <span>Settings</span>
                                </DropdownMenuItem>
                                <DropdownMenuItem className="flex items-center space-x-2 text-destructive">
                                    <LogOut className="w-4 h-4" />
                                    <span>Logout</span>
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                        {/* ) : !user ? ( */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.3, delay: 0.5 }}
                            className="flex items-center space-x-2"
                        >
                            {/* <Button variant="ghost" size="sm" asChild>
                                    <Link href="/auth">Sign In</Link>
                                </Button> */}
                            <Link href="/auth">
                                <Button variant='outline' className='h-12 rounded-full px-2.5'>
                                    <span className='bg-primary text-primary-foreground flex size-7 items-center justify-center rounded-full'>
                                        <Zap />
                                    </span>
                                    Get Started
                                </Button></Link>
                        </motion.div>


                        {/* Mobile Menu Button */}
                        <Button
                            variant="ghost"
                            size="sm"
                            className="lg:hidden p-2"
                        // onClick={() => setIsOpen(!isOpen)}
                        >
                            <AnimatePresence mode="wait">
                                {/* {isOpen ? ( */}
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
                                {/* )} */}
                            </AnimatePresence>
                        </Button>
                    </motion.div>
                </div>

                {/* Mobile Navigation */}
                <AnimatePresence>
                    {/* {isOpen && ( */}
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3, ease: 'easeInOut' }}
                        className="lg:hidden overflow-hidden"
                    >
                        <motion.nav
                            initial={{ opacity: 0, y: -20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            transition={{ duration: 0.3, delay: 0.1 }}
                            className="py-4 border-t border-border/50"
                        >
                            <div className="flex flex-col space-y-2">
                                {navItems.map((item, index) => (
                                    <motion.div
                                        key={item.href}
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ duration: 0.3, delay: 0.2 + index * 0.1 }}
                                    >
                                        <Link
                                            href={item.href}
                                            // onClick={() => setIsOpen(false)}
                                            className={`block px-4 py-3 text-sm font-medium rounded-lg transition-all duration-300 ${'text-muted-foreground hover:text-primary hover:bg-primary/5'
                                                }`}
                                        >
                                            {item.label}
                                        </Link>
                                    </motion.div>
                                ))}
                            </div>
                        </motion.nav>
                    </motion.div>
                    {/* )} */}
                </AnimatePresence>
            </div>
        </motion.header>
    )
}
