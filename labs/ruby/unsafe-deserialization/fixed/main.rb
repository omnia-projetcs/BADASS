# Ruby loader rejecting YAML/Marshal tags and parsing strict JSON objects only.
require "json"

def run(raw)
  return "DENIED" unless raw.is_a?(String) && !raw.start_with?("---")
  data = JSON.parse(raw)
  return "DENIED" unless data.is_a?(Hash) && data.keys == ["user"]
  user = data["user"]
  return "DENIED" unless user.is_a?(String) && user.match?(/\A[a-z0-9_]{1,32}\z/)
  "USER:#{user}"
rescue JSON::ParserError
  "DENIED"
end

print run(ARGV.fetch(0))
