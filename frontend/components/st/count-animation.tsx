"use client";

import { cn } from "@/lib/utils";
import {
  animate,
  useMotionValue,
  useMotionValueEvent,
  useTransform,
} from "framer-motion";
import React from "react";

type Props = {
  number: number;
  className?: string;
  prefix?: string;
  suffix?: string;
  duration?: number;
};

export default function CountAnimation({
  number,
  className,
  prefix,
  suffix,
  duration = 2,
}: Props) {
  const count = useMotionValue(0);
  const rounded = useTransform(count, Math.round);
  const [current, setCurrent] = React.useState(0);

  React.useEffect(() => {
    const animation = animate(count, number, { duration: duration });
    return animation.stop;
  }, [count, number, duration]);

  useMotionValueEvent(rounded, "change", (latest) => {
    setCurrent(latest);
  });

  return (
    <span className={cn(className)}>
      {prefix}
      {current}
      {suffix}
    </span>
  );
}
