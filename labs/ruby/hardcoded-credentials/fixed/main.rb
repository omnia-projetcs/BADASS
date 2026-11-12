require "openssl"

def run(value)
  expected = ENV["BADASS_ADMIN_PASSWORD"]
  return "DENIED" if expected.nil? || expected.empty? || !value.is_a?(String)
  return "DENIED" unless expected.bytesize == value.bytesize
  OpenSSL.fixed_length_secure_compare(expected, value) ? "ADMIN" : "DENIED"
end
print run(ARGV.fetch(0))
