import type { NextConfig } from "next";
import path from "node:path";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  transpilePackages: ["@phosphor-icons/react"],
  outputFileTracingRoot: path.join(__dirname),
};

export default nextConfig;
