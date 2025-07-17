/* eslint-disable react/no-unescaped-entities */

"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { motion } from "framer-motion"
import { ExternalLink, Instagram, Linkedin, Twitter } from "lucide-react"
import Link from "next/link"

const socialLinks = [
    { icon: Instagram, href: "#", label: "Instagram" },
    { icon: Linkedin, href: "#", label: "LinkedIn" },
    { icon: Twitter, href: "#", label: "Twitter" },
]

const caseStudyData = {
    company:
        "Suspendisse vel euismod sem. Sed sollicitudin augue eu facilisis scelerisque. Nullam pharetra tortor ut massa accumsan egestas.",
    industry: "Suspendisse volutpat",
    location: "London, United Kingdom",
    companySize: "11-50",
    website: "https://example.com/",
    topics: "Sed sollicitudin augue eu facilisis scelerisque",
}

export default function CaseStudyDetail() {
    return (
        <section >
            <div className="container mx-auto flex w-full flex-col items-center pb-8 pt-4 md:flex-row md:pb-10 md:pt-8 lg:pb-16">
                <motion.aside
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5 }}
                    className="top-20 mb-8 w-full self-start pt-8 md:sticky md:mr-8 md:w-fit md:min-w-[16rem] md:flex-1 lg:mr-32 lg:max-w-[18rem] lg:shrink-0 2xl:w-full"
                >
                    <div className="mb-8 flex w-full max-w-fit shrink-0 flex-col md:mb-10">
                        <div className="hidden w-full md:mt-1 md:block">
                            <div className="flex w-full items-center space-x-6">
                                {socialLinks.map((social, index) => (
                                    <motion.div
                                        key={social.label}
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ duration: 0.3, delay: index * 0.1 }}
                                        whileHover={{ y: -2 }}
                                    >
                                        <Link href={social.href} className="text-muted-foreground hover:text-foreground transition-colors">
                                            <social.icon className="h-5 w-5" />
                                            <span className="sr-only">{social.label}</span>
                                        </Link>
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    </div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                    >
                        <Card>
                            <CardContent className="p-6 md:p-8">
                                <h3 className="mb-6 font-medium leading-5 md:mb-4.5">About Case Study</h3>

                                <div className="space-y-5">
                                    <div>
                                        <div className="mb-2 text-xs font-semibold">Company</div>
                                        <div className="text-xs text-muted-foreground md:text-sm">{caseStudyData.company}</div>
                                    </div>

                                    <div>
                                        <div className="mb-2 text-xs font-semibold">Industry</div>
                                        <div className="text-xs text-muted-foreground md:text-sm">{caseStudyData.industry}</div>
                                    </div>

                                    <Separator />

                                    <div>
                                        <div className="mb-2 text-xs font-semibold">Location</div>
                                        <div className="text-xs text-muted-foreground md:text-sm">{caseStudyData.location}</div>
                                    </div>

                                    <div>
                                        <div className="mb-2 text-xs font-semibold">Company size</div>
                                        <div className="text-xs text-muted-foreground md:text-sm">{caseStudyData.companySize}</div>
                                    </div>

                                    <div>
                                        <div className="mb-2 text-xs font-semibold">Website</div>
                                        <div className="text-xs text-muted-foreground md:text-sm">
                                            <Link href={caseStudyData.website} className="underline hover:text-foreground transition-colors">
                                                {caseStudyData.website}
                                                <ExternalLink className="ml-1 h-3 w-3 inline" />
                                            </Link>
                                        </div>
                                    </div>

                                    <div>
                                        <div className="mb-2 text-xs font-semibold">Topics</div>
                                        <div className="text-xs text-muted-foreground md:text-sm">{caseStudyData.topics}</div>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </motion.div>
                </motion.aside>

                <motion.article
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                    className="prose prose-sm mx-auto pt-8 dark:prose-invert"
                >
                    <h1>The Joke Tax Chronicles</h1>
                    <p>
                        Once upon a time, in a far-off land, there was a very lazy king who spent all day lounging on his throne.
                        One day, his advisors came to him with a problem: the kingdom was running out of money.
                    </p>
                    <h2>The King's Plan</h2>
                    <p>
                        The king thought long and hard, and finally came up with <a href="#">a brilliant plan</a>: he would tax the
                        jokes in the kingdom.
                    </p>
                    <blockquote>
                        "After all," he said, "everyone enjoys a good joke, so it's only fair that they should pay for the
                        privilege."
                    </blockquote>
                    <h3>The Joke Tax</h3>
                    <p>The king's subjects were not amused. They grumbled and complained, but the king was firm:</p>
                    <ul>
                        <li>1st level of puns: 5 gold coins</li>
                        <li>2nd level of jokes: 10 gold coins</li>
                        <li>3rd level of one-liners: 20 gold coins</li>
                    </ul>
                    <p>
                        As a result, people stopped telling jokes, and the kingdom fell into a gloom. But there was one person who
                        refused to let the king&apos;s foolishness get him down: a court jester named Jokester.
                    </p>
                    <h3>Jokester's Revolt</h3>
                    <p>
                        Jokester began sneaking into the castle in the middle of the night and leaving jokes all over the place:
                        under the king's pillow, in his soup, even in the royal toilet. The king was furious, but he couldn't seem
                        to stop Jokester.
                    </p>
                    <p>
                        And then, one day, the people of the kingdom discovered that the jokes left by Jokester were so funny that
                        they couldn't help but laugh. And once they started laughing, they couldn't stop.
                    </p>
                    <h3>The People's Rebellion</h3>
                    <p>
                        The people of the kingdom, feeling uplifted by the laughter, started to tell jokes and puns again, and soon
                        the entire kingdom was in on the joke.
                    </p>
                    <div>
                        <table>
                            <thead>
                                <tr>
                                    <th>King's Treasury</th>
                                    <th>People's happiness</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Empty</td>
                                    <td>Overflowing</td>
                                </tr>
                                <tr>
                                    <td>Modest</td>
                                    <td>Satisfied</td>
                                </tr>
                                <tr>
                                    <td>Full</td>
                                    <td>Ecstatic</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <p>
                        The king, seeing how much happier his subjects were, realized the error of his ways and repealed the joke
                        tax. Jokester was declared a hero, and the kingdom lived happily ever after.
                    </p>
                    <p>
                        The moral of the story is: never underestimate the power of a good laugh and always be careful of bad ideas.
                    </p>
                </motion.article>
            </div>
        </section>
    )
}
