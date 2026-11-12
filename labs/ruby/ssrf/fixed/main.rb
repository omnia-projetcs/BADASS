# Ruby URL fetch handler enforcing HTTPS and an allowlisted upstream host and path.
require "uri"

def run(raw_url)
  uri = URI.parse(raw_url)
  return "DENIED" unless uri.is_a?(URI::HTTPS) && uri.host == "api.example.test" && uri.port == 443 && uri.path == "/v1/status" && uri.userinfo.nil?
  "PUBLIC_OK"
rescue URI::InvalidURIError
  "DENIED"
end

print run(ARGV.fetch(0))
