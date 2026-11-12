# Ruby profile update permitting only the allowlisted name key.
require "json"

def run(raw)
  incoming = JSON.parse(raw)
  return "DENIED" unless incoming.is_a?(Hash)
  account = { "name" => "Alice", "role" => "user" }
  if incoming["name"].is_a?(String) && incoming["name"].match?(/\A[A-Za-z0-9 _-]{1,32}\z/)
    account["name"] = incoming["name"]
  end
  "#{account['name']}:#{account['role']}"
rescue JSON::ParserError
  "DENIED"
end

print run(ARGV.fetch(0))
