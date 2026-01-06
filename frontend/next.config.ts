/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    // Warning: This allows production builds to succeed even if ESLint errors exist
    ignoreDuringBuilds: true,
  },
  typescript: {
    // Warning: This allows production builds to succeed even if TypeScript errors exist
    ignoreBuildErrors: true,
  },
};

export default nextConfig;