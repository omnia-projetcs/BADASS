# Ruby URL fetch handler permitting requests to internal metadata and loopback addresses.
require "uri"

def run(raw_url)
  uri = URI.parse(raw_url)
  return "LAB_INTERNAL_METADATA" if ["169.254.169.254", "127.0.0.1"].include?(uri.host)
  return "PUBLIC_OK" if uri.scheme == "https" && uri.host == "api.example.test" && uri.path == "/v1/status"
  "NOT_FOUND"
rescue URI::InvalidURIError
  "DENIED"
end

print run(ARGV.fetch(0))
