
"use client"

import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { motion } from "framer-motion"
import Image from "next/image"
import Link from "next/link"

const blogPosts = [
    {
        title: "How VPBank Transforms Team Collaboration",
        description:
            "Discover how VPBank's unified platform eliminates the need for multiple tools and streamlines your team's workflow with real-time collaboration.",
        image: 'https://www.raycast.com/_next/image?url=%2Fuploads%2Fblog-raycast-notes%2Fquicklink.png&w=1920&q=100',
        category: "Productivity",
    },
    {
        title: "Building Powerful Databases with VPBank",
        description:
            "Learn how to create flexible, scalable databases that adapt to your business needs with VPBank's advanced field types and views.",
        image: 'https://www.raycast.com/_next/image?url=%2Fuploads%2Fblog-ios%2Fhome.jpeg&w=1920&q=100',
        category: "Tutorial",
    },
    {
        title: "The Future of Document Collaboration",
        description:
            "Explore how VPBank combines rich document editing with live database embeds to create truly interactive workspaces.",
        image: 'https://www.raycast.com/_next/image?url=%2Fuploads%2Fblog-ios%2Fai.jpeg&w=1920&q=100',
        category: "Features",
    },
    {
        title: "Enterprise Security in VPBank",
        description:
            "Understand how VPBank ensures your data is secure with enterprise-grade security features, SSO, and compliance certifications.",
        image: 'https://www.raycast.com/_next/image?url=%2Fuploads%2Fblog-ios%2Fnotes.jpeg&w=1920&q=100',
        category: "Security",
    },
    {
        title: "Integrating VPBank with Your Existing Tools",
        description:
            "Learn how to connect VPBank with your favorite applications using our comprehensive API and webhook system.",
        image: 'https://www.raycast.com/_next/image?url=%2Fuploads%2Fblog-hype%2Fspike.png&w=1920&q=100',
        category: "Integration",
    },
    {
        title: "Best Practices for Team Workspaces",
        description:
            "Discover proven strategies for organizing your team's work efficiently using VPBank's workspace and permission features.",
        image: 'https://www.raycast.com/_next/image?url=%2Fuploads%2Fperplexity.png&w=1920&q=100',
        category: "Guide",
    },
]

const filterOptions = [
    { value: "categories", placeholder: "Categories" },
    { value: "topics", placeholder: "Topics" },
    { value: "authors", placeholder: "Authors" },
    { value: "date", placeholder: "Date" },
]

const selectOptions = [
    { value: 'option1', label: 'Option 1' },
    { value: 'option2', label: 'Option 2' },
    { value: 'option3', label: 'Option 3' },
]

export default function BlogListing() {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6 }}
        >
            <section className="py-16 md:py-32 w-full">
                <div className="container max-w-7xl px-4 md:px-6 lg:px-8 mx-auto">
                    <div className="mb-6 md:mb-8 lg:mb-10 md:mb-10 lg:mb-12">
                        <h2 className="mb-4 md:mb-6 w-full text-2xl md:text-4xl font-bold md:mb-14 md:text-5xl lg:mb-16 lg:text-6xl">
                            Latest insights and guides
                        </h2>

                        <div className="mb-6 md:mb-10 flex flex-wrap items-center gap-x-3 md:gap-x-4 gap-y-2 md:gap-y-3 lg:gap-x-3">
                            {filterOptions.map((option) => (
                                <div key={option.value}>
                                    <Select>
                                        <SelectTrigger className="text-xs md:text-sm">
                                            <SelectValue placeholder={option.placeholder} />
                                        </SelectTrigger>
                                        <SelectContent>
                                            {selectOptions.map((selectOption) => (
                                                <SelectItem key={selectOption.value} value={selectOption.value}>
                                                    {selectOption.label}
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="grid gap-3 md:gap-4 lg:gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 py-0">
                        {blogPosts.map((post) => (
                            <div key={post.title} className="h-full">
                                <Link href={`/blog/${post.title}`} className="group block">
                                    <Card className="h-full flex flex-col justify-between overflow-hidden py-0 rounded-3xl">
                                        <div>
                                            <div className="aspect-[3/2] overflow-hidden">
                                                <div className="relative h-full w-full">
                                                    <Image
                                                        src={post.image}
                                                        alt={post.title}
                                                        fill
                                                        className="object-cover object-center object-left hover:object-right transition-all duration-300"
                                                    />
                                                </div>
                                            </div>
                                        </div>

                                        <CardContent className="flex-1 flex flex-col justify-between p-4 md:p-6">
                                            <div>
                                                <h3 className="mb-2 line-clamp-3 break-words text-base md:text-lg font-medium md:mb-3 md:text-xl lg:text-2xl">
                                                    {post.title}
                                                </h3>
                                                <p className="mb-6 md:mb-8 line-clamp-2 text-xs md:text-sm text-muted-foreground md:mb-12 md:text-base lg:mb-9">
                                                    {post.description}
                                                </p>
                                            </div>

                                            <div>
                                                <Badge variant="secondary" className="text-xs md:text-sm">{post.category}</Badge>
                                            </div>
                                        </CardContent>
                                    </Card>
                                </Link>
                            </div>
                        ))}
                    </div>
                </div>
            </section>
        </motion.div>
    )
}
