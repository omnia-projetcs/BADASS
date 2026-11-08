def run(value)
  value = value.gsub('\\') { '\\\\' }.gsub("\r") { '\\r' }.gsub("\n") { '\\n' }
  File.write('audit.log', 'user=' + value)
  File.read('audit.log')
end
print run(ARGV.fetch(0))
