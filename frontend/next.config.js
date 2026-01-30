/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  // Allow Next.js to read environment variables prefixed with NEXT_PUBLIC_
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  // Proxy /api/chat → backend (this solves the 404 problem)
  async rewrites() {
    return [
      {
        source: '/api/chat',
        destination: 'http://localhost:8001/api/chat', // ← your backend port
      },
      // Optional: proxy task endpoints too (if your frontend uses them)
      {
        source: '/api/tasks/:path*',
        destination: 'http://localhost:8001/api/tasks/:path*',
      },
    ]
  },
  // Optional: Improve image loading (if you add images later)
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
};

export default nextConfig;