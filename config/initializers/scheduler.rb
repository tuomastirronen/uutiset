require 'rufus-scheduler'

scheduler = Rufus::Scheduler::singleton

scheduler.every '10m' do
  puts "Updating feed..."
  Feed.write_db(nil)
  puts "done."
end