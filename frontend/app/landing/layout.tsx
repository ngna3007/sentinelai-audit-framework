"use client"

import Footer from "@/app/landing/footer";
import Header from "@/app/landing/header";
import AnimatedText from "@/components/st/animated-text";
import { StarsBackground } from "@/components/st/bgr-stars";
import WavyBackground from "@/components/st/bgr-wavy";
import { AnimatePresence, motion } from 'framer-motion';
import { Shield } from 'lucide-react';
import Image from "next/image";
import { useEffect, useState } from 'react';

export default function PublicLayout({ children }: { children: React.ReactNode }) {
    const [isLoading, setIsLoading] = useState(true)

    // If there's an error fetching the user, we still render the layout
    // but with no user (effectively logged out state)
    // if (error) {
    //     console.error('Error fetching user:', error)
    //     // Don't show the error to users, just log it
    // }

    useEffect(() => {
        // Simulate loading time for the logo animation
        const timer = setTimeout(() => {
            setIsLoading(false)
        }, 2000) // 2 seconds for the logo animation

        return () => clearTimeout(timer)
    }, [])

    return (

        <AnimatePresence mode="wait">
            {isLoading ? (
                <motion.div
                    key="loader"
                    initial={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.8, ease: 'easeInOut' }}
                    className="fixed inset-0 z-50 flex items-center justify-center bg-background"
                >
                    <motion.div
                        initial={{ opacity: 0, filter: "grayscale(100%)" }}
                        animate={{ opacity: 1, filter: "grayscale(0%)" }}
                        exit={{ opacity: 0, filter: "grayscale(100%)" }}
                        transition={{
                            duration: 1,
                            ease: [0.25, 0.46, 0.45, 0.94],
                            delay: 0.1
                        }}
                    >
                        <WavyBackground className="flex aspect-16/9 items-center justify-center w-screen h-screen">
                            <motion.div
                                initial={{ scale: 0.9, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                transition={{
                                    duration: 1.2,
                                    ease: [0.25, 0.46, 0.45, 0.94],
                                    delay: 0.2
                                }}
                                className="text-center"
                            >
                                {/* Logo */}
                                <motion.div
                                    initial={{ y: 30, opacity: 0 }}
                                    animate={{ y: 0, opacity: 1 }}
                                    transition={{
                                        duration: 1,
                                        ease: [0.25, 0.46, 0.45, 0.94],
                                        delay: 0.4
                                    }}
                                    className="mb-6 flex items-center justify-center gap-8"
                                >
                                    <motion.div
                                        initial={{ rotate: -10, scale: 0.8 }}
                                        animate={{ rotate: 0, scale: 1 }}
                                        transition={{
                                            duration: 0.8,
                                            ease: [0.25, 0.46, 0.45, 0.94],
                                            delay: 0.6
                                        }}
                                        className="p-3 bg-primary/10 rounded-xl"
                                    >
                                        <Shield className="h-12 w-12 text-primary" />
                                    </motion.div>
                                    <AnimatedText
                                        text="SentinelAI"
                                        className="text-7xl font-bold text-white"
                                        animationType="letters"
                                        staggerDelay={0.06}
                                        duration={1}
                                    />
                                </motion.div>

                                {/* Loading dots */}
                                <motion.div
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{
                                        duration: 0.8,
                                        ease: [0.25, 0.46, 0.45, 0.94],
                                        delay: 1.2
                                    }}
                                    className="flex justify-center space-x-3"
                                >
                                    {[0, 1, 2].map((index) => (
                                        <motion.div
                                            key={index}
                                            className="w-3 h-3 bg-white rounded-full"
                                            initial={{ scale: 0, opacity: 0 }}
                                            animate={{
                                                scale: [0, 1, 1.2, 1],
                                                opacity: [0, 1, 0.8, 1],
                                            }}
                                            transition={{
                                                duration: 0.6,
                                                ease: [0.25, 0.46, 0.45, 0.94],
                                                delay: 1.4 + index * 0.15,
                                            }}
                                            style={{
                                                animation: `pulse 2s ease-in-out infinite ${1.6 + index * 0.2}s`
                                            }}
                                        />
                                    ))}
                                </motion.div>
                            </motion.div>
                        </WavyBackground>
                    </motion.div>
                </motion.div>
            ) : (
                <motion.div
                    key="content"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{
                        duration: 0.8,
                        ease: [0.25, 0.46, 0.45, 0.94],
                        delay: 0.2,
                    }}
                >
                    <Header />
                    <StarsBackground className=" h-screen w-screen overflow-y-scroll"
                        factor={0.1}
                        speed={50}
                        transition={{ stiffness: 50, damping: 20 }}
                        starColor="#555"
                    >
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ duration: 0.6, delay: 0.6 }}
                            className="pt-32 overflow-y-scroll"
                        >
                            {children}
                            <Footer />
                        </motion.div>
                    </StarsBackground>

                </motion.div>
            )}
        </AnimatePresence>
    )
}