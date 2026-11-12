# Ruby XML handler resolving SYSTEM file entities declared in a DOCTYPE subset.
def run(xml)
  if xml =~ /<!ENTITY\s+(\w+)\s+SYSTEM\s+"([^"]+)"/
    entity_name = Regexp.last_match(1)
    target = Regexp.last_match(2)
    content = File.exist?(target) ? File.read(target) : ""
    body = xml.sub(/<!DOCTYPE[^>]*\]>/m, "")
    return body.gsub("&#{entity_name};", content).gsub(/<[^>]+>/, "")
  end
  xml.gsub(/<[^>]+>/, "")
end

print run(ARGV.fetch(0))
