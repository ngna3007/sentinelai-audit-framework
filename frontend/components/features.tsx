"use client";
import React from "react";
import { Timeline } from "./ui/timeline";
import { Icon } from "./ui/plus-icon";

export function Features() {
  const data = [
    {
      title: "Feature 01",
      content: (
        <div>
          <p className="mb-4 text-lg md:text-4xl font-bold ">
            Auto Evidence Collecting
          </p>
          <p className="mb-8 text-xs font-normal text-neutral-800 md:text-sm dark:text-neutral-200">
            Automatically collect and organize compliance evidence from multiple AWS services. Our AI-powered system gathers data from CloudTrail, Config, Security Hub, and other AWS services to build comprehensive audit trails without manual intervention.
          </p>
            <div className="grid grid-cols-1 gap-4">
            <img
              src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop&auto=format"
              alt="Automated evidence collection and data gathering"
              width={500}
              height={700}
              className="h-30 w-full rounded-lg object-cover shadow-[0_0_24px_rgba(34,_42,_53,_0.06),_0_1px_1px_rgba(0,_0,_0,_0.05),_0_0_0_1px_rgba(34,_42,_53,_0.04),_0_0_4px_rgba(34,_42,_53,_0.08),_0_16px_68px_rgba(47,_48,_55,_0.05),_0_1px_0_rgba(255,_255,_255,_0.1)_inset] md:h-60 lg:h-80"
            />
          </div>

        </div>
      ),
    },
    {
      title: "Feature 02",
      content: (
        <div>
          <p className="mb-4 text-lg md:text-4xl font-bold text-neutral-800 dark:text-neutral-200">
            AI-Powered Auditing
          </p>
          <p className="mb-8 text-xs font-normal text-neutral-800 md:text-sm dark:text-neutral-200">
            Strong, fast, and reliable audit result using the smartest LLMs on Earth. Leverage Amazon Bedrock Claude 3.5 for intelligent compliance analysis and automated decision-making.
          </p>
          <div className="grid grid-cols-1 gap-4">
            <img
              src="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=500&h=500&fit=crop&auto=format"
              alt="AI neural networks and machine learning analysis"
              width={500}
              height={500}
              className="h-30 w-full rounded-lg object-cover shadow-[0_0_24px_rgba(34,_42,_53,_0.06),_0_1px_1px_rgba(0,_0,_0,_0.05),_0_0_0_1px_rgba(34,_42,_53,_0.04),_0_0_4px_rgba(34,_42,_53,_0.08),_0_16px_68px_rgba(47,_48,_55,_0.05),_0_1px_0_rgba(255,_255,_255,_0.1)_inset] md:h-60 lg:h-80"
            />
          </div>
        </div>
      ),
    },
    {
      title: "Feature 03",
      content: (
        <div>
          <p className="mb-4 text-lg md:text-4xl font-bold text-neutral-800 dark:text-neutral-200">
            Evidence Tracker
          </p>
          <p className="mb-8 text-xs font-normal text-neutral-800 md:text-sm dark:text-neutral-200">
            Track every testable requirement with our dashboard. Comprehensive evidence collection from AWS Config, CloudTrail, and Security Hub with real-time monitoring and validation.
          </p>
          <div className="grid grid-cols-1 gap-4">
            <img
              src="https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=500&h=500&fit=crop&auto=format"
              alt="Evidence tracking dashboard"
              width={500}
              height={500}
              className="h-30 w-full rounded-lg object-cover shadow-[0_0_24px_rgba(34,_42,_53,_0.06),_0_1px_1px_rgba(0,_0,_0,_0.05),_0_0_0_1px_rgba(34,_42,_53,_0.04),_0_0_4px_rgba(34,_42,_53,_0.08),_0_16px_68px_rgba(47,_48,_55,_0.05),_0_1px_0_rgba(255,_255,_255,_0.1)_inset] md:h-60 lg:h-80"
            />
          </div>
        </div>
      ),
    },
    {
      title: "Feature 04",
      content: (
        <div>
          <p className="mb-4 text-lg md:text-4xl font-bold text-neutral-800 dark:text-neutral-200">
            Track Your Process
          </p>
          <p className="mb-8 text-xs font-normal text-neutral-800 md:text-sm dark:text-neutral-200">
            Click your profile to see what is ahead. Personal dashboard with progress tracking, upcoming audit milestones, and comprehensive reporting across all your compliance initiatives.
          </p>
          <div className="grid grid-cols-1 gap-4">
            <img
              src="https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=500&h=500&fit=crop&auto=format"
              alt="Process tracking dashboard"
              width={500}
              height={500}
              className="h-30 w-full rounded-lg object-cover shadow-[0_0_24px_rgba(34,_42,_53,_0.06),_0_1px_1px_rgba(0,_0,_0,_0.05),_0_0_0_1px_rgba(34,_42,_53,_0.04),_0_0_4px_rgba(34,_42,_53,_0.08),_0_16px_68px_rgba(47,_48,_55,_0.05),_0_1px_0_rgba(255,_255,_255,_0.1)_inset] md:h-60 lg:h-80"
            />
          </div>
        </div>
      ),
    },
  ];

  return (
    <div id="features" className="relative w-full overflow-clip bg-background">
      <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24 lg:py-32">
        <div className="text-center mb-4">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">Our Features</h2>
          <p className="text-lg lg:text-xl text-muted-foreground">
            Discover the powerful features that make SentinelAI the ultimate compliance automation solution
          </p>
        </div>
      </div>

      <Timeline 
        data={data} 
        title=""
        description=""
      />
    </div>
  );
}
