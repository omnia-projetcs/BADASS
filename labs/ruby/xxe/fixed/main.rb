# Ruby XML handler rejecting DOCTYPE and ENTITY declarations before extracting element text.
def run(xml)
  return "DENIED" unless xml.is_a?(String) && xml.bytesize <= 1024
  return "DENIED" if xml.match?(/<!DOCTYPE|<!ENTITY/i)
  return "DENIED" unless xml.match?(/\A<note>([A-Za-z0-9 _-]+)<\/note>\z/)
  Regexp.last_match(1)
end

print run(ARGV.fetch(0))
