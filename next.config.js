/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://172.17.0.2:5000/:path*',
      },
    ]
  },
  images: {
    domains: ['172.17.0.2'],
  },
}

module.exports = nextConfig
