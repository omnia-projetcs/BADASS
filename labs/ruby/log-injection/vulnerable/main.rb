def run(value)
  File.write('audit.log', 'user=' + value)
  File.read('audit.log')
end
print run(ARGV.fetch(0))
