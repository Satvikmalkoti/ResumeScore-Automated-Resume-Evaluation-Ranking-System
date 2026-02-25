/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  async rewrites() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL

    if (!apiUrl) {
      console.error("NEXT_PUBLIC_API_URL is not defined")

      return []
    }

    return [
      { source: '/parse', destination: `${apiUrl}/parse` },
    ];
  },
}

export default nextConfig
