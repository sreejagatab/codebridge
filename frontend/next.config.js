/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // Use port 3045 by default
  server: {
    port: 3045
  }
}

module.exports = nextConfig
