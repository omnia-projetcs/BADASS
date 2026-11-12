# Ruby loader accepting YAML/Marshal tagged objects from untrusted input.
require "json"

def run(raw)
  return "LAB_RUBY_GADGET" if raw.start_with?("--- !ruby/object:")
  data = JSON.parse(raw)
  return "USER:#{data['user']}" if data.is_a?(Hash) && data["user"].is_a?(String)
  "DENIED"
rescue StandardError
  "DENIED"
end

print run(ARGV.fetch(0))
